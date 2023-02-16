#
# Created by Kastra on Asura.
# Feel free to /tell in game or send a PM on FFXIAH you have questions, comments, or suggestions.
#
# Version date: 2023 February 14
#
import numpy as np
from set_stats import *
from get_dex_crit import *

def weaponskill_scaling(main_job, sub_job, ws_name, tp, gearset, equipment, buffs, dStat, dual_wield, enemy_defense, enemy_agi, enemy_int, enemy_mnd, job_abilities, kick_ws_footwork=False):
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
    player_rangedattack = gearset.playerstats["Ranged Attack"]
    crit_rate = 0 # Start from zero crit rate. We add crit rate if the weapon skill is a crit weapon skill and if Shining One is equipped.

    main_wpn_name = equipment["main"]["Name2"]
    phys_rng_ws = ws_name in ["Flaming Arrow", "Namas Arrow", "Apex Arrow", "Refulgent Arrow","Empyreal Arrow", "Sidewinder", "Piercing Arrow", "Jishnu's Radiance", "Blast Arrow", "Hot Shot", "Coronach","Last Stand","Detonator", "Blast Shot", "Slug Shot", "Split Shot", ] # Used to ensure Shining One does not let Ranged Weapon skills crit


    crit_ws = False # Used with Shining One. If the WS can natively crit, then Shining One should NOT add dDEX or gear crit rate since the WS already did.
    hybrid = False
    magical = False
    ws_dINT = 0
    element = "None"
    ftp_hybrid = 0
    acc_bonus = 0

    base_tp = [1000,2000,3000]



    # Sword Weapon skills
    if ws_name == "Fast Blade":
        base_ftp = [1.0, 1.5, 2.0]
        ftp      = np.interp(tp, base_tp, base_ftp)
        ftp_rep = False
        wsc      = 0.4*(player_str + player_dex) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits    = 2
    elif ws_name == "Burning Blade":
        base_ftp = [1.0, 2.09765625, 3.3984375]
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc = 0.4*(player_str + player_int) + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 1
        magical = True
        element = "Fire"
        ws_dINT = 32 if (player_int - enemy_int)/2 + 8 > 32 else (player_int - enemy_int)/2 + 8
    elif ws_name == "Red Lotus Blade":
        base_ftp = [1.0, 2.3828125, 3.75] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc = 0.4*(player_str + player_int) + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 1
        magical = True
        element = "Fire"
        ws_dINT = 32 if (player_int - enemy_int)/2 + 8 > 32 else (player_int - enemy_int)/2 + 8
    elif ws_name == "Shining Blade":
        base_ftp = [1.125, 2.22265625, 3.5234375] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc = 0.4*(player_str + player_mnd) + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 1
        magical = True
        element = "Light"
        ws_dINT = 0
    elif ws_name == "Seraph Blade":
        base_ftp = [1.125, 2.625, 4.125] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc = 0.4*(player_str + player_mnd) + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 1
        magical = True
        element = "Light"
        ws_dINT = 0
    elif ws_name == "Circle Blade":
        ftp  = 1.0
        ftp_rep = False
        wsc = 1.0*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1
    elif ws_name == "Swift Blade":
        acc_boost = [0, 20, 40] # Made these numbers up since it isnt known.
        acc_bonus = np.interp(tp, base_tp, acc_boost)
        ftp  = 1.5
        ftp_rep = True
        wsc = 0.5*(player_str + player_mnd) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 3
    elif ws_name == "Savage Blade":
        base_ftp = [4.0, 10.25, 13.75] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc = 0.5*(player_str + player_mnd) + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 2 # Savage is a 2-hit weaponskill (+1 for offhand)
    elif ws_name == "Sanguine Blade":
        ftp  = 2.75
        ftp_rep = False
        wsc = 0.5*player_mnd + 0.3*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1
        magical = True
        element = "Dark"
        ws_dINT = (player_int - enemy_int)*2
    elif ws_name == "Requiescat":
        atk_boost = [-0.2, -0.1, 0.0] # Requiescat has an attack penalty
        ws_atk_bonus = np.interp(tp, base_tp, atk_boost)
        special_set = set_gear(buffs, equipment, main_job, sub_job, ws_atk_bonus, job_abilities=job_abilities)
        player_attack1 = special_set.playerstats["Attack1"]
        player_attack2 = special_set.playerstats["Attack2"]
        ftp = 1.0
        ftp_rep = True
        wsc = 0.85*player_mnd + dStat[1]*gearset.playerstats[dStat[0]] # Assuming 5/5 Blade: Shun merits. Add clickable drop-down menu to adjust merits later.
        nhits = 5
    elif ws_name == "Knights of Round":
        ftp  = 5.0
        ftp_rep = False
        wsc = 0.4*(player_mnd + player_str) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1
    elif ws_name == "Chant du Cygne":
        crit_ws = True
        crit_rate += gearset.playerstats["Crit Rate"]/100
        crit_boost = [0.15, 0.25, 0.40]
        crit_bonus = np.interp(tp, base_tp, crit_boost) # Bonus crit rate from TP scaling
        crit_rate += crit_bonus
        crit_rate += get_dex_crit(player_dex, enemy_agi) # Bonus crit rate from the player"s DEX stat vs enemy AGI stat
        ftp = 1.6328125
        ftp_rep = True
        wsc = 0.8*player_dex + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 3
    elif ws_name == "Death Blossom":
        ftp  = 4.0
        ftp_rep = False
        wsc = 0.5*player_mnd + 0.3*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 3
    elif ws_name == "Expiacion":
        base_ftp = [3.796875,9.390625,12.1875] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc = 0.3*(player_str + player_int) + 0.2*player_dex + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 2 # Savage is a 2-hit weaponskill (+1 for offhand)
    elif ws_name == "Fast Blade II":
        base_ftp = [1.8, 3.5, 5.0] 
        ftp = np.interp(tp, base_tp, base_ftp)
        ftp_rep = True 
        wsc = 0.8*player_dex + dStat[1]*gearset.playerstats[dStat[0]] 
        nhits = 2 


    # Katana weapon skills
    elif ws_name == "Blade: Retsu":
        base_ftp  = [0.5, 1.5, 2.5]
        ftp       = 1.0
        ftp_rep   = False
        wsc       = 0.6*player_dex + 0.2*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits     = 2
    elif ws_name == "Blade: Teki":
        hybrid    = True
        base_ftp  = [0.5, 1.375, 2.25]
        ftp_hybrid = np.interp(tp, base_tp, base_ftp)
        ftp       = 1.0
        ftp_rep   = False
        wsc       = 0.3*(player_str + player_int) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits     = 1
        element   = "Water"
    elif ws_name == "Blade: To":
        hybrid    = True
        base_ftp  = [0.5, 1.5, 2.5]
        ftp_hybrid = np.interp(tp, base_tp, base_ftp)
        ftp       = 1.0
        ftp_rep   = False
        wsc       = 0.4*(player_str + player_int) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits     = 1
        element   = "Ice"
    elif ws_name == "Blade: Chi":
        hybrid    = True
        base_ftp  = [0.5, 1.375, 2.25]
        ftp_hybrid = np.interp(tp, base_tp, base_ftp)
        ftp       = 1.0
        ftp_rep   = False
        wsc       = 0.3*(player_str + player_int) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits     = 2
        element   = "Earth"
    elif ws_name == "Blade: Ei":
        base_ftp = [1.0, 3.0, 5.0] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc = 0.4*(player_str + player_int) + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 1
        magical = True
        element = "Dark"
        ws_dINT = 32 if (player_int - enemy_int)/2 + 8 > 32 else (player_int - enemy_int)/2 + 8
    elif ws_name == "Blade: Jin":
        crit_ws = True
        crit_rate += gearset.playerstats["Crit Rate"]/100 # Blade: Hi can crit, so define crit rate now
        crit_boost = [0.1, 0.25, 0.5] # Copied Evisceration values due to FTP Scaling and Cyclopedia claiming first value is +10%
        crit_bonus = np.interp(tp, base_tp, crit_boost) # Bonus crit rate from TP scaling
        crit_rate += crit_bonus
        crit_rate += get_dex_crit(player_dex, enemy_agi) # Bonus crit rate from the player"s DEX stat vs enemy AGI stat
        ftp = 1.375
        ftp_rep = True
        wsc = 0.3*(player_dex + player_str) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 3
    elif ws_name == "Blade: Ten":
        base_ftp = [4.5, 11.5, 15.5]
        ftp      = np.interp(tp, base_tp, base_ftp)
        ftp_rep = False
        wsc      = 0.3*(player_str + player_dex) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits    = 1
    elif ws_name == "Blade: Ku":
        acc_boost = [0, 20, 40] # Made these numbers up since it isnt known.
        acc_bonus = np.interp(tp, base_tp, acc_boost)
        ftp  = 1.25
        ftp_rep = True
        wsc = 0.3*(player_str + player_dex) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 5
    elif ws_name == "Blade: Yu":
        ftp = 3.0
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc = 0.4*(player_dex + player_int) + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 1
        magical = True
        element = "Water"
        ws_dINT = 0
    elif ws_name == "Blade: Kamu":
        ftp  = 1.0
        ftp_rep = False
        wsc = 0.6*(player_int + player_str) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1
        special_set = set_gear(buffs, equipment, main_job, sub_job, 1.25, job_abilities=job_abilities) # The attack bonus from Blade: Kamu is similar to Blade: Shun (see above)
        player_attack1 = special_set.playerstats["Attack1"]
        player_attack2 = special_set.playerstats["Attack2"]
        enemy_defense *= 0.75 # TODO: This should be additive with Dia, Frailty, etc? I think it's fine as is.
    elif ws_name == "Blade: Shun":
        atk_boost = [1.0, 2.0, 3.0]
        ws_atk_bonus = np.interp(tp, base_tp, atk_boost) - 1.0
        special_set = set_gear(buffs, equipment, main_job, sub_job, ws_atk_bonus, job_abilities=job_abilities) # The attack bonus from Blade: Shun is applied before buffs. I needed to recalculate player attack with a "special set" to deal with this.
        player_attack1 = special_set.playerstats["Attack1"] # Redefine the player"s attack1 and attack2 used in the weapon skill based on the FTP scaling value
        player_attack2 = special_set.playerstats["Attack2"] # These boosted attack1 and attack2 values do not show up in the player"s stats shown in the final plot.
        ftp = 1.0
        ftp_rep = True
        wsc = 0.85*player_dex + dStat[1]*gearset.playerstats[dStat[0]] # Assuming 5/5 Blade: Shun merits. Add clickable drop-down menu to adjust merits later.
        nhits = 5
    elif ws_name == "Blade: Metsu":
        ftp  = 5.0
        ftp_rep = False
        wsc = 0.8*player_dex + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1
    elif ws_name == "Blade: Hi":
        crit_ws = True
        crit_rate += gearset.playerstats["Crit Rate"]/100 # Blade: Hi can crit, so define crit rate now
        crit_boost = [0.15, 0.2, 0.25]
        crit_bonus = np.interp(tp, base_tp, crit_boost) # Bonus crit rate from TP scaling
        crit_rate += crit_bonus
        crit_rate += get_dex_crit(player_dex, enemy_agi) # Bonus crit rate from the player"s DEX stat vs enemy AGI stat
        ftp = 5.0
        ftp_rep = False
        wsc = 0.8*player_agi + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1


    # Dagger weapon skills
    elif ws_name == "Viper Bite":
        ftp = 1.0
        ftp_rep = False
        ws_atk_bonus = 1.0
        special_set = set_gear(buffs, equipment, main_job, sub_job, ws_atk_bonus, job_abilities=job_abilities) # The attack bonus from Blade: Shun is applied before buffs. I needed to recalculate player attack with a "special set" to deal with this.
        player_attack1 = special_set.playerstats["Attack1"] # Redefine the player"s attack1 and attack2 used in the weapon skill based on the FTP scaling value
        player_attack2 = special_set.playerstats["Attack2"] # These boosted attack1 and attack2 values do not show up in the player"s stats shown in the final plot.
        wsc = 1.0*player_dex + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 2
    elif ws_name == "Dancing Edge":
        acc_boost = [0, 20, 40] # Made these numbers up since it isnt known. Copied Blade: Ku, which i also made up
        acc_bonus = np.interp(tp, base_tp, acc_boost)
        ftp  = 1.1875 
        ftp_rep = False
        wsc = 0.4*(player_chr + player_dex) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 5
    elif ws_name == "Shark Bite":
        base_ftp = [4.5, 6.8, 8.5] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc = 0.4*(player_agi + player_dex) + dStat[1]*gearset.playerstats[dStat[0]] 
        nhits = 2
    elif ws_name == "Evisceration":
        crit_ws = True
        crit_rate += gearset.playerstats["Crit Rate"]/100
        crit_boost = [0.1, 0.25, 0.5]
        crit_bonus = np.interp(tp, base_tp, crit_boost)
        crit_rate += crit_bonus
        crit_rate += get_dex_crit(player_dex, enemy_agi)
        ftp = 1.25
        ftp_rep = True
        wsc = 0.5*player_dex + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 5
    elif ws_name == "Aeolian Edge":
        base_ftp = [2.0, 3.0, 4.5] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc = 0.4*(player_dex + player_int) + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 1
        magical = True
        element = "Wind"
        ws_dINT = 32 if (player_int - enemy_int)/2 + 8 > 32 else (player_int - enemy_int)/2 + 8
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
    elif ws_name == "Rudra's Storm":
        base_ftp = [5.0, 10.19, 13.0] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc = 0.8*player_dex + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1
    elif ws_name == "Mandalic Stab":
        base_ftp = [4.0, 6.09, 8.5]
        ftp = np.interp(tp, base_tp, base_ftp)
        ftp_rep = False
        ws_atk_bonus = 0.75
        special_set = set_gear(buffs, equipment, main_job, sub_job, ws_atk_bonus, job_abilities=job_abilities) # The attack bonus from Blade: Shun is applied before buffs. I needed to recalculate player attack with a "special set" to deal with this.
        player_attack1 = special_set.playerstats["Attack1"] # Redefine the player"s attack1 and attack2 used in the weapon skill based on the FTP scaling value
        player_attack2 = special_set.playerstats["Attack2"] # These boosted attack1 and attack2 values do not show up in the player"s stats shown in the final plot.
        wsc = 0.6*player_dex + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1
    elif ws_name == "Mordant Rime":
        acc_boost = [0, 20, 40] # Made these numbers up since it isnt known. Copied Blade: Ku, which i also made up
        acc_bonus = np.interp(tp, base_tp, acc_boost)
        ftp  = 5.0
        ftp_rep = False
        wsc = 0.7*player_chr + 0.3*player_dex + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 2
    elif ws_name == "Pyrrhic Kleos":
        ftp  = 1.75
        ftp_rep = True
        wsc = 0.4*(player_str + player_dex) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 4


    # Polearm weapon skills
    elif ws_name == "Double Thrust":
        base_ftp = [1.0, 1.5, 2.0] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc = 0.3*(player_str + player_dex) + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 2
    elif ws_name == "Thunder Thrust":
        base_ftp = [1.5, 2.0, 2.5] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc = 0.4*(player_str + player_int) + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 1
        magical = True
        element = "Thunder"
        ws_dINT = 32 if (player_int - enemy_int)/2 + 8 > 32 else (player_int - enemy_int)/2 + 8
    elif ws_name == "Raiden Thrust":
        base_ftp = [1.0, 2.0, 3.0] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc = 0.4*(player_str + player_int) + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 1
        magical = True
        element = "Thunder"
        ws_dINT = 32 if (player_int - enemy_int)/2 + 8 > 32 else (player_int - enemy_int)/2 + 8
    elif ws_name == "Penta Thrust":
        acc_boost = [0, 20, 40] # Made these numbers up since it isnt known. Copied Blade: Ku, which i also made up
        acc_bonus = np.interp(tp, base_tp, acc_boost)
        ftp  = 1.00
        ftp_rep = False
        wsc = 0.2*(player_str + player_dex) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 5
        special_set = set_gear(buffs, equipment, main_job, sub_job, -0.125, job_abilities=job_abilities) # Recalculate the player attack using a negative multiplier bonus
        player_attack1 = special_set.playerstats["Attack1"]
    elif ws_name == "Wheeling Thrust":
        ftp  = 1.75
        ftp_rep = False
        wsc = 0.8*player_str + dStat[1]*gearset.playerstats[dStat[0]] # TODO: remove all these utu/crep dSTAT things from WSs and put one single line at the end: wsc += dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1
        base_enemy_def_scaling = [0.50, 0.625, 0.75]
        enemy_def_scaling = np.interp(tp, base_tp, base_enemy_def_scaling)
        enemy_defense *= (1-enemy_def_scaling)
    elif ws_name == "Impulse Drive":
        base_ftp = [1.0, 3.0, 5.5]
        ftp      = np.interp(tp, base_tp, base_ftp)
        ftp_rep  = False
        wsc      = 1.0*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits    = 2
    elif ws_name == "Sonic Thrust":
        base_ftp = [3.0, 3.7, 4.5]
        ftp      = np.interp(tp, base_tp, base_ftp)
        ftp_rep  = False
        wsc      = 0.4*(player_dex + player_str) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits    = 1
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
        wsc = 0.6*(player_vit + player_str)
        nhits = 1
        base_enemy_def_scaling = [0.125, 0.375, 0.625]
        enemy_def_scaling = np.interp(tp, base_tp, base_enemy_def_scaling)
        enemy_defense *= (1-enemy_def_scaling)
    elif ws_name == "Drakesbane":
        crit_ws = True
        crit_rate += gearset.playerstats["Crit Rate"]/100 # Blade: Hi can crit, so define crit rate now
        crit_boost = [0.1, 0.25, 0.40]
        crit_bonus = np.interp(tp, base_tp, crit_boost) # Bonus crit rate from TP scaling
        crit_rate += crit_bonus
        crit_rate += get_dex_crit(player_dex, enemy_agi) # Bonus crit rate from the player"s DEX stat vs enemy AGI stat
        ftp = 1.0
        ftp_rep = False
        wsc = 0.5*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 4
        special_set = set_gear(buffs, equipment, main_job, sub_job, 0.8125 - 1.0, job_abilities=job_abilities) # Recalculate the player attack using a negative multiplier bonus
        player_attack1 = special_set.playerstats["Attack1"]


    # Great Katana weapon skills
    elif ws_name == "Tachi: Enpi":
        base_ftp = [1.0, 1.5, 2.0]
        ftp = np.interp(tp, base_tp, base_ftp)
        ftp_rep = False
        wsc = 0.6*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 2
    elif ws_name == "Tachi: Goten":
        hybrid    = True
        base_ftp  = [0.5, 1.5, 2.5]
        ftp_hybrid = np.interp(tp, base_tp, base_ftp)
        ftp       = 1.0
        ftp_rep   = False
        wsc       = 0.6*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits     = 1
        element   = "Thunder"
    elif ws_name == "Tachi: Kagero":
        hybrid    = True
        base_ftp  = [0.5, 1.5, 2.5]
        ftp_hybrid = np.interp(tp, base_tp, base_ftp)
        ftp       = 1.0
        ftp_rep   = False
        wsc       = 0.75*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits     = 1
        element   = "Fire"
    elif ws_name == "Tachi: Koki":
        hybrid    = True
        base_ftp  = [0.5, 1.5, 2.5]
        ftp_hybrid = np.interp(tp, base_tp, base_ftp)
        ftp       = 1.0
        ftp_rep   = False
        wsc       = 0.3*player_mnd + 0.5*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits     = 1
        element   = "Light"
    elif ws_name == "Tachi: Jinpu":
        hybrid    = True
        base_ftp  = [0.5, 1.5, 2.5]
        ftp_hybrid = np.interp(tp, base_tp, base_ftp)
        ftp       = 1.0
        ftp_rep   = False
        wsc       = 0.3*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits     = 2
        element   = "Wind"
    elif ws_name == "Tachi: Yukikaze":
        base_ftp = [1.5625, 2.6875, 4.125]
        ftp = np.interp(tp, base_tp, base_ftp)
        ftp_rep = False
        special_set = set_gear(buffs, equipment, main_job, sub_job, 0.5, job_abilities=job_abilities)
        player_attack1 = special_set.playerstats["Attack1"]
        player_attack2 = special_set.playerstats["Attack2"]
        wsc = 0.75*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1
    elif ws_name == "Tachi: Gekko":
        base_ftp = [1.5625, 2.6875, 4.125]
        ftp = np.interp(tp, base_tp, base_ftp)
        ftp_rep = False
        special_set = set_gear(buffs, equipment, main_job, sub_job, 1.0, job_abilities=job_abilities)
        player_attack1 = special_set.playerstats["Attack1"]
        player_attack2 = special_set.playerstats["Attack2"]
        wsc = 0.75*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1
    elif ws_name == "Tachi: Kasha":
        base_ftp = [1.5625, 2.6875, 4.125]
        ftp = np.interp(tp, base_tp, base_ftp)
        ftp_rep = False
        special_set = set_gear(buffs, equipment, main_job, sub_job, 0.65, job_abilities=job_abilities) 
        player_attack1 = special_set.playerstats["Attack1"]
        player_attack2 = special_set.playerstats["Attack2"]
        wsc = 0.75*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1
    elif ws_name == "Tachi: Shoha":
        base_ftp = [1.375, 2.1875, 2.6875]
        ftp = np.interp(tp, base_tp, base_ftp)
        ftp_rep = False
        special_set = set_gear(buffs, equipment, main_job, sub_job, 1.375, job_abilities=job_abilities) # The attack bonus from Tachi: Shoha is similar to Blade: Shun (see above)
        player_attack1 = special_set.playerstats["Attack1"]
        player_attack2 = special_set.playerstats["Attack2"]
        wsc = 0.85*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 2
    elif ws_name == "Tachi: Kaiten":
        ftp  = 3.0
        ftp_rep = False
        wsc = 0.8*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1
    elif ws_name == "Tachi: Fudo":
        base_ftp = [3.75, 5.75, 8.0]
        ftp = np.interp(tp, base_tp, base_ftp)
        ftp_rep = False
        wsc = 0.8*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1
    elif ws_name == "Tachi: Rana":
        acc_boost = [0, 20, 40] # Made these numbers up since it isnt known. Copied Blade: Ku, which i also made up
        acc_bonus = np.interp(tp, base_tp, acc_boost)
        ftp  = 1.0
        ftp_rep = False
        wsc = 0.5*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 3


    # Scythe weapon skills
    elif ws_name == "Slice":
        base_ftp = [1.5, 1.75, 2.0]
        ftp = np.interp(tp, base_tp, base_ftp)
        ftp_rep = False
        wsc = 1.0*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1
    elif ws_name == "Dark Harvest":
        base_ftp = [1.0, 2.0, 2.5] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc = 0.4*(player_str + player_int) + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 1
        magical = True
        element = "Dark"
        ws_dINT = 32 if (player_int - enemy_int)/2 + 8 > 32 else (player_int - enemy_int)/2 + 8
    elif ws_name == "Shadow of Death":
        base_ftp = [1.0, 4.17, 8.6] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc = 0.4*(player_str + player_int) + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 1
        magical = True
        element = "Dark"
        ws_dINT = 32 if (player_int - enemy_int)/2 + 8 > 32 else (player_int - enemy_int)/2 + 8
    elif ws_name == "Spinning Scythe":
        ftp = 1.0
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc = 1.0*player_str + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 1
    elif ws_name == "Cross Reaper":
        base_ftp = [2.0, 4.0, 7.0]
        ftp = np.interp(tp, base_tp, base_ftp)
        ftp_rep = False
        wsc = 0.6*(player_str + player_mnd) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 2
    elif ws_name == "Guillotine":
        ftp = 0.875
        ftp_rep = False
        wsc = 0.3*player_str + 0.5*player_mnd + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 4
    elif ws_name == "Spiral Hell":
        base_ftp = [1.375,2.75,4.75]
        ftp = np.interp(tp, base_tp, base_ftp)
        ftp_rep = False
        wsc = 0.5*(player_str + player_int) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1
    elif ws_name == "Infernal Scythe":
        ftp = 3.5
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc = 0.7*player_int + 0.3*player_str + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 1
        magical = True
        element = "Dark"
        ws_dINT = 0 # TODO: rename dINT to dSTAT
    elif ws_name == "Entropy":
        base_ftp = [0.75, 1.25, 2.0]
        ftp = np.interp(tp, base_tp, base_ftp)
        ftp_rep = True
        wsc = 0.85*(player_int) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 4
    elif ws_name == "Catastrophe":
        ftp  = 2.75
        ftp_rep = False
        wsc = 0.4*(player_str + player_int) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1
    elif ws_name == "Quietus":
        ftp  = 3.0
        ftp_rep = False
        wsc = 0.6*(player_mnd + player_str) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1
        base_enemy_def_scaling = [0.10, 0.30, 0.50]
        enemy_def_scaling = np.interp(tp, base_tp, base_enemy_def_scaling)
        enemy_defense *= (1-enemy_def_scaling)
    elif ws_name == "Insurgency":
        base_ftp = [0.5, 3.25, 6.0]
        ftp = np.interp(tp, base_tp, base_ftp)
        ftp_rep = False
        wsc = 0.2*(player_str + player_int) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 4


    # Great Sword weapon skills
    elif ws_name == "Hard Slash":
        base_ftp = [1.5, 1.75, 2.0] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc = 0.4*(player_str + player_agi) + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 2
    elif ws_name == "Freezebite":
        base_ftp = [1.5, 3.5, 6.0] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc = 0.4*(player_str + player_int) + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 1
        magical = True
        element = "Ice"
        ws_dINT = 32 if (player_int - enemy_int)/2 + 8 > 32 else (player_int - enemy_int)/2 + 8
    elif ws_name == "Shockwave":
        ftp = 1.0
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc = 0.3*(player_str + player_mnd) + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 1
    elif ws_name == "Sickle Moon":
        base_ftp = [1.5, 2.0, 2.75] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc = 0.4*(player_str + player_agi) + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 1
    elif ws_name == "Spinning Slash":
        base_ftp = [2.5,3.0,3.5]
        ftp = np.interp(tp, base_tp, base_ftp)
        ftp_rep = False
        ws_atk_bonus = 0.5
        special_set = set_gear(buffs, equipment, main_job, sub_job, ws_atk_bonus, job_abilities=job_abilities) # The attack bonus from Blade: Shun is applied before buffs. I needed to recalculate player attack with a "special set" to deal with this.
        player_attack1 = special_set.playerstats["Attack1"] # Redefine the player"s attack1 and attack2 used in the weapon skill based on the FTP scaling value
        player_attack2 = special_set.playerstats["Attack2"] # These boosted attack1 and attack2 values do not show up in the player"s stats shown in the final plot.
        wsc = 0.3*(player_str + player_int) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1
    elif ws_name == "Ground Strike":
        base_ftp = [1.5, 1.75, 3.0]
        ftp      = np.interp(tp, base_tp, base_ftp)
        ftp_rep  = False
        wsc      = 0.5*(player_int + player_str) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits    = 1
        special_set = set_gear(buffs, equipment, main_job, sub_job, 0.75, job_abilities=job_abilities)
        player_attack1 = special_set.playerstats["Attack1"]
        player_attack2 = special_set.playerstats["Attack2"]
    elif ws_name == "Herculean Slash":
        ftp = 3.5
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc = 0.8*player_vit + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 1
        magical = True
        element = "Ice"
        ws_dINT = 0 # TODO: rename dINT to dSTAT
    elif ws_name == "Resolution":
        base_ftp = [0.71875, 1.5, 2.25]
        ftp = np.interp(tp, base_tp, base_ftp)
        ftp_rep = True
        wsc = 0.85*(player_str) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 5
    elif ws_name == "Scourge":
        ftp  = 3.0
        ftp_rep = False
        wsc = 0.4*(player_str + player_vit) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1
    elif ws_name == "Torcleaver":
        base_ftp = [4.75, 7.5, 9.765625]
        ftp = np.interp(tp, base_tp, base_ftp)
        ftp_rep = False
        wsc = 0.8*(player_vit) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1
    elif ws_name == "Dimidiation":
        base_ftp = [2.25, 4.5, 6.75]
        ftp = np.interp(tp, base_tp, base_ftp)
        ftp_rep = False
        ws_atk_bonus = 0.25
        special_set = set_gear(buffs, equipment, main_job, sub_job, ws_atk_bonus, job_abilities=job_abilities) # The attack bonus from Blade: Shun is applied before buffs. I needed to recalculate player attack with a "special set" to deal with this.
        player_attack1 = special_set.playerstats["Attack1"] # Redefine the player"s attack1 and attack2 used in the weapon skill based on the FTP scaling value
        player_attack2 = special_set.playerstats["Attack2"] # These boosted attack1 and attack2 values do not show up in the player"s stats shown in the final plot.
        wsc = 0.8*player_dex + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 2


    # Club weapon skills
    elif ws_name == "Shining Strike":
        base_ftp = [1.625, 3.0, 4.625] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc = 0.4*(player_str + player_mnd) + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 1
        magical = True
        element = "Light"
        ws_dINT = 0
    elif ws_name == "Seraph Strike":
        base_ftp = [2.125, 3.675, 6.125] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc = 0.4*(player_str + player_mnd) + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 1
        magical = True
        element = "Light"
        ws_dINT = 0
    elif ws_name == "True Strike":
        crit_ws = True
        crit_rate = 1.0
        acc_boost = [-100, -50, 0] # Made these numbers up since it isnt known.
        acc_bonus = np.interp(tp, base_tp, acc_boost)
        ftp  = 1.0
        ftp_rep = False
        wsc = 1.0*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1
        ws_atk_bonus = 1.0
        special_set = set_gear(buffs, equipment, main_job, sub_job, ws_atk_bonus, job_abilities=job_abilities)
        player_attack1 = special_set.playerstats["Attack1"]
        player_attack2 = special_set.playerstats["Attack2"]
    elif ws_name == "Judgment":
        base_ftp = [3.5, 8.75, 12.0] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc = 0.5*(player_mnd + player_str) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1 # Savage is a 2-hit weaponskill (+1 for offhand)
    elif ws_name == "Hexa Strike":
        crit_ws = True
        crit_rate += gearset.playerstats["Crit Rate"]/100 # Blade: Hi can crit, so define crit rate now
        crit_boost = [0.1, 0.175, 0.25] # Middle value unknown. I just picked the half-way point to force linear scaling.
        crit_bonus = np.interp(tp, base_tp, crit_boost) # Bonus crit rate from TP scaling
        crit_rate += crit_bonus
        crit_rate += get_dex_crit(player_dex, enemy_agi) # Bonus crit rate from the player"s DEX stat vs enemy AGI stat
        ftp = 1.125
        ftp_rep = True
        wsc = 0.3*(player_mnd + player_str) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 6
    elif ws_name == "Black Halo":
        base_ftp = [3.0, 7.25, 9.75] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc = 0.7*player_mnd + 0.3*player_str + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 2 # Savage is a 2-hit weaponskill (+1 for offhand)
    elif ws_name == "Realmrazer":
        acc_boost = [0, 20, 40] # Made these numbers up since it isnt known. Copied Blade: Ku, which i also made up
        acc_bonus = np.interp(tp, base_tp, acc_boost)
        ftp  = 0.9
        ftp_rep = True
        wsc = 0.85*player_mnd + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 7
    elif ws_name == "Randgrith":
        ftp  = 4.25
        ftp_rep = False
        wsc = 0.4*(player_str + player_mnd) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1
    elif ws_name == "Mystic Boon":
        base_ftp = [2.5, 4.0, 7.0] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc = 0.7*player_mnd + 0.3*player_str + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 1 # Savage is a 2-hit weaponskill (+1 for offhand)
    elif ws_name == "Exudation":
        atk_boost = [1.5, 3.625, 4.750]
        ws_atk_bonus = np.interp(tp, base_tp, atk_boost) - 1.0
        special_set = set_gear(buffs, equipment, main_job, sub_job, ws_atk_bonus, job_abilities=job_abilities) # The attack bonus from Blade: Shun is applied before buffs. I needed to recalculate player attack with a "special set" to deal with this.
        player_attack1 = special_set.playerstats["Attack1"] # Redefine the player"s attack1 and attack2 used in the weapon skill based on the FTP scaling value
        player_attack2 = special_set.playerstats["Attack2"] # These boosted attack1 and attack2 values do not show up in the player"s stats shown in the final plot.
        ftp = 2.8
        ftp_rep = False
        wsc = 0.5*(player_mnd + player_int) + dStat[1]*gearset.playerstats[dStat[0]] # Assuming 5/5 Blade: Shun merits. Add clickable drop-down menu to adjust merits later.
        nhits = 1


    # Great Axe weapon skills
    elif ws_name == "Iron Tempest":
        atk_boost = [1.0, 1.2, 1.5]
        ws_atk_bonus = np.interp(tp, base_tp, atk_boost) - 1.0
        special_set = set_gear(buffs, equipment, main_job, sub_job, ws_atk_bonus, job_abilities=job_abilities) # The attack bonus from Blade: Shun is applied before buffs. I needed to recalculate player attack with a "special set" to deal with this.
        player_attack1 = special_set.playerstats["Attack1"] # Redefine the player"s attack1 and attack2 used in the weapon skill based on the FTP scaling value
        player_attack2 = special_set.playerstats["Attack2"] # These boosted attack1 and attack2 values do not show up in the player"s stats shown in the final plot.
        ftp = 1.0
        ftp_rep = False
        wsc = 0.6*player_str + dStat[1]*gearset.playerstats[dStat[0]] # Assuming 5/5 Blade: Shun merits. Add clickable drop-down menu to adjust merits later.
        nhits = 1
    elif ws_name == "Raging Rush":
        crit_ws = True
        crit_rate += gearset.playerstats["Crit Rate"]/100 # Blade: Hi can crit, so define crit rate now
        crit_boost = [0.15, 0.30, 0.50]
        crit_bonus = np.interp(tp, base_tp, crit_boost) # Bonus crit rate from TP scaling
        crit_rate += crit_bonus
        crit_rate += get_dex_crit(player_dex, enemy_agi) # Bonus crit rate from the player"s DEX stat vs enemy AGI stat
        ftp = 1.0
        ftp_rep = True
        wsc = 0.5*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 3
    elif ws_name == "Steel Cyclone":
        base_ftp = [1.5, 2.5, 4.0]
        ftp = np.interp(tp, base_tp, base_ftp)
        ftp_rep = False
        ws_atk_bonus = 0.5
        special_set = set_gear(buffs, equipment, main_job, sub_job, ws_atk_bonus, job_abilities=job_abilities) # The attack bonus from Blade: Shun is applied before buffs. I needed to recalculate player attack with a "special set" to deal with this.
        player_attack1 = special_set.playerstats["Attack1"] # Redefine the player"s attack1 and attack2 used in the weapon skill based on the FTP scaling value
        player_attack2 = special_set.playerstats["Attack2"] # These boosted attack1 and attack2 values do not show up in the player"s stats shown in the final plot.
        wsc = 0.6*(player_str + player_vit) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1
    elif ws_name == "Fell Cleave":
        ftp  = 2.75
        ftp_rep = False
        wsc = 0.6*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1
    elif ws_name == "Upheaval":
        base_ftp = [1.0, 3.5, 6.5] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc = 0.85*player_vit + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 4
    elif ws_name == "Metatron Torment":
        ftp  = 2.75
        ftp_rep = False
        wsc = 0.8*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1
    elif ws_name == "Ukko's Fury":
        crit_ws = True
        crit_rate += gearset.playerstats["Crit Rate"]/100 # Blade: Hi can crit, so define crit rate now
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
        wsc = 0.5*player_str + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 3


    # Axe weapon skills
    elif ws_name == "Raging Axe":
        base_ftp = [1.0, 1.5, 2.0] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc = 0.6*player_str + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 2
    elif ws_name == "Spinning Axe":
        base_ftp = [2.0, 2.5, 3.0] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc = 0.6*player_str + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 2
    elif ws_name == "Rampage":
        crit_ws = True
        crit_rate += gearset.playerstats["Crit Rate"]/100 # Blade: Hi can crit, so define crit rate now
        crit_boost = [0.0, 0.20, 0.40] # Middle value unknown. I just picked the half-way point to force linear scaling.
        crit_bonus = np.interp(tp, base_tp, crit_boost) # Bonus crit rate from TP scaling
        crit_rate += crit_bonus
        crit_rate += get_dex_crit(player_dex, enemy_agi) # Bonus crit rate from the player"s DEX stat vs enemy AGI stat
        ftp = 1.0
        ftp_rep = True
        wsc = 0.5*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 5
    elif ws_name == "Calamity":
        base_ftp = [2.5, 6.5, 10.375] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc = 0.5*(player_str + player_vit) + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 1
    elif ws_name == "Mistral Axe":
        base_ftp = [4.0, 10.5, 13.625]
        ftp      = np.interp(tp, base_tp, base_ftp)
        ftp_rep  = False
        wsc      = 0.5*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits    = 1
    elif ws_name == "Decimation":
        acc_boost = [0, 20, 40] # Made these numbers up since it isnt known. Copied Blade: Ku, which i also made up
        acc_bonus = np.interp(tp, base_tp, acc_boost)
        ftp = 1.75
        ftp_rep = True
        wsc = 0.5*player_str + dStat[1]*gearset.playerstats[dStat[0]] # Assuming 5/5 Blade: Shun merits. Add clickable drop-down menu to adjust merits later.
        nhits = 3
    elif ws_name == "Bora Axe":
        acc_boost = [0, 20, 40] # Made these numbers up since it isnt known.
        acc_bonus = np.interp(tp, base_tp, acc_boost)
        ftp  = 4.5
        ftp_rep = False
        wsc = 1.0*player_dex + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1
    elif ws_name == "Ruinator":
        acc_boost = [0, 20, 40] # Made these numbers up since it isnt known. Copied Blade: Ku, which i also made up
        acc_bonus = np.interp(tp, base_tp, acc_boost)
        ftp  = 1.08
        ws_atk_bonus = 0.1
        special_set = set_gear(buffs, equipment, main_job, sub_job, ws_atk_bonus, job_abilities=job_abilities) # The attack bonus from Blade: Shun is applied before buffs. I needed to recalculate player attack with a "special set" to deal with this.
        player_attack1 = special_set.playerstats["Attack1"] # Redefine the player"s attack1 and attack2 used in the weapon skill based on the FTP scaling value
        player_attack2 = special_set.playerstats["Attack2"] # These boosted attack1 and attack2 values do not show up in the player"s stats shown in the final plot.
        ftp = 1.0
        ftp_rep = True
        wsc = 0.85*player_str + dStat[1]*gearset.playerstats[dStat[0]] # Assuming 5/5 Blade: Shun merits. Add clickable drop-down menu to adjust merits later.
        nhits = 4
    elif ws_name == "Onslaught":
        ftp  = 2.75
        ftp_rep = False
        wsc = 0.8*player_dex + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1
    elif ws_name == "Cloudsplitter":
        base_ftp = [3.75, 6.69921875, 8.5 ] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc = 0.4*(player_str + player_mnd) + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 1
        magical = True
        element = "Thunder"
        ws_dINT = 0
    elif ws_name == "Primal Rend":
        base_ftp = [3.0625,5.8359375,7.5625 ] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc = 0.6*player_chr + 0.3*player_dex + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 1
        magical = True
        element = "Light"
        ws_dINT = 651 if (player_chr - enemy_int)*1.5 > 651 else (player_chr - enemy_int)*1.5


    # Archery weapon skills
    elif ws_name == "Flaming Arrow":
        hybrid    = True
        base_ftp  = [0.5, 1.55, 2.1]
        ftp_hybrid = np.interp(tp, base_tp, base_ftp)
        ftp       = 1.0
        ftp_rep   = False
        wsc       = 0.5*player_agi + 0.2*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits     = 1
        element   = "Fire"
    elif ws_name == "Piercing Arrow":
        ftp  = 1.0
        ftp_rep = True
        wsc = 0.5*player_agi + 0.2*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1
        def_multiplier = [1.0, 0.65, 0.50]
        enemy_defense *= np.interp(tp, base_tp, def_multiplier) # TODO: This should be additive with Dia, Frailty, etc? I think it's fine as is.
    elif ws_name == "Sidewinder":
        acc_boost = [-50, -20, 0] # Made these numbers up since it isnt known.
        acc_bonus = np.interp(tp, base_tp, acc_boost)
        ftp  = 5.0
        ftp_rep = False
        wsc = 0.5*player_agi + 0.2*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1
    elif ws_name == "Blast Arrow":
        acc_boost = [0, 20, 40] # Made these numbers up since it isnt known.
        acc_bonus = np.interp(tp, base_tp, acc_boost)
        ftp  = 2.0
        ftp_rep = False
        wsc = 0.5*player_agi + 0.2*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1
    elif ws_name == "Empyreal Arrow":
        ws_atk_bonus = 1.0 # +100% attack, or a 2.0 multiplier. Gets added to percent_attack_buff in set_stats.py
        special_set = set_gear(buffs, equipment, main_job, sub_job, ws_atk_bonus, job_abilities=job_abilities)
        player_attack1 = special_set.playerstats["Attack1"] # Redefine the player"s attack1 and attack2 used in the weapon skill based on the FTP scaling value
        player_attack2 = special_set.playerstats["Attack2"] # These boosted attack1 and attack2 values do not show up in the player"s stats shown in the final plot.
        player_rangedattack = special_set.playerstats["Ranged Attack"] # These boosted attack1 and attack2 values do not show up in the player"s stats shown in the final plot.
        base_ftp = [1.5, 2.5, 5.0] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False
        wsc = 0.5*player_agi + 0.2*player_str + dStat[1]*gearset.playerstats[dStat[0]] # Assuming 5/5 Blade: Shun merits. Add clickable drop-down menu to adjust merits later.
        nhits = 1
    elif ws_name == "Refulgent Arrow":
        base_ftp = [3.0, 4.25, 7.0]
        ftp      = np.interp(tp, base_tp, base_ftp)
        ftp_rep = False
        wsc      = 0.6*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits    = 1 # BG states this is a 1-hit attack. Could use some testing to confirm since the description on BG says "twofold attack"
    elif ws_name == "Apex Arrow":
        ftp  = 3.0
        ftp_rep = False
        wsc = 0.85*player_agi + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1
        base_enemy_def_scaling = [0.15, 0.30, 0.45] # First number is known. I made up the other two
        enemy_def_scaling = np.interp(tp, base_tp, base_enemy_def_scaling)
        enemy_defense *= (1-enemy_def_scaling)
    elif ws_name == "Namas Arrow":
        ftp  = 2.75
        ftp_rep = False
        wsc = 0.4*(player_str + player_agi) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1
    elif ws_name == "Jishnu's Radiance":
        crit_ws = True
        crit_rate += gearset.playerstats["Crit Rate"]/100
        crit_boost = [0.15, 0.2, 0.25] # No values are known for Jishu's crits. I copied these values from Blade: Hi
        crit_bonus = np.interp(tp, base_tp, crit_boost) # Bonus crit rate from TP scaling
        crit_rate += crit_bonus
        crit_rate += ((player_agi - enemy_agi)/10)/100 # Ranged attacks gain crit rate from AGI, not DEX
        ftp = 1.75
        ftp_rep = True
        wsc = 0.8*player_dex + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 3


    # Marksmanship weapon skills
    elif ws_name == "Hot Shot":
        hybrid    = True
        base_ftp  = [0.5, 1.55, 2.1]
        ftp_hybrid = np.interp(tp, base_tp, base_ftp)
        ftp       = 1.0
        ftp_rep   = False
        wsc       = 0.7*player_agi + dStat[1]*gearset.playerstats[dStat[0]]
        nhits     = 1
        element   = "Fire"
    elif ws_name == "Split Shot":
        ftp  = 1.0
        ftp_rep = True
        wsc = 0.7*player_agi + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1
        def_multiplier = [1.0, 0.65, 0.50]
        enemy_defense *= np.interp(tp, base_tp, def_multiplier) # TODO: This should be additive with Dia, Frailty, etc? I think it's fine as is.
    elif ws_name == "Slug Shot":
        acc_boost = [-50, -20, 0] # Made these numbers up since it isnt known.
        acc_bonus = np.interp(tp, base_tp, acc_boost)
        ftp  = 5.0
        ftp_rep = False
        wsc = 0.7*player_agi + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1
    elif ws_name == "Blast Shot":
        acc_boost = [0, 20, 40] # Made these numbers up since it isnt known.
        acc_bonus = np.interp(tp, base_tp, acc_boost)
        ftp  = 2.0
        ftp_rep = False
        wsc = 0.7*player_agi + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1
    elif ws_name == "Detonator":
        ws_atk_bonus = 1.0 # +100% attack, or a 2.0 multiplier. Gets added to percent_attack_buff in set_stats.py
        special_set = set_gear(buffs, equipment, main_job, sub_job, ws_atk_bonus, job_abilities=job_abilities)
        player_attack1 = special_set.playerstats["Attack1"] # Redefine the player"s attack1 and attack2 used in the weapon skill based on the FTP scaling value
        player_attack2 = special_set.playerstats["Attack2"] # These boosted attack1 and attack2 values do not show up in the player"s stats shown in the final plot.
        player_rangedattack = special_set.playerstats["Ranged Attack"] # These boosted attack1 and attack2 values do not show up in the player"s stats shown in the final plot.
        base_ftp = [1.5, 2.5, 5.0] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False
        wsc = 0.7*player_agi + dStat[1]*gearset.playerstats[dStat[0]] # Assuming 5/5 Blade: Shun merits. Add clickable drop-down menu to adjust merits later.
        nhits = 1
    elif ws_name == "Last Stand":
        base_ftp  = [2.0, 3.0, 4.0]
        ftp = np.interp(tp, base_tp, base_ftp)
        ftp_rep   = True
        wsc       = 0.85*player_agi + dStat[1]*gearset.playerstats[dStat[0]]
        nhits     = 2
    elif ws_name == "Coronach":
        ftp  = 3.0
        ftp_rep = False
        wsc = 0.4*(player_dex + player_agi) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1
    elif ws_name == "Wildfire":
        ftp = 5.5
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc = 0.6*player_agi + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 1
        magical = True
        element = "Fire"
        ws_dINT = 1276 if (player_agi - enemy_int)*2 > 1276 else (player_agi - enemy_int)*2 
    elif ws_name == "Trueflight":
        base_ftp = [3.890625,6.4921875,9.671875] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc = 1.0*player_agi + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 1
        magical = True
        element = "Light"
        ws_dINT = (player_agi - enemy_int)*2 # No known cap.
    elif ws_name == "Leaden Salute":
        base_ftp = [4.0,6.7,10.0] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc = 1.0*player_agi + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 1
        magical = True
        element = "Dark"
        ws_dINT = (player_agi - enemy_int)*2 # No known cap.


    # Staff weapon skills
    elif ws_name == "Heavy Swing":
        base_ftp = [1.0, 1.25, 2.25] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc = 1.0*player_str + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 1
    elif ws_name == "Rock Crusher":
        base_ftp = [1.0, 2.0, 2.5] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc = 0.4*(player_str + player_int) + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 1
        magical = True
        element = "Earth"
        ws_dINT = 32 if (player_int - enemy_int)/2 + 8 > 32 else (player_int - enemy_int)/2 + 8
    elif ws_name == "Earth Crusher":
        base_ftp = [1.0, 2.3125, 3.625] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc = 0.4*(player_str + player_int) + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 1
        magical = True
        element = "Earth"
        ws_dINT = 32 if (player_int - enemy_int)/2 + 8 > 32 else (player_int - enemy_int)/2 + 8
    elif ws_name == "Starburst":
        base_ftp = [1.0, 2.0, 2.5] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc = 0.4*(player_str + player_mnd) + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 1
        magical = True
        element = "Light"
        ws_dINT = 32 if (player_int - enemy_int)/2 + 8 > 32 else (player_int - enemy_int)/2 + 8
    elif ws_name == "Sunburst":
        base_ftp = [1.0, 2.5, 4.0] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc = 0.4*(player_str + player_mnd) + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 1
        magical = True
        element = "Light"
        ws_dINT = 32 if (player_int - enemy_int)/2 + 8 > 32 else (player_int - enemy_int)/2 + 8
    elif ws_name == "Full Swing":
        base_ftp = [1.0, 3.0, 5.0]
        ftp = np.interp(tp, base_tp, base_ftp)
        ftp_rep = False
        wsc = 0.5*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1
    elif ws_name == "Retribution":
        base_ftp = [2.0,2.5,3.0]
        ftp = np.interp(tp, base_tp, base_ftp)
        ftp_rep = False
        ws_atk_bonus = 0.5
        special_set = set_gear(buffs, equipment, main_job, sub_job, ws_atk_bonus, job_abilities=job_abilities) # The attack bonus from Blade: Shun is applied before buffs. I needed to recalculate player attack with a "special set" to deal with this.
        player_attack1 = special_set.playerstats["Attack1"] # Redefine the player"s attack1 and attack2 used in the weapon skill based on the FTP scaling value
        player_attack2 = special_set.playerstats["Attack2"] # These boosted attack1 and attack2 values do not show up in the player"s stats shown in the final plot.
        wsc = 0.5*player_mnd + 0.3*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1
    elif ws_name == "Cataclysm":
        base_ftp = [2.75, 4.0, 5.0] # Base TP bonuses for 1k, 2k, 3k TP
        ftp = np.interp(tp, base_tp, base_ftp) # Effective TP at WS use
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc = 0.3*(player_str + player_int) + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 1
        magical = True
        element = "Dark"
        ws_dINT = 32 if (player_int - enemy_int)/2 + 8 > 32 else (player_int - enemy_int)/2 + 8
    elif ws_name == "Shattersoul":
        ftp = 1.375
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc = 0.85*player_int + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 3
    elif ws_name == "Vidohunir":
        ftp = 1.75
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc = 0.8*player_int + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 1
        magical = True
        element = "Dark"
        ws_dINT = (player_int - enemy_int)*2 # No known cap
    elif ws_name == "Omniscience":
        ftp = 2.0
        ftp_rep = False
        wsc = 0.8*player_mnd + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 1
        magical = True
        element = "Dark"
        ws_dINT = (player_mnd - enemy_mnd)*2 # No known cap
    elif ws_name == "Gate of Tartarus":
        ftp = 3.0
        ftp_rep = False # Does this WS replicate FTP across all hits?
        wsc = 0.8*player_int + dStat[1]*gearset.playerstats[dStat[0]] # Stat modifiers, including things like Utu Grip if applicable.
        nhits = 1


    # Hand-to-Hand weapon skills
    # Notice that each weapon skill has "-1" nhits.
    # This is to allow us to fit in an "off-hand" attack to get full TP, as observed in game.
    # Technically, the off-hand attack does not get any MA procs, but it does get full TP.
    # You could instead think of this as H2H is dual-wielding, with full TP and MA procs for first main+sub hits, but the sub-hit uses the same stats as the main hit since it's the same weapon.
    # Or you could say the first two main-hits get full TP, and there are no sub hits.
    # I treat it as dual-wield so the empyrean/mythic Aftermaths are treated properly in the code and so it's easy to calculate TP return from WSs
    elif ws_name == "Combo":
        base_ftp = [1.0, 2.4, 3.4]
        ftp      = np.interp(tp, base_tp, base_ftp)
        ftp_rep  = True
        wsc      = 0.3*(player_str + player_dex) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits    = 3-1
    elif ws_name == "One Inch Punch":
        ftp  = 1.0
        ftp_rep = True
        wsc = 1.0*player_vit + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 2-1
        def_multiplier = [1.0, 0.75, 0.50]
        enemy_defense *= np.interp(tp, base_tp, def_multiplier) # TODO: This should be additive with Dia, Frailty, etc? I think it's fine as is.
    elif ws_name == "Raging Fists":
        base_ftp = [1.0, 2.1875, 3.75]
        ftp      = np.interp(tp, base_tp, base_ftp)
        ftp_rep  = True
        wsc      = 0.3*(player_str + player_dex) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits    = 5-1
    elif ws_name == "Spinning Attack":
        ftp  = 1.0
        ftp_rep = True
        wsc = 1.0*player_str + dStat[1]*gearset.playerstats[dStat[0]] # Assuming 5/5 Blade: Shun merits. Add clickable drop-down menu to adjust merits later.
        nhits = 2-1
    elif ws_name == "Howling Fist":
        base_ftp = [2.05, 3.55, 5.75]
        ftp      = np.interp(tp, base_tp, base_ftp)
        ftp_rep  = True
        wsc      = 0.5*player_vit + 0.2*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits    = 2-1
        ws_atk_bonus = 0.5
        special_set = set_gear(buffs, equipment, main_job, sub_job, ws_atk_bonus, job_abilities=job_abilities)
        player_attack1 = special_set.playerstats["Attack1"]
        player_attack2 = special_set.playerstats["Attack2"]
    elif ws_name == "Dragon Kick":
        # This is a kick weaponskill that may benefit from Footwork. We re-calculate player attack if footwork is up to deal with Empy+3 feet: Footwork+16%
        base_ftp = [1.7, 3.0, 5.0]
        ftp      = np.interp(tp, base_tp, base_ftp)
        ftp_rep  = True
        wsc      = 0.5*(player_vit + player_str) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits    = 2-1
        special_set = set_gear(buffs, equipment, main_job, sub_job, (0.16+100/1024)*kick_ws_footwork, job_abilities=job_abilities) # 100/1024 base footwork bonus plus 16% from empy+3 feet
        player_attack1 = special_set.playerstats["Attack1"]
        player_attack2 = special_set.playerstats["Attack2"]
    elif ws_name == "Asuran Fists":
        acc_boost = [0, 20, 40] # Made these numbers up since it isnt known. Copied Blade: Ku, which i also made up
        acc_bonus = np.interp(tp, base_tp, acc_boost)
        ftp       = 1.25
        ftp_rep   = True
        wsc       = 0.15*(player_vit + player_str) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits     = 8-1
    elif ws_name == "Tornado Kick":
        # This is a kick weaponskill that may benefit from Footwork. We re-calculate player attack if footwork is up to deal with Empy+3 feet: Footwork+16%
        base_ftp = [1.7, 2.8, 4.5]
        ftp      = np.interp(tp, base_tp, base_ftp)
        ftp_rep  = True
        wsc      = 0.4*(player_vit + player_str) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits    = 3-1
        special_set = set_gear(buffs, equipment, main_job, sub_job, (0.16+100/1024)*kick_ws_footwork, job_abilities=job_abilities) # 100/1024 base footwork bonus plus 16% from empy+3 feet
        player_attack1 = special_set.playerstats["Attack1"]
        player_attack2 = special_set.playerstats["Attack2"]
    elif ws_name == "Shijin Spiral":
        acc_boost = [0, 20, 40] # Made these numbers up since it isnt known. Copied Blade: Ku, which i also made up
        acc_bonus = np.interp(tp, base_tp, acc_boost)
        ftp  = 1.375
        ftp_rep = True
        wsc = 0.85*player_dex + dStat[1]*gearset.playerstats[dStat[0]] # Assuming 5/5 Blade: Shun merits. Add clickable drop-down menu to adjust merits later.
        nhits = 5-1
        ws_atk_bonus = 0.05
        special_set = set_gear(buffs, equipment, main_job, sub_job, ws_atk_bonus, job_abilities=job_abilities)
        player_attack1 = special_set.playerstats["Attack1"]
        player_attack2 = special_set.playerstats["Attack2"]
    elif ws_name == "Final Heaven":
        ftp  = 3.0
        ftp_rep = False
        wsc = 0.8*player_vit
        nhits = 2-1
    elif ws_name == "Victory Smite":
        crit_ws = True
        crit_rate += gearset.playerstats["Crit Rate"]/100 # Blade: Hi can crit, so define crit rate now
        crit_boost = [0.10, 0.25, 0.45]
        crit_bonus = np.interp(tp, base_tp, crit_boost) # Bonus crit rate from TP scaling
        crit_rate += crit_bonus
        crit_rate += get_dex_crit(player_dex, enemy_agi) # Bonus crit rate from the player"s DEX stat vs enemy AGI stat
        ftp = 1.5
        ftp_rep = True
        wsc = 0.8*player_str + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 4-1
    elif ws_name == "Ascetic's Fury":
        crit_ws = True
        crit_rate += gearset.playerstats["Crit Rate"]/100
        crit_boost = [0.20, 0.30, 0.50]
        crit_bonus = np.interp(tp, base_tp, crit_boost) # Bonus crit rate from TP scaling
        crit_rate += crit_bonus
        crit_rate += get_dex_crit(player_dex, enemy_agi) # Bonus crit rate from the player"s DEX stat vs enemy AGI stat
        ftp = 1.0
        ftp_rep = True
        wsc = 0.5*(player_str + player_vit) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 2-1
        ws_atk_bonus = 1.0
        special_set = set_gear(buffs, equipment, main_job, sub_job, ws_atk_bonus, job_abilities=job_abilities)
        player_attack1 = special_set.playerstats["Attack1"]
        player_attack2 = special_set.playerstats["Attack2"]
    elif ws_name == "Stringing Pummel":
        crit_ws = True
        crit_rate += gearset.playerstats["Crit Rate"]/100 
        crit_boost = [0.15, 0.30, 0.45] # Upper limits. Middle value was made up to force linear scaling
        crit_bonus = np.interp(tp, base_tp, crit_boost) # Bonus crit rate from TP scaling
        crit_rate += crit_bonus
        crit_rate += get_dex_crit(player_dex, enemy_agi) # Bonus crit rate from the player"s DEX stat vs enemy AGI stat
        ftp = 1.0
        ftp_rep = True
        wsc = 0.32*(player_str + player_vit) + dStat[1]*gearset.playerstats[dStat[0]]
        nhits = 6-1


    if main_wpn_name == 'Shining One' and not phys_rng_ws:
        # # Shining One allows all weapon skills to crit. Seems pretty OP, but here we are...
        # https://www.bg-wiki.com/ffxi/Shining_One

        if not crit_ws:
            # Add gear and dDEX crit rate if the selected WS did not already do it.
            crit_rate += gearset.playerstats['Crit Rate']/100
            crit_rate += get_dex_crit(gearset.playerstats['DEX'], enemy_agi)

        crit_boost = [0.05, 0.10, 0.15] # Crit rate bonuses based on TP for wielding Shining One
        crit_bonus = np.interp(tp, [1000,2000,3000], crit_boost)
        crit_rate += crit_bonus




    scaling = {"hybrid":hybrid,
               "magical":magical,
               "ws_dINT":ws_dINT,
               "wsc":wsc,
               "nhits":nhits,
               "element":element,
               "ftp":ftp,
               "ftp_rep":ftp_rep,
               "player_attack1":player_attack1,
               "player_attack2":player_attack2,
               "player_rangedattack":player_rangedattack,
               "enemy_def":enemy_defense,
               "crit_rate":crit_rate,
               "ftp_hybrid":ftp_hybrid,
               "acc_bonus":acc_bonus}
    return(scaling)
