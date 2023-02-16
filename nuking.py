# Author: Kastra (Asura)
# Version date: 2023 February 16

from get_dint_m_v import *
import numpy as np

def quickdraw(rng_dmg, ammo_dmg, element, gearset, player_matk, player_magic_damage, enemy_int, enemy_mdb, enemy_meva):
    #
    # Calculate Quick Draw damage
    #
    magic_accuracy = gearset.playerstats["Magic Accuracy"] # Read base Magic Accuracy from playerstats, including traits and gear with "Magic Accuracy"

    magic_accuracy_skill = gearset.playerstats["Magic Accuracy Skill"] # Magic Accuracy from Magic Accuracy Skill. Currently includes off-hand weapon stats.
    magic_accuracy_skill -= gearset.gear["sub"].get("Magic Accuracy Skill",0) # Subtract off the Magic Accuracy Skill from the off-hand slot, since it does not contribute to spell accuracy.
    magic_accuracy += magic_accuracy_skill # Add on the "Magic Accuracy Skill" stat

    dstat_macc = gearset.playerstats.get("AGI",0)/2 # Apparently quick draw gets magic accuracy from AGI. No info on BG, but ffxiclopedia suggests 2 AGI = 1 MAcc.
                                                    # 2:1 seems like a reasonable estimate.
    magic_accuracy += dstat_macc # Add on magic accuracy from dstat

    if "Death Penalty" in gearset.gear["ranged"]["Name2"]:
        magic_accuracy += 60

    base_damage = ((rng_dmg+ammo_dmg)*2 + gearset.playerstats["Quick Draw"] + player_magic_damage)
    damage = base_damage * (1 + gearset.playerstats["Quick Draw II"]/100) # Death Penalty + Empyrean feet.



    elemental_damage_bonus = 1 + (gearset.playerstats['Elemental Bonus'] + gearset.playerstats[f'{element.capitalize()} Elemental Bonus'])/100
    damage *= elemental_damage_bonus
    dayweather = 1.0 # This is changed to 1.25 for SCH helix. Maybe also change it 1.10 for /sch for single-weather.

    magic_hit_rate = get_magic_hit_rate(magic_accuracy, enemy_meva) if enemy_meva > 0 else 1.0 # This is weird for quick draw. I assume my QD macc is incorrect. i recommend always using meva=0 for QD
    resist_state = get_resist_state_average(magic_hit_rate)

    damage *= (100+player_matk)/(100+enemy_mdb)
    damage *= dayweather
    damage *= elemental_damage_bonus
    damage *= (1 + 0.25 * gearset.playerstats["Magic Crit Rate II"]/100) # Magic Crit Rate II is apparently +25% damage x% of the time. Only Sroda tathlum atm
    damage *= resist_state

    return(damage)

def nuking(spell, spelltype, tier, element, gearset, player_INT, player_matk, mdmg, enemy_INT, enemy_mdb, enemy_meva, ninjutsu_damage, futae=False, burst=False, ebullience=False):

    steps = 2 # 2-step skillchain

    # print(spelltype, tier, element, gearset, player_INT, player_matk, mdmg, enemy_INT, enemy_mdb, ninjutsu_damage, futae, burst, steps)

    # Determine Magic Accuracies
    spelltype_skill = gearset.playerstats[f"{spelltype} Skill"] # Magic Accuracy from Ninjutsu Skill.

    magic_accuracy_skill = gearset.playerstats["Magic Accuracy Skill"] # Magic Accuracy from Magic Accuracy Skill. Currently includes off-hand weapon stats.
    magic_accuracy_skill -= gearset.gear["sub"].get("Magic Accuracy Skill",0) # Subtract off the Magic Accuracy Skill from the off-hand slot, since it does not contribute to spell accuracy.

    dstat_macc = get_dstat_macc(player_INT, enemy_INT) # Get magic accuracy from dINT

    magic_accuracy = gearset.playerstats["Magic Accuracy"] # Read base Magic Accuracy from playerstats, including traits and gear with "Magic Accuracy"
    magic_accuracy += magic_accuracy_skill # Add on the "Magic Accuracy Skill" stat
    magic_accuracy += spelltype_skill # Add on the "Ninjutsu Skill" or "Elemental Magic Skill" stat depending on spell being cast
    magic_accuracy += dstat_macc # Add on magic accuracy from dINT

    dINT = player_INT - enemy_INT

    elemental_damage_bonus = 1 + (gearset.playerstats['Elemental Bonus'] + gearset.playerstats[f'{element.capitalize()} Elemental Bonus'])/100

    dayweather = 1.0 # This is changed to 1.25 for SCH helix. Maybe also change it 1.10 for /sch for single-weather.

    if burst: # Do burst stuff now so we can add +100 Magic Accuracy before calculating magic hit rates
        magic_accuracy += 100 + gearset.playerstats["Magic Burst Accuracy"]
        magic_burst_multiplier = 1.35 # Standard +35% damage for magic bursting
        skillchain_steps_bonus = (steps-2)*0.10 # Another +10% for each step in the skillchain after 2
        magic_burst_multiplier += skillchain_steps_bonus
        
        
        burst_bonus1 = 40 if gearset.playerstats['Magic Burst Damage'] > 40 else gearset.playerstats['Magic Burst Damage']
        burst_bonus2 = gearset.playerstats['Magic Burst Damage II']
        burst_bonus3 = gearset.playerstats["Magic Burst Damage Trait"]
        burst_bonus_multiplier = 1 + burst_bonus1/100 + burst_bonus2/100 + burst_bonus3/100

        # for i,k in enumerate(gearset.gear):
        #     print(k,gearset.gear[k]['Name2'])
        # print(burst_bonus1, burst_bonus2, burst_bonus_multiplier)
        # import sys; sys.exit()
    else:
        burst_bonus_multiplier = 1.
        magic_burst_multiplier = 1.

    
    magic_hit_rate = get_magic_hit_rate(magic_accuracy, enemy_meva) if enemy_meva > 0 else 1.0
    resist_state = get_resist_state_average(magic_hit_rate)
    # print(magic_hit_rate,spelltype_skill,magic_accuracy_skill,dstat_macc,magic_accuracy,resist_state)
    # print(magic_accuracy, enemy_meva, magic_hit_rate, resist_state)


    klimaform_bonus = 1.0
    ebullience_bonus = 1.0
    futae_bonus = 1.0
    extra_gear_bonus = 1.0 # For now, this is just Akademos +2% damage if spell element = weather
    if spelltype == "Ninjutsu":
        if tier == "Ichi":
            ninjutsu_skill_potency = ((100 + (spelltype_skill-50)/2)/100 if spelltype_skill <= 250 else 2.0) if spelltype_skill > 50 else 1.0
        elif tier == "Ni":
            ninjutsu_skill_potency = ((100 + (spelltype_skill-126)/2)/100 if spelltype_skill <= 350 else 2.12) if spelltype_skill > 126 else 1.0
        elif tier == "San":
            ninjutsu_skill_potency = ((100 + (spelltype_skill-276)/2)/100 if spelltype_skill <= 500 else 2.12) if spelltype_skill > 276 else 1.0
        else:
            ninjutsu_skill_potency = 0 # If something breaks and tier wasn't given, then just give 0 potency (results in zero damage always).

        m,v = get_mv(tier, player_INT, enemy_INT)
        d = int(v+mdmg+dINT*m)

        if futae: # Futae = False if not Ninjutsu
            futae_bonus = 1.5 # Standard +50% damage when using futae
            if gearset.equipped['hands'] == "Hattori Tekko +3":
                futae_bonus += 0.28

    else: # Else Elemental Magic
        ninjutsu_skill_potency = 1.0

        dINT = 0 if dINT < 0 else dINT # For now, assume that dINT has an absolute minimum of 0. I believe I estimated this to be false as observed in game, but whatever.
        if spell != "Kaustra":
            # Kaustra uses a special base damage formula.

            m, v, window = get_mv_blm(element, tier, player_INT, enemy_INT)
            d = int(v+mdmg+(dINT-window)*m) # Black Magic uses (dINT-window)*m. This was simply a choice of the person who collected and fit the data.
        else:
            player_level = 99
            dINT = 0 if dINT < 0 else dINT 
            dINT = 300 if dINT > 300 else dINT 
            d = np.round(0.067*player_level,1)*(37+int(0.67*dINT))
        if ebullience:
            ebullience_bonus = 1.2
            if gearset.equipped["head"] == "Arbatel Bonnet +3":
                ebullience_bonus += 0.21


    # These next few are outside the Elemental Magic block since they apply for "spells with element that matches day/weather", which technically applies to Ninjutsu until proven otherwise.
    if gearset.equipped["feet"] == "Arbatel Loafers +3": # Only SCH can use these feet
        klimaform_bonus += 0.25 # Assume full-time klimaform on SCH Main

    if tier=="helix": # Only SCH has access to helix spells. TODO: add /sch helix1 spells and use tier=helix1 and tier=helix2 to distinguish between them
        dayweather = 1.25 # Helix spells do not need the Obi to gain weather effects. 
                            # SCH is the only job able to cast Helix2 spells, so if tier="helix", then job=SCH and we can assume double weather is always on.

    if gearset.equipped["main"] == "Akademos": # Technically this applies to Ninjutsu as well, so I've put it outside of the Elemental Magic section
        extra_gear_bonus += 0.02

    d = int(d * ninjutsu_skill_potency)
    d = int(d * (100+player_matk)/(100+enemy_mdb))
    d *= 1 + ninjutsu_damage/100
    d *= dayweather
    d *= magic_burst_multiplier # Standard +35% damage for bursts and +10% more for each step in the skillchain after 2
    d *= burst_bonus_multiplier # Magic Burst damage bonus from gear. BG lists this as separate from the standard MB multiplier
    d *= elemental_damage_bonus

    d *= (1 + 0.25 * gearset.playerstats["Magic Crit Rate II"]/100) # Magic Crit Rate II is apparently +25% damage x% of the time.

    d *= klimaform_bonus
    d *= ebullience_bonus
    d *= extra_gear_bonus
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
