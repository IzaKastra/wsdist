#
# Created by Kastra on Asura.
# Feel free to /tell in game or send a PM on FFXIAH you have questions, comments, or suggestions.
#
# Version date: 2022 January 22
#
# This code contains the function used to calculate the player's fSTR stat.
#
from numba import njit

@njit
def get_fstr(dmg, player_str, enemy_vit):
    #
    # Calculate fSTR using equation from BG wiki
    # https://www.bg-wiki.com/ffxi/FSTR
    #
    dstr = player_str - enemy_vit
    if dstr <= -22:
        fstr = (dstr+13)/4
    elif dstr <= -16:
        fstr = (dstr+12)/4
    elif dstr <= -8:
        fstr = (dstr+10)/4
    elif dstr <= -3:
        fstr = (dstr+9)/4
    elif dstr <= 0:
        fstr = (dstr+8)/4
    elif dstr <= 5:
        fstr = (dstr+7)/4
    elif dstr < 12:
        fstr = (dstr+6)/4
    elif dstr >= 12:
        fstr = (dstr+4)/4

    if fstr < -1*dmg/9.:
        fstr = -1*dmg/9.

    elif fstr > 8+(dmg/9.):
        fstr = 8+(dmg/9.)

    return(fstr)
