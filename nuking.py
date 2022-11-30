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
    # The JP blog (auto translated: https://luteff11.livedoor.blog/archives/49725347.html) is pretty clear.

    # First version based only on BG Wiki. It uses my incorrect interpretation of what BG Wiki is trying to say.
    # dstat_macc = 1.00*max(0,min(enemy_stat+10, player_stat)) + \
    #              0.50*max(0,min((enemy_stat+30)-(enemy_stat+10), player_stat-(enemy_stat+10))) + \
    #              0.25*max(0,min((enemy_stat+70)-(enemy_stat+30), player_stat-(enemy_stat+30)))

    dstat = player_stat - enemy_stat

    if dstat <= -70:
        dstat_macc = -30
    elif dstat <= -30:
        dstat_macc = 0.25*dstat - 12.5
    elif dstat <= -10:
        dstat_macc = 0.5*dstat - 5.0
    elif dstat <= 10:
        dstat_macc = 1.0*dstat
    elif dstat <= 30:
        dstat_macc = 0.5*dstat + 5.0
    elif dstat <= 70:
        dstat_macc = 0.25*dstat + 12.5
    else:
        dstat_macc = 30

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
    # Sounds like this bit simply rolls three times or until your roll wins.
    # Each failed roll halves your damage.
    # 
    # This function is useful if you wanted to do simulations, but magic damage doesn't really need simulations. considering there are only a few possible damage values.
    # I instead use get_resist_state_average() to calculate the average damage from all four resist states (1/1, 1/2, 1/4, 1/8)
    #
    # roll1 = np.random.uniform(0,1)
    # roll2 = np.random.uniform(0,1)
    # roll3 = np.random.uniform(0,1)
    # resist_state = 1*(1-0.5*(roll1 > magic_hit_rate)) * (1-0.5*(roll2 > magic_hit_rate)) * (1-0.5*(roll3 > magic_hit_rate))

    resist_state = 1.0
    for k in range(3):
        if magic_hit_rate >= np.random.uniform(0,1):
            break
        else:
            resist_state *= 0.5

    return(resist_state)

@njit
def get_resist_state_average(magic_hit_rate):
    #
    # Estimate the average resist coefficient using magic hit rate
    #
    # resist_state = 1*1.000*((magic_hit_rate)**3) + \
    #                3*0.500*(magic_hit_rate**2)*(1-magic_hit_rate) + \
    #                3*0.250*(magic_hit_rate)*((1-magic_hit_rate)**2) + \
    #                1*0.125*((1-magic_hit_rate)**3)

    resist_state = magic_hit_rate + \
                   0.500*magic_hit_rate*(1-magic_hit_rate) + \
                   0.250*magic_hit_rate*((1-magic_hit_rate)**2) + \
                   0.125*((1-magic_hit_rate)**3)

    return(resist_state)

if __name__ == "__main__":
    #
    #
    #
    player_INT = 254
    enemy_INT = 217
    print(get_macc_dstat(player_INT, enemy_INT))
