#
# Created by Kastra on Asura.
# Feel free to /tell in game or send a PM on FFXIAH you have questions, comments, or suggestions.
#
# Version date: 2022 December 10
#
import numpy as np
from set_stats import *
from get_dex_crit import *

def weaponskill_scaling(main_job, sub_job, ws_name, tp, gearset, equipment, buffs, dStat, dual_wield, enemy_defense, enemy_agi, enemy_int):
    #
    # Setup weaponskill statistics (TP scaling, # of hits, ftp replication, WSC, etc)
    # Placed in separate file to reduce clutter in main file.
    # Need to sort alphabetically later.
    #
    player_str = gearset.playerstats["STR"]
    player_dex = gearset.playerstats["DEX"]
    player_vit = gearset.playerstats["VIT"]
    player_agi = gearset.playerstats["AGI"]
    player_int = gearset.playerstats["INT"]
    player_mnd = gearset.playerstats["MND"]
    player_chr = gearset.playerstats["CHR"]
    player_attack1 = gearset.playerstats["Attack1"]
    player_attack2 = gearset.playerstats["Attack2"]
    player_attack2 = 0 if not dual_wield else player_attack2
    crit_rate = 0

    hybrid = False
    magical = False
    ws_dINT = 0
    element = "None"
    ftp_hybrid = 0
    acc_bonus = 0

    base_tp = [1000,2000,3000]
    if ws_name == "Savage Blade":
        base_ftp = [4.0, 10.25, 13.75] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc  = 0.5*(player_str + player_mnd) + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 2 # Savage is a 2-hit weaponskill (+1 for offhand)
    if ws_name == "Red Lotus Blade":
        base_ftp = [1.0, 2.3828125, 3.75] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc  = 0.4*(player_str + player_int) + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 1
        magical = True
        element = "Fire"
        ws_dINT = 32 if (player_int - enemy_int)/2 + 8 > 32 else (player_int - enemy_int)/2 + 8
    if ws_name == "Seraph Blade":
        base_ftp = [1.125, 2.625, 4.125] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc  = 0.4*(player_str + player_mnd) + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 1
        magical = True
        element = "Light"
        ws_dINT = 0
    elif ws_name == "Death Blossom":
        ftp  = 4.0
        ftp_rep = False
        wsc = 0.5*player_mnd + 0.3*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 3
    elif ws_name == "Sanguine Blade":
        ftp  = 2.75
        ftp_rep = False
        wsc = 0.5*player_mnd + 0.3*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1
        magical = True
        element = "Dark"
        ws_dINT = (player_int - enemy_int)*2
    elif ws_name == "Knights of Round":
        ftp  = 5.0
        ftp_rep = False
        wsc = 0.4*(player_mnd + player_str) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1
    elif ws_name == "Chant du Cygne":
        crit_rate +=  gearset.playerstats["Crit Rate"]/100 # Blade: Hi can crit, so define crit rate now
        crit_boost = [0.15, 0.25, 0.40]
        crit_bonus = np.interp(tp, base_tp, crit_boost) # Bonus crit rate from TP scaling
        crit_rate += crit_bonus
        crit_rate += get_dex_crit(player_dex, enemy_agi) # Bonus crit rate from the player"s DEX stat vs enemy AGI stat
        ftp = 1.6328125
        ftp_rep = True
        wsc = 0.8*player_dex + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 3
    elif ws_name == "Blade: Shun":
        atk_boost = [1.0, 2.0, 3.0]
        ws_atk_bonus = np.interp(tp, base_tp, atk_boost) - 1.0
        special_set = set_gear(buffs, equipment, main_job, sub_job, ws_atk_bonus) # The attack bonus from Blade: Shun is applied before buffs. I needed to recalculate player attack with a "special set" to deal with this.
        player_attack1 = special_set.playerstats["Attack1"] # Redefine the player"s attack1 and attack2 used in the weapon skill based on the FTP scaling value
        player_attack2 = special_set.playerstats["Attack2"] # These boosted attack1 and attack2 values do not show up in the player"s stats shown in the final plot.
        ftp = 1.0
        ftp_rep = True
        wsc  = 0.85*player_dex + dStat[1]*gearset.playerstats[dStat[0]] # Assuming 5/5 Blade: Shun merits. Add clickable drop-down menu to adjust merits later.
        nhits = 5
    elif ws_name == "Blade: Ten":
        base_ftp = [4.5, 11.5, 15.5]
        ftp      = np.interp(tp, base_tp, base_ftp)
        ftp_rep = False
        wsc      = 0.3*(player_str+player_dex) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits    = 1
    elif ws_name == "Blade: Kamu":
        ftp  = 1.0
        ftp_rep = False
        wsc = 0.6*(player_int+player_str)
        nhits = 1
        special_set = set_gear(buffs, equipment, main_job, sub_job, 1.25) # The attack bonus from Blade: Kamu is similar to Blade: Shun (see above)
        player_attack1 = special_set.playerstats["Attack1"]
        player_attack2 = special_set.playerstats["Attack2"]
        enemy_defense *= 0.75 # TODO: This should be additive with Dia, Frailty, etc? I think it's fine as is.
    elif ws_name == "Blade: Ku":
        acc_boost = [0, 20, 40] # Made these numbers up since it isnt known.
        acc_bonus = np.interp(tp, base_tp, acc_boost)
        ftp  = 1.25
        ftp_rep = True
        wsc = 0.3*(player_str+player_dex) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 5
    elif ws_name == "Blade: Metsu":
        ftp  = 5.0
        ftp_rep = False
        wsc = 0.8*player_dex
        nhits = 1
    elif ws_name == "Namas Arrow":
        ftp  = 2.75
        ftp_rep = False
        wsc = 0.4*(player_str + player_agi)
        nhits = 1
    elif ws_name == "Blade: Hi":
        crit_rate +=  gearset.playerstats["Crit Rate"]/100 # Blade: Hi can crit, so define crit rate now
        crit_boost = [0.15, 0.2, 0.25]
        crit_bonus = np.interp(tp, base_tp, crit_boost) # Bonus crit rate from TP scaling
        crit_rate += crit_bonus
        crit_rate += get_dex_crit(player_dex, enemy_agi) # Bonus crit rate from the player"s DEX stat vs enemy AGI stat
        ftp = 5.0
        ftp_rep = False
        wsc = 0.8*player_agi + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1
    elif ws_name == "Blade: Ei":
        base_ftp = [1.0, 3.0, 5.0] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc  = 0.4*(player_str + player_int) + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 1
        magical = True
        element = "Dark"
        ws_dINT = 32 if (player_int - enemy_int)/2 + 8 > 32 else (player_int - enemy_int)/2 + 8
    elif ws_name == "Blade: Yu":
        ftp = 3.0
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc  = 0.4*(player_dex + player_int) + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 1
        magical = True
        element = "Water"
        ws_dINT = 0
    elif ws_name == "Evisceration":
        crit_rate +=  gearset.playerstats["Crit Rate"]/100
        crit_boost = [0.1, 0.25, 0.5]
        crit_bonus = np.interp(tp, base_tp, crit_boost)
        crit_rate += crit_bonus
        crit_rate += get_dex_crit(player_dex, enemy_agi)
        ftp = 1.25
        ftp_rep = True
        wsc = 0.5*player_dex + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 5
    elif ws_name == "Exenterator":
        ftp = 1.0
        ftp_rep = True
        wsc = 0.85*player_agi + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 4
    elif ws_name == "Mercy Stroke":
        ftp  = 5.0
        ftp_rep = False
        wsc = 0.8*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1
    elif ws_name == "Aeolian Edge":
        base_ftp = [2.0, 3.0, 4.5] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc  = 0.4*(player_dex + player_int) + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 1
        magical = True
        element = "Wind"
        ws_dINT = 32 if (player_int - enemy_int)/2 + 8 > 32 else (player_int - enemy_int)/2 + 8
    elif ws_name == "Blade: Chi":
        hybrid    = True
        base_ftp  = [0.5, 1.375, 2.25]
        ftp_hybrid = np.interp(tp, base_tp, base_ftp)
        ftp       = 1.0
        ftp_rep   = False
        wsc       = 0.3*(player_str+player_int) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits     = 2
        element   = "Earth"
    elif ws_name == "Blade: Teki":
        hybrid    = True
        base_ftp  = [0.5, 1.375, 2.25]
        ftp_hybrid = np.interp(tp, base_tp, base_ftp)
        ftp       = 1.0
        ftp_rep   = False
        wsc       = 0.3*(player_str+player_int) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits     = 1
        element   = "Water"
    elif ws_name == "Blade: To":
        hybrid    = True
        base_ftp  = [0.5, 1.5, 2.5]
        ftp_hybrid = np.interp(tp, base_tp, base_ftp)
        ftp       = 1.0
        ftp_rep   = False
        wsc       = 0.4*(player_str+player_int) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits     = 1
        element   = "Ice"
    elif ws_name == "Blade: Retsu":
        base_ftp  = [0.5, 1.5, 2.5]
        ftp       = 1.0
        ftp_rep   = False
        wsc       = 0.6*player_dex + 0.2*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits     = 2
    elif ws_name == "Asuran Fists":
        acc_boost = [0, 20, 40] # Made these numbers up since it isnt known. Copied Blade: Ku, which i also made up
        acc_bonus = np.interp(tp, base_tp, acc_boost)
        ftp       = 1.25
        ftp_rep   = True
        wsc       = 0.15*(player_vit + player_str) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits     = 8
    elif ws_name == "Impulse Drive":
        base_ftp = [1.0, 3.0, 5.5]
        ftp      = np.interp(tp, base_tp, base_ftp)
        ftp_rep  = False
        wsc      = 1.0*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits    = 2
    elif ws_name == "Stardiver":
        base_ftp = [0.75, 1.25, 1.75]
        ftp      = np.interp(tp, base_tp, base_ftp)
        ftp_rep  = True
        wsc      = 0.85*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits    = 4
    elif ws_name == "Geirskogul":
        ftp      = 3.0
        ftp_rep  = False
        wsc      = 0.8*player_dex + dStat[1]*gearset.playerstats[dStat[0]]
        nhits    = 1
    elif ws_name == "Camlann's Torment":
        ftp  = 3.0
        ftp_rep = False
        wsc = 0.6*(player_vit+player_str)
        nhits = 1
        base_enemy_def_scaling = [0.125, 0.375, 0.625]
        enemy_def_scaling = np.interp(tp, base_tp, base_enemy_def_scaling)
        enemy_defense *= (1-enemy_def_scaling)
    elif ws_name == "Drakesbane":
        crit_rate +=  gearset.playerstats["Crit Rate"]/100 # Blade: Hi can crit, so define crit rate now
        crit_boost = [0.1, 0.25, 0.40]
        crit_bonus = np.interp(tp, base_tp, crit_boost) # Bonus crit rate from TP scaling
        crit_rate += crit_bonus
        crit_rate += get_dex_crit(player_dex, enemy_agi) # Bonus crit rate from the player"s DEX stat vs enemy AGI stat
        ftp = 1.0
        ftp_rep = False
        wsc = 0.5*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 4
        special_set = set_gear(buffs, equipment, main_job, sub_job, 0.8125 - 1.0) # Recalculate the player attack using a negative multiplier bonus
        player_attack1 = special_set.playerstats["Attack1"]
    elif ws_name == "Penta Thrust":
        acc_boost = [0, 20, 40] # Made these numbers up since it isnt known. Copied Blade: Ku, which i also made up
        acc_bonus = np.interp(tp, base_tp, acc_boost)
        ftp  = 1.00
        ftp_rep = False
        wsc = 0.2*(player_str+player_dex) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 5
        special_set = set_gear(buffs, equipment, main_job, sub_job, -0.125) # Recalculate the player attack using a negative multiplier bonus
        player_attack1 = special_set.playerstats["Attack1"]
    elif ws_name == "Tachi: Rana":
        acc_boost = [0, 20, 40] # Made these numbers up since it isnt known. Copied Blade: Ku, which i also made up
        acc_bonus = np.interp(tp, base_tp, acc_boost)
        ftp  = 1.0
        ftp_rep = False
        wsc = 0.5*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 3
    elif ws_name == "Tachi: Fudo":
        base_ftp = [3.75, 5.75, 8.0]
        ftp = np.interp(tp, base_tp, base_ftp)
        ftp_rep = False
        wsc = 0.8*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1
    elif ws_name == "Tachi: Kaiten":
        ftp  = 3.0
        ftp_rep = False
        wsc = 0.8*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1
    elif ws_name == "Tachi: Shoha":
        base_ftp = [1.375, 2.1875, 2.6875]
        ftp = np.interp(tp, base_tp, base_ftp)
        ftp_rep = False
        special_set = set_gear(buffs, equipment, main_job, sub_job, 1.375) # The attack bonus from Tachi: Shoha is similar to Blade: Shun (see above)
        player_attack1 = special_set.playerstats["Attack1"]
        player_attack2 = special_set.playerstats["Attack2"]
        wsc = 0.85*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 2
    elif ws_name == "Tachi: Kasha":
        base_ftp = [1.5625, 2.6875, 4.125]
        ftp = np.interp(tp, base_tp, base_ftp)
        ftp_rep = False
        special_set = set_gear(buffs, equipment, main_job, sub_job, 1.65) # The attack bonus from Tachi: Kasha is similar to Blade: Shun (see above)
        player_attack1 = special_set.playerstats["Attack1"]
        player_attack2 = special_set.playerstats["Attack2"]
        wsc = 0.75*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1
    elif ws_name == "Tachi: Gekko":
        base_ftp = [1.5625, 2.6875, 4.125]
        ftp = np.interp(tp, base_tp, base_ftp)
        ftp_rep = False
        special_set = set_gear(buffs, equipment, main_job, sub_job, 2.0) # The attack bonus from Tachi: Gekko is similar to Blade: Shun (see above)
        player_attack1 = special_set.playerstats["Attack1"]
        player_attack2 = special_set.playerstats["Attack2"]
        wsc = 0.75*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1
    elif ws_name == "Tachi: Koki":
        hybrid    = True
        base_ftp  = [0.5, 1.5, 2.5]
        ftp_hybrid = np.interp(tp, base_tp, base_ftp)
        ftp       = 1.0
        ftp_rep   = False
        wsc       = 0.3*player_mnd + 0.5*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits     = 1
        element   = "Light"
    elif ws_name == "Tachi: Kagero":
        hybrid    = True
        base_ftp  = [0.5, 1.5, 2.5]
        ftp_hybrid = np.interp(tp, base_tp, base_ftp)
        ftp       = 1.0
        ftp_rep   = False
        wsc       = 0.75*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits     = 1
        element   = "Fire"
    elif ws_name == "Tachi: Goten":
        hybrid    = True
        base_ftp  = [0.5, 1.5, 2.5]
        ftp_hybrid = np.interp(tp, base_tp, base_ftp)
        ftp       = 1.0
        ftp_rep   = False
        wsc       = 0.6*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits     = 1
        element   = "Thunder"
    elif ws_name == "Tachi: Jinpu":
        hybrid    = True
        base_ftp  = [0.5, 1.5, 2.5]
        ftp_hybrid = np.interp(tp, base_tp, base_ftp)
        ftp       = 1.0
        ftp_rep   = False
        wsc       = 0.3*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits     = 2
        element   = "Wind"
    elif ws_name == "Tachi: Jinpu":
        hybrid    = True
        base_ftp  = [0.5, 1.5, 2.5]
        ftp_hybrid = np.interp(tp, base_tp, base_ftp)
        ftp       = 1.0
        ftp_rep   = False
        wsc       = 0.3*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits     = 2
        element   = "Wind"
    elif ws_name == "Insurgency":
        base_ftp = [0.5, 3.25, 6.0]
        ftp = np.interp(tp, base_tp, base_ftp)
        ftp_rep = False
        wsc = 0.2*(player_str+player_int) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 4
    elif ws_name == "Cross Reaper":
        base_ftp = [2.0, 4.0, 7.0]
        ftp = np.interp(tp, base_tp, base_ftp)
        ftp_rep = False
        wsc = 0.6*(player_str+player_mnd) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 2
    elif ws_name == "Entropy":
        base_ftp = [0.75, 1.25, 2.0]
        ftp = np.interp(tp, base_tp, base_ftp)
        ftp_rep = True
        wsc = 0.85*(player_int) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 4
    elif ws_name == "Quietus":
        ftp  = 3.0
        ftp_rep = False
        wsc = 0.6*(player_mnd+player_str)
        nhits = 1
        base_enemy_def_scaling = [0.10, 0.30, 0.50]
        enemy_def_scaling = np.interp(tp, base_tp, base_enemy_def_scaling)
        enemy_defense *= (1-enemy_def_scaling)
    elif ws_name == "Catastrophe":
        ftp  = 2.75
        ftp_rep = False
        wsc = 0.4*(player_str+player_int) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1
    elif ws_name == "Scourge":
        ftp  = 3.0
        ftp_rep = False
        wsc = 0.4*(player_str+player_vit) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1
    elif ws_name == "Torcleaver":
        base_ftp = [4.75, 7.5, 9.765625]
        ftp = np.interp(tp, base_tp, base_ftp)
        ftp_rep = False
        wsc = 0.8*(player_vit) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1
    elif ws_name == "Resolution":
        base_ftp = [0.71875, 1.5, 2.25]
        ftp = np.interp(tp, base_tp, base_ftp)
        ftp_rep = True
        wsc = 0.85*(player_str) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 5
    elif ws_name == "Black Halo":
        base_ftp = [3.0, 7.25, 9.75] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc  = 0.7*player_mnd + 0.3*player_str + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 2 # Savage is a 2-hit weaponskill (+1 for offhand)
    elif ws_name == "Hexa Strike":
        crit_rate +=  gearset.playerstats["Crit Rate"]/100 # Blade: Hi can crit, so define crit rate now
        crit_boost = [0.1, 0.175, 0.25] # Middle value unknown. I just picked the half-way point to force linear scaling.
        crit_bonus = np.interp(tp, base_tp, crit_boost) # Bonus crit rate from TP scaling
        crit_rate += crit_bonus
        crit_rate += get_dex_crit(player_dex, enemy_agi) # Bonus crit rate from the player"s DEX stat vs enemy AGI stat
        ftp = 1.125
        ftp_rep = True
        wsc = 0.3*(player_mnd + player_str) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 6
    elif ws_name == "Randgrith":
        ftp  = 4.25
        ftp_rep = False
        wsc = 0.4*(player_str+player_mnd) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1
    elif ws_name == "Judgment":
        base_ftp = [3.5, 8.75, 12.0] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc = 0.5*(player_mnd + player_str) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1 # Savage is a 2-hit weaponskill (+1 for offhand)
    elif ws_name == "Realmrazer":
        acc_boost = [0, 20, 40] # Made these numbers up since it isnt known. Copied Blade: Ku, which i also made up
        acc_bonus = np.interp(tp, base_tp, acc_boost)
        ftp  = 0.9
        ftp_rep = True
        wsc = 0.85*player_mnd + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 7
    elif ws_name == "Seraph Strike":
        base_ftp = [2.125, 3.675, 6.125] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc  = 0.4*(player_str + player_mnd) + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 1
        magical = True
        element = "Light"
        ws_dINT = 0
    elif ws_name == "Upheaval":
        base_ftp = [1.0, 3.5, 6.5] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc  = 0.85*player_vit + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 4
    elif ws_name == "Ukko's Fury":
        crit_rate +=  gearset.playerstats["Crit Rate"]/100 # Blade: Hi can crit, so define crit rate now
        crit_boost = [0.2, 0.35, 0.55] # Middle value unknown. I just picked the half-way point to force linear scaling.
        crit_bonus = np.interp(tp, base_tp, crit_boost) # Bonus crit rate from TP scaling
        crit_rate += crit_bonus
        crit_rate += get_dex_crit(player_dex, enemy_agi) # Bonus crit rate from the player"s DEX stat vs enemy AGI stat
        ftp = 2.0
        ftp_rep = False
        wsc = 0.8*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 2
    elif ws_name == "King's Justice":
        base_ftp = [1.0, 3.0, 5.0] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc  = 0.5*player_str + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 3
    elif ws_name == "Metatron Torment":
        ftp  = 2.75
        ftp_rep = False
        wsc = 0.8*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1
    elif ws_name == "Ruinator":
        acc_boost = [0, 20, 40] # Made these numbers up since it isnt known. Copied Blade: Ku, which i also made up
        acc_bonus = np.interp(tp, base_tp, acc_boost)
        ftp  = 1.08
        ws_atk_bonus = 0.1
        special_set = set_gear(buffs, equipment, main_job, sub_job, ws_atk_bonus) # The attack bonus from Blade: Shun is applied before buffs. I needed to recalculate player attack with a "special set" to deal with this.
        player_attack1 = special_set.playerstats["Attack1"] # Redefine the player"s attack1 and attack2 used in the weapon skill based on the FTP scaling value
        player_attack2 = special_set.playerstats["Attack2"] # These boosted attack1 and attack2 values do not show up in the player"s stats shown in the final plot.
        ftp = 1.0
        ftp_rep = True
        wsc  = 0.85*player_str + dStat[1]*gearset.playerstats[dStat[0]] # Assuming 5/5 Blade: Shun merits. Add clickable drop-down menu to adjust merits later.
        nhits = 4
    elif ws_name == "Decimation":
        acc_boost = [0, 20, 40] # Made these numbers up since it isnt known. Copied Blade: Ku, which i also made up
        acc_bonus = np.interp(tp, base_tp, acc_boost)
        ftp = 1.75
        ftp_rep = True
        wsc  = 0.5*player_str + dStat[1]*gearset.playerstats[dStat[0]] # Assuming 5/5 Blade: Shun merits. Add clickable drop-down menu to adjust merits later.
        nhits = 3
    elif ws_name == "Cloudsplitter":
        base_ftp = [3.75, 6.69921875, 8.5 ] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc  = 0.4*(player_str + player_mnd) + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 1
        magical = True
        element = "Thunder"
        ws_dINT = 0
    elif ws_name == "Rampage":
        crit_rate +=  gearset.playerstats["Crit Rate"]/100 # Blade: Hi can crit, so define crit rate now
        crit_boost = [0, 20, 40] # Middle value unknown. I just picked the half-way point to force linear scaling.
        crit_bonus = np.interp(tp, base_tp, crit_boost) # Bonus crit rate from TP scaling
        crit_rate += crit_bonus
        crit_rate += get_dex_crit(player_dex, enemy_agi) # Bonus crit rate from the player"s DEX stat vs enemy AGI stat
        ftp = 1.0
        ftp_rep = True
        wsc = 0.5*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 5
    elif ws_name == "Empyreal Arrow":
        ws_atk_bonus = 1.0 # +100% attack, or a 2.0 multiplier. Gets added to percent_attack_buff in set_stats.py
        special_set = set_gear(buffs, equipment, main_job, sub_job, ws_atk_bonus)
        player_attack1 = special_set.playerstats["Attack1"] # Redefine the player"s attack1 and attack2 used in the weapon skill based on the FTP scaling value
        player_attack2 = special_set.playerstats["Attack2"] # These boosted attack1 and attack2 values do not show up in the player"s stats shown in the final plot.
        player_rangedattack = special_set.playerstats["Ranged Attack"] # These boosted attack1 and attack2 values do not show up in the player"s stats shown in the final plot.
        base_ftp = [1.5, 2.5, 5.0] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False
        wsc  = 0.5*player_agi + 0.2*player_str + dStat[1]*gearset.playerstats[dStat[0]] # Assuming 5/5 Blade: Shun merits. Add clickable drop-down menu to adjust merits later.
        nhits = 1
    elif ws_name == "Hot Shot":
        hybrid    = True
        base_ftp  = [0.5, 1.55, 2.1]
        ftp_hybrid = np.interp(tp, base_tp, base_ftp)
        ftp       = 1.0
        ftp_rep   = False
        wsc       = 0.7*player_agi + dStat[1]*gearset.playerstats[dStat[0]]
        nhits     = 1
        element   = "Fire"
    elif ws_name == "Flaming Arrow":
        hybrid    = True
        base_ftp  = [0.5, 1.55, 2.1]
        ftp_hybrid = np.interp(tp, base_tp, base_ftp)
        ftp       = 1.0
        ftp_rep   = False
        wsc       = 0.5*player_agi + 0.2*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits     = 1
        element   = "Fire"
    elif ws_name == "Last Stand":
        base_ftp  = [2.0, 3.0, 4.0]
        ftp = np.interp(tp, base_tp, base_ftp)
        ftp_rep   = True
        wsc       = 0.85*player_agi + dStat[1]*gearset.playerstats[dStat[0]]
        nhits     = 2
    elif ws_name == "Leaden Salute":
        base_ftp = [4.0,6.7,10.0] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc  = 1.0*player_agi + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 1
        magical = True
        element = "Dark"
        ws_dINT = (player_agi - enemy_int)*2 # No known cap.
    elif ws_name == "Shadow of Death":
        base_ftp = [1.0, 4.17, 8.6] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc  = 0.4*(player_str + player_int) + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 1
        magical = True
        element = "Dark"
        ws_dINT = 32 if (player_int - enemy_int)/2 + 8 > 32 else (player_int - enemy_int)/2 + 8
    elif ws_name == "Wildfire":
        ftp = 5.5
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc  = 0.6*player_agi + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 1
        magical = True
        element = "Fire"
        ws_dINT = 1276 if (player_agi - enemy_int)*2 > 1276 else (player_agi - enemy_int)*2 
    elif ws_name == "Trueflight":
        base_ftp = [3.890625,6.4921875,9.671875] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc  = 0.4*(player_str + player_mnd) + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 1
        magical = True
        element = "Light"
        ws_dINT = (player_agi - enemy_int)*2 # No known cap.
    elif ws_name == "Infernal Scythe":
        ftp = 3.5
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc  = 0.7*player_int + 0.3*player_str + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 1
        magical = True
        element = "Dark"
        ws_dINT = 0 # TODO: rename dINT to dSTAT
    elif ws_name == "Raiden Thrust":
        base_ftp = [1.0, 2.0, 3.0] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc  = 0.4*(player_str + player_int) + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 1
        magical = True
        element = "Thunder"
        ws_dINT = 32 if (player_int - enemy_int)/2 + 8 > 32 else (player_int - enemy_int)/2 + 8
    elif ws_name == "Thunder Thrust":
        base_ftp = [1.5, 2.0, 2.5] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc  = 0.4*(player_str + player_int) + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 1
        magical = True
        element = "Thunder"
        ws_dINT = 32 if (player_int - enemy_int)/2 + 8 > 32 else (player_int - enemy_int)/2 + 8
    elif ws_name == "Primal Rend":
        base_ftp = [3.0625,5.8359375,7.5625 ] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc  = 0.6*player_chr + 0.3*player_dex + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 1
        magical = True
        element = "Light"
        ws_dINT = 651 if (player_chr - enemy_int)*1.5 > 651 else (player_chr - enemy_int)*1.5
    elif ws_name == "Herculean Slash":
        ftp = 3.5
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc  = 0.8*player_vit + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 1
        magical = True
        element = "Ice"
        ws_dINT = 0 # TODO: rename dINT to dSTAT
    elif ws_name == "Freezebite":
        base_ftp = [1.5, 3.5, 6.0] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc  = 0.4*(player_str + player_int) + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 1
        magical = True
        element = "Ice"
        ws_dINT = 32 if (player_int - enemy_int)/2 + 8 > 32 else (player_int - enemy_int)/2 + 8
    elif ws_name == "Dark Harvest":
        base_ftp = [1.0, 2.0, 2.5] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc  = 0.4*(player_str + player_int) + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 1
        magical = True
        element = "Dark"
        ws_dINT = 32 if (player_int - enemy_int)/2 + 8 > 32 else (player_int - enemy_int)/2 + 8
    elif ws_name == "Earth Crusher":
        base_ftp = [1.0, 2.3125, 3.625] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc  = 0.4*(player_str + player_int) + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 1
        magical = True
        element = "Earth"
        ws_dINT = 32 if (player_int - enemy_int)/2 + 8 > 32 else (player_int - enemy_int)/2 + 8
    elif ws_name == "Cataclysm":
        base_ftp = [2.75, 4.0, 5.0] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc  = 0.3*(player_str + player_int) + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 1
        magical = True
        element = "Dark"
        ws_dINT = 32 if (player_int - enemy_int)/2 + 8 > 32 else (player_int - enemy_int)/2 + 8
    elif ws_name == "Vidohunir":
        ftp = 1.75
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc  = 0.8*player_int + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 1
        magical = True
        element = "Dark"
        ws_dINT = (player_int - enemy_int)*2 # No known cap
    elif ws_name == "Mordant Rime":
        acc_boost = [0, 20, 40] # Made these numbers up since it isnt known. Copied Blade: Ku, which i also made up
        acc_bonus = np.interp(tp, base_tp, acc_boost)
        ftp  = 5.0
        ftp_rep = False
        wsc  = 0.7*player_chr + 0.3*player_dex + dStat[1]*gearset.playerstats[dStat[0]] # Assuming 5/5 Blade: Shun merits. Add clickable drop-down menu to adjust merits later.
        nhits = 2
    elif ws_name == "Dancing Edge":
        acc_boost = [0, 20, 40] # Made these numbers up since it isnt known. Copied Blade: Ku, which i also made up
        acc_bonus = np.interp(tp, base_tp, acc_boost)
        ftp  = 1.1875 
        ftp_rep = False
        wsc  = 0.4*(player_chr + player_dex) + dStat[1]*gearset.playerstats[dStat[0]] # Assuming 5/5 Blade: Shun merits. Add clickable drop-down menu to adjust merits later.
        nhits = 5
    elif ws_name == "Shark Bite":
        base_ftp = [4.5, 6.8, 8.5] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc  = 0.4*(player_agi + player_dex) + dStat[1]*gearset.playerstats[dStat[0]] # Assuming 5/5 Blade: Shun merits. Add clickable drop-down menu to adjust merits later.
        nhits = 2
    elif ws_name == "Rudra's Storm":
        base_ftp = [5.0, 10.19, 13.0] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc  = 0.8*player_dex + dStat[1]*gearset.playerstats[dStat[0]] # Assuming 5/5 Blade: Shun merits. Add clickable drop-down menu to adjust merits later.
        nhits = 1
    elif ws_name == "Shattersoul":
        ftp = 1.375
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc  = 0.85*player_int + dStat[1]*gearset.playerstats[dStat[0]] # Assuming 5/5 Blade: Shun merits. Add clickable drop-down menu to adjust merits later.
        nhits = 3




    # I don't record enemy_MND, so let's just ignore Omniscience for now... 
    # elif ws_name == "Omniscience":
    #     ftp = 2.0
    #     ftp_rep = False # Does this WS replicate FTP across all hits?
    #     wsc  = 0.8*player_int + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
    #     nhits = 1
    #     magical = True
    #     element = "Dark"
    #     ws_dINT = (player_mnd - enemy_mnd)*2 # No known cap


    scaling = {"hybrid":hybrid, # TODO. I'm not even using acc_bonus from Ku and stuff??
               "magical":magical,
               "ws_dINT":ws_dINT,
               "wsc":wsc,
               "nhits":nhits,
               "element":element,
               "ftp":ftp,
               "ftp_rep":ftp_rep,
               "player_attack1":player_attack1,
               "player_attack2":player_attack2,
               "enemy_def":enemy_defense,
               "crit_rate":crit_rate,
               "ftp_hybrid":ftp_hybrid,
               "acc_bonus":acc_bonus}
    return(scaling)
