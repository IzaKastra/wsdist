#
# Created by Kastra on Asura.
# Feel free to /tell in game or send a PM on FFXIAH you have questions, comments, or suggestions.
#
# Version date: 2023 January 21
#
# This code contains the function used to hit rates using the equation on BG Wiki
#
from numba import njit

@njit
def get_hitrate(player_accuracy, ws_acc, enemy_eva, weaponslot, first, skill_type):
    #
    # Calculate hit rates based on player and enemy stats. Uses equation from BG wiki
    # https://www.bg-wiki.com/ffxi/Hit_Rate
    # The first main- and sub-hits gain +100 accuracy (https://www.bg-wiki.com/ffxi/Category:Weapon_Skills)
    #
    if weaponslot in ["ranged", "sub"] or skill_type in ["Great Sword", "Great Axe", "Great Katana", "Scythe", "Staff", "Polearm"]: # off-hand, 2-handed, and ranged hits cap at 95% hit rate
        hitrate_cap = 0.95
    else:
        hitrate_cap = 0.99 # TODO: call this hitrate_cap instead
        
    hitrate_check = (75 + 0.5*(player_accuracy + ws_acc + 100*first - enemy_eva))/100

    hitrate_floor = 0 if weaponslot=="ranged" else 0.2 # 20% melee hit rate minimum. 0% for ranged

    if hitrate_check > hitrate_cap:
        hitrate = hitrate_cap
    elif hitrate_check < hitrate_floor:
        hitrate = hitrate_floor
    else:
        hitrate = hitrate_check

    return(hitrate)
