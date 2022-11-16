#
# Created by Kastra on Asura.
# Feel free to /tell in game or send a PM on FFXIAH you have questions, comments, or suggestions.
#
# Version date: 2022 January 22
#
# This code contains the function used to hit rates using the equation on BG Wiki
#
from numba import njit

@njit
def get_hitrate(player_accuracy, ws_acc, enemy_eva, weaponslot, first):
    #
    # Calculate hit rates based on player and enemy stats. Uses equation from BG wiki
    # https://www.bg-wiki.com/ffxi/Hit_Rate
    # The first main- and sub-hits gain +100 accuracy (https://www.bg-wiki.com/ffxi/Category:Weapon_Skills)
    #
    if weaponslot == 'main': # Main hits caps at 99% hit rate
        accuracy_cap = 0.99
    elif weaponslot == 'sub': # Sub hits cap at 95% hit rate
        accuracy_cap = 0.95

    acc_check = (75 + 0.5*(player_accuracy + ws_acc + 100*first - enemy_eva))/10

    if acc_check > accuracy_cap:
        hitrate = accuracy_cap
    elif acc_check < 0.2: # Minimum hit rate is 20%
        hitrate = 0.2
    else:
        hitrate = acc_check

    return(hitrate)
