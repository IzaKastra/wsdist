# Author: Kastra (Asura)
# Version date: 2022 November 27

from get_dint_m_v import *

def nuking(spelltype, tier, element, gearset, player_INT, player_matk, mdmg, enemy_INT, enemy_mdb, ninjutsu_damage, futae=False, burst=False, steps=2):

    # print(spelltype, tier, element, gearset, player_INT, player_matk, mdmg, enemy_INT, enemy_mdb, ninjutsu_damage, futae, burst, steps)

    dINT = player_INT - enemy_INT

    elemental_damage_bonus = 1+gearset.playerstats['Elemental Bonus']/100 + gearset.playerstats[f'{element.capitalize()} Elemental Bonus']/100

    dayweather = 1.0

    if burst:
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


    futae_bonus = 1.0
    if spelltype == "Ninjutsu":
        ninjutsu_skill_potency = 2.00 if tier=="Ichi" else 2.12 # Assumes maximum bonus damage from Ninjutsu Skill. This is true for ML24+ NIN with Relic feet. ML20=496 skill
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

    else:
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

    return(d)
