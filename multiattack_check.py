#
# Created by Kastra on Asura.
# Feel free to /tell in game or send a PM on FFXIAH you have questions, comments, or suggestions.
#
# Version date: 2022 January 22
#
# This code contains the function used to calculate physical damage dealt from a multi-attack.
#
from get_phys_damage import *
from pdif import *
import numpy as np

@njit
def multiattack_check(bonus_hits, ma_tp_hits, total_hits, player_attack, wpn_type_skill, pdl_trait, pdl_gear, enemy_defense, crit_rate, wpn_dmg, fstr, wsc, ftp2, crit_dmg, ws_bonus, hitrate):
    physical_damage = 0
    for k in range(bonus_hits):
        if total_hits >= 8:
            continue
        total_hits += 1 # Each hit of the multi-attack counts towards the total of 8 allowed hits per weapon skill
        if random.uniform(0,1) < hitrate:
            ma_tp_hits += 1
            pdif, crit = get_pdif_melee(player_attack, wpn_type_skill, pdl_trait, pdl_gear, enemy_defense, crit_rate)
            physical_damage += get_phys_damage(wpn_dmg, fstr, wsc, pdif, ftp2, crit, crit_dmg, 0, ws_bonus, 1) # Notice that multi-attacks all use wsd=0 and ftp2
    return(physical_damage, ma_tp_hits, total_hits)
