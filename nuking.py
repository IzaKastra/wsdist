# Author: Kastra (Asura)
# Version date: 2022 November 29

from get_dint_m_v import *
import numpy as np

def nuking(spelltype, tier, element, gearset, player_INT, player_matk, mdmg, enemy_INT, enemy_mdb, enemy_meva, ninjutsu_damage, futae=False, burst=False, steps=2):

    # print(spelltype, tier, element, gearset, player_INT, player_matk, mdmg, enemy_INT, enemy_mdb, ninjutsu_damage, futae, burst, steps)

    # Determine Magic Accuracies
    spelltype_skill = gearset.playerstats[f"{spelltype} Skill"] # Magic Accuracy from Ninjutsu Skill

    magic_accuracy_skill = gearset.playerstats["Magic Accuracy Skill"] # Magic Accuracy from Magic Accuracy Skill. Currently includes off-hand weapon stats.
    magic_accuracy_skill -= gearset.gear["sub"].get("Magic Accuracy Skill",0) # Subtract off the Magic Accuracy Skill from the off-hand slot, since it does not contribute to spell accuracy.
 
    dstat_macc = get_dstat_macc(player_INT, enemy_INT) # Get magic accuracy from dINT

    magic_accuracy = gearset.playerstats["Magic Accuracy"] # Read base Magic Accuracy from playerstats, including traits and gear with "Magic Accuracy"
    magic_accuracy += magic_accuracy_skill # Add on the "Magic Accuracy Skill" stat
    magic_accuracy += spelltype_skill # Add on the "Ninjutsu Skill" or "Elemental Magic Skill" stat depending on spell being cast
    magic_accuracy += dstat_macc # Add on magic accuracy from dINT

    dINT = player_INT - enemy_INT

    elemental_damage_bonus = 1+gearset.playerstats['Elemental Bonus']/100 + gearset.playerstats[f'{element.capitalize()} Elemental Bonus']/100

    dayweather = 1.0

    if burst: # Do burst stuff now so we can add +100 Magic Accuracy before calculating magic hit rates
        magic_accuracy += 100
        magic_burst_multiplier = 1.35 # Standard +35% damage for magic bursting
        skillchain_steps_bonus = (steps-2)*0.10 # Another +10% for each step in the skillchain after 2
        magic_burst_multiplier += skillchain_steps_bonus
        
        
        burst_bonus1 = 40 if gearset.playerstats['Magic Burst Damage'] > 40 else gearset.playerstats['Magic Burst Damage']
        burst_bonus2 = gearset.playerstats['Magic Burst Damage II']
        burst_bonus_multiplier = 1 + burst_bonus1/100 + burst_bonus2/100

        # for i,k in enumerate(gearset.gear):
        #     print(k,gearset.gear[k]['Name2'])
        # print(burst_bonus1, burst_bonus2, burst_bonus_multiplier)
        # import sys; sys.exit()
    else:
        burst_bonus_multiplier = 1.
        magic_burst_multiplier = 1.

    
    magic_hit_rate = get_magic_hit_rate(magic_accuracy, enemy_meva)
    resist_state = get_resist_state_average(magic_hit_rate)
    # print(magic_hit_rate,spelltype_skill,magic_accuracy_skill,dstat_macc,magic_accuracy,resist_state)
    # print(magic_accuracy, enemy_meva, magic_hit_rate, resist_state)



    futae_bonus = 1.0
    if spelltype == "Ninjutsu":
        ninjutsu_skill_potency = 2.00 if tier=="Ichi" else 2.12 # Assumes maximum bonus damage from Ninjutsu Skill > 500. 
                                                                # This should be true at ML31 with Ninjutsu merits.
                                                                # Or at ML8 with Ninjutsu merits and the Relic+3 feet equipped.
        m,v = get_mv(tier, player_INT, enemy_INT)
        d = int(v+mdmg+dINT*m)

        if futae: # Futae = False if not Ninjutsu
            futae_bonus = 1.5 # Standard +50% damage when using futae
            hands = gearset.equipped['hands']
            if hands == "Hattori Tekko +3":
                futae_bonus += 0.28
            elif hands == "Hattori Tekko +2":
                futae_bonus += 0.26
            elif hands == "Hattori Tekko +1":
                futae_bonus += 0.24

    else: # Else Elemental Magic
        ninjutsu_skill_potency = 1.0
        m, v, window = get_mv_blm(element, tier, player_INT, enemy_INT)
        d = int(v+mdmg+(dINT-window)*m) # Black Magic uses (dINT-window)*m. This was simply a choice of the person who collected and fit the data.

    d = int(d * ninjutsu_skill_potency)
    d = int(d * (100+player_matk)/(100+enemy_mdb))
    d *= 1 + ninjutsu_damage/100
    d *= dayweather
    d *= magic_burst_multiplier # Standard +35% damage for bursts and +10% more for each step in the skillchain after 2
    d *= burst_bonus_multiplier # Magic Burst damage bonus from gear. BG lists this as separate from the standard MB multiplier
    d *= elemental_damage_bonus

    d *= futae_bonus

    d *= resist_state

    return(d)

@njit
def get_dstat_macc(player_stat, enemy_stat):
    #
    # Calculate the magic accuracy obtained from player stats vs enemy stats.
    #
    #   Note: BG Wiki states that Ninjutsu magic accuracy does not have a dSTAT term.
    #         "Ninjutsu accuracy is not affected by any dSTAT"
    #   I believe BG Wiki is incorrect and that Ninjutsu uses dINT for magic accuracy as well as damage. My reasoning is:
    #     1) The BG Wiki page for Ninjutsu is already known to be incorrect, stating
    #           "Ninjutsu have a unified V value based on tier levels, all elemental Ninjustus have the same V at the same tiers."
    #           "Like V, Ninjutsu have a unified M value not based on ΔINT ranges, but on tier level."
    #        I've already demonstrated that [M,V] changes with dINT, proving that BG Wiki is incorrect.
    #        See my testing on ffxiah: https://www.ffxiah.com/forum/topic/56749/updated-ninjutsu-damage-formulae/
    #     2) Consider other forms of magic damage:
    #            Black Magic damage and accuracy change with dINT
    #            White Magic damage and accuracy change with dMND
    #            Ninjutsu damage changes with dINT.
    #        Thus it makes sense that Ninjutsu magic accuracy also changes with dINT. I assume the functional form is identical to the other forms of magic accuracy from dSTAT.
    #     3) Ninjutsu not having any dSTAT accuracy term would be a huge magic accuracy loss that is not observed in game.
    #        This means that Ninjutsu MUST have a huge hidden magic accuracy bonus or it simply follows the same dSTAT formula as other magic damage.
    #        Since dINT affects Ninjutsu damage, I assume that dINT also affects Ninjutsu magic accuracy
    #
    #
    # The process for estimating Magic Accuracy from STAT is not explained well on the BG Wiki page...
    # My interpretation is:
    #
    # Consider the equation of a straight line:
    # 
    #     y = m*x + b
    # or
    #     MAcc_stat = m*dSTAT + b
    #
    # BG Wiki gives the slope (m) for various dSTAT ranges, but has no mention of the y-intercept (b) for these ranges.
    # BG instead provides a CHANGE in MAcc caused by a CHANGE in dSTAT. This is a derivative, so we need the derivative of the straight-line equation to relate it to BG Wiki:
    #
    #     dy = m*dx   (assuming m and b are constants)
    #
    # Now I assume that this derivative formula has an additional reasonable boundary condition:
    #
    #     y(0) = 0 
    #    (Magic Accuracy from STAT is +0 when the player has exactly 0 STAT total)
    #
    # This suggests that b = 0 for the first dSTAT range (up to dSTAT=10).
    # This is the only b value that matters for our purposes, but we could use derivative boundary conditions to derive exact formulae for y=mx+b in all ranges if we wanted to.
    #
    # We can now write a simple formula relating magic_accuracy to player_stat, enemy_stat, and m for various dSTAT ranges:
    #
    #     MAcc = 1.00*min(Enemy_INT+10, Player_INT) + 
    #            0.50*min((Enemy_INT+30)-(Enemy_INT+10), Player_INT-(Enemy_INT+10)) + 
    #            0.25*min((Enemy_INT+70)-(Enemy_INT+30), Player_INT-(Enemy_INT+30))
    #
    # As an example, consider player_INT = 254 and enemy_INT = 217.
    # 1) dINT = +37, so we need to sum the contribution from the dINT<=10 range, the dINT<=30 range, and the partial dINT<=70 range.
    # 2) dINT = 10 when player_INT = enemy_INT+10 = 227, so we gain +227 Magic Accuracy from this first dINT range just for having dINT>10
    # 3) dINT = 30 when player_INT = enemy_INT+30, but we need to subtract off the dINT<10 range or we'll double count it.
    #    This leaves Player_INT-(Enemy_INT+10) <= 20 dINT contributing to Magic Accuracy in this range. Since we have dINT=+37, we use the full 20 in this range.
    #    m=0.5 in this range, so total magic accuracy gained is 20*0.5 = 10
    # 4) Now dINT = 70 when player_INT = enemy_INT+70 = 287, which is higher than our player_INT; only a portion of our remaining INT contributes in this range
    #    Again, we need to remove the contribution from the previous dINT ranges to avoid double-counting them
    #    This leaves Player_INT-(Enemy_INT+30) <= 40 contributing in this range.
    #    In our case, we only have 254 INT, so only 254 - 217+30 = 7 of our INT contributes to this range
    #    m=0.25 for this dINT range, so we have 7*0.25 = +1.75 Magic Accuracy in the final dINT range
    #
    # 5) Adding all of these together, we get 227 + 10 + 1.75 = +238.75 Magic Accuracy from dINT alone
    # 6) This should probably be truncated, so we have +238 Magic Accuracy total from dINT alone.
    # 
    # This gets added to Magic Accuracy, <Ninjutsu> Skill, and Magic Accuracy Skill to determine Magic Hit Rate, which gives resist states later.
    #
    # As an extreme example, if we had infinite INT, then the maximum possible Magic Accuracy gained from STAT is determined entirely from the enemy_INT:
    #
    #     dstat_macc = 1.00*(enemy_stat+10) + 0.5*20 + 0.25*40
    #                = enemy_stat + 30
    #
    # For enemy_stat = 293, the maximum Magic Accuracy we could obtain from STAT would be 293+30 = 323 as long as we had dSTAT>70
    #
    dstat_macc = 1.00*max(0,min(enemy_stat+10, player_stat)) + \
                 0.50*max(0,min((enemy_stat+30)-(enemy_stat+10), player_stat-(enemy_stat+10))) + \
                 0.25*max(0,min((enemy_stat+70)-(enemy_stat+30), player_stat-(enemy_stat+30)))

    return(dstat_macc)

@njit
def get_magic_hit_rate(player_macc, enemy_meva=0):
    #
    # https://www.bg-wiki.com/ffxi/Magic_Hit_Rate
    # These equations are straightforward without room for other interpretations.
    # Looks like you simply need +45 more Magic Accuracy than the enemy's Magic Evasion to cap at 95% Magic Hit Rate
    # There is no listed MINIMUM hit rate. I assume 0% based on my previous Ninjutsu testing showing a ton of 1/16 resists in a row before including magic accuracy gear.
    dMAcc = player_macc - enemy_meva

    magic_hit_rate = 0.50 + int(dMAcc/2)/100 if dMAcc < 0 else 0.50 + int(dMAcc)/100
    magic_hit_rate = 0.95 if magic_hit_rate > 0.95 else magic_hit_rate # BG claims cap of 95%, but it feels like it should be 99%. I'll look into this later with Huge Hornets on BLM
    magic_hit_rate = 0 if magic_hit_rate < 0 else magic_hit_rate # Minimum is 0% hit rate, which always leads to a 1/8 resist.
    return(magic_hit_rate)

def get_resist_state(magic_hit_rate):
    #
    # https://www.bg-wiki.com/ffxi/Resist
    # Sounds like this bit simply rolls three times.
    # Each failed roll halves your damage.
    # 
    # This function is useful if you wanted to do simulations, but magic damage doesn't really need simulations. considering there are only a few possible damage values.
    # I instead use get_resist_state_average() to calculate the average damage from all four resist states (1/1, 1/2, 1/4, 1/8)
    #
    roll1 = np.random.uniform(0,1)
    roll2 = np.random.uniform(0,1)
    roll3 = np.random.uniform(0,1)
    resist_state = 1*(1-0.5*(roll1 > magic_hit_rate)) * (1-0.5*(roll2 > magic_hit_rate)) * (1-0.5*(roll3 > magic_hit_rate))
    return(resist_state)

@njit
def get_resist_state_average(magic_hit_rate):
    #
    # Estimate the average resist coefficient using magic hit rate
    #
    resist_state = 1*1.000*((magic_hit_rate)**3) + \
                   3*0.500*(magic_hit_rate**2)*(1-magic_hit_rate) + \
                   3*0.250*(magic_hit_rate)*((1-magic_hit_rate)**2) + \
                   1*0.125*((1-magic_hit_rate)**3)
    return(resist_state)

if __name__ == "__main__":
    #
    #
    #
    player_INT = 254
    enemy_INT = 217
    print(get_macc_dstat(player_INT, enemy_INT))
