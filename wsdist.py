#
# Created by Kastra on Asura.
# Feel free to /tell in game or send a PM on FFXIAH you have questions, comments, or suggestions.
#
# Version date: 2022 December 09
#
# This is the main code that gets run. It reads in the GUI window for user-defined parameters and runs the simulations to find the best gear set by calling the functions within this code and within other codes.
#
from numba import njit
import numpy as np

from get_ma_rate import get_ma_rate3
from get_fstr import *
from get_dex_crit import *
from get_phys_damage import *
from get_hitrate import *
from weaponskill_scaling import *
from check_weaponskill_bonus import *
from multiattack_check import *
from pdif import *
from nuking import *

from get_tp import get_tp
from fancy_plot import *

import random

class TP_Error(Exception):
    pass

def weaponskill(main_job, sub_job, ws_name, enemy, gearset, tp, buffs, equipment, final=False, nuke=False, spell=False, burst=False, futae=False, ebullience=False):
    #
    # Use the player and enemy stats to calculate weapon skill damage.
    # This function works, but needs to be cleaned up. There is too much going on within it.
    # It would be easier to rewrite the entire code and simply borrow from what I already have.
    #
    if not nuke:
        if tp < 1000:
            print(f'TP must be greater than 1000 to use a Weapon skill; TP = {tp}')
            raise TP_Error

    # Save the main and sub weapon names for later.
    # Used to check if giving weapon skill damage bonuses on things like Gokotai (if "Gokotai" in main_wpn_name)
    main_wpn_name = gearset.equipment()['main'] # TODO: Why is this one using the .equipment() method, but the other two are using .gear[]
    sub_wpn_name = gearset.gear['sub']['Name2']
    rng_wpn_name = gearset.gear['ranged']['Name2']

    sub_type = gearset.gear['sub'].get('Type', 'None') # Check if the item equipped in the sub slot is a weapon or a grip or shield. If the item doesn't have a "Type" Key then return "None". All items SHOULD have a type.
    dual_wield = sub_type == 'Weapon'

    main_type_skill = gearset.gear['main']['Skill Type']
    sub_type_skill = gearset.gear['sub'].get('Skill Type', 'None') # If the sub item doesn't have a skill type (Katana/Dagger/Scythe, etc) then return "None"
    rng_type_skill = gearset.gear['ranged'].get('Skill Type', 'None') # If the sub item doesn't have a skill type (Katana/Dagger/Scythe, etc) then return "None"

    tp += gearset.playerstats['TP Bonus'] # Add TP bonus
    tp = 3000 if tp > 3000 else int(tp) # Cap TP at 3000

    main_dmg = gearset.playerstats['DMG1']
    sub_dmg  = gearset.playerstats['DMG2']
    rng_dmg  = gearset.playerstats['Ranged DMG']

    fotia_ftp = gearset.playerstats['ftp']
    pdl_gear  = gearset.playerstats['PDL']/100.
    pdl_trait = gearset.playerstats['PDL Trait']/100.

    player_str = gearset.playerstats['STR']
    player_dex = gearset.playerstats['DEX']
    player_vit = gearset.playerstats['VIT']
    player_agi = gearset.playerstats['AGI']
    player_int = gearset.playerstats['INT']
    player_mnd = gearset.playerstats['MND']
    player_chr = gearset.playerstats['CHR']

    player_attack1 = gearset.playerstats['Attack1']
    player_attack2 = gearset.playerstats['Attack2']
    player_attack2 = 0 if not dual_wield else player_attack2
    player_rangedattack = gearset.playerstats['Ranged Attack']

    player_accuracy1 = gearset.playerstats['Accuracy1']
    player_accuracy2 = gearset.playerstats['Accuracy2'] if dual_wield else 0
    player_rangedaccuracy = gearset.playerstats['Ranged Accuracy']

    delay1 = gearset.playerstats['Delay1'] # Main-hand delay.
    delay2 = gearset.playerstats['Delay2'] if dual_wield else delay1 # Off-hand delay if dual wielding
    dw = gearset.playerstats['Dual Wield']/100 if dual_wield else 0
    mdelay = (delay1+delay2)/2.*(1.-dw) if dual_wield else delay1 # Modified delay based on weapon delays and dual wield

    wsd = gearset.playerstats['Weaponskill Damage']/100. # Applies to first hit only
    ws_acc = gearset.gearstats['Weaponskill Accuracy']
    ws_bonus = gearset.playerstats['Weaponskill Bonus']/100. # Bonus damage multiplier to every hit on the WS. Stuff like Gokotai, Naegling, hidden Relic/Mythic WS damage, REMA augments. TODO: DRG is different term

    crit_dmg = gearset.playerstats['Crit Damage']/100.
    crit_rate = 0 # WSs can't crit unless they explicitly say they can (Blade: Hi, Evisceration, CDC, etc). Crit rate is read in properly only for those weapon skills (see below) and the special case with Shining One

    qa = gearset.playerstats['QA']/100
    ta = gearset.playerstats['TA']/100
    da = gearset.playerstats['DA']/100
    oa3 = 0 # Only applies with Mythic Aftermath on WSs and only on the hand holding the weapon. Same deal as crit rate. OA3 and OA2 are read in properly if using Nagi main hand for AM3. See below.
    oa2 = 0 # Only applies with Mythic Aftermath on WSs and only on the hand holding the weapon. Same deal as crit rate. OA3 and OA2 are read in properly if using Nagi main hand for AM3. See below.

    stp = gearset.playerstats['Store TP']/100

    player_mab = gearset.playerstats['Magic Attack']
    player_magic_damage = gearset.playerstats['Magic Damage']
    magic_crit_rate2 = gearset.playerstats["Magic Crit Rate II"]/100 # Magic Crit Rate II is apparently +25% damage x% of the time.
    
    enemy_int = enemy["INT"]
    enemy_agi = enemy["AGI"]
    enemy_vit = enemy["VIT"]
    enemy_eva = enemy["Evasion"]
    enemy_def = enemy["Defense"]
    enemy_mdb = enemy["Magic Defense"]
    enemy_meva = enemy["Magic Evasion"]

    magic_accuracy_skill = gearset.playerstats["Magic Accuracy Skill"] # Magic Accuracy from Magic Accuracy Skill. Currently includes off-hand weapon stats.
    magic_accuracy_skill -= gearset.gear["sub"].get("Magic Accuracy Skill",0) # Subtract off the Magic Accuracy Skill from the off-hand slot, since it does not contribute to spell accuracy or main-hand WS damage
    dstat_macc = get_dstat_macc(player_int, enemy_int) # Get magic accuracy from dINT. I assume this applies to magical weapon skills too
    magic_accuracy = gearset.playerstats["Magic Accuracy"] # Read base Magic Accuracy from playerstats, including traits and gear with "Magic Accuracy"
    magic_accuracy += magic_accuracy_skill # Add on the "Magic Accuracy Skill" stat
    magic_accuracy += dstat_macc # Add on magic accuracy from dINT

    ninjutsu_damage = gearset.playerstats['Ninjutsu Damage'] if main_job.lower() == "nin" else 0
     
    dStat = ['STR', 0] # Part of the fix for Crepuscular Knife's CHR bonus. Needed to first assign a base dStat bonus. In this case I just used STR with 0 bonus to apply to all WSs, and Crepsecular just changes this to ['CHR', 0.03]. Utu Grip changes this to ['DEX', 0.10]
    if sub_wpn_name == "Crepuscular Knife":
        dStat = ['CHR', 3]
    elif sub_wpn_name == "Utu Grip":
        dStat = ['DEX', 10]
    dStat[1] /= 100.

    # Nuking stuff. Move this to a separate Nuke() function for the Nuke tab to call later. TODO
    if nuke:
        # Define Ninjutsu specifics: element, tier, bonus damage
        if ": Ichi" in spell or ": Ni" in spell or ": San" in spell:
            # Add Ninjutsu Magic Attack to Ninjutsu nukes
            player_mab += gearset.playerstats['Ninjutsu Magic Attack']
            
            spells = {
                    "Katon": "Fire",
                    "Suiton": "Water",
                    "Raiton": "Thunder",
                    "Doton": "Earth",
                    "Huton": "Wind",
                    "Hyoton": "Ice"
                    }

            element = spells[spell.split(":")[0]].lower()
            tier = spell.split()[-1]

            damage = nuking("Ninjutsu", tier, element, gearset, player_int, player_mab, player_magic_damage, enemy_int, enemy_mdb, enemy_meva, ninjutsu_damage, futae, burst, ebullience)

        else:
            # If not Ninjutsu, then assume Elemental Magic
            spells = {
                    "Stone": "Earth",
                    "Water": "Water",
                    "Aero": "Wind",
                    "Fire": "Fire",
                    "Blizzard": "Ice",
                    "Thunder": "Thunder",
                    }
            jaspells = {
                    "Stoneja": "Earth",
                    "Waterja": "Water",
                    "Aeroja": "Wind",
                    "Firaja": "Fire",
                    "Blizzaja": "Ice",
                    "Thundaja": "Thunder",
                    }
            helixspells = {
                    "Geohelix II": "Earth",
                    "Hydrohelix II": "Water",
                    "Anemohelix II": "Wind",
                    "Pyrohelix II": "Fire",
                    "Cryohelix II": "Ice",
                    "Ionohelix II": "Thunder",
                    "Luminohelix II": "Light",
                    "Noctohelix II": "Dark",
            }
            if spell[-2:] == "ja":
                element = jaspells[spell].lower()
                tier = "ja"
            elif "helix" in spell.lower():
                element = helixspells[spell].lower()
                tier = "helix"
            elif len(spell.split()) == 1:
                element = spells[spell.split()[0]].lower()
                tier = "I"
            elif len(spell.split()) == 2:
                element = spells[spell.split()[0]].lower()
                tier = spell.split()[-1]

            damage = nuking("Elemental Magic", tier, element, gearset, player_int, player_mab, player_magic_damage, enemy_int, enemy_mdb, enemy_meva, 0, futae, burst, ebullience)

        return(damage,0) # If nuke, then don't bother running the rest of the code, simply return the magic damage (and 0 TP return) and continue with the testing.


    # Check weapon + weapon skill synergy for things like bonus weapon skill damage. (and mythic AM3)
    # See "check_weaponskill_bonuses.py"
    bonuses = check_weaponskill_bonus(main_wpn_name, ws_name, gearset, tp, enemy_agi)
    ws_bonus += bonuses['ws_bonus']
    crit_rate += bonuses['crit_rate']
    oa3 += bonuses['oa3'] ; oa2 += bonuses['oa2']

    # Obtain weapon skill TP scaling. "Damage varies with TP"
    # See "weaponskill_scaling.py"
    scaling = weaponskill_scaling(main_job, sub_job, ws_name, tp, gearset, equipment, buffs, dStat, dual_wield, enemy_def, enemy_agi, enemy_int)
    wsc = scaling['wsc']
    ftp = scaling['ftp']
    ftp_rep = scaling['ftp_rep']
    nhits = scaling['nhits']
    element = scaling['element']
    hybrid = scaling['hybrid']
    magical = scaling['magical']
    player_attack1 = scaling['player_attack1'] # Some weaponskills enhance/reduce player attack or enemy defense. TODO: add ranged attack (last stand, empyreal arrow)
    player_attack2 = scaling['player_attack2']
    enemy_def = scaling['enemy_def']
    crit_rate = scaling['crit_rate']
    ftp_hybrid = scaling['ftp_hybrid']
    ws_dINT = scaling["ws_dINT"] # dINT used for magical weapon skills. Some WSs have maximum values, some don't even use a dSTAT.

    # Setup replicating ftp for specific WSs.
    ftp += fotia_ftp
    if hybrid:
        ftp_hybrid += fotia_ftp
    ftp2 = 1.0 if not ftp_rep else ftp # FTP for additional and off-hand hits.

    # Define elemental damage bonuses now that we know what element your hybrid/magical weapon skill is.
    if hybrid or magical:
        
        element_magic_attack_bonus = 1 + (gearset.playerstats.get(element + ' Elemental Bonus', 0) + gearset.playerstats['Elemental Bonus'])/100 # Archon Ring, Pixie Hairpin +1, Orpheus

    # fSTR calculation for main-hand and off-hand
    fstr_main = get_fstr(main_dmg, player_str, enemy_vit)
    fstr_sub  = get_fstr(sub_dmg, player_str, enemy_vit)

    # Start the damage calculations.
    damage = 0

    if magical:
        # Magical weapon skills have no physical portion, so they use a different, simpler, damage algorithm.
        # In this case, we will not make a plot since the damage is always the same.
        # This is why we exclude "magical" weaponskills from the rest of this function.
        #
        # Assuming Magical weapon skills can not multi-attack. TODO: test this in game using heishi + Lv1 dagger. Does damage change when unequipping dagger? (the offhand hit might not exist either)
        weapon_level = 119
        crocea = True if gearset.gear["main"]["Name2"] == "Crocea Mors R25C" else False
        magical_damage = int(((152 + int((weapon_level-99)*2.45)+wsc)*ftp)*(1+crocea) + ws_dINT + player_magic_damage)

        magic_hit_rate = get_magic_hit_rate(magic_accuracy, enemy_meva) if enemy_meva > 0 else 1.0
        resist_state = get_resist_state_average(magic_hit_rate)

        affinity = 1 + 0.05*gearset.playerstats[f'{element} Affinity'] + 0.05*(gearset.playerstats[f'{element} Affinity']>0) # Affinity Bonus. Only really applies to Magian Trial staves. Archon Ring is different.
        dayweather = 1.0 # 0.65, 0.8, 0.9, 1.0, 1.1, 1.2, 1.35. Assume no day/weather bonus/penalty.
        magic_attack_ratio = (100 + player_mab) / (100 + enemy_mdb)
        enemy_mdt = 1.0 # Usually 1.0 unless the enemy casts shell or a similar spell/ability.

        magic_multiplier = affinity*resist_state*dayweather*magic_attack_ratio*enemy_mdt*element_magic_attack_bonus
        magical_damage *= magic_multiplier
        magical_damage *= (1+wsd)*(1+ws_bonus) # TODO: *(1+ws_trait)
        magical_damage *= (1 + 0.25*magic_crit_rate2) # Magic Crit Rate II is apparently +25% damage x% of the time.

        return(magical_damage,0) # Return 0 TP for now.


    if not final: # If the best set hasn't been determined yet, then just take a simple average. No need to run a bunch of simulations unless you're making a plot.

        # Check hit rates for each hand and for each hit.
        hitrate11 = get_hitrate(player_accuracy1, ws_acc, enemy_eva, 'main',  True) # First main-hand hit.
        hitrate21 = get_hitrate(player_accuracy2, ws_acc, enemy_eva,  'sub',  True) # First off-hand hit.
        hitrate12 = get_hitrate(player_accuracy1, ws_acc, enemy_eva, 'main', False) # Additional main-hand hits. "False" to not gain the +100 accuracy.
        hitrate22 = get_hitrate(player_accuracy2, ws_acc, enemy_eva,  'sub', False) # Additional off-hand hits.
        hitrate_matrix = np.array([[hitrate11, hitrate21],[hitrate12, hitrate22]])

        # Determine the number of main- and off-hand hits that actually land. Ignore TP return here.
        main_hits, sub_hits = get_ma_rate3(nhits, qa, ta, da, oa3, oa2, sub_type, hitrate_matrix)

        # Calculate average damage dealt per hit for each hand.
        avg_pdif1 = get_avg_pdif_melee(player_attack1, main_type_skill, pdl_trait, pdl_gear, enemy_def, crit_rate) # Main-hand average PDIF
        avg_pdif2 = get_avg_pdif_melee(player_attack2, sub_type_skill, pdl_trait, pdl_gear, enemy_def, crit_rate)  # Off-hand average PDIF
        main_hit_damage =    get_avg_phys_damage(main_dmg, fstr_main, wsc, avg_pdif1, ftp,  crit_rate, crit_dmg, wsd, ws_bonus) # Calculate the physical damage dealt by the first main hit.
        sub_hit_damage =     get_avg_phys_damage( sub_dmg,  fstr_sub, wsc, avg_pdif2, ftp2, crit_rate, crit_dmg,   0, ws_bonus) # Calculate the physical damage dealt by the off-hand hits separately, no weapon skill damage provided here.
        main_hit_ma_damage = get_avg_phys_damage(main_dmg, fstr_main, wsc, avg_pdif1, ftp2, crit_rate, crit_dmg,   0, ws_bonus) # Calculate the physical damage dealt by extra main-hand hits

        phys = main_hit_damage + (main_hits-1)*main_hit_ma_damage + sub_hits*sub_hit_damage
        damage += phys

        if hybrid:
            # Calculate the magic multiplier for the magical part of Hybrid weapon skills
            # https://www.ffxiah.com/forum/topic/51313/tachi-jinpu-set/
            magic_hit_rate = get_magic_hit_rate(magic_accuracy, enemy_meva) if enemy_meva > 0 else 1.0
            resist_state = get_resist_state_average(magic_hit_rate)

            affinity = 1 + 0.05*gearset.playerstats[f'{element} Affinity'] + 0.05*(gearset.playerstats[f'{element} Affinity']>0) # Affinity Bonus. Only really applies to Magian Trial staves. Archon Ring is different.
            dayweather = 1.0 # 0.65, 0.8, 0.9, 1.0, 1.1, 1.2, 1.35. Assume no day/weather bonus/penalty.
            magic_attack_ratio = (100 + player_mab) / (100 + enemy_mdb)
            enemy_mdt = 1.0 # Usually 1.0 unless the enemy casts shell or a similar spell/ability.

            magic_multiplier = affinity*resist_state*dayweather*magic_attack_ratio*enemy_mdt*element_magic_attack_bonus
            magical_damage = (phys*ftp_hybrid + player_magic_damage)*magic_multiplier*(1+wsd)*(1+ws_bonus)

            damage += magical_damage

        return(damage, 0) # Return the average damage dealt and 0 TP return.

    # This marks the end of the damage calculation for average estimates.



    # Start the actual damage simulations now.
    # This part is run after you've already found the "best average" set, now you simply want to plot the damage distribution.
    #   If you do not care to plot the damage distribution, then it should be skipped by passing in nsim = 0  TODO
    # Alternatively, you can just manually pass in final=True to force this part to run instead of the average estimate.
    #   This is what should happen when the user inputs n_iter = 0 in the GUI. It'll skip doing iterations of averages and jump straight to the end.
    total_hits = 0 # Weapon skills cannot exceed 8 hits
    ma_count_limit = 0 # Limited to 2 MA procs per WS
    ma_tp_hits = 0 # Number of additional hits that landed and are not the first main-hand or off-hand hits. Used for TP return.
    subhit = False # The off-hand hit has not yet landed, don't give TP for it yet.
    mainhit = False # The main-hand hit has not yet landed, don't give TP for it yet.

    for n in range(nhits): # TODO: rename n to something better....   n = the current swing of your N total hits. Shun swings 5 times. I use n>1 to represent the not-first hit for TP, but this name is bad.
        # Loop nhits times, summing the damage from each hit.
        # Example: Blade: Shun is 5 hits, so loop 5 times.
        # For n == 0, the first main hit is checked, then the first sub hit is checked, then n becomes 1 and the subhits are no longer checked until we do MA procs in the next big for-loop.

        total_hits += 1 # You've started the weapon skill's first hit. Even if it misses, it counts towards the 8-hit total so increase total_hits by 1

        if total_hits > 8: # Don't bother after 8 hits
            continue

        if n > 0:
            ftp = ftp2 # After the first hit, use secondary FTP for main-hand hits. This will equal primary FTP if the WS is FTP-replicating, otherwise it's 1.0

        # Calculate hit rates for the natural main- and sub-hits (the first of each get a ~+100 Accuracy bonus).
        # Future main- and off-hand hits do not get accuracy+100 (n!=0).
        hitrate1 = get_hitrate(player_accuracy1, ws_acc, enemy_eva, 'main', n==0)
        hitrate2 = get_hitrate(player_accuracy2, ws_acc, enemy_eva,  'sub', n==0)

        # Check if your hit lands
        if np.random.uniform() < hitrate1:
            if n > 0: # If your hit landed successfully (n>0 so youre checking AFTER the first main+sub hits here), then add 1 to the number of additional hits that provide TP
                ma_tp_hits += 1
            else:
                mainhit = True # The first main hit successfully landed so it provides full TP. (n=0 is the first main hit)
            pdif1, crit = get_pdif_melee(player_attack1, main_type_skill, pdl_trait, pdl_gear, enemy_def, crit_rate) # Calculate the PDIF for this swing of the main-hand weapon. Return whether or not that hit was a crit.
            physical_damage = get_phys_damage(main_dmg, fstr_main, wsc, pdif1, ftp, crit, crit_dmg, wsd, ws_bonus, n) # Calculate the physical damage dealt by a single hit. The first hit gets WSD.
            damage += physical_damage

        # Bonus hit for dual-wielding.
        # The dual-wielding hit occurs immediately after first main-hit. This can be confirmed by watching your in-game TP return.
        if total_hits < 8 and dual_wield and n == 0: # By necessity of order-of-operations, total_hits==1 right now, so we can remove the "total_hits < 8" bit. TODO
            total_hits += 1 # You are starting to try to hit with your off-hand weapon, add one to the total hits.
            if np.random.uniform() < hitrate2:
                subhit = True # For TP return. The successful sub-hit gets full TP
                pdif2, crit = get_pdif_melee(player_attack2, sub_type_skill, pdl_trait, pdl_gear, enemy_def, crit_rate) # Calculate the pdif for this off-hand hit. Return whether or not it was a crit.
                physical_damage = get_phys_damage(sub_dmg, fstr_sub, wsc, pdif2, ftp2, crit, crit_dmg, 0, ws_bonus, 1) # Calculate its damage. Notice that subhit uses ftp2 and wsd=0.
                damage += physical_damage

        # This is the last line of the natural main/sub-hit for-loop


    # This part checks for multi-attack procs. It does so after all of the natural main-hits and the one sub-hit
    if total_hits < 8:

        # The main hand gets 1 MA check if dual-wielding, 1+0 MA checks if single-wielding and using a 1-hit weaponskill, or 1+1 MA checks if single-wielding and using a 2+ hit weapon skill
        # Single-wielding weapons (including 2-handed weapons):
        #   One natural hit (Blade: Ten, Blade: Metsu, etc):
        #     One multi-attack check total.
        #   More than one natural hit (Shun=5, Ku=5, Jin=3, etc):
        #     Two multi-attack checks total.
        # Dual-wielding weapons:
        #   Two multi-attack checks total.
        #     The main hand gets one check, the off-hand gets the other.
        #       Shun is 5+1 hits. The first main hand gets one check, the first off-hand gets the other, the remaining 4 main hand hits get nothing.
        main_ma_checks = 1 if dual_wield else 1+(nhits>1)
        # Start by checking if the main-hit multi-attacks.
        for i in range(main_ma_checks):
            hitrate1 = get_hitrate(player_accuracy1, ws_acc, enemy_eva, 'main', False)
            hitrate2 = get_hitrate(player_accuracy2, ws_acc, enemy_eva,  'sub', False)

            # Check multi-attacks in order:
            # Quad > Triple > Double > OA3 > OA2 > Single
            # Kclub is not checked here.

            if np.random.uniform() < qa and ma_count_limit < 2:
                # If you rolled lower than your quadruple attack %, then you perform a quadruple attack.
                ma_count_limit += 1 # This counts as one of your two allowed multi-attack procs, even if you can only swing once out of the whole QA proc due to the 8-hit limit
                physical_damage, ma_tp_hits, total_hits = multiattack_check(3, ma_tp_hits, total_hits, player_attack1, main_type_skill, pdl_trait, pdl_gear, enemy_def, crit_rate, main_dmg, fstr_main, wsc, ftp2, crit_dmg, ws_bonus, hitrate1)
                damage += physical_damage
            elif np.random.uniform() < ta and ma_count_limit < 2: # If you failed the quadruple attack check, then you get to try to roll lower than your triple attack value.
                ma_count_limit += 1
                physical_damage, ma_tp_hits, total_hits = multiattack_check(2, ma_tp_hits, total_hits, player_attack1, main_type_skill, pdl_trait, pdl_gear, enemy_def, crit_rate, main_dmg, fstr_main, wsc, ftp2, crit_dmg, ws_bonus, hitrate1)
                damage += physical_damage
            elif np.random.uniform() < da and ma_count_limit < 2: # If you failed the triple attack check, then you get to try a double attack roll
                ma_count_limit += 1
                physical_damage, ma_tp_hits, total_hits = multiattack_check(1, ma_tp_hits, total_hits, player_attack1, main_type_skill, pdl_trait, pdl_gear, enemy_def, crit_rate, main_dmg, fstr_main, wsc, ftp2, crit_dmg, ws_bonus, hitrate1)
                damage += physical_damage
            elif np.random.uniform() < oa3 and ma_count_limit < 2: # If you failed double attack, then you get to try OA3 roll (skipping Oa8, OA7, OA6, etc)
                ma_count_limit += 1
                physical_damage, ma_tp_hits, total_hits = multiattack_check(2, ma_tp_hits, total_hits, player_attack1, main_type_skill, pdl_trait, pdl_gear, enemy_def, crit_rate, main_dmg, fstr_main, wsc, ftp2, crit_dmg, ws_bonus, hitrate1)
                damage += physical_damage
            elif np.random.uniform() < oa2 and ma_count_limit < 2: # If you failed OA3, try OA2.
                ma_count_limit += 1
                physical_damage, ma_tp_hits, total_hits = multiattack_check(1, ma_tp_hits, total_hits, player_attack1, main_type_skill, pdl_trait, pdl_gear, enemy_def, crit_rate, main_dmg, fstr_main, wsc, ftp2, crit_dmg, ws_bonus, hitrate1)
                damage += physical_damage

        # Now check multi-attacks for the off-hand.
        # Note that this part is set up without OA3 and OA2 because the occasional attacks N times stat only applies to the weapon that has it.
        # In this case, the only weapon that I have coded with this is Nagi, which only works main hand anyway.
        # This will need to be changed if we get ilvl Magian weapons with occasionally attacks X.
        # This does not deal with "follow-up" attacks from things like Fudo Masamune (but this is where you'd throw that check in if you wanted to)
        if dual_wield: # If you have an off-hand weapon equipped, then it gets one of your two multi-attack procs. Check that multi-attack proc now.
            if np.random.uniform() < qa and ma_count_limit < 2:
                ma_count_limit += 1
                ma_damage, ma_tp_hits, total_hits = multiattack_check(3, ma_tp_hits, total_hits, player_attack2, sub_type_skill, pdl_trait, pdl_gear, enemy_def, crit_rate, sub_dmg, fstr_sub, wsc, ftp2, crit_dmg, ws_bonus, hitrate2)
                damage += ma_damage
            elif np.random.uniform() < ta and ma_count_limit < 2:
                ma_count_limit += 1
                ma_damage, ma_tp_hits, total_hits = multiattack_check(2, ma_tp_hits, total_hits, player_attack2, sub_type_skill, pdl_trait, pdl_gear, enemy_def, crit_rate, sub_dmg, fstr_sub, wsc, ftp2, crit_dmg, ws_bonus, hitrate2)
                damage += ma_damage
            elif np.random.uniform() < da and ma_count_limit < 2:
                ma_count_limit += 1
                ma_damage, ma_tp_hits, total_hits = multiattack_check(1, ma_tp_hits, total_hits, player_attack2,   sub_type_skill, pdl_trait, pdl_gear, enemy_def, crit_rate, sub_dmg, fstr_sub, wsc, ftp2, crit_dmg, ws_bonus, hitrate2)
                damage += ma_damage

    phys = damage
    # This is the last line of the physical portion.


    # If the weapon skill is labeled as a hybrid, then calculate the magic portion and add it to the total damage here.
    if hybrid:
        # Calculate the magic multiplier for the magical part of Hybrid weapon skills
        # https://www.ffxiah.com/forum/topic/51313/tachi-jinpu-set/
        magic_hit_rate = get_magic_hit_rate(magic_accuracy, enemy_meva) if enemy_meva > 0 else 1.0
        resist_state = get_resist_state_average(magic_hit_rate) # TODO: Use a randomizer instead of the average resist state for hybrid simulations.

        affinity = 1 + 0.05*gearset.playerstats[f'{element} Affinity'] + 0.05*(gearset.playerstats[f'{element} Affinity']>0)
        dayweather = 1.0
        magic_attack_ratio = (100 + player_mab) / (100 + enemy_mdb)
        enemy_mdt = 1.0
        magic_multiplier = affinity*resist_state*dayweather*magic_attack_ratio*enemy_mdt*element_magic_attack_bonus

        magical_damage = (phys*ftp_hybrid + player_magic_damage)*magic_multiplier*(1+wsd)*(1+ws_bonus)
        damage += magical_damage

    # damage = 99999 if damage > 99999 else damage  # Cap damage at 99999. This ruins the scale of the plots for high-buff situations. Better to leave damage uncapped.
    tp_returned = get_tp(mainhit+subhit, mdelay, stp) + int(10*(1+stp))*ma_tp_hits

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

def test_set(main_job, sub_job, ws_name, enemy, buffs, equipment, gearset, tp1, tp2, n_simulations, show_final_plot, final=False, nuke=False, spell=False, burst=False, futae=False, ebullience=False):
    damage = []
    tp_return = []

    if nuke:
        show_final_plot = False
    if final:
        for k in range(n_simulations):

            tp = np.random.uniform(tp1,tp2)
            values = weaponskill(main_job, sub_job, ws_name, enemy, gearset, tp, buffs, equipment, final, nuke, spell, burst, futae, ebullience) # values = [damage, TP_return]
            damage.append(values[0]) # Append the damage from each simulation to a list. Plot this list as a histogram later.
            tp_return.append(values[1])

        print()
        print()
        if nuke:
            print(f"Best '{spell}' gear with the provided buffs:\n")
        else:
            print(f"Best '{ws_name}' gear for the TP range [{tp1}, {tp2}] and the provided buffs:\n")
        for k in equipment:
            print(f"{k:>10s}  {equipment[k]['Name2']:<50s}")
        print()
        if nuke:
            print(f"{'Spell':<15s} | {'Minimum':>8s} | {'Average':>8s} | {'Median':>8s} | {'Maximum':>8s}")
            print(f"{spell:<15s} | {int(np.min(damage)):>8d} | {int(np.average(damage)):>8d} | {int(np.median(damage)):>8d} | {int(np.max(damage)):>8d}")
        else:
            print(f"{'WeaponSkill':<15s} | {'Minimum':>8s} | {'Average':>8s} | {'Median':>8s} | {'Maximum':>8s}")
            print(f"{ws_name:<15s} | {int(np.min(damage)):>8d} | {int(np.average(damage)):>8d} | {int(np.median(damage)):>8d} | {int(np.max(damage)):>8d}")

        if show_final_plot:
            plot_final(damage, gearset, tp1, tp2, ws_name)
        return()
    else:
        tp = np.average([tp1,tp2])

        damage, _ = weaponskill(main_job, sub_job, ws_name, enemy, gearset, tp, buffs, equipment, final, nuke, spell, burst, futae, ebullience)
        return(damage)



def run_weaponskill(main_job, sub_job, ws_name, mintp, maxtp, n_iter, n_simulations, check_gear, check_slots, buffs, enemy, starting_gearset, show_final_plot, nuke, spell, burst=False, futae=False, ebullience=False):
    tcount = 0 # Total number of valid sets checked. Useless, but interesting to see. A recent Blade: Ten run checked 84,392 sets
    for k in starting_gearset:
        # print(starting_gearset[k])
        if main_job.lower() not in starting_gearset[k]["Jobs"]:
            starting_gearset[k] = Empty # Unequip gear you can't wear if it's already equipped.

    # Define JSE earrings now. We'll use them later to prevent Balder's Earring+1 and a JSE+2 being equipped at the same time since we ignore right_ear requirement for testing.
    jse_ears = [k + " Earring +2" for k in ["Hattori", "Heathen's", "Lethargy", "Ebers", "Wicce", "Peltast's", "Boii", "Bhikku", "Skulkers", "Chevalier's", "Nukumi", "Fili", "Amini", "Kasuga", "Beckoner's", "Hashishin", "Chasseur's", "Karagoz", "Maculele", "Arbatel", "Azimuth", "Erilaz"]]

    if nuke:
        show_final_plot = False

    Best_Gearset =  starting_gearset.copy()
    for k in Best_Gearset:
        # Assign a Name2 to all gear to allow the later code to be cleaned up. TODO: remove this. we already assign Name2 to everything in gear.py
        name2 = Best_Gearset[k].get('Name2','None')
        if name2 == 'None':
            Best_Gearset[k].update({'Name2': Best_Gearset[k]['Name']})


    tp1 = mintp
    tp2 = maxtp
    print("---------------")
    if nuke:
        print(f"Checking:  {spell}")
    else:
        print(f"Checking:  {ws_name}  TP=[{tp1},{tp2}]")

    print("---------------")
    nconverge = 2 # Number of consecutive iterations resulting in insignificant damage improvements before code returns the best set.
                                
    # Start the code.
    converge_count = 0 # Count for convergence (number of times the change between iterations was <0.1% for example; see near the end of this code for the exact value used)
    best_damage = 0
    damage_list = np.ones(n_iter) # Nothing to do with plotting. This is for checking how the damage changed between consecutive iterations.
    for z in range(n_iter):

        if converge_count >= nconverge: # Check if converged
            print(f"No significant change after {converge_count} consecutive iterations - exiting.")
            break

        # Start testing stuff
        print(f"Current iteration: {z+1}")
        for i,a in enumerate(check_gear): # "i" is a counter (0, 1, 2, etc), "a" is a gear slot list (mains, subs, ammos, heads, necks, etc)
            for i2, a2 in enumerate(check_gear): # Swap 2 pieces at once
                for i3, a3 in enumerate(check_gear): # Swap 3 pieces at once. Generally takes too long to be worth it.

                    if i3 < i or i3 < i2 or i2 < i: # Skip repeat sets (for example: only do the upper-triangular for 2D)
                        continue

                    slot1 = check_slots[i] # Something like slot1 = "main"  # TODO: a, a2, a3 are the slots right? just remove these 3 lines and rename a to slot1, a2 to slot2, and a3 to slot3
                    slot2 = check_slots[i2]
                    slot3 = check_slots[i3]

                    fitn = 2 # Definitely don't change this to 3 now. Each set takes ages to run when this is 3 since we added so much gear.
                    if fitn == 2: # If only fitting two simultaneous slots, then skip all combinations where slot2 is not the same as slot3
                        if slot3 != slot2:
                            continue

                    elif fitn == 1: # If only fitting one slot, then skip all combinations where all three slots are not the same
                        if slot3 != slot2 or slot2 != slot1:
                            continue



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
                                        
                    # new_set is the set that's being adjusted/tested.
                    for k in new_set:
                        # Assign a Name2 to all gear to clean up the later code. We did this for "Best_Gearset" already, though...
                        # Probably best to add "Name2" to all equipment pieces in the gear.py file at the end.  TODO (to do later. Already done? Can delete all of these Name checks)
                        name2 = new_set[k].get('Name2','None')
                        if name2 == 'None':
                            new_set[k].update({'Name2': new_set[k]['Name']})


                    for j,b in enumerate(a): # "j" is a counter (0, 1, 2, etc), "b" is a piece of gear that you said you wanted to be tested in gear slot "a" (a=neck, b=(Caro_Necklace, Fotia_Gorget, Ninja_Nodowa, etc)). "b" is the NEW item to be tested against the old item
                        # if main_job.lower() not in b["Jobs"]: # Only test items your main job can equip. I add this same check later. Commenting it out here. remove it later TODO
                        #     continue
                        if b.get("Name2",'None') == 'None': # Another Name2 declaration here? That's 3 times so far?  TODO. I think I already fixed this by adding Name2 to everything at the end of gear.py
                            b.update({'Name2': b['Name']})
                        for j2,b2 in enumerate(a2): # same thing, but for the 2nd piece of gear being swapped simultaneously
                            # if main_job.lower() not in b2["Jobs"]: # Remove this check too TODO
                            #     continue
                            if b2.get("Name2",'None') == 'None':
                                b2.update({'Name2': b2['Name']})
                            for j3,b3 in enumerate(a3): # same thing, but for the 3rd piece of gear being swapped simultaneously
                                # if main_job.lower() not in b2["Jobs"]: # Remove this check too TODO
                                #     continue
                                if b3.get("Name2",'None') == 'None':
                                    b3.update({'Name2': b3['Name']})

                                # Save the names of the first of the one/two/three item swaps and the item currently equipped in its position
                                swap_item1 = b['Name2'] # New item being tested.
                                                        # Maybe rename this variable to "new_item1"  TODO
                                equipped_item1 = Best_Gearset[slot1]['Name2'] # Old item currently equipped

                                # Save the names of the second of the one/two/three swaps and the item currently equipped in its position
                                swap_item2 = b2['Name2']
                                equipped_item2 = Best_Gearset[slot2]['Name2']

                                # Save the names of the third of the one/two/three item swaps and the item currently equipped in its position
                                swap_item3 = b3['Name2']
                                equipped_item3 = Best_Gearset[slot3]['Name2']

                                # If the two swapped pieces are in the same slot, only check the damage if they're the same item (don't try to equip two different items in the same slot)
                                # This is the code block that allows changing only one item, instead of always changing two.
                                # This bit of code is also very important for preventing the third item equipped from overwriting the second item equipped later.
                                #   As long as we keep this bit of code here, then the third item WILL overwrite the second item, but they'll be the same thing anyway.
                                if i2 == i:
                                    if swap_item1 != swap_item2:
                                        continue
                                if i3 == i:
                                    if swap_item1 != swap_item3:
                                        continue
                                if i3 == i2:
                                    if swap_item3 != swap_item2:
                                        continue

                                # Don't try to equip the item if it's already equipped in the same slot.
                                # This seems bad to include, but trying to equip the same item in the same slot is the same as not changing that slot.
                                #   This means you're effectively checking one fewer slots for that round.
                                #   This situation is covered above when slot1==slot2==slot3.
                                # By skipping this version of this situation, we prevent extra tests that already happened (wasting time)
                                # if equipped_item1 == swap_item1 or equipped_item2 == swap_item2 or equipped_item3 == swap_item3:
                                #     continue

                                # Each piece of gear selected for this iteration will not be equipped.
                                # We will consider the validity of the set AFTER things have been equipped.
                                new_set[slot1]  = b  # Equip swap_item1 to slot1
                                new_set[slot2]  = b2 # Equip swap_item2 to slot2
                                new_set[slot3]  = b3 # Equip swap_item3 to slot3

                                # Do not equip two of the same item in rings, earrings, and main+sub slots.
                                # Items in these slots can be placed in either of their pair.
                                # 1-handed weapons can go in Main+Sub if dual wielding.
                                # Rings can go in either ring slot.
                                # Earrings can go in either earring slot.
                                # I use Mache Earring +1 A and B to get around this for non-rare items.
                                if new_set["ring1"]["Name2"] == new_set["ring2"]["Name2"]:
                                    continue
                                if new_set["ear1"]["Name2"] == new_set["ear2"]["Name2"]:
                                    continue
                                if new_set["main"]["Name2"] == new_set["sub"]["Name2"]:
                                    if new_set["main"]["Name2"] != "Empty": # Allow both weapons to be Empty. This is to test the bonanza bow later for fun.
                                        continue

                                # Only check gear that your main job can equip.
                                for new_slot in new_set:
                                    if main_job.lower() not in new_set[new_slot]["Jobs"]:
                                        continue


                                # Do not test 1-handed weapons with grips.
                                one_handed = ["Axe", "Club", "Dagger", "Sword", "Katana"]
                                if new_set["main"]["Skill Type"] in one_handed and new_set["sub"]["Type"] == "Grip":
                                    continue
                                # Do not allow 2-handed weapons with shields or 1-handed weapons.
                                two_handed = ["Great Sword", "Great Katana", "Great Axe", "Polearm", "Scythe", "Staff"]
                                if new_set["main"]["Skill Type"] in two_handed and (new_set["sub"]["Type"]=="Weapon" or new_set["sub"]["Type"]=="Shield"):
                                    continue
                                # Do not allow anything in the off-hand of hand-to-hand weapons.
                                if new_set["main"]["Skill Type"] == "Hand-to-Hand":
                                    if new_set["Name"] != Empty:
                                        continue

                                # Do not allow dual wielding unless NIN, DNC, THF main or subjobs.
                                if main_job not in ["NIN", "DNC", "THF"] and sub_job not in ["NIN", "DNC"]:
                                    if new_set["sub"]["Type"] == "Weapon":
                                        continue

                                # Do not equip an ammo incompatible with your ranged weapon
                                if new_set["ranged"].get("Type","None")=="Gun" and new_set["ammo"].get("Type","None") not in ["Bullet","None"]:
                                    continue

                                if new_set["ranged"].get("Type","None")=="Bow" and new_set["ammo"].get("Type","None") not in ["Arrow","None"]:
                                    continue

                                # Equipping a bullet requires a gun to be equipped. (or a crossbow with a bolt)
                                if new_set["ammo"].get("Type","None") == "Bullet" and new_set["ranged"].get("Type","None") != "Gun":
                                    continue

                                # Equipping an arrow requires a bow to be equipped.
                                if new_set["ammo"].get("Type","None") == "Arrow" and new_set["ranged"].get("Type","None") != "Bow":
                                    continue

                                # Do not equip Balder Earring +1 and the JSE +2 ears at the same time. They both only work if in the right ear.
                                if new_set["ear1"]["Name2"] in jse_ears and new_set["ear2"]["Name2"] == "Balder Earring +1":
                                    continue
                                if new_set["ear2"]["Name2"] in jse_ears and new_set["ear1"]["Name2"] == "Balder Earring +1":
                                    continue

                                # At this point, you SHOULD have a valid gear set.
                                # Now we actually test the approximate damage using averages.

                                test_Gearset = set_gear(buffs, new_set, main_job, sub_job) # This line turns that gear dictionary into a Python class, formalizing the player stats.
                                                                        # This contains the player and gear stats as well as a list of gear equipped in each slot that can be easily printed

                                # Average damage is not necessarily appropriate for multi-peaked distributions.
                                damage = int(test_set(main_job, sub_job, ws_name, enemy, buffs, new_set, test_Gearset, tp1, tp2, n_simulations, show_final_plot, False, nuke, spell , burst, futae, ebullience)) # Test the set and return its damage as a single number
                                tcount += 1
                                # if slot1==slot2:
                                #     print(slot1, swap_item1,damage)
                                # else:
                                #     print(slot1, slot2, swap_item1, swap_item2, damage)

                                # If the damage returned after swapping those 1~3 pieces is higher than the previous best, then run this next bit of code to print the swap that was performed and the change in damage observed.
                                if damage > best_damage:
                                    if (swap_item1 == swap_item2) and (swap_item1 == swap_item3):
                                        print(f"{check_slots[i]}:   {equipped_item1} ->  {swap_item1}   [{best_damage:>6.0f} -> {damage:>6.0f}]") # Print the new best damage and the new item that led to this new record

                                    elif (swap_item1 == swap_item2) and (swap_item1 != swap_item3):
                                        print(f"[{check_slots[i]} & {check_slots[i3]}]:   [{equipped_item1} & {equipped_item3}]  ->  [{swap_item1} & {swap_item3}]   [{best_damage:>6.0f} -> {damage:>6.0f}]") # Print the new best damage and the new item that led to this new record

                                    elif (swap_item1 == swap_item3) and (swap_item1 != swap_item2):
                                        print(f"[{check_slots[i]} & {check_slots[i2]}]:   [{equipped_item1} & {equipped_item2}]  ->  [{swap_item1} & {swap_item2}]   [{best_damage:>6.0f} -> {damage:>6.0f}]")

                                    elif (swap_item2 == swap_item3) and (swap_item1 != swap_item2):
                                        print(f"[{check_slots[i]} & {check_slots[i2]}]:   [{equipped_item1} & {equipped_item2}]  ->  [{swap_item1} & {swap_item2}]   [{best_damage:>6.0f} -> {damage:>6.0f}]")

                                    elif (swap_item2 != swap_item3) and (swap_item1 != swap_item2) and (swap_item1 != swap_item3):
                                        print(f"[{check_slots[i]} & {check_slots[i2]} & {check_slots[i3]}]:   [{equipped_item1} & {equipped_item2} & {equipped_item3}]  ->  [{swap_item1} & {swap_item2} & {swap_item3}]   [{best_damage:>6.0f} -> {damage:>6.0f}]")

                                    # If your new set is better than your previous best set, then:
                                    best_damage = damage      # Save the highest damage to compare with future test gearsets
                                    Best_Gearset[slot1]  = b  # Assign to the Best_Gearset dictionary the new piece of gear into the appropriate slot
                                    Best_Gearset[slot2] = b2  # Assign to the Best_Gearset dictionary the new piece of gear into the appropriate slot
                                    Best_Gearset[slot3] = b3  # Assign to the Best_Gearset dictionary the new piece of gear into the appropriate slot

                                damage_list[z] = best_damage  # Update the damage_list[] array to contain the best damage obtained from this iteration.
                                                              # This has nothing to do with plotting right now. Only used to compare damage from consecutive iterations.


        if z > 0: # After the first iteration:
            if np.abs(damage_list[z]-damage_list[z-1])/damage_list[z] < 0.001:
                # If the new best damage is less than 0.1% better than the old best_damage, then converge count += 1
                # After nconv such consecutive iterations, break out of the loop and create the final plot. This prevent the code from bouncing back and forth between two nearly identical items for 20 iterations.
                converge_count += 1
            else:
                converge_count = 0 # Reset the converge count. This ensures that only consecutive trials count towards convergence


    # Place JSE+2 earrings in the right_ear to make it look nice.
    if Best_Gearset["ear1"]["Name2"] in jse_ears:
        temp_ear2 = Best_Gearset["ear2"]
        temp_ear1 = Best_Gearset["ear1"]
        Best_Gearset["ear1"] = temp_ear2
        Best_Gearset["ear2"] = temp_ear1

    # At this point, the code has run up to 20 iterations and found the gearset that returns the highest average damage. Now we use this best set to create a proper distribution of damage that you'd expect to see in game based on its stats.
    best_set = set_gear(buffs, Best_Gearset, main_job, sub_job) # Create a class from the best gearset
    # print(f"{tcount} valid gear sets checked.")
    # Run the simulator once more, but with "final=True" to tell the code to create a proper distribution.


    test_set(main_job, sub_job, ws_name, enemy, buffs, Best_Gearset, best_set, tp1, tp2, n_simulations, show_final_plot, True, nuke, spell, burst, futae, ebullience)
    
    return(Best_Gearset)

if __name__ == "__main__":

    main_job = "DRK"
    sub_job = "WAR"
    ws_name = "Blade: Shun"
    min_tp = 1000
    max_tp = 1500
    n_iter = 10
    n_sims = 10000
    # check_gear = [[Heishi,Kikoku],[Fotia_Gorget, Ninja_Nodowa]]
    # check_slots = ["main","neck"]
    # check_gear = [mains, subs, ammos, heads, necks, ears, ears2, bodies, hands, rings, rings2, capes, waists, legs, feet]
    # check_slots = ["main", "sub", "ammo", "head", "neck", "ear1", "ear2", "body", "hands", "ring1", "ring2", "back", "waist", "legs", "feet"]
    check_gear = [mains, subs, ammos, heads, necks, ears, ears2,]
    check_slots = ["main", "sub", "ammo", "head", "neck", "ear1", "ear2"]
    buffs = {"food": Grape_Daifuku,
             "brd": {"Attack": 0, "Accuracy": 0, "Ranged Accuracy": 0},
             "cor": {"Attack": 0, "Store TP": 0, "Accuracy": 0, "Magic Attack": 0, "DA":0, "Crit Rate": 0},
             "geo": {"Attack": 0, "Ranged Attack": 0, "Accuracy": 0, "Ranged Accuracy":0, "STR":0,"DEX":0, "VIT":0, "AGI":0, "INT":0, "MND":0, "CHR":0,},
             "whm": {"Haste": 0, "STR":0,"DEX":0, "VIT":0, "AGI":0, "INT":0, "MND":0, "CHR":0}, # WHM buffs like boost-STR. Not tested
             }
    from enemies import *
    enemy = apex_toad

    starting_gearset1 = {
                'main' : Heishi,
                'sub' : Kunimitsu,
                'ranged' : Empty,
                'ammo' : Yetshila,
                'head' : Blistering_Sallet,
                'body' : Mpaca_Doublet,
                'hands' : Ryuo_Tekko_A,
                'legs' : Jokushu_Haidate,
                'feet' : Mochizuki_Kyahan,
                'neck' : Ninja_Nodowa,
                'waist' : Fotia_Gorget,
                'ear1' : Odr_Earring,
                'ear2' : Lugra_Earring_Aug,
                'ring1' : Regal_Ring,
                'ring2' : Gere_Ring,
                'back' : Andartia_Critdex}
    show_final_plot = True

    nuke = False # True/False
    spell = "Doton: Ichi" # "Doton: Ichi" etc
    burst = True # True/False
    futae = False # True/False. Only for Ninjutsu
    ebullience = False # True/False. Only for SCH main with Elemental Magic

    if False:
        import cProfile
        cProfile.run("run_weaponskill(main_job, sub_job, ws_name, min_tp, max_tp, n_iter, n_sims, check_gear, check_slots, buffs, enemy, starting_gearset1, show_final_plot, nuke, spell, burst, futae, ebullience)",sort="cumtime")
    else:
        run_weaponskill(main_job, sub_job, ws_name, min_tp, max_tp, n_iter, n_sims, check_gear, check_slots, buffs, enemy, starting_gearset1, show_final_plot, nuke, spell, burst, futae, ebullience)

    # TODO:
    # 2-handed weapons cap at 95% accuracy. The code currently uses 99% since it was based on NIN dual-wielding two single-handed weapons.
    #   Maybe use something like
    # 
    #       if sub_type == "grip":
    #           hit_rate = 0.95 if hit_rate > 0.95 else hit rate
    #
    # Add Magic Accuracy and resistance ranks to magic calculations.
