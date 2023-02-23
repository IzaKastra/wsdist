#
# Created by Kastra on Asura.
# Feel free to /tell in game or send a PM on FFXIAH you have questions, comments, or suggestions.
#
# Version date: 2023 February 16
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
from get_delay_timing import *

from get_tp import get_tp
from fancy_plot import *

import random

class TP_Error(Exception):
    pass

def weaponskill(main_job, sub_job, ws_name, enemy, gearset, tp1, tp2, tp0, buffs, equipment, nuke, spell, job_abilities, burst=False, final=False, check_tp_set=False):
    #
    # Use the player and enemy stats to calculate weapon skill damage.
    # This function works, but needs to be cleaned up. There is too much going on within it.
    # It would be easier to rewrite the entire code and simply borrow from what I already have.
    #

    tp1 = 1000 if tp1 < 1000 else tp1
    tp2 = 1000 if tp2 < 1000 else tp2

    tp1 = 3000 if tp1 > 3000 else tp1
    tp2 = 3000 if tp2 > 3000 else tp2

    if final:
        # Randomly sample the TP range if running WS simulations.
        tp = np.random.uniform(tp1,tp2)
    else:
        # Use average TP value if testing WS sets.
        # TP sets always use the minimum value.
        tp = np.average([tp1,tp2])

    # Break apart the job abilities dictionary # TODO: this isnt necessary if we write the rest of the code better...

    footwork = job_abilities["Footwork"]
    futae = job_abilities["Futae"]
    ebullience = job_abilities["Ebullience"]
    building_flourish = job_abilities["Building Flourish"]
    climactic_flourish = job_abilities["Climactic Flourish"]
    striking_flourish = job_abilities["Striking Flourish"]
    ternary_flourish = job_abilities["Ternary Flourish"]
    sneak_attack = job_abilities["Sneak Attack"]
    trick_attack = job_abilities["Trick Attack"]
    impetus = job_abilities["Impetus"]
    hover_shot = job_abilities["Hover Shot"]
    true_shot_toggle = job_abilities["True Shot"]
    blood_rage = job_abilities["Blood Rage"]
    mighty_strikes = job_abilities["Mighty Strikes"]
    last_resort = job_abilities["Last Resort"]

    # Ranged WSs can't multi-attack. Here we define a thing that we can use later to deal with ranged-specific damage
    # It would be better to just use a separate melee/ranged/magical/hybrid WS function and not have to do this. but i'll do that later TODO
    phys_rng_ws = ws_name in ["Flaming Arrow", "Namas Arrow", "Apex Arrow", "Refulgent Arrow","Empyreal Arrow", "Sidewinder", "Piercing Arrow", "Jishnu's Radiance", "Blast Arrow", "Hot Shot", "Coronach","Last Stand","Detonator", "Blast Shot", "Slug Shot", "Split Shot", ] # Used to ensure Shining One does not let Ranged Weapon skills crit

    kick_ws_footwork = footwork and (ws_name in ["Dragon Kick", "Tornado Kick"])

    # Save the main and sub weapon names for later.
    # Used to check if giving weapon skill damage bonuses on things like Gokotai (if "Gokotai" in main_wpn_name)
    main_wpn_name = gearset.equipment()['main'] # TODO: Why is this one using the .equipment() method, but the other two are using .gear[]
    sub_wpn_name = gearset.gear['sub']['Name2']
    rng_wpn_name = gearset.gear['ranged']['Name'] # Use name1 so we don't have to deal with " R15" in the check_weaponskill_bonuses.py file

    sub_type = gearset.gear['sub'].get('Type', 'None') # Check if the item equipped in the sub slot is a weapon or a grip or shield. If the item doesn't have a "Type" Key then return "None". All items SHOULD have a type.
    dual_wield = sub_type == 'Weapon'

    main_type_skill = gearset.gear['main']['Skill Type']
    sub_type_skill = gearset.gear['sub'].get('Skill Type', 'None') # If the sub item doesn't have a skill type (Katana/Dagger/Scythe, etc) then return "None"
    rng_type_skill = gearset.gear['ranged'].get('Skill Type', 'None') # If the sub item doesn't have a skill type (Katana/Dagger/Scythe, etc) then return "None"

    tp += gearset.playerstats['TP Bonus'] # Add TP bonus
    tp = 3000 if tp > 3000 else int(tp) # Cap TP at 3000

    if gearset.gear["main"]["Skill Type"] != "Hand-to-Hand":
        main_dmg = gearset.playerstats['DMG1']
        delay1 = gearset.playerstats['Delay1'] # Main-hand delay.

        marts = 0
        kick_dmg = 0
    else:
        base_dmg = 3 + int((gearset.playerstats["Hand-to-Hand Skill"]+gearset.gear["main"]["Hand-to-Hand Skill"])*0.11) # Base damage for no H2H with no weapon equipped.
        main_dmg = base_dmg + gearset.playerstats['DMG1'] # Add the "+damage" from H2H weapons
        kick_dmg = base_dmg + gearset.playerstats["Kick Attacks Attack"]

        dual_wield = True # Treat H2H WSs as dual-wielding such that the off-hand hit (which is identical to the main-hand hit) gains full TP and can MA.
                          # The weaponskill_scaling.py code already subtracts one hit from each WS to account for this extra DW hit.

        if footwork:
            kick_dmg = main_dmg + 20 + 20 + gearset.playerstats["Kick Attacks Attack"] # +20 footwork base, +20 from JP, and +x from gear: https://www.ffxiah.com/forum/topic/55864/new-monk-questions/#3600604
                                                                              # See also: https://www.ffxiah.com/forum/topic/36705/iipunch-monk-guide/213/#3368961
                                                                              # and this official post saying kick attacks use weapon damage with footwork: https://forum.square-enix.com/ffxi/threads/52969-August.-3-2017-%28JST%29-Version-Update
            if kick_ws_footwork and not check_tp_set:
                main_dmg = kick_dmg

        base_delay = 480
        marts = gearset.playerstats["Martial Arts"]
        delay1 = (base_delay + gearset.playerstats['Delay1']) # We include Martial Arts later.

    sub_dmg  = gearset.playerstats['DMG2']
    rng_dmg  = gearset.playerstats.get('Ranged DMG',0)
    rng_delay  = gearset.playerstats.get('Ranged Delay',0)
    ammo_dmg = gearset.playerstats.get("Ammo DMG",0)
    ammo_delay = gearset.playerstats.get("Ammo Delay",0)

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

    delay2 = gearset.playerstats['Delay2'] if (dual_wield and gearset.gear["main"]["Skill Type"]!="Hand-to-Hand") else delay1 # Off-hand delay if dual wielding
    dw = gearset.playerstats['Dual Wield']/100 if (dual_wield and gearset.gear["main"]["Skill Type"]!="Hand-to-Hand") else 0.
    mdelay = (delay1+delay2)/2.*(1.-dw) if (dual_wield and gearset.gear["main"]["Skill Type"]!="Hand-to-Hand") else delay1 - marts # Modified delay based on weapon delays, dual wield, and martial arts. Used for TP return from weapon skills

    # Read in haste values. We apply limits in the get_delay_timing() function/file.
    gear_haste  = gearset.playerstats['Gear Haste']/102.4
    magic_haste = gearset.playerstats['Magic Haste']
    ja_haste    = gearset.playerstats['JA Haste']/102.4

    tpa = get_delay_timing(delay1, delay2, dw, marts, magic_haste, ja_haste, gear_haste)

    daken = (gearset.playerstats['Daken'])/100 if main_job=="NIN" and gearset.gear["ammo"].get("Skill Type","None") == "Throwing" else 0 # Do not allow daken without nin and shuriken
    kickattacks = (gearset.playerstats['Kick Attacks'] + 20*footwork)/100 if (main_job=="MNK" or sub_job=="MNK") and gearset.gear["main"]["Skill Type"] == "Hand-to-Hand" else 0 # do not allow kicks without mnk and h2h

    # Limits these to 100% proc rate.
    daken = 1.0 if daken > 1.0 else daken
    kickattacks = 1.0 if kickattacks > 1.0 else kickattacks

    wsd = gearset.playerstats['Weaponskill Damage']/100. # Applies to first hit only
    if phys_rng_ws and main_job == "SAM":
        wsd -= 19/100 # Undo the Overwhelm merits for ranged weapon skills
        # TODO: also remove from magical ranged WSs

    ws_acc = gearset.gearstats['Weaponskill Accuracy']
    ws_bonus = gearset.playerstats['Weaponskill Bonus']/100. # Bonus damage multiplier to every hit on the WS. Stuff like Gokotai, Naegling, hidden Relic/Mythic WS damage, REMA augments.
    ws_trait = gearset.playerstats.get("Weaponskill Trait",0)/100 # Only DRG traits go here. DRG main job also gets wyvern bonus 10% here.

    rng_crit_dmg = gearset.playerstats['Ranged Crit Damage']/100
    crit_dmg = gearset.playerstats['Crit Damage']/100 + gearset.playerstats["Ranged Crit Damage"]/100*phys_rng_ws*0
    crit_rate = 0 # WSs can't crit unless they explicitly say they can (Blade: Hi, Evisceration, CDC, etc). Crit rate is read in properly only for those weapon skills (see below) and the special case with Shining One

    true_shot = gearset.playerstats['True Shot']/100 * true_shot_toggle # 0 if False


    sneak_attack_bonus = (gearset.playerstats["DEX"] * (1+gearset.playerstats["Sneak Attack"]/100))*sneak_attack
    trick_attack_bonus = (gearset.playerstats["AGI"] * (1+gearset.playerstats["Trick Attack"]/100))*trick_attack
    climactic_flourish_bonus = (0.5*gearset.playerstats["CHR"] * (1+gearset.playerstats["Flourish Bonus"]/100))*climactic_flourish
    striking_flourish_bonus = (1.0*gearset.playerstats["CHR"] * (1+gearset.playerstats["Flourish Bonus"]/100))*striking_flourish
    ternary_flourish_bonus = (1.0*gearset.playerstats["CHR"] * (1+gearset.playerstats["Flourish Bonus"]/100))*ternary_flourish

    vajra_bonus = gearset.gear["main"]["Name"]=="Vajra" and (sneak_attack or trick_attack) # We use this to enhance crit damage by 30% only for the first hit in get_phys_dmg later.
    dnc_empy_head_bonus = gearset.gear["head"]["Name"]=="Maculele Tiara +3" and climactic_flourish # We use this to enhance crit damage by 31% only for the first hit in get_phys_dmg later.
    dnc_empy_body_bonus = gearset.gear["body"]["Name"]=="Maculele Casaque +3" and striking_flourish # We use this to enhance crit rate by 70% only for the first hit in get_phys_dmg later.

    # Zanshin stuff.
    two_handed = ["Great Sword", "Great Katana", "Great Axe", "Polearm", "Scythe", "Staff"]
    zanshin = gearset.playerstats["Zanshin"]/100*(1+0.25*(main_job=="SAM")) + 0.1*(main_job=="SAM") if gearset.gear["main"]["Skill Type"] in two_handed else 0
    zanshin = 1 if zanshin > 1 else zanshin
    zanhasso = gearset.playerstats["Zanshin"]/100/4 if main_job=="SAM" else 0
    zanhasso = 0.25 if zanhasso > 0.25 else zanhasso
    zanhasso += 0.1
    zanhasso = 0 if main_job != "SAM" else zanhasso
    zanshin_oa2 = gearset.playerstats["Zanshin OA2"]/100

    qa = gearset.playerstats['QA']/100
    ta = gearset.playerstats['TA']/100
    da = gearset.playerstats['DA']/100
    oa3_main = 0 # Only applies with Mythic Aftermath on WSs and only on the hand holding the weapon. Same deal as crit rate. OA3 and OA2 are read in properly if using Nagi main hand for AM3. See below.
    oa2_main = 0 # Only applies with Mythic Aftermath on WSs and only on the hand holding the weapon. Same deal as crit rate. OA3 and OA2 are read in properly if using Nagi main hand for AM3. See below.

    oa8_sub = gearset.gear["sub"].get("OA8",0)/100
    oa7_sub = gearset.gear["sub"].get("OA7",0)/100
    oa6_sub = gearset.gear["sub"].get("OA6",0)/100
    oa5_sub = gearset.gear["sub"].get("OA5",0)/100
    oa4_sub = gearset.gear["sub"].get("OA4",0)/100
    oa3_sub = gearset.gear["sub"].get("OA4",0)/100
    oa2_sub = gearset.gear["sub"].get("OA3",0)/100

    stp = gearset.playerstats['Store TP']/100

    player_mab = gearset.playerstats['Magic Attack']
    player_magic_damage = gearset.playerstats['Magic Damage']
    magic_crit_rate2 = gearset.playerstats["Magic Crit Rate II"]/100 # Magic Crit Rate II is apparently +25% damage x% of the time.

    enemy_int = enemy["INT"]
    enemy_agi = enemy["AGI"]
    enemy_vit = enemy["VIT"]
    enemy_mnd = enemy["MND"]
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


    if nuke:

        if spell=="Ranged Attack": # /ra auto attack
            #
            # Estimate the average white damage from a single /ra ranged attack.
            #

            if gearset.gear["ranged"]["Name"]=="Empty":
                rng_delay = 0

            doubleshot_toggle = job_abilities["Double Shot"]
            double_shot = 0.4 + gearset.playerstats["Double Shot"]/100 if doubleshot_toggle else 0
            double_shot_damage = gearset.playerstats["Double Shot Damage"]/100
            double_shot = 1.0 if double_shot > 1.0 else double_shot

            tripleshot_toggle = job_abilities["Triple Shot"]
            triple_shot = 0.4 + gearset.playerstats["Triple Shot"]/100 if tripleshot_toggle else 0
            triple_shot_damage = gearset.playerstats["Triple Shot Damage"]/100
            triple_shot = 1.0 if triple_shot > 1.0 else triple_shot

            quad_shot = 0

            # If using COR+3 empy hands, then half your total triple shot rate is converted to quad shot.
            # http://wiki.ffo.jp/html/30818.html
            # https://www.ffxiah.com/forum/topic/31312/the-pirates-lair-a-guide-to-corsair/154/#3323623
            if gearset.gear["hands"]["Name"] == "Lanun Gants +3":
                quad_shot += triple_shot/2
                triple_shot /= 2

            # If using RNG+3 relic body, then half your total double shot rate is converted to triple shot.
            if gearset.gear["body"]["Name"] == "Arcadian Jerkin +3":
                triple_shot += double_shot/2
                double_shot /= 2
                double_shot += 0.05 # 5/5 Snapshot merits with Relic+3 body augment. Assuming it is not converted to triple shot since it procs without the ability active.

            crit_dagi = ((player_agi - enemy_agi)/10)/100 if (player_agi > enemy_agi) else 0

            crit_rate = gearset.playerstats['Crit Rate']/100 + crit_dagi # Ranged attacks gain crit rate from AGI, not DEX
            crit_dmg = gearset.playerstats['Crit Damage']/100 + gearset.playerstats["Ranged Crit Damage"]/100 # Crit damage plus Dead Aim bonuses

            phys = 0 # Total physical damage dealt
            tp = 0  # Average TP return from a single /ra
            hitrate_ranged = get_hitrate(player_rangedaccuracy+100*hover_shot, 0, enemy_eva, "ranged", False, rng_type_skill) # Calculate ranged hit rate
            fstr_rng = get_fstr2(rng_dmg, player_str, enemy_vit)

            # Calculate average damage from a single /ra hit
            main_hits = 1*hitrate_ranged
            tp += get_tp(main_hits, rng_delay+ammo_delay, stp)
            avg_pdif_rng = get_avg_pdif_ranged(player_rangedattack, rng_type_skill, pdl_trait, pdl_gear, enemy_def, crit_rate)
            ranged_hit_damage = get_avg_phys_damage(rng_dmg+ammo_dmg, fstr_rng, 0, avg_pdif_rng, 1.0, crit_rate, crit_dmg, 0, 0, 0)
            phys += ranged_hit_damage*main_hits

            # Add the bonus damage from a double shot proc
            double_shot_hits = 1*hitrate_ranged*double_shot
            tp += get_tp(double_shot_hits, rng_delay+ammo_delay, stp)
            ranged_hit_damage = get_avg_phys_damage(rng_dmg+ammo_dmg, fstr_rng, 0, avg_pdif_rng, 1.0, crit_rate, crit_dmg, 0, 0, 0)
            phys += ranged_hit_damage*double_shot_hits*(1+double_shot_damage)

            # Add the bonus damage from a triple shot proc
            triple_shot_hits = 2*hitrate_ranged*triple_shot
            tp += get_tp(triple_shot_hits, rng_delay+ammo_delay, stp)
            ranged_hit_damage = get_avg_phys_damage(rng_dmg+ammo_dmg, fstr_rng, 0, avg_pdif_rng, 1.0, crit_rate, crit_dmg, 0, 0, 0)
            phys += ranged_hit_damage*triple_shot_hits*(1+triple_shot_damage)

            # Add the bonus damage from a quad shot proc
            quad_shot_hits = 3*hitrate_ranged*quad_shot
            tp += get_tp(quad_shot_hits, rng_delay+ammo_delay, stp)
            phys += ranged_hit_damage*quad_shot_hits

            if gearset.gear["head"]["Name"] == "Arcadian Beret +3":
                recycle = gearset.playerstats["Recycle"]/100
                recycle = 90 if recycle > 90 else recycle
                tp += 50*recycle/100 # +10 TP per Recycle merit when Recycle procs. Assume 5/5 merits for +50 TP up to 90% of the time.

            # Multiply damage by true shot bonuses
            phys *= (1+true_shot)

            # Multiply by the hover shot bonus (+100%)
            phys *= (1+hover_shot)

            if gearset.gear["ranged"]["Name"] in ["Gandiva","Armageddon"]:
                # Assume AM3, which triples damage 50% of the time, or doubles damage on all shots on average
                phys *= (1+2*0.5)
            elif gearset.gear["ranged"]["Name"] in ["Annihilator","Yoichinoyumi"]:
                # Relics which triples damage 13% of the time
                phys *= (1+2*0.13)

            priority = job_abilities["metric"] # not a job ability, but this is an easy way to smuggle a variable from the GUI into this part of the main code
            if priority=="Damage > TP":
                metric = phys*phys*tp/1e6
            elif priority=="TP > Damage":
                metric = phys*tp*tp/1e4
            elif priority=="TP only":
                metric = tp
            elif priority=="Damage only":
                metric = phys

            return(metric,tp)


        cor_shots = ["Earth Shot", "Water Shot", "Wind Shot", "Fire Shot", "Ice Shot", "Thunder Shot"]
        if spell in cor_shots:
            player_mab += gearset.playerstats['Ninjutsu Magic Attack']
            damage = quickdraw(rng_dmg, ammo_dmg, spell.lower().split()[0], gearset, player_mab, player_magic_damage, enemy_int, enemy_mdb, enemy_meva)
            return(damage, 0) # Return 0 TP


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

            damage = nuking(spell, "Ninjutsu", tier, element, main_job, sub_job, gearset, player_int, player_mab, player_magic_damage, enemy_int, enemy_mdb, enemy_meva, ninjutsu_damage, futae, burst, ebullience)

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

            if spell=="Kaustra":
                element="Dark"
                tier = "None"
            elif spell[-2:] == "ja":
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

            damage = nuking(spell, "Elemental Magic", tier, element, main_job, sub_job, gearset, player_int, player_mab, player_magic_damage, enemy_int, enemy_mdb, enemy_meva, 0, futae, burst, ebullience)

        return(damage,0) # If nuke, then don't bother running the rest of the code, simply return the magic damage (and 0 TP return) and continue with the testing.




    # Check weapon + weapon skill synergy for things like bonus weapon skill damage. (and mythic AM3)
    # See "check_weaponskill_bonuses.py"
    ws_weapons = [main_wpn_name, rng_wpn_name]
    bonuses = check_weaponskill_bonus(ws_weapons, ws_name, gearset, tp, enemy_agi)
    ws_bonus += bonuses['ws_bonus']
    # crit_rate = bonuses['crit_rate'] # Crit rate adjusted for Shining One. Commented out. We'll do this in "weaponskill_scaling" instead.
    oa3_main += bonuses['oa3'] ; oa2_main += bonuses['oa2'] # Mythic OA3 and OA2 rates
    # triple_dmg_rate += bonuses['triple_dmg_rate'] # Empyrean triple damage rate

    # fSTR calculation for main-hand and off-hand
    fstr_main = get_fstr(main_dmg, player_str, enemy_vit)
    fstr_sub  = get_fstr(sub_dmg, player_str, enemy_vit)
    fstr_kick = get_fstr(kick_dmg, player_str, enemy_vit)
    fstr_rng = get_fstr2(rng_dmg, player_str, enemy_vit)


    # Must be a list, since numba doesnt like dictionaries
    # oa_dict = {"oa3_main":oa3_main,
    #            "oa2_main":oa2_main,
    #            "oa8_sub":oa8_sub,
    #            "oa7_sub":oa7_sub,
    #            "oa6_sub":oa6_sub,
    #            "oa5_sub":oa5_sub,
    #            "oa4_sub":oa4_sub,
    #            "oa3_sub":oa3_sub,
    #            "oa2_sub":oa2_sub}
    oa_list = np.array([oa3_main,oa2_main,oa8_sub,oa7_sub,oa6_sub,oa5_sub,oa4_sub,oa3_sub,oa2_sub],dtype=np.float32)

    if check_tp_set:

        phys = 0
        # Run TP set separately from WS set. This includes copy/pasted functions just to keep things separate. We can move this entire if-statement to a separate function/file later.
        # Need to check TP sets before reading in WS scaling stuff, or we might accidentally give WS bonuses to our TP attacks
        crit_rate = gearset.playerstats['Crit Rate']/100

        # Check hit rates for melee and ranged weapons. None of these hits get +100 accuracy since this is not a weapon skill
        hitrate11 = get_hitrate(player_accuracy1, 0, enemy_eva, 'main',  False, main_type_skill) # First main-hand hit.
        hitrate21 = get_hitrate(player_accuracy2, 0, enemy_eva,  'sub',  False, sub_type_skill) # First off-hand hit.
        hitrate12 = get_hitrate(player_accuracy1, 0, enemy_eva, 'main', False, main_type_skill) # Additional main-hand hits. "False" to not gain the +100 accuracy.
        hitrate22 = get_hitrate(player_accuracy2, 0, enemy_eva,  'sub', False, sub_type_skill) # Additional off-hand hits.
        hitrate_matrix = np.array([[hitrate11, hitrate21],[hitrate12, hitrate22]])

        hitrate_ranged2 = get_hitrate(player_rangedaccuracy, 0, enemy_eva, "ranged", False, "Throwing") # Ranged hitrate here only applies for daken. I have no plans for ranged TPing

        zanshin_hitrate = get_hitrate(player_accuracy1+34, 0, enemy_eva, "main", False, main_type_skill)

        # Estimate number of hits for the average attack round, including daken and kicks
        main_hits, sub_hits, daken_hits, kickattack_hits, zanshin_hits = get_ma_rate3(main_job, 1, qa, ta, da, oa_list, dual_wield, hitrate_matrix, hitrate_ranged2, daken, kickattacks, zanshin, zanhasso, zanshin_hitrate, zanshin_oa2, tp_round=True)

        # Calculate average TP return from these hits
        tp = 0
        tp += get_tp(main_hits + sub_hits + kickattack_hits - zanshin_hits, mdelay, stp)  # Non-zanshin hits get normal TP
        tp += get_tp(zanshin_hits, mdelay, stp, main_job=="SAM") # Zanshin hits get bonus TP if SAM is your main job and you have Ikishoten merits
        tp += get_tp(daken_hits, ammo_delay, stp)

        ws_threshold = tp1
        # print("Average time per WS: ",ws_threshold/tp*tpa)
        time_to_ws = (ws_threshold-tp0)/tp*tpa


        # print("Main hits: ",main_hits)
        # print("Sub hits: ",sub_hits)
        # print("Daken hits: ",daken_hits)
        # print("Kick hits: ",kickattack_hits)
        # print("Hitrate1: ",hitrate12)
        # print("Hitrate2: ",hitrate22)
        # print("Store TP: ",stp)
        # print("delay1: ",delay1)
        # print("delay2: ",delay2)
        # print("dw: ",dw)
        # print("mdelay: ",mdelay)
        # print("WS Thresh: ",ws_threshold)
        # print("Average TP Return: ",tp)
        # print("Time per attack round: ",tpa)
        # print("Time per weapon skill: ",time_to_ws)
        # print("-----------------")

        # -------------------
        # -------------------
        # -------------------
        empyrean_aftermath_multiplier = (1+2*0.5) if gearset.gear["main"]["Name"] in ["Verethragna","Twashtar","Almace","Caladbolg","Farsha","Ukonvasara","Redemption","Kannagi","Rhongomiant","Gambanteinn","Masamune","Hvergelmir"] else 1.0
        relic_aftermath_multiplier = (1+2*0.13) if gearset.gear["main"]["Name"] in ["Spharai","Mandau","Excalibur","Ragnarok","Guttler","Bravura","Apocalypse","Gungnir Kikoku","Amanomurakumo","Mjollnir","Claustrum"] else 1.0

        # Get melee damage from the main-hand attacks
        main_hit_pdif = get_avg_pdif_melee(player_attack1, main_type_skill, pdl_trait, pdl_gear, enemy_def, crit_rate)
        main_hit_damage = get_avg_phys_damage(main_dmg, fstr_main, 0, main_hit_pdif, 1.0, crit_rate, crit_dmg, 0, 0, 0)

        # Calculate first main hit damage (relic aftermath only applies to this one hit so we should calculate it separately.)
        phys += hitrate11*main_hit_damage*hitrate12*empyrean_aftermath_multiplier*relic_aftermath_multiplier

        # Add in the remaining hits, which can get empyrean aftermath procs
        phys += (main_hits-hitrate11)*main_hit_damage*hitrate12*empyrean_aftermath_multiplier

        # Get melee damage from the off-hand attacks
        sub_hit_pdif = get_avg_pdif_melee(player_attack2, sub_type_skill, pdl_trait, pdl_gear, enemy_def, crit_rate)
        sub_hit_damage = get_avg_phys_damage(sub_dmg, fstr_sub, 0, sub_hit_pdif, 1.0, crit_rate, crit_dmg, 0, 0, 0)
        phys += sub_hits*sub_hit_damage*hitrate22

        # Get melee damage from the extra kick attack
        kick_hit_pdif = get_avg_pdif_melee(player_attack1, "Hand-to-Hand", pdl_trait, pdl_gear, enemy_def, crit_rate)
        kick_hit_damage = get_avg_phys_damage(kick_dmg, fstr_kick, 0, kick_hit_pdif, 1.0, crit_rate, crit_dmg, 0, 0, 0)
        phys += kickattack_hits*kick_hit_damage*hitrate12

        # -------------------
        # -------------------
        # -------------------
        # Get ranged damage
        if daken > 0:
            avg_pdif_rng = get_avg_pdif_ranged(player_rangedattack, "Throwing", pdl_trait, pdl_gear, enemy_def, crit_rate)
            ranged_hit_damage = get_avg_phys_damage(ammo_dmg, fstr_rng, 0, avg_pdif_rng, 1.0, crit_rate, crit_dmg, 0, 0, 0) # Daken throw damage. Uses WSD formula, but all WSD related stuff is 0, and ftp=1.
            phys += ranged_hit_damage*hitrate_ranged2

        dps = phys / tpa # damage / time_per_action. Not useful until I add "DA dmg" "TA dmg" etc

        priority = job_abilities["metric"]
        if priority=="Damage" and False:
            metric = 1/dps
        else:
            metric = time_to_ws

        # import sys; sys.exit()
        return(metric, tp) # Return time (seconds) per WS and total TP per average attack round.



    # print("Before: ",ws_bonus,crit_rate)
    # Obtain weapon skill TP scaling. "Damage varies with TP"
    # See "weaponskill_scaling.py"
    scaling = weaponskill_scaling(main_job, sub_job, ws_name, tp, gearset, equipment, buffs, dStat, dual_wield, enemy_def, enemy_agi, enemy_int, enemy_mnd, job_abilities, kick_ws_footwork,)
    wsc = scaling['wsc']
    ftp = scaling['ftp']
    ftp_rep = scaling['ftp_rep']
    nhits = scaling['nhits']
    element = scaling['element']
    hybrid = scaling['hybrid']
    magical = scaling['magical']
    player_attack1 = scaling['player_attack1'] # Some weaponskills enhance/reduce player attack or enemy defense.
    player_attack2 = scaling['player_attack2']
    player_rangedattack = scaling['player_rangedattack']
    enemy_def = scaling['enemy_def']
    crit_rate = scaling['crit_rate'] # Crit Rate is only enabled if the weapon skill can crit natively, or if using Shining One
    ftp_hybrid = scaling['ftp_hybrid']
    ws_dINT = scaling["ws_dINT"] # dINT used for magical weapon skills. Some WSs have maximum values, some don't even use a dSTAT.
    acc_bonus = scaling["acc_bonus"] # Accuracy varies with TP.
    # print("After: ",ws_bonus,crit_rate)

    crit_rate += 0.2*blood_rage if crit_rate > 0 else 0 # Add 20% crit rate if blood rage is enabled
    crit_rate = 1.0 if mighty_strikes else crit_rate # Set crit rate to 100% if mighty strikes is enabled.

    player_accuracy1 += acc_bonus
    player_accuracy2 += acc_bonus
    player_rangedaccuracy += acc_bonus

    # Setup replicating ftp for specific WSs.
    ftp += fotia_ftp
    if hybrid:
        ftp_hybrid += fotia_ftp
    ftp2 = 1.0 if not ftp_rep else ftp # FTP for additional and off-hand hits.

    # Define elemental damage bonuses now that we know what element your hybrid/magical weapon skill is.
    if hybrid or magical:

        element_magic_attack_bonus = 1 + (gearset.playerstats.get(element + ' Elemental Bonus', 0) + gearset.playerstats['Elemental Bonus'])/100 # Archon Ring, Pixie Hairpin +1, Orpheus

    # Start the damage calculations.
    damage = 0

    if magical: # TODO: move magical/hybrid/ranged/physical into their own functions
        # Magical weapon skills have no physical portion, so they use a different, simpler, damage algorithm.
        # In this case, we will not make a plot since the damage is always the same.
        # This is why we exclude "magical" weaponskills from the rest of this function.
        #
        # Assuming Magical weapon skills can not multi-attack. TODO: test this in game using heishi + Lv1 dagger. Does damage change when unequipping dagger? (the offhand hit might not exist either)
        weapon_level = 119
        crocea = True if gearset.gear["main"]["Name2"] == "Crocea Mors R25C" else False
        magical_damage = int(((152 + int((weapon_level-99)*2.45)+wsc)*ftp)*(1+crocea) + ws_dINT + player_magic_damage)

        magic_hit_rate = get_magic_hit_rate(magic_accuracy + 100*hover_shot, enemy_meva) if enemy_meva > 0 else 1.0
        resist_state = get_resist_state_average(magic_hit_rate)

        klimaform_bonus = 1.0 # Klimaform with Empy+3 feet boosts magical WS damage by 25%
        if gearset.equipped["feet"] == "Arbatel Loafers +3": # Only SCH can use these feet
            klimaform_bonus += 0.25

        affinity = 1 + 0.05*gearset.playerstats[f'{element} Affinity'] + 0.05*(gearset.playerstats[f'{element} Affinity']>0) # Affinity Bonus. Only really applies to Magian Trial staves. Archon Ring is different.

        dayweather = 1.0
        if gearset.gear["waist"]["Name"]=="Hachirin-no-Obi":
          if main_job == "SCH":
            dayweather = 1.25
          elif sub_job == "SCH":
            dayweather = 1.1

#        dayweather = 1.0 # 0.65, 0.8, 0.9, 1.0, 1.1, 1.22, 1.35. Assume no day/weather bonus/penalty.
        magic_attack_ratio = (100 + player_mab) / (100 + enemy_mdb)
        enemy_mdt = 1.0 # Usually 1.0 unless the enemy casts shell or a similar spell/ability.

        magic_multiplier = affinity*resist_state*dayweather*magic_attack_ratio*enemy_mdt*element_magic_attack_bonus*klimaform_bonus
        magical_damage *= magic_multiplier
        magical_damage *= (1+wsd)*(1+ws_bonus)*(1+ws_trait)
        magical_damage *= (1 + 0.25*magic_crit_rate2) # Magic Crit Rate II is apparently +25% damage x% of the time.
        magical_damage *= (1 + hover_shot)

        return(magical_damage,0) # Return 0 TP for now.


    if not final: # If the best set hasn't been determined yet, then just take a simple average. No need to run a bunch of simulations unless you're making a plot.

        if not phys_rng_ws: # Do normal melee physical WS stuff here. otherwise skip all of it and do ranged physical WS stuff
            # Check hit rates for each hand and for each hit.
            hitrate11 = get_hitrate(player_accuracy1, ws_acc, enemy_eva, 'main',  True, main_type_skill) # First main-hand hit.
            hitrate21 = get_hitrate(player_accuracy2, ws_acc, enemy_eva,  'sub',  True, sub_type_skill) # First off-hand hit.
            hitrate12 = get_hitrate(player_accuracy1, ws_acc, enemy_eva, 'main', False, main_type_skill) # Additional main-hand hits. "False" to not gain the +100 accuracy.
            hitrate22 = get_hitrate(player_accuracy2, ws_acc, enemy_eva,  'sub', False, sub_type_skill) # Additional off-hand hits.

            if sneak_attack or trick_attack:
                hitrate11 = 1.0
                hitrate21 = 1.0

            hitrate_matrix = np.array([[hitrate11, hitrate21],[hitrate12, hitrate22]])


            # Estimate number of hits per weapon, including flourishes.
            main_hits, sub_hits, daken_hits, kickattack_hits, zanshin_hits = get_ma_rate3(main_job, nhits, qa, ta, da, oa_list, dual_wield, hitrate_matrix, 0, 0, 0, 0, 0, 0, 0, striking_flourish, ternary_flourish, check_tp_set) # Zero for ranged hit rate, daken, and kick attacks since this is the melee WS check

            # Assuming absolutely zero bonuses, how much damage would the main-hand hits do, all together?
            main_hit_pdif = get_avg_pdif_melee(player_attack1, main_type_skill, pdl_trait, pdl_gear, enemy_def, crit_rate)
            main_hit_damage = get_avg_phys_damage(main_dmg, fstr_main, wsc, main_hit_pdif, ftp2, crit_rate, crit_dmg, 0, ws_bonus, ws_trait) # No bonuses, so using FTP2, WSD=0, etc
            phys = main_hits*main_hit_damage

            # Now calculate the true damage of the first main hit, with all of its bonuses:
            first_main_hit_crit_rate = (1.0 if sneak_attack or trick_attack or climactic_flourish else (crit_rate+0.7*dnc_empy_body_bonus*(crit_rate>0))) # Special crit rate for SA/TA/Flourishes.
            adjusted_crit_dmg = (crit_dmg + 0.3*vajra_bonus + 0.31*dnc_empy_head_bonus) # Special crit damage that applies to first hit of SA/TA/ClimacticFlourish
            first_main_hit_pdif = get_avg_pdif_melee(player_attack1, main_type_skill, pdl_trait, pdl_gear, enemy_def, first_main_hit_crit_rate)
            first_main_hit_damage = get_avg_phys_damage(main_dmg, fstr_main, wsc, first_main_hit_pdif, ftp, first_main_hit_crit_rate, adjusted_crit_dmg, wsd, ws_bonus, ws_trait, sneak_attack_bonus, trick_attack_bonus, climactic_flourish_bonus, striking_flourish_bonus, ternary_flourish_bonus)

            # Our original damage was assuming ZERO bonuses. This next line just adds the extra damage gained by those bonuses to the first hit.
            phys += (first_main_hit_damage*hitrate11 - main_hit_damage*hitrate11)

            # Striking Flourish also boosts the crit rate for its double attack hit, but doesn't provide the +100% CHR bonus (probably)
            if striking_flourish:
                # Define a new crit rate that adds 70% only if crit_rate>0 already (only for critical hit WSs)
                striking_flourish_crit_rate = crit_rate+0.7*dnc_empy_body_bonus*(crit_rate>0) # This crit_rate>0 ensures we aren't letting non-crit WSs crit.
                striking_flourish_pdif1 = get_avg_pdif_melee(player_attack1, main_type_skill, pdl_trait, pdl_gear, enemy_def, striking_flourish_crit_rate)
                striking_flourish_DA_damage = get_avg_phys_damage(main_dmg, fstr_main, wsc, striking_flourish_pdif1, ftp2, striking_flourish_crit_rate, crit_dmg, 0, ws_bonus, ws_trait)
                phys += (striking_flourish_DA_damage - main_hit_damage)*hitrate11

            # Calculate the damage for off-hand hits, which receive no bonuses anyway.
            offhand_pdif = get_avg_pdif_melee(player_attack2, sub_type_skill, pdl_trait, pdl_gear, enemy_def, crit_rate)
            offhand_damage = get_avg_phys_damage(sub_dmg, fstr_sub, wsc, offhand_pdif, ftp2, crit_rate, crit_dmg, 0, ws_bonus, ws_trait)
            phys += offhand_damage*sub_hits

        else:
            hitrate_ranged1 = get_hitrate(player_rangedaccuracy + 100*hover_shot, ws_acc, enemy_eva, "ranged", True, rng_type_skill) # Assume first ranged hit gets +100 accuracy. Melee hits do at least...
            hitrate_ranged2 = get_hitrate(player_rangedaccuracy + 100*hover_shot, ws_acc, enemy_eva, "ranged", False, rng_type_skill) # Additional ranged hits

            avg_pdif_rng = get_avg_pdif_ranged(player_rangedattack, rng_type_skill, pdl_trait, pdl_gear, enemy_def, crit_rate)

            ranged_hit_damage = get_avg_phys_damage(rng_dmg+ammo_dmg, fstr_rng, wsc, avg_pdif_rng, ftp,  crit_rate, crit_dmg, wsd, ws_bonus, ws_trait) # The amount of damage done by the first hit of the WS if it does not miss
            ranged_hit_damage2 = get_avg_phys_damage(rng_dmg+ammo_dmg, fstr_rng, wsc, avg_pdif_rng, ftp2,  crit_rate, crit_dmg, 0, ws_bonus, ws_trait) # Hits after the first main hit (jishnu hits 2+3. Last stand hit 2, etc)
            phys = ranged_hit_damage*hitrate_ranged1 + ranged_hit_damage2*hitrate_ranged2*(nhits-1)
            phys *= (1+true_shot)


        damage += phys

        if hybrid:
            # Calculate the magic multiplier for the magical part of Hybrid weapon skills
            # https://www.ffxiah.com/forum/topic/51313/tachi-jinpu-set/
            magic_hit_rate = get_magic_hit_rate(magic_accuracy, enemy_meva) if enemy_meva > 0 else 1.0
            resist_state = get_resist_state_average(magic_hit_rate)

            dayweather = 1.0
            if gearset.gear["waist"]["Name"]=="Hachirin-no-Obi":
              if main_job == "SCH":
                dayweather = 1.25
              elif sub_job == "SCH":
                dayweather = 1.1

            affinity = 1 + 0.05*gearset.playerstats[f'{element} Affinity'] + 0.05*(gearset.playerstats[f'{element} Affinity']>0) # Affinity Bonus. Only really applies to Magian Trial staves. Archon Ring is different.
            #dayweather = 1.0 # 0.65, 0.8, 0.9, 1.0, 1.1, 1.2, 1.35. Assume no day/weather bonus/penalty.
            magic_attack_ratio = (100 + player_mab) / (100 + enemy_mdb)
            enemy_mdt = 1.0 # Usually 1.0 unless the enemy casts shell or a similar spell/ability.

            magic_multiplier = affinity*resist_state*dayweather*magic_attack_ratio*enemy_mdt*element_magic_attack_bonus
            magical_damage = (phys*ftp_hybrid + player_magic_damage)*magic_multiplier*(1+wsd)*(1+ws_bonus)

            damage += magical_damage

        damage *= (1 + hover_shot)

        return(damage, 0) # Return the average damage dealt and 0 TP return.

    # This marks the end of the damage calculation for average estimates. We'll start the proper simulations next.


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

        if not phys_rng_ws:
            # Calculate hit rates for the natural main- and sub-hits (the first of each get a ~+100 Accuracy bonus).
            # Future main- and off-hand hits do not get accuracy+100 (n!=0).
            hitrate1 = get_hitrate(player_accuracy1, ws_acc, enemy_eva, 'main', n==0, main_type_skill)
            hitrate2 = get_hitrate(player_accuracy2, ws_acc, enemy_eva,  'sub', n==0, sub_type_skill)

            if sneak_attack or trick_attack and n==0: # only the first hit gets 100% hit rate with SA/TA
                hitrate1 = 1.0
                hitrate2 = 1.0

            # Check if your hit lands
            if np.random.uniform() < hitrate1:
                if n == 0:
                    mainhit = True # The first main hit successfully landed so it provides full TP. (n=0 is the first main hit)
                else:
                    ma_tp_hits += 1 # Number of hits that provide 10 TP (multiplied by STP later)


                if (sneak_attack or trick_attack or climactic_flourish) and n==0:
                    crit_dmg2 = crit_dmg + 0.3*vajra_bonus + 0.31*dnc_empy_head_bonus # It's unclear to me if DNC Empy+3 head allows a 2nd WS hit to crit. For now I assume not.
                else:
                    crit_dmg2 = crit_dmg

                pdif1, crit = get_pdif_melee(player_attack1, main_type_skill, pdl_trait, pdl_gear, enemy_def, max( sneak_attack*(n==0), trick_attack*(n==0), climactic_flourish*(n==0), (crit_rate+0.7*dnc_empy_body_bonus*(n==0)*(crit_rate>0)) ) ) # Calculate the PDIF for this swing of the main-hand weapon. Return whether or not that hit was a crit.

                # Reminder that crit=True/False and is decided in the pdif function above.
                physical_damage = get_phys_damage(main_dmg, fstr_main, wsc, pdif1, ftp, crit, crit_dmg2, wsd, ws_bonus, ws_trait, n, sneak_attack_bonus, trick_attack_bonus, climactic_flourish_bonus, striking_flourish_bonus, ternary_flourish_bonus) # Calculate the physical damage dealt by a single hit. The first hit gets WSD and SA/TA bonuses
                damage += physical_damage

            # Bonus hit for dual-wielding.
            # The dual-wielding hit occurs immediately after first main-hit. This can be confirmed by watching your in-game TP return.
            if total_hits < 8 and dual_wield and n == 0: # By necessity of order-of-operations, total_hits==1 right now, so we can remove the "total_hits < 8" bit. TODO
                total_hits += 1 # You are starting to try to hit with your off-hand weapon, add one to the total hits.
                if np.random.uniform() < hitrate2:
                    subhit = True # For TP return. The successful sub-hit gets full TP
                    pdif2, crit = get_pdif_melee(player_attack2, sub_type_skill, pdl_trait, pdl_gear, enemy_def, crit_rate) # Calculate the pdif for this off-hand hit. Return whether or not it was a crit.
                    physical_damage = get_phys_damage(sub_dmg, fstr_sub, wsc, pdif2, ftp2, crit, crit_dmg, 0, ws_bonus, ws_trait, 1) # Calculate its damage. Notice that subhit uses ftp2 and wsd=0.
                    damage += physical_damage

        else:
            hitrate_ranged = get_hitrate(player_rangedaccuracy, ws_acc, enemy_eva, "ranged", n==0, rng_type_skill)

            if np.random.uniform() < hitrate_ranged:
                if n == 0:
                    mainhit = True # The first main hit successfully landed so it provides full TP. (n=0 is the first main hit)
                else:
                    ma_tp_hits += 1 # Number of hits that provide 10 TP (multiplied by STP later)

                pdif_rng, crit = get_pdif_ranged(player_rangedattack, rng_type_skill, pdl_trait, pdl_gear, enemy_def, crit_rate) # Calculate the PDIF for this shot of the ranged weapon. Return whether or not that hit was a crit.
                physical_damage = get_phys_damage(rng_dmg+ammo_dmg, fstr_rng, wsc, pdif_rng, ftp, crit, crit_dmg, wsd*(n==0), ws_bonus, ws_trait, n) # Calculate the physical damage dealt by a single hit. The first hit gets WSD.
                damage += physical_damage*(1+true_shot)


            # This is the last line of the natural main/sub-hit for-loop. We'll check our two multi-attack procs next. We skip those for ranged weaponskills.


    # This part checks for multi-attack procs. It does so after all of the natural main-hits and the one sub-hit
    if total_hits < 8 and not phys_rng_ws: # Don't bother with this section at all if using a physical ranged WS

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
            hitrate1 = get_hitrate(player_accuracy1, ws_acc, enemy_eva, 'main', False, main_type_skill)
            hitrate2 = get_hitrate(player_accuracy2, ws_acc, enemy_eva,  'sub', False, sub_type_skill)

            # Sneak and Trick attacks do not affect accuracy of the multi-attack hits

            # Check multi-attacks in order:
            # Quad > Triple > Double > OA3 > OA2 > Single
            # Kclub is not checked here.

            if striking_flourish and (i==0): # The first main hit is forced to DA. No QA/TA allowed
                da_main = 1.0
                ta_main = 0
                qa_main = 0
            elif ternary_flourish and (i==0): # The first main hit is forced to TA. No QA/DA allowed
                da_main = 0
                ta_main = 1.0
                qa_main = 0
            else:
                da_main = da
                ta_main = ta
                qa_main = qa


            if np.random.uniform() < qa_main and ma_count_limit < 2:
                # If you rolled lower than your quadruple attack %, then you perform a quadruple attack.
                ma_count_limit += 1 # This counts as one of your two allowed multi-attack procs, even if you can only swing once out of the whole QA proc due to the 8-hit limit
                physical_damage, ma_tp_hits, total_hits = multiattack_check(i, 3, ma_tp_hits, total_hits, player_attack1, main_type_skill, pdl_trait, pdl_gear, enemy_def, crit_rate, main_dmg, fstr_main, wsc, ftp2, crit_dmg, ws_bonus, ws_trait, hitrate1)
                damage += physical_damage
            elif np.random.uniform() < ta_main and ma_count_limit < 2: # If you failed the quadruple attack check, then try a triple attack.
                ma_count_limit += 1
                physical_damage, ma_tp_hits, total_hits = multiattack_check(i, 2, ma_tp_hits, total_hits, player_attack1, main_type_skill, pdl_trait, pdl_gear, enemy_def, crit_rate, main_dmg, fstr_main, wsc, ftp2, crit_dmg, ws_bonus, ws_trait, hitrate1)
                damage += physical_damage
            elif np.random.uniform() < da_main and ma_count_limit < 2: # If you failed the triple attack check, then you get to try a double attack roll.
                ma_count_limit += 1
                striking_crit_rate = crit_rate+0.7*dnc_empy_body_bonus*(crit_rate>0)*(i==0) # Calculate the crit rate of this free Double Attack hit if striking flourish and empy body are both equipped.
                physical_damage, ma_tp_hits, total_hits = multiattack_check(i, 1, ma_tp_hits, total_hits, player_attack1, main_type_skill, pdl_trait, pdl_gear, enemy_def, striking_crit_rate, main_dmg, fstr_main, wsc, ftp2, crit_dmg, ws_bonus, ws_trait, hitrate1) # Striking Flourish boosts the crit rate with empy+3 head, but does not supply the +100% CHR
                damage += physical_damage
            elif np.random.uniform() < oa3_main and ma_count_limit < 2: # If you failed double attack, then you get to try OA3 roll (skipping OA8, OA7, OA6, etc)
                ma_count_limit += 1
                physical_damage, ma_tp_hits, total_hits = multiattack_check(i, 2, ma_tp_hits, total_hits, player_attack1, main_type_skill, pdl_trait, pdl_gear, enemy_def, crit_rate, main_dmg, fstr_main, wsc, ftp2, crit_dmg, ws_bonus, ws_trait, hitrate1)
                damage += physical_damage
            elif np.random.uniform() < oa2_main and ma_count_limit < 2: # If you failed OA3, try OA2.
                ma_count_limit += 1
                physical_damage, ma_tp_hits, total_hits = multiattack_check(i, 1, ma_tp_hits, total_hits, player_attack1, main_type_skill, pdl_trait, pdl_gear, enemy_def, crit_rate, main_dmg, fstr_main, wsc, ftp2, crit_dmg, ws_bonus, ws_trait, hitrate1)
                damage += physical_damage

        # Now check multi-attacks for the off-hand.
        # Note that this part is set up without OA3 and OA2 because the occasional attacks N times stat only applies to the weapon that has it.
        # In this case, the only weapon that I have coded with this is Nagi, which only works main hand anyway.
        # This will need to be changed if we get ilvl Magian weapons with occasionally attacks X.
        # This does not deal with "follow-up" attacks from things like Fudo Masamune (but this is where you'd throw that check in if you wanted to)
        if dual_wield: # If you have an off-hand weapon equipped, then it gets one of your two multi-attack procs. Check that multi-attack proc now.
            if np.random.uniform() < qa and ma_count_limit < 2:
                ma_count_limit += 1
                ma_damage, ma_tp_hits, total_hits = multiattack_check(100, 3, ma_tp_hits, total_hits, player_attack2, sub_type_skill, pdl_trait, pdl_gear, enemy_def, crit_rate, sub_dmg, fstr_sub, wsc, ftp2, crit_dmg, ws_bonus, ws_trait, hitrate2)
                damage += ma_damage
            elif np.random.uniform() < ta and ma_count_limit < 2:
                ma_count_limit += 1
                ma_damage, ma_tp_hits, total_hits = multiattack_check(100, 2, ma_tp_hits, total_hits, player_attack2, sub_type_skill, pdl_trait, pdl_gear, enemy_def, crit_rate, sub_dmg, fstr_sub, wsc, ftp2, crit_dmg, ws_bonus, ws_trait, hitrate2)
                damage += ma_damage
            elif np.random.uniform() < da and ma_count_limit < 2:
                ma_count_limit += 1
                ma_damage, ma_tp_hits, total_hits = multiattack_check(100, 1, ma_tp_hits, total_hits, player_attack2, sub_type_skill, pdl_trait, pdl_gear, enemy_def, crit_rate, sub_dmg, fstr_sub, wsc, ftp2, crit_dmg, ws_bonus, ws_trait, hitrate2)
                damage += ma_damage
            elif np.random.uniform() < oa8_sub and ma_count_limit < 2: # If you failed double attack, then you get to try OA3 roll (skipping OA8, OA7, OA6, etc)
                ma_count_limit += 1
                physical_damage, ma_tp_hits, total_hits = multiattack_check(100, 7, ma_tp_hits, total_hits, player_attack2, sub_type_skill, pdl_trait, pdl_gear, enemy_def, crit_rate, main_dmg, fstr_sub, wsc, ftp2, crit_dmg, ws_bonus, ws_trait, hitrate2)
                damage += physical_damage
            elif np.random.uniform() < oa7_sub and ma_count_limit < 2: # If you failed double attack, then you get to try OA3 roll (skipping OA8, OA7, OA6, etc)
                ma_count_limit += 1
                physical_damage, ma_tp_hits, total_hits = multiattack_check(100, 6, ma_tp_hits, total_hits, player_attack2, sub_type_skill, pdl_trait, pdl_gear, enemy_def, crit_rate, main_dmg, fstr_sub, wsc, ftp2, crit_dmg, ws_bonus, ws_trait, hitrate2)
                damage += physical_damage
            elif np.random.uniform() < oa6_sub and ma_count_limit < 2: # If you failed double attack, then you get to try OA3 roll (skipping OA8, OA7, OA6, etc)
                ma_count_limit += 1
                physical_damage, ma_tp_hits, total_hits = multiattack_check(100, 5, ma_tp_hits, total_hits, player_attack2, sub_type_skill, pdl_trait, pdl_gear, enemy_def, crit_rate, main_dmg, fstr_sub, wsc, ftp2, crit_dmg, ws_bonus, ws_trait, hitrate2)
                damage += physical_damage
            elif np.random.uniform() < oa5_sub and ma_count_limit < 2: # If you failed double attack, then you get to try OA3 roll (skipping OA8, OA7, OA6, etc)
                ma_count_limit += 1
                physical_damage, ma_tp_hits, total_hits = multiattack_check(100, 4, ma_tp_hits, total_hits, player_attack2, sub_type_skill, pdl_trait, pdl_gear, enemy_def, crit_rate, main_dmg, fstr_sub, wsc, ftp2, crit_dmg, ws_bonus, ws_trait, hitrate2)
                damage += physical_damage
            elif np.random.uniform() < oa4_sub and ma_count_limit < 2: # If you failed double attack, then you get to try OA3 roll (skipping OA8, OA7, OA6, etc)
                ma_count_limit += 1
                physical_damage, ma_tp_hits, total_hits = multiattack_check(100, 3, ma_tp_hits, total_hits, player_attack2, sub_type_skill, pdl_trait, pdl_gear, enemy_def, crit_rate, main_dmg, fstr_sub, wsc, ftp2, crit_dmg, ws_bonus, ws_trait, hitrate2)
                damage += physical_damage
            elif np.random.uniform() < oa3_sub and ma_count_limit < 2: # If you failed double attack, then you get to try OA3 roll (skipping OA8, OA7, OA6, etc)
                ma_count_limit += 1
                physical_damage, ma_tp_hits, total_hits = multiattack_check(100, 2, ma_tp_hits, total_hits, player_attack2, sub_type_skill, pdl_trait, pdl_gear, enemy_def, crit_rate, main_dmg, fstr_sub, wsc, ftp2, crit_dmg, ws_bonus, ws_trait, hitrate2)
                damage += physical_damage
            elif np.random.uniform() < oa2_sub and ma_count_limit < 2: # If you failed double attack, then you get to try OA3 roll (skipping OA8, OA7, OA6, etc)
                ma_count_limit += 1
                physical_damage, ma_tp_hits, total_hits = multiattack_check(100, 1, ma_tp_hits, total_hits, player_attack2, sub_type_skill, pdl_trait, pdl_gear, enemy_def, crit_rate, main_dmg, fstr_sub, wsc, ftp2, crit_dmg, ws_bonus, ws_trait, hitrate2)
                damage += physical_damage

    phys = damage
    # This is the last line of the physical portion.


    # If the weapon skill is labeled as a hybrid, then calculate the magic portion and add it to the total damage here.
    if hybrid:
        # Calculate the magic multiplier for the magical part of Hybrid weapon skills
        # https://www.ffxiah.com/forum/topic/51313/tachi-jinpu-set/
        magic_hit_rate = get_magic_hit_rate(magic_accuracy, enemy_meva) if enemy_meva > 0 else 1.0
        resist_state = get_resist_state_average(magic_hit_rate) # TODO: Use a randomizer instead of the average resist state for hybrid simulations.

        dayweather = 1.0
        if gearset.gear["waist"]["Name"]=="Hachirin-no-Obi":
          if main_job == "SCH":
            dayweather = 1.25
          elif sub_job == "SCH":
            dayweather = 1.1

        affinity = 1 + 0.05*gearset.playerstats[f'{element} Affinity'] + 0.05*(gearset.playerstats[f'{element} Affinity']>0)
        #dayweather = 1.0
        magic_attack_ratio = (100 + player_mab) / (100 + enemy_mdb)
        enemy_mdt = 1.0
        magic_multiplier = affinity*resist_state*dayweather*magic_attack_ratio*enemy_mdt*element_magic_attack_bonus

        magical_damage = (phys*ftp_hybrid + player_magic_damage)*magic_multiplier*(1+wsd)*(1+ws_bonus)*(1+ws_trait)
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

def test_set(main_job, sub_job, ws_name, enemy, buffs, equipment, gearset, tp1, tp2, tp0, n_simulations, show_final_plot, nuke, spell, job_abilities, burst=False, final=False, check_tp_set=False):
    damage = []
    tp_return = []
    if nuke:
        show_final_plot = False
    if final:
        # final is always false for check_tp_set=True
        for k in range(n_simulations):

            tp = np.random.uniform(tp1,tp2)
            values = weaponskill(main_job, sub_job, ws_name, enemy, gearset, tp1, tp2, tp0, buffs, equipment, nuke, spell, job_abilities, burst, final, check_tp_set=False)
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
            plot_final(damage, gearset, tp1, tp2, ws_name, main_job, sub_job)
        return()
    else:
        tp = np.average([tp1,tp2])
        damage, tp = weaponskill(main_job, sub_job, ws_name, enemy, gearset, tp1, tp2, tp0, buffs, equipment, nuke, spell, job_abilities, burst, final, check_tp_set)
        return(damage, tp)



def run_weaponskill(main_job, sub_job, ws_name, mintp, maxtp, tp0, n_iter, n_simulations, check_gear, check_slots, buffs, enemy, starting_gearset, show_final_plot, nuke, spell, job_abilities, conditions, burst=False, check_tp_set=False):

    # We use this ws_dict to ensure that the main-hand weapon matches the WS being used.
    ws_dict = {"Katana": ["Blade: Chi", "Blade: Hi", "Blade: Kamu", "Blade: Metsu", "Blade: Shun", "Blade: Ten", "Blade: Ku", "Blade: Ei", "Blade: Yu", "Blade: Retsu","Blade: Jin","Blade: Teki", "Blade: To"],
                "Great Katana": ["Tachi: Rana", "Tachi: Fudo", "Tachi: Kaiten", "Tachi: Shoha", "Tachi: Kasha", "Tachi: Gekko", "Tachi: Jinpu", "Tachi: Koki", "Tachi: Goten", "Tachi: Kagero","Tachi: Enpi","Tachi: Yukikaze"],
                "Dagger": ["Evisceration", "Exenterator", "Mercy Stroke", "Aeolian Edge", "Rudra's Storm", "Shark Bite", "Dancing Edge", "Mordant Rime","Mandalic Stab","Pyrrhic Kleos", "Viper Bite"],
                "Sword": ["Savage Blade", "Expiacion", "Death Blossom", "Chant du Cygne", "Knights of Round", "Sanguine Blade", "Seraph Blade","Red Lotus Blade","Requiescat","Circle Blade","Swift Blade","Fast Blade","Burning Blade","Fast Blade II"],
                "Scythe": ["Insurgency", "Cross Reaper", "Entropy", "Quietus", "Catastrophe","Infernal Scythe","Shadow of Death","Dark Harvest","Spiral Hell","Slice","Spinning Scythe","Guillotine"],
                "Great Sword":["Torcleaver","Scourge","Resolution","Freezebite", "Herculean Slash","Ground Strike","Dimidiation","Shockwave","Sickle Moon","Spinning Slash","Hard Slash"],
                "Club":["Hexa Strike","Realmrazer","Seraph Strike","Randgrith","Black Halo","Judgment","Exudation","Shining Strike","True Strike","Mystic Boon"],
                "Polearm":["Stardiver", "Impulse Drive", "Penta Thrust", "Geirskogul", "Drakesbane", "Camlann's Torment","Raiden Thrust","Thunder Thrust","Wheeling Thrust", "Sonic Thrust","Double Thrust"],
                "Staff":["Cataclysm","Shattersoul","Earth Crusher","Vidohunir","Retribution","Full Swing","Sunburst","Heavy Swing","Starburst","Gate of Tartarus","Rock Crusher","Omniscience"],
                "Great Axe":["Ukko's Fury", "Upheaval", "Metatron Torment", "King's Justice","Raging Rush","Fell Cleave","Steel Cyclone","Iron Tempest"],
                "Axe":["Cloudsplitter","Ruinator","Decimation","Rampage","Primal Rend","Mistral Axe","Onslaught","Calamity","Bora Axe","Spinning Axe","Raging Axe"],
                "Archery":["Empyreal Arrow", "Flaming Arrow", "Namas Arrow","Jishnu's Radiance","Apex Arrow","Refulgent Arrow","Sidewinder","Blast Arrow","Piercing Arrow"],
                "Marksmanship":["Last Stand","Hot Shot","Leaden Salute","Wildfire","Coronach","Trueflight", "Detonator","Blast Shot","Slug Shot","Split Shot"],
                "Hand-to-Hand":["Raging Fists","Howling Fist","Dragon Kick","Asuran Fists","Tornado Kick","Shijin Spiral","Final Heaven","Victory Smite","Ascetic's Fury","Stringing Pummel","Spinning Attack","Combo","One Inch Punch"],
                "None":["This is only used when the weapon slot is Empty. Using this entry to skip sets with empty main hand. Will need to remove it later for the Bonanza bow."]}

    tcount = 0 # Total number of valid sets checked. Useless, but interesting to see. A recent Blade: Ten run checked 84,392 sets
    for k in starting_gearset:
        # print(starting_gearset[k])
        if main_job.lower() not in starting_gearset[k]["Jobs"]:
            starting_gearset[k] = Empty # Unequip gear you can't wear if it's already equipped.

    # Define JSE earrings now. We'll use them later to prevent Balder's Earring+1 and a JSE+2 being equipped at the same time since we ignore right_ear requirement for testing.
    jse_ears = [k + " Earring +2" for k in ["Hattori", "Heathen's", "Lethargy", "Ebers", "Wicce", "Peltast's", "Boii", "Bhikku", "Skulkers", "Chevalier's", "Nukumi", "Fili", "Amini", "Kasuga", "Beckoner's", "Hashishin", "Chasseur's", "Karagoz", "Maculele", "Arbatel", "Azimuth", "Erilaz"]]

    if nuke:
        show_final_plot = False
        # TODO: Don't show final plot if using magical WS either. Maybe just compare ws_name to a list of magical WSs

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
    elif check_tp_set:
        print(f"Checking TP set: WS at {tp1} TP")
    else:
        print(f"Checking:  {ws_name}  TP=[{tp1},{tp2}]")
    print("---------------")



    # We only check for PDT and MDT.
    # It seems that checking for extra conditions requires extra gear to be swapped simultaneously.
    # So adding Subtle Blow would require swapping 3 pieces at once, which could make this process take many minutes to find the best set.

    pdt = 100 # How much PDT the set has
    mdt = 100

    conditional_converge_count = 0 # This uses a while loop, so if we don't add a condition to break out, then it'll run forever trying to find 1% more DT that doesn't exist.
    pdt_old = 100 # Used to check if the automatic set finder gets stuck trying to find a set that doesn't exist. Compare this value to the old value. If no change in 3 consecutive iterations, then break out.
    mdt_old = 100

    pdt_thresh = conditions["PDT"] # How much PDT the final set is aiming for, taken from the user input.
    mdt_thresh = conditions["MDT"]

    pdt_thresh_temp = 100 # How much PDT the current new set must have to be accepted. This line is just to ensure the while-loop runs.
    mdt_thresh_temp = 100


    nconverge = 1 # Number of consecutive iterations resulting in insignificant damage improvements before code returns the best set.
    while pdt > pdt_thresh or mdt > mdt_thresh:
        print(f"\nChecking conditions: PDT:{pdt_thresh_temp},  MDT:{mdt_thresh_temp}")

        # Start the code.
        converge_count = 0 # Count for convergence (number of times the change between iterations was <0.1% for example; see near the end of this code for the exact value used)
        best_damage = 0 # Highest WS damage. Used to find "best" WS sets
        best_time = 999 # Lowest time to WS. Used to find "best" TP sets
        damage_list = np.ones(n_iter) # Nothing to do with plotting. This is for checking how the damage changed between consecutive iterations.
        time_list = np.ones(n_iter) # Nothing to do with plotting. This is for checking how the time to WS changed between consecutive iterations.


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

                        # print(new_set["main"],new_set["sub"])

                        # new_set is the set that's being adjusted/tested.
                        for k in new_set:
                            # Assign a Name2 to all gear to clean up the later code. We did this for "Best_Gearset" already, though...
                            # Probably best to add "Name2" to all equipment pieces in the gear.py file at the end.  TODO (to do later. Already done? Can delete all of these Name checks)
                            name2 = new_set[k].get('Name2','None')
                            if name2 == 'None':
                                new_set[k].update({'Name2': new_set[k]['Name']})
                        #     print(new_set[k]["Name2"])
                        # print("-------")


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

                                    # Each piece of gear selected for this iteration will now be equipped.
                                    # We will consider the validity of the set AFTER things have been equipped.
                                    new_set[slot1]  = b  # Equip swap_item1 to slot1
                                    new_set[slot2]  = b2 # Equip swap_item2 to slot2
                                    new_set[slot3]  = b3 # Equip swap_item3 to slot3

                                    # print(b["Name2"], b2["Name2"])

                                    # Do not equip two of the same item in rings, earrings, and main+sub slots.
                                    # Items in these slots can be placed in either of their pair.
                                    # 1-handed weapons can go in Main+Sub if dual wielding.
                                    # Rings can go in either ring slot.
                                    # Earrings can go in either earring slot.
                                    # I use Mache Earring +1 A and B to get around this for non-rare items.
                                    if new_set["ring1"]["Name2"] == new_set["ring2"]["Name2"]:
                                        if new_set["ring1"]["Name2"] != "Empty":
                                            # print("test1: ring1 and ring2 same and not empty")
                                            continue
                                    if new_set["ear1"]["Name2"] == new_set["ear2"]["Name2"]:
                                        if new_set["ear1"]["Name2"] != "Empty":
                                            # print("test2: ear1 and ear2 same and not empty")
                                            continue
                                    if new_set["main"]["Name2"] == new_set["sub"]["Name2"]:
                                        if new_set["main"]["Name2"] != "Empty": # Allow both weapons to be Empty. This is to test the bonanza bow later for fun.
                                            # print("test3: main and sub are same weapon and not empty")
                                            continue

                                    # Only check gear that your main job can equip.
                                    for new_slot in new_set:
                                        if main_job.lower() not in new_set[new_slot]["Jobs"]:
                                            # print("test4")
                                            continue


                                    # Do not test 1-handed weapons with grips.
                                    one_handed = ["Axe", "Club", "Dagger", "Sword", "Katana"]
                                    if new_set["main"]["Skill Type"] in one_handed and new_set["sub"]["Type"] == "Grip":
                                        # print("test5: 1h weapon with a grip")
                                        continue
                                    # Do not allow 2-handed weapons with shields or 1-handed weapons.
                                    two_handed = ["Great Sword", "Great Katana", "Great Axe", "Polearm", "Scythe", "Staff"]
                                    if new_set["main"]["Skill Type"] in two_handed and (new_set["sub"]["Type"]=="Weapon" or new_set["sub"]["Type"]=="Shield"):
                                        # print("test6: 2h weapon with a grip or shield")
                                        continue

                                    # Do not equip H2H weapon with an off-hand item.
                                    if new_set["main"]["Skill Type"] == "Hand-to-Hand" and new_set["sub"]["Name"] != "Empty":
                                        # print("test18: h2h main without empty sub")
                                        continue

                                    # Require that a ranged weapon that matches your selected ranged weapon skill be equipped IF you're using a ranged weapon skill.
                                    # This prevents something like Seething Bomblet +1 R15 from being BiS for Empyreal Arrow for some reason.
                                    archery = ["Empyreal Arrow", "Jishnu's Radiance", "Flaming Arrow", "Namas Arrow","Apex Arrow","Refulgent Arrow"]
                                    marksmanship = ["Coronach","Last Stand","Hot Shot", "Leaden Salute", "Wildfire", "Trueflight","Detonator"]
                                    if ws_name in archery:
                                        if new_set["ranged"]["Skill Type"] != "Archery":
                                            # print("test8: using a bow WS without a bow")
                                            continue
                                    if ws_name in marksmanship:
                                        if new_set["ranged"]["Skill Type"] != "Marksmanship":
                                            # print("test9: using a gun WS without a gun")
                                            continue

                                    # Do not allow dual wielding unless NIN, DNC, THF main or subjobs.
                                    if main_job not in ["NIN", "DNC", "THF", "BLU"] and sub_job not in ["NIN", "DNC"]:
                                        if new_set["sub"]["Type"] == "Weapon":
                                            # print("test10: dual wielding without trait")
                                            continue

                                    # Do not equip an ammo incompatible with your ranged weapon
                                    if new_set["ranged"].get("Type","None")=="Gun" and new_set["ammo"].get("Type","None") not in ["Bullet","None"]:
                                        # print("test11: gun without bullet/none")
                                        continue

                                    if new_set["ranged"].get("Type","None")=="Bow" and new_set["ammo"].get("Type","None") not in ["Arrow","None"]:
                                        # print("test12: bow without arrow/none")
                                        continue

                                    if (ws_name in marksmanship or ws_name in archery or spell=="Ranged Attack"):
                                        if new_set["ranged"]["Type"]=="Gun" and new_set["ammo"]["Type"]!="Bullet":
                                            # print("test12: Ammo type must match weapon type")
                                            continue
                                        if new_set["ranged"]["Type"]=="Crossbow" and new_set["ammo"]["Type"]!="Bolt":
                                            # print("test12: Ammo type must match weapon type")
                                            continue
                                        if new_set["ranged"]["Type"]=="Bow" and new_set["ammo"]["Type"]!="Arrow":
                                            # print("test12: Ammo type must match weapon type")
                                            continue

                                    # Equipping a bullet requires a gun to be equipped. (or a crossbow with a bolt)
                                    if new_set["ammo"].get("Type","None") == "Bullet" and new_set["ranged"].get("Type","None") != "Gun":
                                        # print("test13: bullet without gun")
                                        continue

                                    # Equipping an arrow requires a bow to be equipped.
                                    if new_set["ammo"].get("Type","None") == "Arrow" and new_set["ranged"].get("Type","None") != "Bow":
                                        # print("test14: arrow without bow")
                                        continue

                                    # Equipping an bolt requires a crossbow to be equipped.
                                    if new_set["ammo"].get("Type","None") == "Bolt" and new_set["ranged"].get("Type","None") != "Crossbow":
                                        # print("test14 2: bolt without crossbow")
                                        continue

                                    # Do not equip ammo if you equip an instrument (Linos).
                                    if new_set["ranged"].get("Type","None") == "Instrument" and new_set["ammo"].get("Type","None") != "None":
                                        # print("test15: instrument and equipement ")
                                        continue


                                    # Do not equip Balder Earring +1 and the JSE +2 ears at the same time. They both only work if in the right ear.
                                    if new_set["ear1"]["Name2"] in jse_ears and new_set["ear2"]["Name2"] == "Balder Earring +1":
                                        # print("test16: JSE and Balder both equipped ear1")
                                        continue
                                    if new_set["ear2"]["Name2"] in jse_ears and new_set["ear1"]["Name2"] == "Balder Earring +1":
                                        # print("test17: JSE and Balder both equipped ear2")
                                        continue

                                    # "Cannot equip headgear" armor is checked here.
                                    if new_set["body"]["Name2"] in ["Cohort Cloak +1 R15"] and new_set["head"]["Name"] != "Empty":
                                        # print("test18: Cohort cloak and head equipped")
                                        continue

                                    # Some weapon skills require specific weapons to be equipped for use.
                                    restricted_ws = {"Blade: Metsu":"Kikoku",
                                                    "Final Heaven":"Spharai",
                                                    "Mercy Stroke":"Mandau",
                                                    "Knights of Round":"Excalibur",
                                                    "Scourge":"Ragnarok",
                                                    "Onslaught":"Guttler",
                                                    "Metatron Torment":"Bravura",
                                                    "Catastrophe":"Apocalypse",
                                                    "Geirskogul":"Gungnir",
                                                    "Tachi: Kaiten":"Amanomurakumo",
                                                    "Randgrith":"Mjollnir",
                                                    "Gates of Tartarus":"Claustrum",
                                                    "Namas Arrow":"Yoichinoyumi",
                                                    "Coronach":"Annihilator",
                                                    "Fast Blade II":"Onion Sword III"}
                                    if ws_name in restricted_ws and not (check_tp_set or nuke):
                                        if restricted_ws[ws_name] not in new_set["main"]["Name2"] and restricted_ws[ws_name] not in new_set["ranged"]["Name2"]:
                                            # print("weapon restriction test1")
                                            continue

                                    # Do not test main-hand weapons that can't use the selected WS, if they are selected.
                                    # Does not apply if using "Run Magic" or "Quicklook Magic" for nukes.
                                    # Does not apply to ranged weapon skills.
                                    if not nuke:
                                        if ws_name not in ws_dict[new_set["main"]["Skill Type"]] and ws_name not in ws_dict["Archery"]+ws_dict["Marksmanship"]:
                                            # print("test19: ",f"{new_set['main']['Name2']} can't use {ws_name}.")
                                            continue


                                    # At this point, you SHOULD have a valid gear set.
                                    # Now we actually test the approximate damage using averages.

                                    # Don't even test the set if the DT requirement is not met in both PDT and MDT
                                    pdt = 0
                                    mdt = 0 - 29*job_abilities["shell v"] # If WHM is selected on the GUI, then assume you have shell V active
                                    for slot in new_set:
                                        pdt += new_set[slot].get("PDT",0) + new_set[slot].get("DT",0) + new_set[slot].get("PDT2",0)
                                        mdt += new_set[slot].get("MDT",0) + new_set[slot].get("DT",0)
                                    if pdt > pdt_thresh_temp or mdt > mdt_thresh_temp:
                                        continue

                                    test_Gearset = set_gear(buffs, new_set, main_job, sub_job, job_abilities=job_abilities) # This line turns that gear dictionary into a Python class, formalizing the player stats.
                                                                            # This contains the player and gear stats as well as a list of gear equipped in each slot that can be easily printed


                                    if not check_tp_set: # If not checking TP set (checking WS or Nuke set), then use "damage" as indicator of quality

                                        # Test the set and return its damage as a single number
                                        damage, tp = test_set(main_job, sub_job, ws_name, enemy, buffs, new_set, test_Gearset, tp1, tp2, tp0, n_simulations, show_final_plot, nuke, spell, job_abilities, burst, False, check_tp_set)
                                        damage = int(damage)
                                        # print(b["Name2"], b2["Name2"], damage)

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
                                    else:
                                        # Test the set and return its damage as a single number
                                        time_to_ws, tp = test_set(main_job, sub_job, ws_name, enemy, buffs, new_set, test_Gearset, tp1, tp2, tp0, n_simulations, show_final_plot, nuke, spell, job_abilities, burst, False, check_tp_set)
                                        # print(b["Name2"], b2["Name2"], time_to_ws)

                                        tcount += 1
                                        # if slot1==slot2:
                                        #     print(slot1, swap_item1,damatime_to_wsge)
                                        # else:
                                        #     print(slot1, slot2, swap_item1, swap_item2, time_to_ws)

                                        # If the damage returned after swapping those 1~3 pieces is higher than the previous best, then run this next bit of code to print the swap that was performed and the change in damage observed.
                                        if time_to_ws < best_time:
                                            if (swap_item1 == swap_item2) and (swap_item1 == swap_item3):
                                                print(f"[{check_slots[i]:<15s}]: {equipped_item1} -> {swap_item1} [{best_time:>6.2f} -> {time_to_ws:>6.2f}]") # Print the new best item and it's statistic
                                            elif fitn==2 and swap_item1==equipped_item1:
                                                print(f"[{check_slots[i2]:<15s}]: {equipped_item2} -> {swap_item2} [{best_time:>6.2f} -> {time_to_ws:>6.2f}]") # Print the new best item and it's statistic
                                            elif fitn==2 and swap_item2==equipped_item2:
                                                print(f"[{check_slots[i]:<15s}]: {equipped_item1} -> {swap_item1} [{best_time:>6.2f} -> {time_to_ws:>6.2f}]") # Print the new best item and it's statistic



                                            elif (swap_item1 == swap_item2) and (swap_item1 != swap_item3):
                                                print(f"[{check_slots[i]:<6s} & {check_slots[i3]:<6s}]: [{equipped_item1} & {equipped_item3}] -> [{swap_item1} & {swap_item3}] [{best_time:>6.2f} -> {time_to_ws:>6.2f}]") # Print the new best damage and the new item that led to this new record

                                            elif (swap_item1 == swap_item3) and (swap_item1 != swap_item2):
                                                print(f"[{check_slots[i]:<6s} & {check_slots[i2]:<6s}]: [{equipped_item1} & {equipped_item2}] -> [{swap_item1} & {swap_item2}] [{best_time:>6.2f} -> {time_to_ws:>6.2f}]")

                                            elif (swap_item2 == swap_item3) and (swap_item1 != swap_item2):
                                                print(f"[{check_slots[i]:<6s} & {check_slots[i2]:<6s}]: [{equipped_item1} & {equipped_item2}] -> [{swap_item1} & {swap_item2}] [{best_time:>6.2f} -> {time_to_ws:>6.2f}]")


                                            # No plans to fit 3 pieces simultaneously again. Commenting out this bit of code that prints the swaps
                                            # elif (swap_item2 != swap_item3) and (swap_item1 != swap_item2) and (swap_item1 != swap_item3):
                                            #     print(f"[{check_slots[i]} & {check_slots[i2]} & {check_slots[i3]}]: [{equipped_item1} & {equipped_item2} & {equipped_item3}] -> [{swap_item1} & {swap_item2} & {swap_item3}] [{best_time:>6.2f} -> {time_to_ws:>6.2f}]")

                                            # If your new set is better than your previous best set, then:
                                            best_time = time_to_ws    # Save the best time to compare with future test gearsets
                                            Best_Gearset[slot1]  = b  # Assign to the Best_Gearset dictionary the new piece of gear into the appropriate slot
                                            Best_Gearset[slot2] = b2  # Assign to the Best_Gearset dictionary the new piece of gear into the appropriate slot
                                            Best_Gearset[slot3] = b3  # Assign to the Best_Gearset dictionary the new piece of gear into the appropriate slot

                                        time_list[z] = best_time  # Update the damage_list[] array to contain the best damage obtained from this iteration.
                                                                    # This has nothing to do with plotting right now. Only used to compare time between consecutive iterations.



            # TODO: Is this next bit needed now? It was originally only in for when the code ran 50,000 simulations to deal with fluctuations in the damage due to "low" number statistics
            # Maybe delete this bit now.
            if not check_tp_set:
                if z > 0: # After the first iteration:
                    if np.abs(damage_list[z]-damage_list[z-1])/damage_list[z] < 0.001:
                        # If the new best damage is less than 0.1% better than the old best_damage, then converge count += 1
                        # After nconv such consecutive iterations, break out of the loop and create the final plot. This prevent the code from bouncing back and forth between two nearly identical items for 20 iterations.
                        converge_count += 1
                    else:
                        converge_count = 0 # Reset the converge count. This ensures that only consecutive trials count towards convergence
            else:
                if z > 0: # After the first iteration:
                    if np.abs(time_list[z]-time_list[z-1])/time_list[z] < 0.001:
                        # If the new best time to WS is less than 0.1% better than the old best_time, then converge count += 1
                        # After nconv such consecutive iterations, break out of the loop and create the final plot. This prevent the code from bouncing back and forth between two nearly identical items for 20 iterations.
                        converge_count += 1
                    else:
                        converge_count = 0 # Reset the converge count. This ensures that only consecutive trials count towards convergence


        # We've found the fastest set that satisfied the temporary conditions.
        # Now let's increase those temporary restrictions slightly and rerun the code to find a slightly better set.
        # We'll repeat this until the main conditions are met.
        pdt = 0
        mdt = 0 - 29*job_abilities["shell v"] # If WHM is selected on the GUI, then assume you have shell V active
        for slot in Best_Gearset:
            pdt += Best_Gearset[slot].get("PDT",0) + Best_Gearset[slot].get("DT",0) + Best_Gearset[slot].get("PDT2",0)
            mdt += Best_Gearset[slot].get("MDT",0) + Best_Gearset[slot].get("DT",0)
            # print(Best_Gearset[slot]["Name2"],Best_Gearset[slot].get("PDT",0),Best_Gearset[slot].get("DT",0))

        # Compare the pdt and mdt values from this iteration with the previous iteration.
        if pdt == pdt_old and mdt == mdt_old:
            conditional_converge_count += 1
            if conditional_converge_count >= 3:
                print("Unable to find a set which satisfies the conditions better than the current set. Exiting.")
                break
        else:
            conditional_converge_count = 0

        # Save the pdt and mdt values from this iteration to compare with the next iteration.
        pdt_old = pdt
        mdt_old = mdt

        pdt_thresh_temp = pdt - 1
        mdt_thresh_temp = mdt - 1
        print(f"Current best set: PDT:{pdt},  MDT:{mdt}")
        # print(f"Setting new targets: PDT:{mdt_thresh_temp},  MDT:{mdt_thresh_temp}\n")

    # Place JSE+2 earrings in the right_ear to make it look nice.
    if Best_Gearset["ear1"]["Name2"] in jse_ears:
        temp_ear2 = Best_Gearset["ear2"]
        temp_ear1 = Best_Gearset["ear1"]
        Best_Gearset["ear1"] = temp_ear2
        Best_Gearset["ear2"] = temp_ear1


    # At this point, the code has run up to 20 iterations and found the gearset that returns the highest average damage. Now we use this best set to create a proper distribution of damage that you'd expect to see in game based on its stats.
    best_set = set_gear(buffs, Best_Gearset, main_job, sub_job, job_abilities=job_abilities) # Create a class from the best gearset
    # print(f"{tcount} valid gear sets checked.")
    # Run the simulator once more, but with "final=True" to tell the code to create a proper distribution.

    if not nuke and not check_tp_set: # Don't run damage distributions for nukes or TP sets.
        test_set(main_job, sub_job, ws_name, enemy, buffs, Best_Gearset, best_set, tp1, tp2, tp0, n_simulations, show_final_plot, nuke, spell, job_abilities, burst, True, check_tp_set)
    elif check_tp_set:
        print(f"\nBest TP set to reach {tp1} TP with the provided buffs:\n")
        for k in Best_Gearset:
            print(f"{k:>10s}  {Best_Gearset[k]['Name2']:<50s}")
    elif nuke:
        print(f"\nBest {spell} set with the provided buffs:\n")
        for k in Best_Gearset:
            print(f"{k:>10s}  {Best_Gearset[k]['Name2']:<50s}")



    return(Best_Gearset)

if __name__ == "__main__":

    main_job = "DRK"
    sub_job = "WAR"
    ws_name = "Catastrophe"
    min_tp = 1000
    max_tp = 1500
    tp0 = 0 # Starting TP value (after a WS you'll have like 100 TP initially)
    n_iter = 10
    n_sims = 10000
    check_gear = [[Heishi,Kikoku],[Fotia_Gorget, Ninja_Nodowa]]
    check_slots = ["main","neck"]
    # check_gear = [mains, subs, ammos, heads, necks, ears, ears2, bodies, hands, rings, rings2, capes, waists, legs, feet]
    # check_slots = ["main", "sub", "ammo", "head", "neck", "ear1", "ear2", "body", "hands", "ring1", "ring2", "back", "waist", "legs", "feet"]
    # check_gear = [mains, subs, ammos, heads, necks, ears, ears2,]
    # check_slots = ["main", "sub", "ammo", "head", "neck", "ear1", "ear2"]
    buffs = {"food": Grape_Daifuku,
             "brd": {"Attack": 0, "Accuracy": 0, "Ranged Accuracy": 0,"STR":0,"DEX":0, "VIT":0, "AGI":0, "INT":0, "MND":0, "CHR":0,},
             "cor": {"Attack": 0, "Store TP": 0, "Accuracy": 0, "Magic Attack": 0, "DA":0, "Crit Rate": 0},
             "geo": {"Attack": 0, "Ranged Attack": 0, "Accuracy": 0, "Ranged Accuracy":0, "STR":0,"DEX":0, "VIT":0, "AGI":0, "INT":0, "MND":0, "CHR":0,},
             "whm": {"Haste": 0, "STR":0,"DEX":0, "VIT":0, "AGI":0, "INT":0, "MND":0, "CHR":0}, # WHM buffs like boost-STR.
             }
    from enemies import *
    enemy = apex_toad

    starting_gearset1 = {
                'main' : Heishi,
                'sub' : Kunimitsu30,
                'ranged' : Empty,
                'ammo' : Yetshila,
                'head' : Blistering_Sallet,
                'body' : Mpaca_Doublet30,
                'hands' : Ryuo_Tekko_A,
                'legs' : Jokushu_Haidate,
                'feet' : Mochizuki_Kyahan,
                'neck' : Ninja_Nodowa,
                'waist' : Fotia_Gorget,
                'ear1' : Odr_Earring,
                'ear2' : Lugra_Earring_Aug,
                'ring1' : Regal_Ring,
                'ring2' : Gere_Ring,
                'back' : Empty}
    show_final_plot = True

    nuke = False # True/False
    spell = "Doton: Ichi" # "Doton: Ichi" etc
    burst = True # True/False
    job_abilities = {"Ebullience":False,
                        "Futae":False,
                        "Sneak Attack":False,
                        "Trick Attack":False,
                        "Footwork":False,
                        "Impetus":False,
                        "Building Flourish":False,
                        "Climactic Flourish":False,
                        "Striking Flourish":False,
                        "Ternary Flourish":False,
                        "True Shot":False,
                        "Blood Rage":False,
                        "Mighty Strikes":False}

    conditions = {"PDT":-30,"MDT":-30}

    if False:
        import cProfile
        cProfile.run("run_weaponskill(main_job, sub_job, ws_name, min_tp, max_tp, tp0, n_iter, n_sims, check_gear, check_slots, buffs, enemy, starting_gearset1, show_final_plot, nuke, spell, job_abilities, conditions, burst,)",sort="cumtime")
    else:
        run_weaponskill(main_job, sub_job, ws_name, min_tp, max_tp, tp0, n_iter, n_sims, check_gear, check_slots, buffs, enemy, starting_gearset1, show_final_plot, nuke, spell, job_abilities, conditions, burst)
