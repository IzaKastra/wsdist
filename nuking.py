from get_dint_m_v import *

def nuking(tier,element,gearset,player_INT, player_matk, mdmg, enemy_INT,enemy_mdb,ninjutsu_damage,futae=False,burst=False,steps=2):

    # print(tier,element,gearset,player_INT, player_matk, mdmg, enemy_INT,enemy_mdb,futae,burst,steps)

    dINT = player_INT - enemy_INT

    elemental_damage_bonus = 1+gearset.playerstats['Elemental Bonus']/100

    dayweather = 1.0

    skill_potency = 2.12 if tier > 1 else 2.0 # Assumes maximum bonus damage from Ninjutsu Skill


    if burst:
        skillchain_multiplier = 1.35 + (steps-2)*0.10

        burst_bonus1 = 40 if gearset.playerstats['Magic Burst Damage'] > 40 else gearset.playerstats['Magic Burst Damage']
        burst_bonus2 = gearset.playerstats['Magic Burst Damage II']
        burst_bonus_multiplier = 1 + burst_bonus1/100 + burst_bonus2/100

        # for i,k in enumerate(gearset.gear):
        #     print(k,gearset.gear[k]['Name2'])
        # print(burst_bonus1, burst_bonus2, burst_bonus_multiplier)
        # import sys; sys.exit()
    else:
        burst_bonus_multiplier = 1.
        skillchain_multiplier = 1.

    m,v = get_mv(tier, player_INT, enemy_INT)

    d = v+mdmg+dINT*m
    d *= (100+player_matk)/(100+enemy_mdb)
    d *= 1 + ninjutsu_damage/100
    d *= dayweather
    d *= skill_potency
    # d *= skillchain_multiplier  # Skillchain bonus should not be considered when comparing damage between different sets.
    d *= burst_bonus_multiplier
    d *= elemental_damage_bonus

    if futae:
        hands = gearset.equipped['hands']
        if "Hattori Tekko" in hands:
            d *= 1.28

    return(d)
