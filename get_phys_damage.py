#
# Created by Kastra on Asura.
# Feel free to /tell in game or send a PM on FFXIAH you have questions, comments, or suggestions.
#
# Version date: 2022 January 22
#
# This code contains the function used to calculate physical damage dealt from a single weapon swing.
#
from numba import njit

@njit
def get_phys_damage(wpn_dmg, fstr_wpn, wsc, pdif, ftp, crit, crit_dmg, wsd, ws_bonus, n):
    #
    # Calculate physical damage dealt for a single attack of a weapon skill. Uses equation from BG wiki
    # https://www.bg-wiki.com/ffxi/Weapon_Skill_Damage
    #
    phys = int(  (wpn_dmg + fstr_wpn + wsc) * ftp * pdif * (1 + crit*crit_dmg) * (1+wsd*(n==0)) * (1+ws_bonus)  )
    return(phys)

@njit
def get_avg_phys_damage(wpn_dmg, fstr_wpn, wsc, pdif, ftp, crit_rate, crit_dmg, wsd, ws_bonus):
    #
    # Calculate average physical damage dealt for a single attack of a weapon skill. Uses equation from BG wiki
    # https://www.bg-wiki.com/ffxi/Weapon_Skill_Damage
    #
    phys = int(  (wpn_dmg + fstr_wpn + wsc) * ftp * pdif * (1 + crit_rate*crit_dmg) * (1+wsd)*(1+ws_bonus)  )
    return(phys)
