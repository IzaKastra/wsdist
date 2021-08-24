#
# Created by Kastra on Asura.
# Feel free to /tell in game or send a PM on FFXIAH you have questions, comments, or suggestions.
#
# Version date: 2021 August 22
#
# This is the main code that gets run. It reads in the init file for user-defined parameters and runs the simulations to find the best gear set by calling the functions within this code and within other codes.
#
from numba import njit
from scipy.interpolate import interp1d
import numpy as np

import datetime

from pdif import *
from get_tp import get_tp
from gearsets import *
from get_mdelay import *
from buffs import *
from fancy_plot import *

import random

class TP_Error(Exception):
    pass

base_tp = [1000,2000,3000]

@njit
def get_ma_rate(nhits, qa, ta, da, oa3, oa2, sub_type, hitrate_matrix):
    #
    # Estimate the number of attacks per weapon through simulation.
    # You can use things like:
    #     ta_rate = (1-qa)*ta
    #     da_rate = (1-qa)*(1-ta)*da
    #     oa3_rate = (1-qa)*(1-ta)*(1-da)*oa3
    #   but you'd need an increasingly-complicated correction term in each formula to deal with the 8-hit maximum preventing some of the hits from taking place
    # It's easier for me to just run 50,000 simulations to estimate the true values than sit down and calculate the correction term by hand and then type it out here
    #
    dual_wield = True if sub_type == 'Weapon' else False # Check if the item equipped in the sub slot is a weapon. If this line returns an error, check the "gear.py" file to see if the item in the sub slot has a "Type" key. Python is case-sensitive too

    n_sim = 50000
    main_hits_list = np.zeros(n_sim) # List containing number of main hits per simulation. Will take average of this later
    sub_hits_list = np.zeros(n_sim) # List containing number of sub hits per simuation. Will take average of this later
    for k in range(n_sim):
        main_hits = 0
        sub_hits = 0
        total_hits = 0

        for l in range(nhits):

            if l==0:
                first = 1
            else:
                first = 0


            hitrate1 = hitrate_matrix[first][0] # Main hand hit rate. Caps at 99%
            hitrate2 = hitrate_matrix[first][1] # Off hand hit rate. Caps at 95%

            if total_hits >= 8:
                continue
            main_hits += 1*hitrate1
            total_hits += 1
            if l == 0 or (l == 1 and not dual_wield): # Main hit gets two multi-attack proc checks if not dual wielding
                if random.uniform(0,1) < qa:
                    for m in range(3):
                        if total_hits >= 8:
                            continue
                        main_hits += 1*hitrate1
                        total_hits += 1
                elif random.uniform(0,1) < ta:
                    for m in range(2):
                        if total_hits >= 8:
                            continue
                        main_hits += 1*hitrate1
                        total_hits += 1
                elif random.uniform(0,1) < da:
                    for m in range(1):
                        if total_hits >= 8:
                            continue
                        main_hits += 1*hitrate1
                        total_hits += 1
                elif random.uniform(0,1) < oa3:
                    for m in range(2):
                        if total_hits >= 8:
                            continue
                        main_hits += 1*hitrate1
                        total_hits += 1
                elif random.uniform(0,1) < oa2:
                    for m in range(1):
                        if total_hits >= 8:
                            continue
                        main_hits += 1*hitrate1
                        total_hits += 1

            if l == 0: # Check sub hit after the first main hit
                if dual_wield:
                    sub_hits += 1*hitrate2
                    total_hits += 1
                    if random.uniform(0,1) < qa:
                        for m in range(3):
                            if total_hits >= 8:
                                continue
                            sub_hits += 1*hitrate2
                            total_hits += 1
                    elif random.uniform(0,1) < ta:
                        for m in range(2):
                            if total_hits >= 8:
                                continue
                            sub_hits += 1*hitrate2
                            total_hits += 1
                    elif random.uniform(0,1) < da:
                        for m in range(1):
                            if total_hits >= 8:
                                continue
                            sub_hits += 1*hitrate2
                            total_hits += 1

        main_hits_list[k] = main_hits
        sub_hits_list[k] = sub_hits

    main_hits = np.mean(main_hits_list)
    sub_hits = np.mean(sub_hits_list)

    return(main_hits, sub_hits)


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

@njit
def get_dex_crit(player_dex, enemy_agi):
    #
    # Calculate DEX-based crit using the equation from BG wiki
    # https://www.bg-wiki.com/ffxi/Critical_Hit_Rate
    #
    ddex = player_dex - enemy_agi

    if ddex <= 6:
        dex_crit = 0.00
    elif ddex <=13:
        dex_crit = 0.01
    elif ddex <= 19:
        dex_crit = 0.02
    elif ddex <= 29:
        dex_crit = 0.03
    elif ddex <=39:
        dex_crit = 0.04
    else:
        ddex_check = (ddex-35)/100
        dex_crit = ddex_check if ddex_check <= 0.15 else 0.15

    return(dex_crit)


@njit
def get_phys_damage(wpn_dmg, fstr_wpn, wsc, pdif, ftp, crit, crit_dmg, wsd, ws_bonus, total_hits):
    #
    # Calculate physical damage dealt for a single attack of a weapon skill. Uses equation from BG wiki
    # https://www.bg-wiki.com/ffxi/Weapon_Skill_Damage
    #
    # This function probably doesn't need "total_hits"
    # I could update it to remove "total_hits" and simply pass in wsd=0 for non-first hits, which I already do anyway.
    # Will look into this later, but I think it's safe to remove "total_hits" right now.
    # Can also remove "crit" and simply pass "crit_dmg=0" if not a crit.
    #
    phys = int(  (wpn_dmg + fstr_wpn + wsc) * ftp * pdif * (1 + crit*crit_dmg) * (1+ws_bonus+wsd*(total_hits==1))  )
    return(phys)

@njit
def get_avg_phys_damage(wpn_dmg, fstr_wpn, wsc, pdif, ftp, crit_rate, crit_dmg, wsd, ws_bonus):
    #
    # Calculate average physical damage dealt for a single attack of a weapon skill. Uses equation from BG wiki
    # https://www.bg-wiki.com/ffxi/Weapon_Skill_Damage
    #
    phys = int(  (wpn_dmg + fstr_wpn + wsc) * ftp * pdif * (1 + crit_rate*crit_dmg) * (1+ws_bonus+wsd)  )
    return(phys)


@njit
def get_hitrate(player_accuracy, ws_acc, enemy_eva, enemy_lvl, weaponslot, hitaki, first):
    #
    # Calculate hit rates based on player and enemy stats. Uses equation from BG wiki
    # https://www.bg-wiki.com/ffxi/Hit_Rate
    # The first main and sub hits gain +100 accuracy (https://www.bg-wiki.com/ffxi/Category:Weapon_Skills)
    #
    # I think this function also doesn't really need "weaponslot", "first", or "ws_acc"
    # Might update it later, but it works for now so not a big deal.
    #
    if weaponslot == 'main': # Main hits caps at 99% hit rate
        accuracy_cap = 0.99
    elif weaponslot == 'sub': # Sub hits cap at 95% hit rate
        accuracy_cap = 0.95

    acc_check = (75 + 0.5*(player_accuracy+100*first + ws_acc - enemy_eva) - 2*(enemy_lvl - (119-0*hitaki)))/100 # Assume player level is 119. I previously thought that Hitaki dropped iLvl to 117, but I checked this in game again and notice no ilvl drop when using Hitaki.

    if acc_check > accuracy_cap:
        hitrate = accuracy_cap
    elif acc_check < 0.2: # Minimum hit rate is 20%
        hitrate = 0.2
    else:
        hitrate = acc_check

    return(hitrate)

def weaponskill(ws_name, gearset, tp, enemy_lvl, enemy_defense, enemy_eva, enemy_vit, enemy_agi, enemy_mdb, attack_cap, buffs, equipment, final=False):
    #
    # Use the player and enemy stats to calculate weapon skill damage.
    # This function works, but needs to be cleaned up. There is too much going on within it.
    # It would be easier to rewrite the entire code and simply borrow from what I already have.
    #
    if tp < 1000:
        print(f'TP must be greater than 1000 to use a Weapon skill; TP = {tp}')
        raise TP_Error

    # Save the main and sub weapon names for later.
    # Used to check if giving weapon skill damage bonuses on things like Gokotai (if "Gokotai" in main_wpn_name)
    main_wpn_name = gearset.equipment()['main']
    try:
        sub_wpn_name = gearset.gear['sub']['Name2']
    except:
        sub_wpn_name = gearset.gear['sub']['Name']

    sub_type = gearset.gear['sub'].get('Type', 'None') # Check if the item equipped in the sub slot is a weapon or a grip. If the item doesn't have a "Type" Key then return "None"
    dual_wield = sub_type == 'Weapon'

    main_type_skill = gearset.gear['main']['Skill Type']
    sub_type_skill = gearset.gear['sub'].get('Skill Type', 'None') # If the sub item doesn't have a skill type (Katana/Dagger/Scythe, etc) then return "None"

    tp += gearset.playerstats['TP Bonus'] # Add TP bonus
    tp = 3000 if tp > 3000 else int(tp) # Cap TP at 3000

    main_dmg = gearset.playerstats['DMG1']
    sub_dmg  = gearset.playerstats['DMG2']

    fotia_ftp = gearset.playerstats['ftp']
    pdl_gear  = gearset.playerstats['PDL']
    pdl_trait = gearset.playerstats['PDL Trait']

    player_str = gearset.playerstats['STR']
    player_dex = gearset.playerstats['DEX']
    player_vit = gearset.playerstats['VIT']
    player_agi = gearset.playerstats['AGI']
    player_int = gearset.playerstats['INT']
    player_mnd = gearset.playerstats['MND']
    player_chr = gearset.playerstats['CHR']

    player_attack1 = gearset.playerstats['Attack1'] if not attack_cap else 99999 # If you set "attack_cap = True" then use attack = 99999 to be lazy.
    player_attack2 = gearset.playerstats['Attack2'] if not attack_cap else 99999
    player_attack2 = 0 if not dual_wield else player_attack2

    player_accuracy1 = gearset.playerstats['Accuracy1']
    player_accuracy2 = gearset.playerstats['Accuracy2'] if dual_wield else 0

    delay1 = gearset.playerstats['Delay1'] # Main-hand delay, used for TP return
    delay2 = gearset.playerstats['Delay2'] if dual_wield else delay1 # Main-hand delay, used for TP return
    dw = gearset.playerstats['Dual Wield'] if dual_wield else 0 # Used for TP return
    mdelay = get_mdelay(delay1, delay2, dw) # Used for TP return

    wsd = gearset.playerstats['Weaponskill Damage'] # Applies to first hit only
    ws_acc = gearset.gearstats['Weaponskill Accuracy']
    ws_bonus = gearset.playerstats['Weaponskill Bonus'] # Bonus damage multiplier to every hit on the WS. Stuff like Gokotai, Naegling, hideen Relic/Mythic WS damage, REMA augments, and /drg

    crit_dmg = gearset.playerstats['Crit Damage'] # Only gets applied if the weapon skill crits
    crit_rate = 0 # WSs can't crit unless they explicitly say they can (Blade: Hi, Evisceration, etc). Crit rate is read in properly only for those weapon skills (see below) and the special case with Shining One

    qa = gearset.playerstats['QA']/100
    ta = gearset.playerstats['TA']/100
    da = gearset.playerstats['DA']/100
    oa3 = 0 # Only applies with Mythic Aftermath on WSs and only on the hand holding the weapon. Same deal as crit rate. OA3 and OA2 are read in properly if using Nagi main hand for AM3. See below.
    oa2 = 0 # Only applies with Mythic Aftermath on WSs and only on the hand holding the weapon. Same deal as crit rate. OA3 and OA2 are read in properly if using Nagi main hand for AM3. See below.

    stp = gearset.playerstats['STP']/100

    player_mab = gearset.playerstats['Magic Attack']
    player_magic_damage = gearset.playerstats['Magic Damage']

    dStat = ['STR', 0] # Part of the fix for Crepsecular Knife's CHR bonus. Needed to first assign a base dStat bonus. In this case I just used STR with 0 bonus to apply to all WSs, and Crepsecular just changes this to ['CHR', 0.03]. Utu Grip changes this to ['DEX', 0.10]

    # Setup special weapon bonuses
    if main_wpn_name == 'Naegling':
        if ws_name == 'Savage Blade':
            ws_bonus += 0.15
    elif 'Kikoku' in main_wpn_name:
        if ws_name == 'Blade: Metsu':
            ws_bonus += 0.68 # Hidden +40% Relic WS damage * R15 +20% WS damage (1.4)*(1.2)
    elif 'Kannagi' in main_wpn_name:
        if ws_name == 'Blade: Hi':
            ws_bonus += 0.1
    elif 'Nagi' in main_wpn_name:
        oa3 += 0.2 ; oa2 += 0.4
        if ws_name == 'Blade: Kamu':
            ws_bonus += 0.495 # Hidden +30% Relic WS damage * R15 +15% WS damage (1.3)*(1.15)
    elif 'Heishi' in main_wpn_name:
        if ws_name == 'Blade: Shun':
            ws_bonus += 0.1
    elif main_wpn_name == 'Gokotai':
        if ws_name == 'Blade: Ku':
            ws_bonus += 0.6
    elif main_wpn_name == 'Tauret':
        if ws_name == 'Evisceration':
            ws_bonus += 0.5
    elif main_wpn_name == 'Karambit':
        if ws_name == "Asuran Fists":
            ws_bonus += 0.5
    elif main_wpn_name == 'Dojikiri Yasutsuna':
        if ws_name == 'Tachi: Shoha':
            ws_bonus += 0.1
    elif main_wpn_name == 'Kogarasumaru':
        oa3 += 0.2 ; oa2 += 0.4
        if ws_name == 'Tachi: Rana':
            ws_bonus += 0.495
    elif main_wpn_name == 'Masamune':
        if ws_name == 'Tachi: Fudo':
            ws_bonus += 0.1
    elif main_wpn_name == 'Amanomurakumo':
        if ws_name == 'Tachi: Kaiten':
            ws_bonus += 0.68
    elif main_wpn_name == 'Shining One':
        # Shining One allows all weapon skills to crit. Seems pretty OP, but here we are...
        # https://www.bg-wiki.com/ffxi/Shining_One
        crit_rate +=  gearset.playerstats['Crit Rate']/100
        crit_boost = [0.05, 0.10, 0.15]
        crit_bonus = interp1d(base_tp, crit_boost)(tp)
        crit_rate += crit_bonus
        crit_rate += get_dex_crit(player_dex, enemy_agi)
        if ws_name == 'Impulse Drive':
            ws_bonus += 0.4
    elif main_wpn_name == 'Hachimonji':
        # Hachimonji does some weird stuff with store TP and multi-hits. I didn't include it here. The effect seems actually detrimental for TPing.
        # https://www.bg-wiki.com/ffxi/Hachimonji
        if ws_name == 'Tachi: Kasha':
            ws_bonus += 0.25

    if sub_wpn_name == "Crepsecular Knife":
        dStat = ['CHR', 0.03]
    elif sub_wpn_name == "Utu Grip":
        dStat = ['DEX', 0.10]

    # Setup weaponskill statistics (TP scaling, # of hits, ftp replication, WSC, etc)
    hybrid = False # All weaponskills are assumed physical. This is changed to True for hybrids to add in the bonus magic damage.
    magical = False # Have not added in magical weapon skill yet.
    if ws_name == 'Savage Blade':
        base_ftp = [4.0, 10.25, 13.75] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = interp1d(base_tp, base_ftp)(tp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc  = int(0.5*(player_str + player_mnd) + dStat[1]*gearset.playerstats[dStat[0]]) # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 2 # Savage is a 2-hit weaponskill (+1 for offhand)
    elif ws_name == 'Blade: Shun':
        atk_boost = [1.0, 2.0, 3.0]
        ws_atk_bonus = interp1d(base_tp, atk_boost)(tp) - 1.0
        special_set = set_gear(buffs, equipment, ws_atk_bonus) # The attack bonus from Blade: Shun is applied before buffs. I needed to recalculate player attack with a "special set" to deal with this.
        player_attack1 = special_set.playerstats['Attack1'] # Redefine the player's attack1 and attack2 used in the weapon skill based on the FTP scaling value
        player_attack2 = special_set.playerstats['Attack2'] # These boosted attack1 and attack2 values do not show up in the player's stats shown in the final plot.
        ftp = 1.0
        ftp_rep = True
        wsc  = 0.85*player_dex + dStat[1]*gearset.playerstats[dStat[0]] # Assuming 5/5 Blade: Shun merits.
        nhits = 5
    elif ws_name == 'Blade: Ten':
        base_ftp = [4.5, 11.5, 15.5]
        ftp      = interp1d(base_tp, base_ftp)(tp)
        ftp_rep = False
        wsc      = 0.3*(player_str+player_dex) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits    = 1
    elif ws_name == 'Blade: Kamu':
        ftp  = 1.0
        ftp_rep = False
        wsc = 0.6*(player_int+player_str)
        nhits = 1
        special_set = set_gear(buffs, equipment, 1.25) # The attack bonus from Blade: Kamu is similar to Blade: Shun (see above)
        player_attack1 = special_set.playerstats['Attack1']
        player_attack2 = special_set.playerstats['Attack2']
        enemy_defense *= 0.75
    elif ws_name == 'Blade: Ku':
        acc_boost = [1.0, 1.05, 1.1] # Made these numbers up since it isnt known. It's probably just something like "accuracy+0/20/40".
        acc_bonus = interp1d(base_tp, acc_boost)(tp)
        ftp  = 1.25
        ftp_rep = True
        wsc = 0.3*(player_str+player_dex) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 5
    elif ws_name == 'Blade: Metsu':
        ftp  = 5.0
        ftp_rep = False
        wsc = 0.8*player_dex
        nhits = 1
    elif ws_name == 'Blade: Hi':
        crit_rate +=  gearset.playerstats['Crit Rate']/100 # Blade: Hi can crit, so define crit rate now
        crit_boost = [0.15, 0.2, 0.25]
        crit_bonus = interp1d(base_tp, crit_boost)(tp) # Bonus crit rate from TP scaling
        crit_rate += crit_bonus
        crit_rate += get_dex_crit(player_dex, enemy_agi) # Bonus crit rate from the player's DEX stat vs enemy AGI stat
        ftp = 5.0
        ftp_rep = False
        wsc = 0.8*player_agi + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1
    elif ws_name == 'Evisceration':
        crit_rate +=  gearset.playerstats['Crit Rate']/100
        crit_boost = [0.1, 0.25, 0.5]
        crit_bonus = interp1d(base_tp, crit_boost)(tp)
        crit_rate += crit_bonus
        crit_rate += get_dex_crit(player_dex, enemy_agi)
        ftp = 1.25
        ftp_rep = True
        wsc = 0.5*player_dex + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 5
    elif ws_name == 'Blade: Chi':
        hybrid    = True
        base_ftp  = [0.5, 1.375, 2.25]
        ftp_hybrid = interp1d(base_tp, base_ftp)(tp)
        ftp       = 1.0
        ftp_rep   = False
        wsc       = 0.3*(player_str+player_int) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits     = 2
        element   = 'Earth'
    elif ws_name == 'Blade: Teki':
        hybrid    = True
        base_ftp  = [0.5, 1.375, 2.25]
        ftp_hybrid = interp1d(base_tp, base_ftp)(tp)
        ftp       = 1.0
        ftp_rep   = False
        wsc       = 0.3*(player_str+player_int) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits     = 1
        element   = 'Water'
    elif ws_name == 'Blade: To':
        hybrid    = True
        base_ftp  = [0.5, 1.5, 2.5]
        ftp_hybrid = interp1d(base_tp, base_ftp)(tp)
        ftp       = 1.0
        ftp_rep   = False
        wsc       = 0.4*(player_str+player_int) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits     = 1
        element   = 'Ice'
    elif ws_name == 'Blade: Retsu':
        base_ftp  = [0.5, 1.5, 2.5]
        ftp       = 1.0
        ftp_rep   = False
        wsc       = 0.6*player_dex + 0.2*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits     = 2
    elif ws_name == 'Asuran Fists':
        acc_boost = [1.0, 1.1, 1.2] # Made these numbers up, same as Blade: Ku (see above)
        acc_bonus = interp1d(base_tp, acc_boost)(tp)
        ftp       = 1.25
        ftp_rep   = True
        wsc       = 0.15*(player_vit + player_str) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits     = 8
    elif ws_name == 'Impulse Drive':
        base_ftp = [1.0, 3.0, 5.5]
        ftp      = interp1d(base_tp, base_ftp)(tp)
        ftp_rep  = False
        wsc      = 1.0*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits    = 2
    elif ws_name == 'Stardiver':
        base_ftp = [0.75, 1.25, 1.75]
        ftp      = interp1d(base_tp, base_ftp)(tp)
        ftp_rep  = True
        wsc      = 0.85*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits    = 4
    elif ws_name == 'Tachi: Rana':
        acc_boost = [1.0, 1.05, 1.1] # Made these numbers up since it isnt known. It's probably just something like "accuracy+0/20/40".
        acc_bonus = interp1d(base_tp, acc_boost)(tp)
        ftp  = 1.0
        ftp_rep = False
        wsc = 0.5*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 3
    elif ws_name == 'Tachi: Fudo':
        base_ftp = [3.75, 5.75, 8.0]
        ftp = interp1d(base_tp, base_ftp)(tp)
        ftp_rep = False
        wsc = 0.8*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1
    elif ws_name == 'Tachi: Kaiten':
        ftp  = 3.0
        ftp_rep = False
        wsc = 0.8*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1
    elif ws_name == 'Tachi: Shoha':
        base_ftp = [1.375, 2.1875, 2.6875] # Made these numbers up since it isnt known. It's probably just something like "accuracy+0/20/40".
        ftp = interp1d(base_tp, base_ftp)(tp)
        ftp_rep = False
        special_set = set_gear(buffs, equipment, 1.375) # The attack bonus from Blade: Kamu is similar to Blade: Shun (see above)
        player_attack1 = special_set.playerstats['Attack1']
        player_attack2 = special_set.playerstats['Attack2']
        wsc = 0.85*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 2
    elif ws_name == 'Tachi: Kasha':
        base_ftp = [1.5625, 2.6875, 4.125] # Made these numbers up since it isnt known. It's probably just something like "accuracy+0/20/40".
        ftp = interp1d(base_tp, base_ftp)(tp)
        ftp_rep = False
        special_set = set_gear(buffs, equipment, 1.65) # The attack bonus from Blade: Kamu is similar to Blade: Shun (see above)
        player_attack1 = special_set.playerstats['Attack1']
        player_attack2 = special_set.playerstats['Attack2']
        wsc = 0.75*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1
    elif ws_name == 'Tachi: Gekko':
        base_ftp = [1.5625, 2.6875, 4.125] # Made these numbers up since it isnt known. It's probably just something like "accuracy+0/20/40".
        ftp = interp1d(base_tp, base_ftp)(tp)
        ftp_rep = False
        special_set = set_gear(buffs, equipment, 2.0) # The attack bonus from Blade: Kamu is similar to Blade: Shun (see above)
        player_attack1 = special_set.playerstats['Attack1']
        player_attack2 = special_set.playerstats['Attack2']
        wsc = 0.75*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1
    elif ws_name == 'Tachi: Koki':
        hybrid    = True
        base_ftp  = [0.5, 1.5, 2.5]
        ftp_hybrid = interp1d(base_tp, base_ftp)(tp)
        ftp       = 1.0
        ftp_rep   = False
        wsc       = 0.3*player_mnd + 0.5*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits     = 1
        element   = 'Light'
    elif ws_name == 'Tachi: Kagero':
        hybrid    = True
        base_ftp  = [0.5, 1.5, 2.5]
        ftp_hybrid = interp1d(base_tp, base_ftp)(tp)
        ftp       = 1.0
        ftp_rep   = False
        wsc       = 0.75*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits     = 1
        element   = 'Fire'
    elif ws_name == 'Tachi: Goten':
        hybrid    = True
        base_ftp  = [0.5, 1.5, 2.5]
        ftp_hybrid = interp1d(base_tp, base_ftp)(tp)
        ftp       = 1.0
        ftp_rep   = False
        wsc       = 0.6*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits     = 1
        element   = 'Thunder'
    elif ws_name == 'Tachi: Jinpu':
        hybrid    = True
        base_ftp  = [0.5, 1.5, 2.5]
        ftp_hybrid = interp1d(base_tp, base_ftp)(tp)
        ftp       = 1.0
        ftp_rep   = False
        wsc       = 0.3*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits     = 2
        element   = 'Wind'

    # Define elemental damage bonuses now that we know what element your hybrid/magical weapon skill is.
    if hybrid or magical:
        elemental_damage_bonus = gearset.playerstats['Elemental Bonus'] + gearset.playerstats.get(element + ' Elemental Bonus', 0)

    # Setup replicating ftp for specific WSs.
    ftp += fotia_ftp
    if hybrid:
        ftp_hybrid += fotia_ftp
    ftp2 = 1.0 if not ftp_rep else ftp

    # fSTR calculation for main-hand and off-hand
    fstr_main = get_fstr(main_dmg, player_str, enemy_vit)
    fstr_sub  = get_fstr(sub_dmg, player_str, enemy_vit)




    # Start the actual damage part.
    damage = 0

    if not final: # if the best set hasn't been recovered yet, then just take a simple average without running proper simulations
        hitrate11 = get_hitrate(player_accuracy1, ws_acc, enemy_eva, enemy_lvl, 'main', sub_wpn_name=='Hitaki', True)
        hitrate21 = get_hitrate(player_accuracy2, ws_acc, enemy_eva, enemy_lvl, 'sub',  sub_wpn_name=='Hitaki', True)
        hitrate12 = get_hitrate(player_accuracy1, ws_acc, enemy_eva, enemy_lvl, 'main', sub_wpn_name=='Hitaki', False) # False meaning not the first hit. It does not gain +100 accuracy bonus
        hitrate22 = get_hitrate(player_accuracy2, ws_acc, enemy_eva, enemy_lvl, 'sub',  sub_wpn_name=='Hitaki', False)

        hitrate_matrix = np.array([[hitrate11, hitrate21],[hitrate12, hitrate22]])
        # Determine the number of attacks each weapon will get
        main_hits, sub_hits = get_ma_rate(nhits, qa, ta, da, oa3, oa2, sub_type, hitrate_matrix) # Get the number of main- and off-hand hits that actually land. Ignore TP return here.

        avg_pdif1 = get_avg_pdif_melee(player_attack1, main_type_skill, pdl_trait, pdl_gear, enemy_defense, crit_rate)
        avg_pdif2 = get_avg_pdif_melee(player_attack2, sub_type_skill, pdl_trait, pdl_gear, enemy_defense, crit_rate)
        main_hit_damage =    get_avg_phys_damage(main_dmg, fstr_main, wsc, avg_pdif1, ftp,  crit_rate, crit_dmg, wsd, ws_bonus) # Calculate the physical damage dealt by the first main hit.
        sub_hit_damage =     get_avg_phys_damage( sub_dmg,  fstr_sub, wsc, avg_pdif2, ftp2, crit_rate, crit_dmg,   0, ws_bonus) # Calculate the physical damage dealt by the off-hand hits separately, no weapon skill damage provided here.
        main_hit_ma_damage = get_avg_phys_damage(main_dmg, fstr_main, wsc, avg_pdif1, ftp2, crit_rate, crit_dmg,   0, ws_bonus) # Calculate the physical damage dealt by extra main-hand hits

        phys = main_hit_damage + (main_hits-1)*main_hit_ma_damage + sub_hits*sub_hit_damage
        damage = phys
        if hybrid:
            # Calculate the magic multiplier for the magical part of Hybrid weapon skills
            # https://www.ffxiah.com/forum/topic/51313/tachi-jinpu-set/
            affinity = 1 + 0.05*gearset.playerstats[f'{element} Affinity'] + 0.05*(gearset.playerstats[f'{element} Affinity']>0)
            resist = 1.0     # 1, 1/2, 1/4, 1/8. Need magic accuracy to counter. Assume no resist for weapon skills
            dayweather = 1.0 # 0.65, 0.8, 0.9, 1.0, 1.1, 1.2, 1.35
            magic_attack_ratio = (100 + player_mab) / (100 + enemy_mdb)
            enemy_mdt = 1.0 # Usually 1.0 unless the enemy casts shell or a similar spell/ability.
            ele_dmg_bonus = 1.0 + elemental_damage_bonus # Multiplier from orpheus based on distance
            magic_multiplier = affinity*resist*dayweather*magic_attack_ratio*enemy_mdt*ele_dmg_bonus
            magical_damage = (phys*ftp_hybrid + player_magic_damage)*magic_multiplier*(1+wsd+ws_bonus)

            damage += magical_damage

        return(damage, 0) # Return the average damage dealt and 0 TP return.




    # Start the actual damage simulations now. This part is run after you've already found the "best average" set. Alternatively, you can just manually pass in final=True to force this part to run instead.
    total_hits = 0 # WS cannot exceed 8 hits
    ma_count = 0 # Limited to 2 MA procs per WS
    ma_hits = 0 # Number of hits that landed and are not the first main-hand or off-hand hit. Used for TP return
    subhit = False # The off-hand hit has not yet landed, don't give TP for it yet
    mainhit = False # The main-hand hit has not yet landed, don't give TP for it yet

    for n in range(nhits):
        # Loop nhits times, summing the damage from each hit.
        # For n == 0, the first main hit is checked, then the first sub hit is checked, then n becomes 1 and the subhits are no longer checked until we do MA procs in the next big for-loop.

        total_hits += 1 # You've started the weapon skill's first hi. Even if it misses, it counts towards the 8-hit total so increase total_hits by 1

        if total_hits > 8: # Don't bother after 8 hits
            continue
        if total_hits > 1:
            ftp = ftp2 # After the first hit, use secondary FTP for main-hand hits. This will equal primary FTP if the WS is FTP-replicating, otherwise it's 1.0

        # Calculate hit rates for the natural main and sub hits (the first of each get a ~+100 Accuracy bonus)
        hitrate1 = get_hitrate(player_accuracy1, ws_acc, enemy_eva, enemy_lvl, 'main', sub_wpn_name=='Hitaki', n==0)
        hitrate2 = get_hitrate(player_accuracy2, ws_acc, enemy_eva, enemy_lvl, 'sub',  sub_wpn_name=='Hitaki', n==0)

        # Check if your hit lands
        if np.random.uniform() < hitrate1:
            # If your hit landed succesfully, and you're not checking the first main or sub hit, then add 1 to the number of MA hits that provide TP
            if n > 0:
                ma_hits += 1
            else:
                mainhit = True # The first main hit successfully landed so it provides full TP.
            pdif1, crit = get_pdif_melee(player_attack1, main_type_skill, pdl_trait, pdl_gear, enemy_defense, crit_rate) # Calculate the PDIF for this swing of the main-hand weapon. Return whether or not that hit was a crit.
            physical_damage = get_phys_damage(main_dmg, fstr_main, wsc, pdif1, ftp, crit, crit_dmg, wsd, ws_bonus, total_hits) # Calculate the physical damage dealt by a single hit. The first hit gets WSD.
            damage += physical_damage


        # Bonus hit for dual-wielding.
        # The dual-wielding hit occurs immediately after first main hit. This can be confirmed by watching your in-game TP return.
        if total_hits < 8 and sub_type=='Weapon' and n == 0:
            total_hits += 1
            if np.random.uniform() < hitrate2:
                pdif2, crit = get_pdif_melee(player_attack2, sub_type_skill, pdl_trait, pdl_gear, enemy_defense, crit_rate)
                physical_damage = get_phys_damage(sub_dmg, fstr_sub, wsc, pdif2, ftp2, crit, crit_dmg, 0, ws_bonus, total_hits) # Notice that subhit uses ftp2, crit=False, and wsd=0. crit=False says don't apply the crit_damage stat
                subhit = True # For TP return. The successful sub-hit gets full TP
                damage += physical_damage
                # This is the last line of the natural main/sub hit for-loop



    # This part checks for MA procs. It does so after all of the natural main hits and the one sub hit
    if total_hits < 8:


        sub_ma_check = sub_type=='Weapon' # If you have a sub-weapon equipped, then it will get one of your two MA proc checks, otherwise the main-weapon will get both multi-attack checks if the weapon skill has at least two hits

        max_ma_checks_main = 1 if sub_ma_check else 1+nhits>1 # The main hand gets 1 MA check if dual-wielding, 1+0 MA checks if single-wielding and using a 1-hit weaponskill, or 1+1 MA checks if single-wielding and using a 2+ hit weapon skill

        # Start by checking if the main-hit multi-attacks.
        for ma_check_n in range(max_ma_checks_main):

            hitrate1 = get_hitrate(player_accuracy1, ws_acc, enemy_eva, enemy_lvl, 'main', sub_wpn_name=='Hitaki', False)
            hitrate2 = get_hitrate(player_accuracy2, ws_acc, enemy_eva, enemy_lvl, 'sub',  sub_wpn_name=='Hitaki', False)

            if np.random.uniform() < qa and ma_count < 2:
                # If you rolled lower than your quadruple attack %, then you do a quadruple attack.
                ma_count += 1 # This counts as one of your two allowed multi-attack procs, even if you can only swing once out of the whole QA proc due to the 8-hit limit
                for k in range(3): # 3 total bonus hits
                    if total_hits >= 8:
                        continue
                    total_hits += 1 # Each hit of the multi-attack counts towards the total of 8 allowed hits per weapon skill
                    if np.random.uniform() < hitrate1:
                        pdif1, crit = get_pdif_melee(player_attack1, main_type_skill, pdl_trait, pdl_gear, enemy_defense, crit_rate)
                        physical_damage = get_phys_damage(main_dmg, fstr_main, wsc, pdif1, ftp2, crit, crit_dmg, 0, ws_bonus, total_hits) # Notice that multi-attacks all use ftp2 and manually pass in wsd=0
                        ma_hits += 1
                        damage += physical_damage

            elif np.random.uniform() < ta and ma_count < 2: # If you failed the quadruple attack check, then you get to try to roll lower than your triple attack value.
                ma_count += 1
                for k in range(2):
                    if total_hits >= 8:
                        continue
                    total_hits += 1
                    if np.random.uniform() < hitrate1:
                        pdif1, crit = get_pdif_melee(player_attack1, main_type_skill, pdl_trait, pdl_gear, enemy_defense, crit_rate)
                        physical_damage = get_phys_damage(main_dmg, fstr_main, wsc, pdif1, ftp2, crit, crit_dmg, 0, ws_bonus, total_hits)
                        ma_hits += 1
                        damage += physical_damage

            elif np.random.uniform() < da and ma_count < 2: # If you failed the triple attack check, then you get to try a double attack roll
                ma_count += 1
                if total_hits < 8:
                    total_hits += 1
                    if np.random.uniform() < hitrate1:
                        pdif1, crit = get_pdif_melee(player_attack1, main_type_skill, pdl_trait, pdl_gear, enemy_defense, crit_rate)
                        physical_damage = get_phys_damage(main_dmg, fstr_main, wsc, pdif1, ftp2, crit, crit_dmg, 0, ws_bonus, total_hits)
                        ma_hits += 1
                        damage += physical_damage

            elif np.random.uniform() < oa3 and ma_count < 2: # If you failed double attack, then you get to try OA3 roll (skipping Oa8, OA7, OA6, etc)
                ma_count += 1
                for k in range(2):
                    if total_hits >= 8:
                        continue
                    total_hits += 1
                    if np.random.uniform() < hitrate1:
                        pdif1, crit = get_pdif_melee(player_attack1, main_type_skill, pdl_trait, pdl_gear, enemy_defense, crit_rate)
                        physical_damage = get_phys_damage(main_dmg, fstr_main, wsc, pdif1, ftp2, crit, crit_dmg, 0, ws_bonus, total_hits)
                        ma_hits += 1
                        damage += physical_damage

            elif np.random.uniform() < oa2 and ma_count < 2: # If you failed OA3, try OA2.
                ma_count += 1
                if total_hits < 8:
                    total_hits += 1
                    if np.random.uniform() < hitrate1:
                        pdif1, crit = get_pdif_melee(player_attack1, main_type_skill, pdl_trait, pdl_gear, enemy_defense, crit_rate)
                        physical_damage = get_phys_damage(main_dmg, fstr_main, wsc, pdif1, ftp2, crit, crit_dmg, 0, ws_bonus, total_hits)
                        ma_hits += 1
                        damage += physical_damage


        # Now check multi-attacks for the off-hand.
        # Note that this part is set up without OA3 and OA2 because the occasional attacks N times stat only applies to the weapon that has it. In this case, the only weapon that I have coded with this is Nagi, which only works main hand.
        # This will need to be changed if we get ilvl Magian weapons with occasionally attacks X.
        # This does not deal with "follow-up" attacks from things like Fudo Masamune (but this is where you'd throw that check in if you wanted to)
        if sub_ma_check: # If you have an off-hand weapon equipped, then it gets one of your two multi-attack procs. Check that multi-attack proc now.
            if np.random.uniform() < qa and ma_count < 2:
                ma_count += 1
                for k in range(3):
                    if total_hits >= 8:
                        continue
                    total_hits += 1
                    if np.random.uniform() < hitrate2:
                        pdif2, crit = get_pdif_melee(player_attack2, sub_type_skill, pdl_trait, pdl_gear, enemy_defense, crit_rate)
                        physical_damage = get_phys_damage(sub_dmg, fstr_sub, wsc, pdif2, ftp2, crit, crit_dmg, 0, ws_bonus, total_hits)
                        ma_hits += 1
                        damage += physical_damage

            elif np.random.uniform() < ta and ma_count < 2:
                ma_count += 1
                for k in range(2):
                    if total_hits >= 8:
                        continue
                    total_hits += 1
                    if np.random.uniform() < hitrate2:
                        pdif2, crit = get_pdif_melee(player_attack2, sub_type_skill, pdl_trait, pdl_gear, enemy_defense, crit_rate)
                        physical_damage = get_phys_damage(sub_dmg, fstr_sub, wsc, pdif2, ftp2, crit, crit_dmg, 0, ws_bonus, total_hits)
                        ma_hits += 1
                        damage += physical_damage

            elif np.random.uniform() < da and ma_count < 2:
                ma_count += 1
                if total_hits < 8:
                    total_hits += 1
                    if np.random.uniform() < hitrate2:
                        pdif2, crit = get_pdif_melee(player_attack2, sub_type_skill, pdl_trait, pdl_gear, enemy_defense, crit_rate)
                        physical_damage = get_phys_damage(sub_dmg, fstr_sub, wsc, pdif2, ftp2, crit, crit_dmg, 0, ws_bonus, total_hits)
                        ma_hits += 1
                        damage += physical_damage
    phys = damage
    # This is the last line of the physical portion.


    # If the weapon skill is labeled as a hybrid, then calculate the magic portion and add it to the total damage here.
    if hybrid:
        # Calculate the magic multiplier for the magical part of Hybrid weapon skills
        # https://www.ffxiah.com/forum/topic/51313/tachi-jinpu-set/
        affinity = 1 + 0.05*gearset.playerstats[f'{element} Affinity'] + 0.05*(gearset.playerstats[f'{element} Affinity']>0)
        resist = 1.0     # 1, 1/2, 1/4, 1/8. Need magic accuracy to counter. Assume no resist for weapon skills
        dayweather = 1.0 # 0.65, 0.8, 0.9, 1.0, 1.1, 1.2, 1.35
        magic_attack_ratio = (100 + player_mab) / (100 + enemy_mdb)
        enemy_mdt = 1.0 # Usually 1.0 unless the enemy casts shell or a similar spell/ability.
        ele_dmg_bonus = 1.0 + elemental_damage_bonus # Multiplier from orpheus based on distance
        magic_multiplier = affinity*resist*dayweather*magic_attack_ratio*enemy_mdt*ele_dmg_bonus

        magical_damage = (phys*ftp_hybrid + player_magic_damage)*magic_multiplier*(1+wsd+ws_bonus)

        damage += magical_damage
    # damage = 99999 if damage > 99999 else damage  # Cap damage at 99999
    tp_returned = get_tp(mainhit+subhit, mdelay, stp) + int(10*(1+stp))*ma_hits

    # Print a bunch of stuff for debugging
    # print(phys,get_pdif_melee(player_attack1, pdl_gear, enemy_defense, crit_rate)[0], get_pdif_melee(player_attack2, pdl_gear, enemy_defense, crit_rate)[0], ftp, ftp2, wsc, fstr_main, fstr_sub, player_attack1, player_attack2, pdl_gear, wsd, ws_bonus, wsc)
    return(int(damage), int(tp_returned))


'''
==========================================================================================
==========================================================================================
==========================================================================================
==========================================================================================
==========================================================================================
==========================================================================================
==========================================================================================
==========================================================================================
==========================================================================================
==========================================================================================
'''

def test_set(WS_name, buffs, equipment, gearset, tp1, tp2, attack_cap=False, final=False):
    if final:

        if savetext:
            with open(f'{savepath}{shortname}{output_file_suffix}_{tp1}_{tp2}.txt', 'w') as ofile:
                ofile.write(f"{WS_name} best available gear set.\n\n")
                print(f"{WS_name} best available gear set.")
                for k in best_set.gear:
                    try:
                        if savetext:
                            ofile.write(f"{k:>8s}  {best_set.gear[k]['Name2']:<50s}\n")
                        print(f"{k:>8s}  {best_set.gear[k]['Name2']:<50s}")
                    except:
                        if savetext:
                            ofile.write(f"{k:>8s}  {best_set.gear[k]['Name']:<50s}\n")
                        print(f"{k:>8s}  {best_set.gear[k]['Name']:<50s}")

    damage = []
    tp_return = []

    if final:
        for k in range(ntrials):
            tp = np.random.uniform(tp1,tp2)

            # Define your target to simulate against. Toads have 3 possible options, but you could easily code something like Kin and only have one set of stats to pull from.
            enemy_index = random.choice([0,1,2]) # Pick one of the three Apex Toads.
            enemy_index = 1 # Force the average toad.
            enemy_lvl = apex_toad['Level'][enemy_index]
            enemy_def = apex_toad['Defense'][enemy_index]
            enemy_vit = apex_toad['VIT'][enemy_index]
            enemy_agi = apex_toad['AGI'][enemy_index]
            enemy_mdb = apex_toad['Magic Defense'][enemy_index]
            enemy_eva = apex_toad['Evasion'][enemy_index]
            values = weaponskill(WS_name, gearset, tp, enemy_lvl, enemy_def, enemy_eva, enemy_vit, enemy_agi, enemy_mdb, attack_cap, buffs, equipment, final) # values = [damage, TP_return]
            damage.append(values[0]) # Append the damage from each simulation to a list. Plot this list as a histogram later.
            tp_return.append(values[1])

        plot_final(damage, gearset, attack_cap, shortname, output_file_suffix, tp1, tp2, WS_name)
        return()
    else:
        tp = np.average([tp1,tp2])

        enemy_index = 1
        enemy_lvl = apex_toad['Level'][enemy_index]
        enemy_def = apex_toad['Defense'][enemy_index]
        enemy_vit = apex_toad['VIT'][enemy_index]
        enemy_agi = apex_toad['AGI'][enemy_index]
        enemy_mdb = apex_toad['Magic Defense'][enemy_index]
        enemy_eva = apex_toad['Evasion'][enemy_index]
        damage, _ = weaponskill(WS_name, gearset, tp, enemy_lvl, enemy_def, enemy_eva, enemy_vit, enemy_agi, enemy_mdb, attack_cap, buffs, equipment, final)
        return(damage)

from init import *

profile = False # Profile the code (check how long each function call takes)
if profile:
    # If you want to profile the code, then start here.
    import cProfile, pstats
    profiler = cProfile.Profile()
    profiler.enable()





for o in range(len(tp1_list)):


    Best_Gearset =  starting_gearset.copy()

    tp1 = tp1_list[o]
    tp2 = tp2_list[o]
    print("---------------")
    print("---------------")
    print(f"Checking:  {shortname}{output_file_suffix}_{tp1}_{tp2}")
    print("---------------")
    print("---------------")
    n_iter=20 # Maximum number of of times to check every combination of gear? Usually stops changing around iteration 2 or 3, but putting 20 doesn't hurt since we also have a convergence criterion.
    nconverge = 3 # Number of consecutive iterations resulting in insignificant damage improvements before code returns the best set.

    converge_count = 0 # Count for convergence (number of times the change between iterations was <0.1% for example; see near the end of this code for the exact value used)
    best_damage = 0
    damage_list = np.zeros(n_iter)
    for z in range(n_iter):

        if converge_count >= nconverge: # Check if converged
            print(f"No significant change after  {converge_count}  iterations - stopping. {str(datetime.datetime.now())}")
            break

        # Start testing stuff
        print(f"Current iteration: {z+1}   {str(datetime.datetime.now())}")
        for i,a in enumerate(all_gear): # "i" is a counter (0, 1, 2, etc), "a" is a gear slot (main, sub, ammo, head, neck, etc)
            for i2, a2 in enumerate(all_gear): # Swap 2 pieces at once
                if fit2:
                    if i2 < i: # Treat the swapped piece combinations as an upper/lower triangular matrix (test A+B, dont test B+A because A+B is the same thing. This explicitly allows testing A+A, which acts as swapping only 1 piece)
                        continue
                else:
                    if i2 != i:
                        continue

                slot1 = names[i]
                slot2 = names[i2]

                # Example (with fit2=True)
                # Starting with some gear set:
                #   Consider the ammo slot:
                #     1. Check every ammo equipment by itself to see if any are an improvement over your best set
                #     2. Now check every combination of ammo and head to see if a specific pair is an improvement
                #     3. Now check every combination of ammo and necklace to see if a specific pair is an improvement
                #     4. Repeat til every ammo + everything_else is checked
                #   Now consider the head slot:
                #     1. Check every head equipment by itself to see if any are an improvement over your best set
                #     2. Now check every combination of head and necklace to see if a specific pair is an improvement
                #     3. Now check every combination of head and ear1 to see if a specific pair is an improvement
                #     4. Repeat til every head + everything_else is checked
                #   Repeat til all combinations of all armor has been checked
                # Repeat that whole process n_iter times.
                # Stop early if converge_count >= nconverge

                # Copy the current best set so that you can swap pieces without modifying the original.
                new_set = {'main':Best_Gearset['main'],
                           'sub':Best_Gearset['sub'],
                           'ranged':Best_Gearset['ranged'],
                           'ammo':Best_Gearset['ammo'],
                           'head':Best_Gearset['head'],
                           'body':Best_Gearset['body'],
                           'hands':Best_Gearset['hands'],
                           'legs':Best_Gearset['legs'],
                           'feet':Best_Gearset['feet'],
                           'neck':Best_Gearset['neck'],
                           'waist':Best_Gearset['waist'],
                           'ear1':Best_Gearset['ear1'],
                           'ear2':Best_Gearset['ear2'],
                           'ring1':Best_Gearset['ring1'],
                           'ring2':Best_Gearset['ring2'],
                           'back':Best_Gearset['back']}

                for j,b in enumerate(a): # "j" is a counter (0, 1, 2, etc), "b" is a piece of gear that you said you wanted to be tested in gear slot "a" (a=neck, b=(Caro_Necklace, Fotia_Gorget, Ninja_Nodowa, etc)). "b" is the NEW item to be tested against the old item
                    for j2,b2 in enumerate(a2): # same thing, but for the 2nd piece of gear being swapped simultaneously

                        # From here on: there are a lot of try/except blocks. This is because augmented pieces need a "Name2" and a "Name" dictionary key to distinguish between different augment paths.
                        # We could remove all of these try/except blocks if EVERY piece of gear had a "Name2" dictionary key. Since the code works as is, I'll fix this later.

                        try: # Save the names of the first of the two item swaps and the item currently equipped in its position
                            swap_item1 = b['Name2'] # New item being tested
                        except:
                            swap_item1 = b['Name']
                        try:
                            equipped_item1 = Best_Gearset[slot1]['Name2'] # Old item
                        except:
                            equipped_item1 = Best_Gearset[slot1]['Name']

                        try: # Save the names of the second of the two item swaps and the item currently equipped in its position
                             swap_item2 = b2['Name2']
                        except:
                             swap_item2 = b2['Name']
                        try:
                            equipped_item2 = Best_Gearset[slot2]['Name2']
                        except:
                            equipped_item2 = Best_Gearset[slot2]['Name']

                        if i2 == i:
                            # If the two swapped pieces are in the same slot, only check the damage if they're the same item
                            # This is the code block that allows changing only one item, instead of always changing two.
                            if swap_item1 != swap_item2:
                                continue


                        # Now we perform simple checks to save some time and prevent bad results. Stuff like making sure we aren't equipping two identical "Rare" items (i.e. one Gere Ring in each ring slot)
                        if swap_item1 == equipped_item1 or swap_item1 == equipped_item2: # Don't swap to an item that's already equipped in the same slot (don't compare Mpaca's Cap to Mpaca's Cap)
                            continue
                        if swap_item2 == equipped_item1 or swap_item2 == equipped_item2:
                            continue
                        if swap_item1 == swap_item2 and i2 != i:
                            continue


                        # If the item you're trying to place in ring2/ear2 is already in ring1/ear1, then skip it (don't try to equip two copies of a Rare item; I use Mache_EarringA and Mache_EarringB naming to allow one in each ear
                        if slot1 == 'ring2' or slot1 == 'ear2':
                            try:
                                if swap_item1 == Best_Gearset[names[i-1]]['Name2']:
                                    continue
                            except:
                                if swap_item1 == Best_Gearset[names[i-1]]['Name']:
                                    continue
                        if slot2 == 'ring2' or slot2 == 'ear2':
                            try:
                                if swap_item2 == Best_Gearset[names[i2-1]]['Name2']:
                                    continue
                            except:
                                if swap_item2 == Best_Gearset[names[i2-1]]['Name']:
                                    continue

                        # If the item you're trying to place in ring1/ear1 is already in ring2/ear2, then skip it (don't try to equip two copies of a Rare item; I use Mache_EarringA and Mache_EarringB naming to allow one in each ear
                        if names[i] == 'ring1' or names[i] == 'ear1':
                            try:
                                if swap_item1 == Best_Gearset[names[i+1]]['Name2']:
                                    continue
                            except:
                                if swap_item1 == Best_Gearset[names[i+1]]['Name']:
                                    continue
                        if names[i2] == 'ring1' or names[i2] == 'ear1':
                            try:
                                if swap_item2 == Best_Gearset[names[i2+1]]['Name2']:
                                    continue
                            except:
                                if swap_item2 == Best_Gearset[names[i2+1]]['Name']:
                                    continue


                        # If the code is checking both ring1 and ring2 slots at the same time, make sure it isn't trying the same ring in both slots (don't place the same Rare item in two different slots at the same time)
                        if (names[i] == 'ring1' and names[i2] == 'ring2') or (names[i2] == 'ring1' and names[i] == 'ring2'):
                            if swap_item1 == swap_item2:
                                continue

                        # If the code is checking both ear1 and ear2 slots at the same time, make sure it isn't trying the same earring in both slots (don't place the same Rare item in two different slots at the same time)
                        if (names[i] == 'ear1' and names[i2] == 'ear2') or (names[i2] == 'ear1' and names[i] == 'ear2'):
                            if swap_item1 == swap_item2:
                                continue

                        # The pieces of gear to be equipped have passed the basic tests. Now we're ready to equip them and run a simulation.
                        new_set[slot1]  = b  # Equip swap_item1 to slot1
                        new_set[slot2]  = b2 # Equip swap_item2 to slot2
                        test_Gearset = set_gear(buffs, new_set) # This line turns that gear dictionary into a Python class, which contains the player and gear stats as well as a list of gear equipped in each slot that can be easily printed

                        # Now test the gearset by calculating its average damage.
                        # Average damage is not necessarily appropriate, but it's simple and allows the results to be more easily compared to the well known spreadsheets.
                        damage = int(test_set(WS_name, buffs, new_set, test_Gearset, tp1, tp2, attack_cap)) # Test the set and return its damage as a single number

                        # If the damage returned after swapping those 1~2 pieces is higher than the previous best, then run this next bit of code to print to the terminal the swap that was performed and the change in damage observed.
                        if damage > best_damage:
                            if fit2:
                                if swap_item1 == swap_item2:
                                    try:
                                        print(f"New best item found {names[i]}:   {equipped_item1} ->  {swap_item1}   [{best_damage:>6.0f} -> {damage:>6.0f}]") # Print the new best damage and the new item that led to this new record
                                    except:
                                        print(f"New best item found {names[i]}:  {Best_Gearset[names[i]]['Name']}  ->  {b['Name2']}   [{best_damage:>6.0f} -> {damage:>6.0f}]") # Print the new best damage and the new item that led to this new record
                                else:
                                    try:
                                        print(f"New best items found [{names[i]} & {names[i2]}]:   [{equipped_item1} & {equipped_item2}]  ->  [{swap_item1} & {swap_item2}]   [{best_damage:>6.0f} -> {damage:>6.0f}]") # Print the new best damage and the new item that led to this new record
                                    except:
                                        print(f"New best items found [{names[i]} & {names[i2]}]:   [{Best_Gearset[names[i]]['Name']} & {Best_Gearset[names[i2]]['Name']}]  ->  [{b['Name2']} & {b2['Name2]']}]   [{best_damage:>6.0f} -> {damage:>6.0f}]") # Print the new best damage and the new item that led to this new record
                            else: # If fitting one item, print which it is.
                                try:
                                    print(f"New best item found {names[i]}:   {equipped_item1} ->  {swap_item1}   [{best_damage:>6.0f} -> {damage:>6.0f}]") # Print the new best damage and the new item that led to this new record
                                except:
                                    print(f"New best item found {names[i]}:  {Best_Gearset[names[i]]['Name']}  ->  {b['Name2']}   [{best_damage:>6.0f} -> {damage:>6.0f}]") # Print the new best damage and the new item that led to this new record

                            # If your new set returned the highest damage, then:
                            best_damage = damage      # Save the highest damage to compare with future test gearsets
                            Best_Gearset[slot1]  = b  # Assign to the Best_Gearset dictionary the new piece of gear into the appropriate slot
                            Best_Gearset[slot2] = b2  # Assign to the Best_Gearset dictionary the new piece of gear into the appropriate slot
                        damage_list[z] = best_damage  # Update the damage_list[] array to contain the best damage obtained from this iteration




        if z > 0: # After the first iteration:
            if np.abs(damage_list[z]-damage_list[z-1])/damage_list[z] < 0.001:
                # If the new best damage is less than 0.1% better than the old best_damage, then converge count += 1
                # After nconv such consecutive iterations, break out of the loop and create the final plot. This prevent the code from bouncing back and forth between two nearly identical items for 20 iterations.
                converge_count += 1
            else:
                converge_count = 0 # Reset the converge count. This ensures that only consecutive trials count towards convergence



    # At this point, the code has run up to 20 iterations and found the gearset that returns the highest average damage. Now we use this best set to create a proper distribution of damage that you'd expect to see in game based on its stats.
    best_set = set_gear(buffs, Best_Gearset) # Create a class from the best gearset

    # Run the simulator once more, but with "final=True" to tell the code to create a proper distribution.
    test_set(WS_name, buffs, Best_Gearset, best_set, tp1, tp2, attack_cap, True)

if profile:
    # If you wanted to profile the code, then disable the profile at this point and print the results.
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumtime')
    stats.print_stats()
