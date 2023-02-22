#
# Created by Kastra on Asura.
# Feel free to /tell in game or send a PM on FFXIAH you have questions, comments, or suggestions.
#
# Version date: 2023 February 14
#
# This code holds the methods for building a player's stats.
#
from buffs import *
from gear import *

def get_fencer_bonus(level):
    #
    # Return the TP Bonus and Crit boost from Fencer
    #
    if level > 8:
        level = 8 # Cap it at Fencer VIII

    fencer = {0:[0,0],
              1:[200,3],
              2:[300,5],
              3:[400,7],
              4:[450,9],
              5:[500,10],
              6:[550,11],
              7:[600,12],
              8:[630,13]}
    return(fencer[level])

class set_gear:
    #
    # Python class used to build a dictionary of player stats from gear, buffs, and food.
    # First create zero'd gear stat dictionary, containing all of the offensive stats from the provided gear set
    # Then create a base-player stat dictionary, containing all of the offensive stats a player would have at master level 20 NIN without a subjob
    # Add stats and traits from the selected subjob
    # Check the gear set for set bonuses, then apply those to the gearstats dictionary
    # Build the gearstats dictionary using stats from the provided gearset
    # Build the playerstats dictionary using the stats from the provided gearset. But the playerstats dictionary doesnt have "Attack" or "Accuracy". We need to calculation "Attack1" and "Accuracy2", later for main- and off-hand
    #

    def __init__(self, buffs, gear, main_job, sub_job, ws_atk_bonus=0.0, job_abilities={}):

        self.gear = gear

        mainjob = main_job.upper()
        subjob = sub_job.upper()

        impetus = job_abilities.get("Impetus",False)

        sub_type = gear['sub'].get('Type', 'None') # Check if the item equipped in the sub slot is a weapon, a grip, or nothing. If the item doesn't have a "Type" Key then return "None", meaning nothing is equipped.
        dual_wield = sub_type == 'Weapon'
        ranged_type = gear["ranged"].get("Skill Type", "None") # Not sure if we'll need this, but adding it now just in case.

        # Initialize empty gearset for modification.
        # This will contain all stats that come from gear only. Player stats are defined later
        # Stats that are not defined here are ignored on gear. The code should still run, but gear stats missing from this dictionary are not counted.
        # Stats that are not defined in the playerstats{} dictionary will cause the code to crash.
        self.gearstats = {
                 'STR':0, 'DEX':0, 'VIT':0, 'AGI':0, 'INT':0, 'MND':0, 'CHR':0,
                 'Katana Skill':0, 'Dagger Skill':0, 'Sword Skill':0, 'Hand-to-Hand Skill':0, 'Great Katana Skill':0, 'Club Skill':0, 'Throwing Skill':0,
                 'Axe Skill':0,'Great Axe Skill':0,'Polearm Skill':0,'Scythe Skill':0,'Staff Skill':0,'Great Sword Skill':0,'Archery Skill':0,'Marksmanship Skill':0,
                 'Ninjutsu Skill':0, 'Great Sword Skill':0, 'Marksmanship Skill':0, "Elemental Magic Skill":0, "Evasion Skill":0,
                 'Accuracy':0, 'Attack':0,
                 'Ranged Accuracy':0, 'Ranged Attack':0,
                 'Magic Accuracy':0, 'Magic Attack':0, 'Magic Damage':0, 'Magic Accuracy Skill':0, 'Ninjutsu Magic Attack':0, 'Ninjutsu Damage':0, 'Magic Crit Rate':0,
                 'Magic Burst Damage':0, 'Magic Burst Damage II':0, 'Magic Burst Damage Trait':0,  "Magic Burst Accuracy":0,
                 "Quick Draw":0,"Quick Draw II":0,
                 'Daken':0, 'QA':0, 'TA':0, 'DA':0, 'OA8':0, 'OA7':0, 'OA6':0, 'OA5':0, 'OA4':0, 'OA3':0, 'OA2':0,"Double Shot":0,"Triple Shot":0,
                 "Kick Attacks":0,"Kick Attacks Attack":0,"Kick Attacks Accuracy":0,
                 'Crit Rate':0, 'Crit Damage':0, 'DA DMG':0, 'TA DMG':0,"Sneak Attack":0,"Trick Attack":0,"Flourish Bonus":0,"Ranged Crit Damage":0,
                 'Store TP':0, "True Shot":0,"Double Shot Damage":0,"Triple Shot Damage":0,"Double Shot DMG":0,"Triple Shot DMG":0,
                 'PDL':0,"PDL Trait":0,
                 'Dual Wield':0, 'Magic Haste':0, 'Gear Haste':0, 'JA Haste':0,"Martial Arts":0,
                 'Zanshin':0, "Zanshin OA2":0, "Fencer":0,"Fencer TP Bonus":0,"Hasso":0,"Recycle":0,
                 'Weaponskill Damage':0, 'Weaponskill Bonus':0, "Weaponskill Trait":0, 'Skillchain Bonus':0, 'ftp':0, 'TP Bonus':0, 'Weaponskill Accuracy':0,
                 'Delay1':0, 'Delay2':0, 'Delay':0, 'Ammo Delay':0, "Ranged Delay":0,
                 'DMG1':0, 'DMG2':0, 'Ammo DMG':0, "Ranged DMG":0,
                 'Light Elemental Bonus':0, 'Dark Elemental Bonus':0, 'Fire Elemental Bonus':0, 'Earth Elemental Bonus':0, 'Water Elemental Bonus':0, 'Wind Elemental Bonus':0, 'Ice Elemental Bonus':0, 'Thunder Elemental Bonus':0,'Elemental Bonus':0,
                 'Light Affinity':0, 'Dark Affinity':0, 'Fire Affinity':0,'Earth Affinity':0, 'Water Affinity':0, 'Wind Affinity':0,'Ice Affinity':0, 'Thunder Affinity':0,
                 "Magic Crit Rate II":0,"PDT":0,"MDT":0,"DT":0,"PDT2":0,"Magic Evasion":0,"Evasion":0,"Magic Def":0,"Subtle Blow":0,"Subtle Blow II":0,
                 }


        # Initialize base player stats with no gear and no subjob.
        # Subjob stats and gear stats will be added later in another part of the code.
        # Base 5% crit rate (0+5), +5 for 5/5 crit merits for 0+5+5

        if mainjob == "NIN":  # Master Level 20 Ninja stats
            self.playerstats = {'STR':113, 'DEX':115, 'VIT':113, 'AGI':115, 'INT':110, 'MND':101, 'CHR':104,
                     'Katana Skill':444+16, 'Dagger Skill':398+16, 'Sword Skill':393+16, 'Hand-to-Hand Skill':320+16, 'Great Katana Skill':388+16, 'Club Skill':320+16, 'Throwing Skill':444+16,
                     'Axe Skill':0+16,'Great Axe Skill':0+16,'Polearm Skill':0+16,'Scythe Skill':0+16,'Staff Skill':0+16,'Great Sword Skill':0+16,'Archery Skill':320+16,'Marksmanship Skill':393+16,
                     'Ninjutsu Skill':473+16, "Elemental Magic Skill":0+16, "Evasion Skill":437+16,
                     'Accuracy1':56, 'Accuracy2':56, 'Attack1':70, 'Attack2':70,
                     'Ranged Accuracy':56, 'Ranged Attack':70,
                     'Magic Accuracy':50, 'Magic Attack':28, 'Magic Damage':40, 'Magic Accuracy Skill':0, 'Ninjutsu Magic Attack':0, 'Ninjutsu Damage':0, 'Magic Crit Rate':0,
                     'Magic Burst Damage':0, 'Magic Burst Damage II':0, 'Magic Burst Damage Trait':7,  "Magic Burst Accuracy":0,
                     "Quick Draw":0,"Quick Draw II":0,
                     'Daken':54, 'QA':0, 'TA':0, 'DA':0, 'OA8':0, 'OA7':0, 'OA6':0, 'OA5':0, 'OA4':0, 'OA3':0, 'OA2':0,"Double Shot":0,"Triple Shot":0,
                     "Kick Attacks":0,"Kick Attacks Attack":0,"Kick Attacks Accuracy":0,
                     'Crit Rate':10, 'Crit Damage':0, 'DA DMG':0, 'TA DMG':0,"Sneak Attack":0,"Trick Attack":0,"Flourish Bonus":0,"Ranged Crit Damage":0,
                     'Store TP':0, "True Shot":0,"Double Shot Damage":0,"Triple Shot Damage":0,"Double Shot DMG":0,"Triple Shot DMG":0,
                     'PDL':0, 'PDL Trait':10,
                     'Dual Wield':35, 'Magic Haste':0, 'Gear Haste':0, 'JA Haste':0,"Martial Arts":0,
                     'Zanshin':0, "Zanshin OA2":0, "Fencer":0,"Fencer TP Bonus":0,"Hasso":0,"Recycle":0,
                     'Weaponskill Damage':5, 'Weaponskill Bonus':0, "Weaponskill Trait":0, 'Skillchain Bonus':12, 'ftp':0, 'TP Bonus':0, 'Weaponskill Accuracy':0,
                     'Delay1':0, 'Delay2':0, 'Delay':0, 'Ammo Delay':0, "Ranged Delay":0,
                     'DMG1':0, 'DMG2':0, 'Ammo DMG':0, "Ranged DMG":0,
                     'Light Elemental Bonus':0, 'Dark Elemental Bonus':0, 'Fire Elemental Bonus':0,'Earth Elemental Bonus':0, 'Water Elemental Bonus':0, 'Wind Elemental Bonus':0,'Ice Elemental Bonus':0, 'Thunder Elemental Bonus':0,'Elemental Bonus':0, 'Weaponskill Accuracy':0,
                     'Light Affinity':0, 'Dark Affinity':0, 'Fire Affinity':0,'Earth Affinity':0, 'Water Affinity':0, 'Wind Affinity':0,'Ice Affinity':0, 'Thunder Affinity':0,
                     "Magic Crit Rate II":0,"PDT":0,"MDT":0,"DT":0,"PDT2":0,"Magic Evasion":36,"Evasion":64,"Magic Def":0,"Subtle Blow":27+5,"Subtle Blow II":0,
                     }
        elif mainjob == "DRK":  # Master Level 20 Dark Knight stats
            self.playerstats = {'STR':117, 'DEX':113, 'VIT':113, 'AGI':110, 'INT':113, 'MND':101, 'CHR':101,
                     'Scythe Skill':444+16, 'Dagger Skill':393+16, 'Sword Skill':408+16, 'Hand-to-Hand Skill':0+16, 'Great Katana Skill':0+16, 'Club Skill':388+16, 'Throwing Skill':0+16,
                     'Katana Skill':0+16, 'Axe Skill':408+16,'Great Axe Skill':408+16,'Polearm Skill':0+16,'Staff Skill':0+16,'Great Sword Skill':437+16,'Archery Skill':0+16,'Marksmanship Skill':320+16,
                     'Ninjutsu Skill':0, 'Dark Magic Skill':473+16, "Elemental Magic Skill":424+16, "Evasion Skill":393+16,
                     'Accuracy1':22, 'Accuracy2':22, 'Attack1':202, 'Attack2':202,
                     'Ranged Accuracy':22, 'Ranged Attack':202,
                     'Magic Accuracy':30, 'Magic Attack':0, 'Magic Damage':0, 'Magic Accuracy Skill':0, 'Ninjutsu Magic Attack':0, 'Magic Crit Rate':0,
                     'Magic Burst Damage':0,'Magic Burst Damage II':0, 'Magic Burst Damage Trait':0, "Magic Burst Accuracy":0,
                     "Quick Draw":0,"Quick Draw II":0,
                     'Daken':0, 'QA':0, 'TA':0, 'DA':0, 'OA8':0, 'OA7':0, 'OA6':0, 'OA5':0, 'OA4':0, 'OA3':0, 'OA2':0,"Double Shot":0,"Triple Shot":0,
                     "Kick Attacks":0,"Kick Attacks Attack":0,"Kick Attacks Accuracy":0,
                     'Crit Rate':10, 'Crit Damage':16, 'DA DMG':0, 'TA DMG':0,"Sneak Attack":0,"Trick Attack":0,"Flourish Bonus":0,"Ranged Crit Damage":0,
                     'Store TP':0, "True Shot":0,"Double Shot Damage":0,"Triple Shot Damage":0,"Double Shot DMG":0,"Triple Shot DMG":0,
                     'PDL':0, 'PDL Trait':50,
                     'Dual Wield':0, 'Magic Haste':0, 'Gear Haste':0, 'JA Haste':0,"Martial Arts":0,
                     'Zanshin':0, "Zanshin OA2":0, "Fencer":0,"Fencer TP Bonus":0,"Hasso":0,"Recycle":0,
                     'Weaponskill Damage':8, 'Weaponskill Bonus':0, "Weaponskill Trait":0, 'Skillchain Bonus':12, 'ftp':0, 'TP Bonus':0, 'Weaponskill Accuracy':0,
                     'Delay1':0, 'Delay2':0, 'Delay':0, 'Ammo Delay':0, "Ranged Delay":0,
                     'DMG1':0, 'DMG2':0, 'Ammo DMG':0, "Ranged DMG":0,
                     'Light Elemental Bonus':0, 'Dark Elemental Bonus':0, 'Fire Elemental Bonus':0,'Earth Elemental Bonus':0, 'Water Elemental Bonus':0, 'Wind Elemental Bonus':0,'Ice Elemental Bonus':0, 'Thunder Elemental Bonus':0,'Elemental Bonus':0, 'Weaponskill Accuracy':0,
                     'Light Affinity':0, 'Dark Affinity':0, 'Fire Affinity':0,'Earth Affinity':0, 'Water Affinity':0, 'Wind Affinity':0,'Ice Affinity':0, 'Thunder Affinity':0,
                     "Magic Crit Rate II":0,"PDT":0,"MDT":0,"DT":0,"PDT2":0,"Magic Evasion":36,"Evasion":22,"Magic Def":0,"Subtle Blow":0,"Subtle Blow II":0,
                     }
        elif mainjob == "WAR":  # Master Level 20 Warrior stats. Smite and Fencer are added later
            self.playerstats = {'STR':117, 'DEX':113, 'VIT':110, 'AGI':113, 'INT':104, 'MND':104, 'CHR':107,
                     'Scythe Skill':424+16, 'Dagger Skill':408+16, 'Sword Skill':418+16, 'Hand-to-Hand Skill':334+16, 'Great Katana Skill':0+16, 'Club Skill':408+16, 'Throwing Skill':354+16,
                     'Katana Skill':0+16, 'Axe Skill':437+16,'Great Axe Skill':444+16,'Polearm Skill':408+16,'Staff Skill':418+16,'Great Sword Skill':424+16,'Archery Skill':354+16,'Marksmanship Skill':354+16,
                     'Ninjutsu Skill':0, 'Dark Magic Skill':0+16, "Elemental Magic Skill":0+16, "Evasion Skill":393+16,
                     'Accuracy1':26, 'Accuracy2':26, 'Attack1':70+35, 'Attack2':70+35,
                     'Ranged Accuracy':26, 'Ranged Attack':70+35,
                     'Magic Accuracy':26, 'Magic Attack':0, 'Magic Damage':0, 'Magic Accuracy Skill':0, 'Ninjutsu Magic Attack':0, 'Magic Crit Rate':0,
                     'Magic Burst Damage':0,'Magic Burst Damage II':0, 'Magic Burst Damage Trait':0, "Magic Burst Accuracy":0,
                     "Quick Draw":0,"Quick Draw II":0,
                     'Daken':0, 'QA':0, 'TA':0, 'DA':0+18, 'OA8':0, 'OA7':0, 'OA6':0, 'OA5':0, 'OA4':0, 'OA3':0, 'OA2':0,"Double Shot":0,"Triple Shot":0,
                     "Kick Attacks":0,"Kick Attacks Attack":0,"Kick Attacks Accuracy":0,
                     'Crit Rate':10+10, 'Crit Damage':10+8, 'DA DMG':0, 'TA DMG':0,"Sneak Attack":0,"Trick Attack":0,"Flourish Bonus":0,"Ranged Crit Damage":0,
                     'Store TP':0, "True Shot":0,"Double Shot Damage":0,"Triple Shot Damage":0,"Double Shot DMG":0,"Triple Shot DMG":0,
                     'PDL':0, 'PDL Trait':20,
                     'Dual Wield':0, 'Magic Haste':0, 'Gear Haste':0, 'JA Haste':0,"Martial Arts":0,
                     'Zanshin':0, "Zanshin OA2":0, "Zanshin OA2":0, "Fencer":0,"Fencer TP Bonus":180,"Hasso":0,"Recycle":0,
                     'Weaponskill Damage':8, 'Weaponskill Bonus':0, "Weaponskill Trait":0, 'Skillchain Bonus':12, 'ftp':0, 'TP Bonus':0, 'Weaponskill Accuracy':0,
                     'Delay1':0, 'Delay2':0, 'Delay':0, 'Ammo Delay':0, "Ranged Delay":0,
                     'DMG1':0, 'DMG2':0, 'Ammo DMG':0, "Ranged DMG":0,
                     'Light Elemental Bonus':0, 'Dark Elemental Bonus':0, 'Fire Elemental Bonus':0,'Earth Elemental Bonus':0, 'Water Elemental Bonus':0, 'Wind Elemental Bonus':0,'Ice Elemental Bonus':0, 'Thunder Elemental Bonus':0,'Elemental Bonus':0, 'Weaponskill Accuracy':0,
                     'Light Affinity':0, 'Dark Affinity':0, 'Fire Affinity':0,'Earth Affinity':0, 'Water Affinity':0, 'Wind Affinity':0,'Ice Affinity':0, 'Thunder Affinity':0,
                     "Magic Crit Rate II":0,"PDT":0,"MDT":0,"DT":0,"PDT2":0,"Magic Evasion":36,"Evasion":36,"Magic Def":0,"Subtle Blow":0,"Subtle Blow II":0,
                     }
        elif mainjob == "SAM":  # Master Level 20 Samurai stats. Hasso stuff is added later. Zanshin is +50% from traits, +5% from merits, +10% from job gifts. The additional +10% from gifts are added in the main code for now as "zanhasso"
            self.playerstats = {'STR':113, 'DEX':113, 'VIT':113, 'AGI':110, 'INT':107, 'MND':107, 'CHR':110,
                     'Scythe Skill':0+16, 'Dagger Skill':320+16, 'Sword Skill':398+16, 'Hand-to-Hand Skill':0+16, 'Great Katana Skill':444+16, 'Club Skill':320+16, 'Throwing Skill':398+16,
                     'Katana Skill':0+16, 'Axe Skill':0+16,'Great Axe Skill':0+16,'Polearm Skill':408+16,'Staff Skill':0+16,'Great Sword Skill':0+16,'Archery Skill':398+16,'Marksmanship Skill':0+16,
                     'Ninjutsu Skill':0, "Elemental Magic Skill":0, "Evasion Skill":424+16,
                     'Accuracy1':36, 'Accuracy2':36, 'Attack1':70, 'Attack2':70,
                     'Ranged Accuracy':36, 'Ranged Attack':70,
                     'Magic Accuracy':26, 'Magic Attack':0, 'Magic Damage':0, 'Magic Accuracy Skill':0, 'Ninjutsu Magic Attack':0, 'Magic Crit Rate':0,
                     'Magic Burst Damage':0,'Magic Burst Damage II':0, 'Magic Burst Damage Trait':0, "Magic Burst Accuracy":0,
                     "Quick Draw":0,"Quick Draw II":0,
                     'Daken':0, 'QA':0, 'TA':0, 'DA':0, 'OA8':0, 'OA7':0, 'OA6':0, 'OA5':0, 'OA4':0, 'OA3':0, 'OA2':0,"Double Shot":0,"Triple Shot":0,
                     "Kick Attacks":0,"Kick Attacks Attack":0,"Kick Attacks Accuracy":0,
                     'Crit Rate':10, 'Crit Damage':0, 'DA DMG':0, 'TA DMG':0,"Sneak Attack":0,"Trick Attack":0,"Flourish Bonus":0,"Ranged Crit Damage":0,
                     'Store TP':8+40, "True Shot":0,"Double Shot Damage":0,"Triple Shot Damage":0,"Double Shot DMG":0,"Triple Shot DMG":0,
                     'PDL':0, 'PDL Trait':20,
                     'Dual Wield':0, 'Magic Haste':0, 'Gear Haste':0, 'JA Haste':0,"Martial Arts":0,
                     'Zanshin':50+5+10, "Zanshin OA2":0, "Fencer":0,"Fencer TP Bonus":0,"Hasso":0,"Recycle":0,
                     'Weaponskill Damage':8+19, 'Weaponskill Bonus':0, "Weaponskill Trait":0, 'Skillchain Bonus':8+16, 'ftp':0, 'TP Bonus':0, 'Weaponskill Accuracy':0,
                     'Delay1':0, 'Delay2':0, 'Delay':0, 'Ammo Delay':0, "Ranged Delay":0,
                     'DMG1':0, 'DMG2':0, 'Ammo DMG':0, "Ranged DMG":0,
                     'Light Elemental Bonus':0, 'Dark Elemental Bonus':0, 'Fire Elemental Bonus':0,'Earth Elemental Bonus':0, 'Water Elemental Bonus':0, 'Wind Elemental Bonus':0,'Ice Elemental Bonus':0, 'Thunder Elemental Bonus':0,'Elemental Bonus':0, 'Weaponskill Accuracy':0,
                     'Light Affinity':0, 'Dark Affinity':0, 'Fire Affinity':0,'Earth Affinity':0, 'Water Affinity':0, 'Wind Affinity':0,'Ice Affinity':0, 'Thunder Affinity':0,
                     "Magic Crit Rate II":0,"PDT":0,"MDT":0,"DT":0,"PDT2":0,"Magic Evasion":36,"Evasion":36,"Magic Def":0,"Subtle Blow":0,"Subtle Blow II":0,
                     }
        elif mainjob == "DRG":  # Master Level 20 Dragoon stats. Smite is added later. Bonuses for having a Wyvern out are added later.
            self.playerstats = {'STR':115, 'DEX':110, 'VIT':113, 'AGI':110, 'INT':104, 'MND':107, 'CHR':113,
                     'Scythe Skill':0+16, 'Dagger Skill':320+16, 'Sword Skill':388+16, 'Hand-to-Hand Skill':0+16, 'Great Katana Skill':0+16, 'Club Skill':320+16, 'Throwing Skill':0+16,
                     'Katana Skill':0+16, 'Axe Skill':0+16,'Great Axe Skill':0+16,'Polearm Skill':444+16,'Staff Skill':408+16,'Great Sword Skill':0+16,'Archery Skill':0+16,'Marksmanship Skill':0+16,
                     'Ninjutsu Skill':0, "Elemental Magic Skill":0, "Evasion Skill":408+16,
                     'Accuracy1':64+35, 'Accuracy2':64+35, 'Attack1':55+22, 'Attack2':55+22,
                     'Ranged Accuracy':64+35, 'Ranged Attack':55,
                     'Magic Accuracy':26, 'Magic Attack':0, 'Magic Damage':0, 'Magic Accuracy Skill':0, 'Ninjutsu Magic Attack':0, 'Magic Crit Rate':0,
                     'Magic Burst Damage':0,'Magic Burst Damage II':0, 'Magic Burst Damage Trait':0, "Magic Burst Accuracy":0,
                     "Quick Draw":0,"Quick Draw II":0,
                     'Daken':0, 'QA':0, 'TA':0, 'DA':0, 'OA8':0, 'OA7':0, 'OA6':0, 'OA5':0, 'OA4':0, 'OA3':0, 'OA2':0,"Double Shot":0,"Triple Shot":0,
                     "Kick Attacks":0,"Kick Attacks Attack":0,"Kick Attacks Accuracy":0,
                     'Crit Rate':10, 'Crit Damage':8, 'DA DMG':0, 'TA DMG':0,"Sneak Attack":0,"Trick Attack":0,"Flourish Bonus":0,"Ranged Crit Damage":0,
                     'Store TP':0, "True Shot":0,"Double Shot Damage":0,"Triple Shot Damage":0,"Double Shot DMG":0,"Triple Shot DMG":0,
                     'PDL':0, 'PDL Trait':30,
                     'Dual Wield':0, 'Magic Haste':0, 'Gear Haste':0, 'JA Haste':0,"Martial Arts":0,
                     'Zanshin':0, "Zanshin OA2":0, "Fencer":0,"Fencer TP Bonus":0,"Hasso":0,"Recycle":0,
                     'Weaponskill Damage':0, 'Weaponskill Bonus':0, "Weaponskill Trait":21, 'Skillchain Bonus':0, 'ftp':0, 'TP Bonus':0, 'Weaponskill Accuracy':0,
                     'Delay1':0, 'Delay2':0, 'Delay':0, 'Ammo Delay':0, "Ranged Delay":0,
                     'DMG1':0, 'DMG2':0, 'Ammo DMG':0, "Ranged DMG":0,
                     'Light Elemental Bonus':0, 'Dark Elemental Bonus':0, 'Fire Elemental Bonus':0,'Earth Elemental Bonus':0, 'Water Elemental Bonus':0, 'Wind Elemental Bonus':0,'Ice Elemental Bonus':0, 'Thunder Elemental Bonus':0,'Elemental Bonus':0, 'Weaponskill Accuracy':0,
                     'Light Affinity':0, 'Dark Affinity':0, 'Fire Affinity':0,'Earth Affinity':0, 'Water Affinity':0, 'Wind Affinity':0,'Ice Affinity':0, 'Thunder Affinity':0,
                     "Magic Crit Rate II":0,"PDT":0,"MDT":0,"DT":0,"PDT2":0,"Magic Evasion":36,"Evasion":36,"Magic Def":0,"Subtle Blow":0,"Subtle Blow II":0,
                     }
        elif mainjob == "BLM":  # Master Level 20 Black Mage stats.
            self.playerstats = {'STR':104, 'DEX':113, 'VIT':104, 'AGI':113, 'INT':117, 'MND':107, 'CHR':110,
                     'Katana Skill':0+16, 'Dagger Skill':354+16, 'Sword Skill':0+16, 'Hand-to-Hand Skill':0+16, 'Great Katana Skill':0+16, 'Club Skill':398+16, 'Throwing Skill':354+16,
                     'Axe Skill':0+16,'Great Axe Skill':0+16,'Polearm Skill':0+16,'Scythe Skill':320+16,'Staff Skill':408+16,'Great Sword Skill':0+16,'Archery Skill':0+16,'Marksmanship Skill':0+16,
                     'Ninjutsu Skill':0+16, "Elemental Magic Skill":480+16, "Evasion Skill":320+16,
                     'Accuracy1':0, 'Accuracy2':0, 'Attack1':0, 'Attack2':0,
                     'Ranged Accuracy':0, 'Ranged Attack':0,
                     'Magic Accuracy':62, 'Magic Attack':50+40+10, 'Magic Damage':43, 'Magic Accuracy Skill':0, 'Ninjutsu Magic Attack':0, 'Ninjutsu Damage':0, 'Magic Crit Rate':0,
                     'Magic Burst Damage':0, 'Magic Burst Damage II':0, 'Magic Burst Damage Trait':43+13, "Magic Burst Accuracy":0,
                     "Quick Draw":0,"Quick Draw II":0,
                     'Daken':0, 'QA':0, 'TA':0, 'DA':0, 'OA8':0, 'OA7':0, 'OA6':0, 'OA5':0, 'OA4':0, 'OA3':0, 'OA2':0,"Double Shot":0,"Triple Shot":0,
                     "Kick Attacks":0,"Kick Attacks Attack":0,"Kick Attacks Accuracy":0,
                     'Crit Rate':10, 'Crit Damage':0, 'DA DMG':0, 'TA DMG':0,"Sneak Attack":0,"Trick Attack":0,"Flourish Bonus":0,"Ranged Crit Damage":0,
                     'Store TP':0, "True Shot":0,"Double Shot Damage":0,"Triple Shot Damage":0,"Double Shot DMG":0,"Triple Shot DMG":0,
                     'PDL':0, 'PDL Trait':0,
                     'Dual Wield':0, 'Magic Haste':0, 'Gear Haste':0, 'JA Haste':0,"Martial Arts":0,
                     'Zanshin':0, "Zanshin OA2":0, "Fencer":0,"Fencer TP Bonus":0,"Hasso":0,"Recycle":0,
                     'Weaponskill Damage':0, 'Weaponskill Bonus':0, "Weaponskill Trait":0, 'Skillchain Bonus':0, 'ftp':0, 'TP Bonus':0, 'Weaponskill Accuracy':0,
                     'Delay1':0, 'Delay2':0, 'Delay':0, 'Ammo Delay':0, "Ranged Delay":0,
                     'DMG1':0, 'DMG2':0, 'Ammo DMG':0, "Ranged DMG":0,
                     'Light Elemental Bonus':0, 'Dark Elemental Bonus':0, 'Fire Elemental Bonus':0,'Earth Elemental Bonus':0, 'Water Elemental Bonus':0, 'Wind Elemental Bonus':0,'Ice Elemental Bonus':0, 'Thunder Elemental Bonus':0,'Elemental Bonus':0, 'Weaponskill Accuracy':0,
                     'Light Affinity':0, 'Dark Affinity':0, 'Fire Affinity':0,'Earth Affinity':0, 'Water Affinity':0, 'Wind Affinity':0,'Ice Affinity':0, 'Thunder Affinity':0,
                     "Magic Crit Rate II":0,"PDT":0,"MDT":0,"DT":0,"PDT2":0,"Magic Evasion":42,"Evasion":0,"Magic Def":0,"Subtle Blow":0,"Subtle Blow II":0,
                     }
        elif mainjob == "WHM":  # Master Level 20 White Mage stats.
            self.playerstats = {'STR':110, 'DEX':104, 'VIT':110, 'AGI':107, 'INT':107, 'MND':117, 'CHR':113,
                     'Katana Skill':0+16, 'Dagger Skill':0+16, 'Sword Skill':0+16, 'Hand-to-Hand Skill':0+16, 'Great Katana Skill':0+16, 'Club Skill':424+16, 'Throwing Skill':320+16,
                     'Axe Skill':0+16,'Great Axe Skill':0+16,'Polearm Skill':0+16,'Scythe Skill':0+16,'Staff Skill':398+16,'Great Sword Skill':0+16,'Archery Skill':0+16,'Marksmanship Skill':0+16,
                     'Ninjutsu Skill':0+16, "Elemental Magic Skill":0+16, "Evasion Skill":320+16,
                     'Accuracy1':14, 'Accuracy2':14, 'Attack1':0, 'Attack2':0,
                     'Ranged Accuracy':14, 'Ranged Attack':0,
                     'Magic Accuracy':70, 'Magic Attack':22, 'Magic Damage':0, 'Magic Accuracy Skill':0, 'Ninjutsu Magic Attack':0, 'Ninjutsu Damage':0, 'Magic Crit Rate':0,
                     'Magic Burst Damage':0, 'Magic Burst Damage II':0, 'Magic Burst Damage Trait':0, "Magic Burst Accuracy":0,
                     "Quick Draw":0,"Quick Draw II":0,
                     'Daken':0, 'QA':0, 'TA':0, 'DA':0, 'OA8':0, 'OA7':0, 'OA6':0, 'OA5':0, 'OA4':0, 'OA3':0, 'OA2':0,"Double Shot":0,"Triple Shot":0,
                     "Kick Attacks":0,"Kick Attacks Attack":0,"Kick Attacks Accuracy":0,
                     'Crit Rate':10, 'Crit Damage':0, 'DA DMG':0, 'TA DMG':0,"Sneak Attack":0,"Trick Attack":0,"Flourish Bonus":0,"Ranged Crit Damage":0,
                     'Store TP':0, "True Shot":0,"Double Shot Damage":0,"Triple Shot Damage":0,"Double Shot DMG":0,"Triple Shot DMG":0,
                     'PDL':0, 'PDL Trait':0,
                     'Dual Wield':0, 'Magic Haste':0, 'Gear Haste':0, 'JA Haste':0,"Martial Arts":0,
                     'Zanshin':0, "Zanshin OA2":0, "Fencer":0,"Fencer TP Bonus":0,"Hasso":0,"Recycle":0,
                     'Weaponskill Damage':0, 'Weaponskill Bonus':0, "Weaponskill Trait":0, 'Skillchain Bonus':0, 'ftp':0, 'TP Bonus':0, 'Weaponskill Accuracy':0,
                     'Delay1':0, 'Delay2':0, 'Delay':0, 'Ammo Delay':0, "Ranged Delay":0,
                     'DMG1':0, 'DMG2':0, 'Ammo DMG':0, "Ranged DMG":0,
                     'Light Elemental Bonus':0, 'Dark Elemental Bonus':0, 'Fire Elemental Bonus':0,'Earth Elemental Bonus':0, 'Water Elemental Bonus':0, 'Wind Elemental Bonus':0,'Ice Elemental Bonus':0, 'Thunder Elemental Bonus':0,'Elemental Bonus':0, 'Weaponskill Accuracy':0,
                     'Light Affinity':0, 'Dark Affinity':0, 'Fire Affinity':0,'Earth Affinity':0, 'Water Affinity':0, 'Wind Affinity':0,'Ice Affinity':0, 'Thunder Affinity':0,
                     "Magic Crit Rate II":0,"PDT":0,"MDT":0,"DT":0,"PDT2":0,"Magic Evasion":50,"Evasion":0,"Magic Def":20,"Subtle Blow":0,"Subtle Blow II":0,
                     }
        elif mainjob == "RDM":  # Master Level 20 Red Mage stats. +15+25 "Magic Accuracy" from assumed merits. +35% TA from Temper2
            self.playerstats = {'STR':110, 'DEX':110, 'VIT':107, 'AGI':107, 'INT':113, 'MND':113, 'CHR':110,
                     'Katana Skill':0+16, 'Dagger Skill':418+16, 'Sword Skill':418+16, 'Hand-to-Hand Skill':0+16, 'Great Katana Skill':0+16, 'Club Skill':354+16, 'Throwing Skill':285+16,
                     'Axe Skill':0+16,'Great Axe Skill':0+16,'Polearm Skill':0+16,'Scythe Skill':0+16,'Staff Skill':0+16,'Great Sword Skill':0+16,'Archery Skill':354+16,'Marksmanship Skill':0+16,
                     'Ninjutsu Skill':0+16, "Elemental Magic Skill":398+16, "Evasion Skill":354+16,
                     'Accuracy1':70+32, 'Accuracy2':70+32, 'Attack1':0, 'Attack2':0,
                     'Ranged Accuracy':22, 'Ranged Attack':0,
                     'Magic Accuracy':90+15+25, 'Magic Attack':48+28, 'Magic Damage':0, 'Magic Accuracy Skill':0, 'Ninjutsu Magic Attack':0, 'Ninjutsu Damage':0, 'Magic Crit Rate':0,
                     'Magic Burst Damage':0, 'Magic Burst Damage II':0, 'Magic Burst Damage Trait':0+7, "Magic Burst Accuracy":0,
                     "Quick Draw":0,"Quick Draw II":0,
                     'Daken':0, 'QA':0, 'TA':35, 'DA':0, 'OA8':0, 'OA7':0, 'OA6':0, 'OA5':0, 'OA4':0, 'OA3':0, 'OA2':0,"Double Shot":0,"Triple Shot":0,
                     "Kick Attacks":0,"Kick Attacks Attack":0,"Kick Attacks Accuracy":0,
                     'Crit Rate':10, 'Crit Damage':0, 'DA DMG':0, 'TA DMG':0,"Sneak Attack":0,"Trick Attack":0,"Flourish Bonus":0,"Ranged Crit Damage":0,
                     'Store TP':0, "True Shot":0,"Double Shot Damage":0,"Triple Shot Damage":0,"Double Shot DMG":0,"Triple Shot DMG":0,
                     'PDL':0, 'PDL Trait':10,
                     'Dual Wield':0, 'Magic Haste':0, 'Gear Haste':0, 'JA Haste':0,"Martial Arts":0,
                     'Zanshin':0, "Zanshin OA2":0, "Fencer":0,"Fencer TP Bonus":0,"Hasso":0,"Recycle":0,
                     'Weaponskill Damage':0, 'Weaponskill Bonus':0, "Weaponskill Trait":0, 'Skillchain Bonus':0, 'ftp':0, 'TP Bonus':0, 'Weaponskill Accuracy':0,
                     'Delay1':0, 'Delay2':0, 'Delay':0, 'Ammo Delay':0, "Ranged Delay":0,
                     'DMG1':0, 'DMG2':0, 'Ammo DMG':0, "Ranged DMG":0,
                     'Light Elemental Bonus':0, 'Dark Elemental Bonus':0, 'Fire Elemental Bonus':0,'Earth Elemental Bonus':0, 'Water Elemental Bonus':0, 'Wind Elemental Bonus':0,'Ice Elemental Bonus':0, 'Thunder Elemental Bonus':0,'Elemental Bonus':0, 'Weaponskill Accuracy':0,
                     'Light Affinity':0, 'Dark Affinity':0, 'Fire Affinity':0,'Earth Affinity':0, 'Water Affinity':0, 'Wind Affinity':0,'Ice Affinity':0, 'Thunder Affinity':0,
                     "Magic Crit Rate II":0,"PDT":0,"MDT":0,"DT":0,"PDT2":0,"Magic Evasion":56,"Evasion":0,"Magic Def":14,"Subtle Blow":0,"Subtle Blow II":0,
                     }
        elif mainjob == "SCH":  # Master Level 20 Scholar stats. +15 Magic Accuracy from Klimaform.
            self.playerstats = {'STR':104, 'DEX':110, 'VIT':107, 'AGI':110, 'INT':115, 'MND':110, 'CHR':113,
                     'Katana Skill':0+16, 'Dagger Skill':354+16, 'Sword Skill':0+16, 'Hand-to-Hand Skill':0+16, 'Great Katana Skill':0+16, 'Club Skill':398+16, 'Throwing Skill':354+16,
                     'Axe Skill':0+16,'Great Axe Skill':0+16,'Polearm Skill':0+16,'Scythe Skill':0+16,'Staff Skill':398+16,'Great Sword Skill':0+16,'Archery Skill':0+16,'Marksmanship Skill':0+16,
                     'Ninjutsu Skill':0+16, "Elemental Magic Skill":460+16, "Evasion Skill":320+16,
                     'Accuracy1':0, 'Accuracy2':0, 'Attack1':0, 'Attack2':0,
                     'Ranged Accuracy':0, 'Ranged Attack':0,
                     'Magic Accuracy':27+15, 'Magic Attack':36, 'Magic Damage':0, 'Magic Accuracy Skill':0, 'Ninjutsu Magic Attack':0, 'Ninjutsu Damage':0, 'Magic Crit Rate':0,
                     'Magic Burst Damage':0, 'Magic Burst Damage II':0, 'Magic Burst Damage Trait':13+9,"Magic Burst Accuracy":0,
                     "Quick Draw":0,"Quick Draw II":0,
                     'Daken':0, 'QA':0, 'TA':0, 'DA':0, 'OA8':0, 'OA7':0, 'OA6':0, 'OA5':0, 'OA4':0, 'OA3':0, 'OA2':0,"Double Shot":0,"Triple Shot":0,
                     "Kick Attacks":0,"Kick Attacks Attack":0,"Kick Attacks Accuracy":0,
                     'Crit Rate':10, 'Crit Damage':0, 'DA DMG':0, 'TA DMG':0,"Sneak Attack":0,"Trick Attack":0,"Flourish Bonus":0,"Ranged Crit Damage":0,
                     'Store TP':0, "True Shot":0,"Double Shot Damage":0,"Triple Shot Damage":0,"Double Shot DMG":0,"Triple Shot DMG":0,
                     'PDL':0, 'PDL Trait':0,
                     'Dual Wield':0, 'Magic Haste':0, 'Gear Haste':0, 'JA Haste':0,"Martial Arts":0,
                     'Zanshin':0, "Zanshin OA2":0, "Fencer":0,"Fencer TP Bonus":0,"Hasso":0,"Recycle":0,
                     'Weaponskill Damage':0, 'Weaponskill Bonus':0, "Weaponskill Trait":0, 'Skillchain Bonus':0, 'ftp':0, 'TP Bonus':0, 'Weaponskill Accuracy':0,
                     'Delay1':0, 'Delay2':0, 'Delay':0, 'Ammo Delay':0, "Ranged Delay":0,
                     'DMG1':0, 'DMG2':0, 'Ammo DMG':0, "Ranged DMG":0,
                     'Light Elemental Bonus':0, 'Dark Elemental Bonus':0, 'Fire Elemental Bonus':0,'Earth Elemental Bonus':0, 'Water Elemental Bonus':0, 'Wind Elemental Bonus':0,'Ice Elemental Bonus':0, 'Thunder Elemental Bonus':0,'Elemental Bonus':0, 'Weaponskill Accuracy':0,
                     'Light Affinity':0, 'Dark Affinity':0, 'Fire Affinity':0,'Earth Affinity':0, 'Water Affinity':0, 'Wind Affinity':0,'Ice Affinity':0, 'Thunder Affinity':0,
                     "Magic Crit Rate II":0,"PDT":0,"MDT":0,"DT":0,"PDT2":0,"Magic Evasion":42,"Evasion":0,"Magic Def":0,"Subtle Blow":0,"Subtle Blow II":0,
                     }
        elif mainjob == "COR":  # Master Level 20 Corsair stats.
            self.playerstats = {'STR':107, 'DEX':113, 'VIT':107, 'AGI':115, 'INT':113, 'MND':107, 'CHR':107,
                     'Katana Skill':0+16, 'Dagger Skill':424+16, 'Sword Skill':408+16, 'Hand-to-Hand Skill':0+16, 'Great Katana Skill':0+16, 'Club Skill':0+16, 'Throwing Skill':398+16,
                     'Axe Skill':0+16,'Great Axe Skill':0+16,'Polearm Skill':0+16,'Scythe Skill':0+16,'Staff Skill':0+16,'Great Sword Skill':0+16,'Archery Skill':0+16,'Marksmanship Skill':418+16,
                     'Ninjutsu Skill':0+16, "Elemental Magic Skill":0+16, "Evasion Skill":354+16,
                     'Accuracy1':26, 'Accuracy2':26, 'Attack1':26, 'Attack2':26,
                     'Ranged Accuracy':46, 'Ranged Attack':26,
                     'Magic Accuracy':26, 'Magic Attack':10, 'Magic Damage':0, 'Magic Accuracy Skill':0, 'Ninjutsu Magic Attack':0, 'Ninjutsu Damage':0, 'Magic Crit Rate':0,
                     'Magic Burst Damage':0, 'Magic Burst Damage II':0, 'Magic Burst Damage Trait':0, "Magic Burst Accuracy":0,
                     "Quick Draw":40,"Quick Draw II":0, # Quick Draw is "Magic Damage" for quick draw. "Quick Draw II" is the percent boost (empy feet here, but death penalty is treated separately)
                     'Daken':54, 'QA':0, 'TA':0, 'DA':0, 'OA8':0, 'OA7':0, 'OA6':0, 'OA5':0, 'OA4':0, 'OA3':0, 'OA2':0,"Double Shot":0,"Triple Shot":20,
                     "Kick Attacks":0,"Kick Attacks Attack":0,"Kick Attacks Accuracy":0,
                     'Crit Rate':10, 'Crit Damage':0, 'DA DMG':0, 'TA DMG':0,"Sneak Attack":0,"Trick Attack":0,"Flourish Bonus":0,"Ranged Crit Damage":0,
                     'Store TP':0, "True Shot":0+5,"Double Shot Damage":0,"Triple Shot Damage":0,"Double Shot DMG":0,"Triple Shot DMG":0,
                     'PDL':0, 'PDL Trait':10,
                     'Dual Wield':0, 'Magic Haste':0, 'Gear Haste':0, 'JA Haste':0,"Martial Arts":0,
                     'Zanshin':0, "Zanshin OA2":0, "Fencer":0,"Fencer TP Bonus":0,"Hasso":0,"Recycle":0,
                     'Weaponskill Damage':0, 'Weaponskill Bonus':0, "Weaponskill Trait":0, 'Skillchain Bonus':0, 'ftp':0, 'TP Bonus':0, 'Weaponskill Accuracy':0,
                     'Delay1':0, 'Delay2':0, 'Delay':0, 'Ammo Delay':0, "Ranged Delay":0,
                     'DMG1':0, 'DMG2':0, 'Ammo DMG':0, "Ranged DMG":0,
                     'Light Elemental Bonus':0, 'Dark Elemental Bonus':0, 'Fire Elemental Bonus':0,'Earth Elemental Bonus':0, 'Water Elemental Bonus':0, 'Wind Elemental Bonus':0,'Ice Elemental Bonus':0, 'Thunder Elemental Bonus':0,'Elemental Bonus':0, 'Weaponskill Accuracy':0,
                     'Light Affinity':0, 'Dark Affinity':0, 'Fire Affinity':0,'Earth Affinity':0, 'Water Affinity':0, 'Wind Affinity':0,'Ice Affinity':0, 'Thunder Affinity':0,
                     "Magic Crit Rate II":0,"PDT":0,"MDT":0,"DT":0,"PDT2":0,"Magic Evasion":36,"Evasion":22,"Magic Def":0,"Subtle Blow":0,"Subtle Blow II":0,
                     }
        elif mainjob == "BRD":  # Master Level 20 Bard stats. Fencer is added later.
            self.playerstats = {'STR':110, 'DEX':110, 'VIT':110, 'AGI':104, 'INT':110, 'MND':110, 'CHR':115,
                     'Katana Skill':0+16, 'Dagger Skill':408+16, 'Sword Skill':388+16, 'Hand-to-Hand Skill':0+16, 'Great Katana Skill':0+16, 'Club Skill':358+16, 'Throwing Skill':320+16,
                     'Axe Skill':0+16,'Great Axe Skill':0+16,'Polearm Skill':0+16,'Scythe Skill':0+16,'Staff Skill':398+16,'Great Sword Skill':0+16,'Archery Skill':0+16,'Marksmanship Skill':0+16,
                     'Ninjutsu Skill':0+16, "Elemental Magic Skill":0+16, "Evasion Skill":354+16,
                     'Accuracy1':16, 'Accuracy2':16, 'Attack1':0, 'Attack2':0,
                     'Ranged Accuracy':16, 'Ranged Attack':26,
                     'Magic Accuracy':26, 'Magic Attack':0, 'Magic Damage':0, 'Magic Accuracy Skill':0, 'Ninjutsu Magic Attack':0, 'Ninjutsu Damage':0, 'Magic Crit Rate':0,
                     'Magic Burst Damage':0, 'Magic Burst Damage II':0,'Magic Burst Damage Trait':0,"Magic Burst Accuracy":0,
                     "Quick Draw":40,"Quick Draw II":0,
                     'Daken':0, 'QA':0, 'TA':0, 'DA':0, 'OA8':0, 'OA7':0, 'OA6':0, 'OA5':0, 'OA4':0, 'OA3':0, 'OA2':0,"Double Shot":0,"Triple Shot":0,
                     "Kick Attacks":0,"Kick Attacks Attack":0,"Kick Attacks Accuracy":0,
                     'Crit Rate':10, 'Crit Damage':0, 'DA DMG':0, 'TA DMG':0,"Sneak Attack":0,"Trick Attack":0,"Flourish Bonus":0,"Ranged Crit Damage":0,
                     'Store TP':0, "True Shot":0,"Double Shot Damage":0,"Triple Shot Damage":0,"Double Shot DMG":0,"Triple Shot DMG":0,
                     'PDL':0, 'PDL Trait':0,
                     'Dual Wield':0, 'Magic Haste':0, 'Gear Haste':0, 'JA Haste':0,"Martial Arts":0,
                     'Zanshin':0, "Zanshin OA2":0, "Fencer":0,"Fencer TP Bonus":0,"Hasso":0,"Recycle":0,
                     'Weaponskill Damage':0, 'Weaponskill Bonus':0, "Weaponskill Trait":0, 'Skillchain Bonus':0, 'ftp':0, 'TP Bonus':0, 'Weaponskill Accuracy':0,
                     'Delay1':0, 'Delay2':0, 'Delay':0, 'Ammo Delay':0, "Ranged Delay":0,
                     'DMG1':0, 'DMG2':0, 'Ammo DMG':0, "Ranged DMG":0,
                     'Light Elemental Bonus':0, 'Dark Elemental Bonus':0, 'Fire Elemental Bonus':0,'Earth Elemental Bonus':0, 'Water Elemental Bonus':0, 'Wind Elemental Bonus':0,'Ice Elemental Bonus':0, 'Thunder Elemental Bonus':0,'Elemental Bonus':0, 'Weaponskill Accuracy':0,
                     'Light Affinity':0, 'Dark Affinity':0, 'Fire Affinity':0,'Earth Affinity':0, 'Water Affinity':0, 'Wind Affinity':0,'Ice Affinity':0, 'Thunder Affinity':0,
                     "Magic Crit Rate II":0,"PDT":0,"MDT":0,"DT":0,"PDT2":0,"Magic Evasion":36,"Evasion":22,"Magic Def":0,"Subtle Blow":0,"Subtle Blow II":0,
                     }
        elif mainjob == "THF":  # Master Level 20 Thief stats.
            self.playerstats = {'STR':110, 'DEX':117, 'VIT':110, 'AGI':115, 'INT':113, 'MND':101, 'CHR':101,
                     'Katana Skill':0+16, 'Dagger Skill':444+16, 'Sword Skill':354+16, 'Hand-to-Hand Skill':320+16, 'Great Katana Skill':388+16, 'Club Skill':320+16, 'Throwing Skill':444+16,
                     'Axe Skill':0+16,'Great Axe Skill':0+16,'Polearm Skill':0+16,'Scythe Skill':0+16,'Staff Skill':0+16,'Great Sword Skill':0+16,'Archery Skill':388+16,'Marksmanship Skill':398+16,
                     'Ninjutsu Skill':0+16, "Elemental Magic Skill":0+16, "Evasion Skill":444+16,
                     'Accuracy1':36, 'Accuracy2':36, 'Attack1':50, 'Attack2':50,
                     'Ranged Accuracy':36, 'Ranged Attack':50,
                     'Magic Accuracy':26, 'Magic Attack':0, 'Magic Damage':0, 'Magic Accuracy Skill':0, 'Ninjutsu Magic Attack':0, 'Ninjutsu Damage':0, 'Magic Crit Rate':0,
                     'Magic Burst Damage':0, 'Magic Burst Damage II':0, 'Magic Burst Damage Trait':0, "Magic Burst Accuracy":0,
                     "Quick Draw":0,"Quick Draw II":0,
                     'Daken':0, 'QA':0, 'TA':8+6, 'DA':0, 'OA8':0, 'OA7':0, 'OA6':0, 'OA5':0, 'OA4':0, 'OA3':0, 'OA2':0,"Double Shot":0,"Triple Shot":0,
                     "Kick Attacks":0,"Kick Attacks Attack":0,"Kick Attacks Accuracy":0,
                     'Crit Rate':10, 'Crit Damage':8+14, 'DA DMG':0, 'TA DMG':0,"Sneak Attack":20,"Trick Attack":20,"Flourish Bonus":0,"Ranged Crit Damage":0,
                     'Store TP':0, "True Shot":0,"Double Shot Damage":0,"Triple Shot Damage":0,"Double Shot DMG":0,"Triple Shot DMG":0,
                     'PDL':0, 'PDL Trait':10,
                     'Dual Wield':30, 'Magic Haste':0, 'Gear Haste':0, 'JA Haste':0,"Martial Arts":0,
                     'Zanshin':0, "Zanshin OA2":0, "Fencer":0,"Fencer TP Bonus":0,"Hasso":0,"Recycle":0,
                     'Weaponskill Damage':0, 'Weaponskill Bonus':0, "Weaponskill Trait":0, 'Skillchain Bonus':0, 'ftp':0, 'TP Bonus':0, 'Weaponskill Accuracy':0,
                     'Delay1':0, 'Delay2':0, 'Delay':0, 'Ammo Delay':0, "Ranged Delay":0,
                     'DMG1':0, 'DMG2':0, 'Ammo DMG':0, "Ranged DMG":0,
                     'Light Elemental Bonus':0, 'Dark Elemental Bonus':0, 'Fire Elemental Bonus':0,'Earth Elemental Bonus':0, 'Water Elemental Bonus':0, 'Wind Elemental Bonus':0,'Ice Elemental Bonus':0, 'Thunder Elemental Bonus':0,'Elemental Bonus':0, 'Weaponskill Accuracy':0,
                     'Light Affinity':0, 'Dark Affinity':0, 'Fire Affinity':0,'Earth Affinity':0, 'Water Affinity':0, 'Wind Affinity':0,'Ice Affinity':0, 'Thunder Affinity':0,
                     "Magic Crit Rate II":0,"PDT":0,"MDT":0,"DT":0,"PDT2":0,"Magic Evasion":36,"Evasion":70+72,"Magic Def":0,"Subtle Blow":0,"Subtle Blow II":0,
                     }
        elif mainjob == "MNK":  # Master Level 20 Monk stats. Smite is added later. Kick attacks are zeroed out after adding gear stats later if not using a h2h weapon.
            self.playerstats = {'STR':113, 'DEX':115, 'VIT':117, 'AGI':104, 'INT':101, 'MND':110, 'CHR':107,
                     'Katana Skill':0+16, 'Dagger Skill':0+16, 'Sword Skill':0+16, 'Hand-to-Hand Skill':444+16, 'Great Katana Skill':0+16, 'Club Skill':398+16, 'Throwing Skill':320+16,
                     'Axe Skill':0+16,'Great Axe Skill':0+16,'Polearm Skill':0+16,'Scythe Skill':0+16,'Staff Skill':418+16,'Great Sword Skill':0+16,'Archery Skill':0+16,'Marksmanship Skill':0+16,
                     'Ninjutsu Skill':0+16, "Elemental Magic Skill":0+16, "Evasion Skill":424+16,
                     'Accuracy1':41, 'Accuracy2':41, 'Attack1':40, 'Attack2':40,
                     'Ranged Accuracy':41, 'Ranged Attack':40,
                     'Magic Accuracy':26, 'Magic Attack':0, 'Magic Damage':0, 'Magic Accuracy Skill':0, 'Ninjutsu Magic Attack':0, 'Ninjutsu Damage':0, 'Magic Crit Rate':0,
                     'Magic Burst Damage':0, 'Magic Burst Damage II':0, 'Magic Burst Damage Trait':0, "Magic Burst Accuracy":0,
                     "Quick Draw":0,"Quick Draw II":0,
                     'Daken':0, 'QA':0, 'TA':0, 'DA':0, 'OA8':0, 'OA7':0, 'OA6':0, 'OA5':0, 'OA4':0, 'OA3':0, 'OA2':0,"Double Shot":0,"Triple Shot":0,
                     "Kick Attacks":5+14,"Kick Attacks Attack":0,"Kick Attacks Accuracy":0, # TODO: we need +40 flat attack and +20 acc to kicks only somehow
                     'Crit Rate':10, 'Crit Damage':0, 'DA DMG':0, 'TA DMG':0,"Sneak Attack":0,"Trick Attack":0,"Flourish Bonus":0,"Ranged Crit Damage":0,
                     'Store TP':0, "True Shot":0,"Double Shot Damage":0,"Triple Shot Damage":0,"Double Shot DMG":0,"Triple Shot DMG":0,
                     'PDL':0, 'PDL Trait':30,
                     'Dual Wield':0, 'Magic Haste':0, 'Gear Haste':0, 'JA Haste':0,"Martial Arts":210,
                     'Zanshin':0, "Zanshin OA2":0, "Fencer":0,"Fencer TP Bonus":0,"Hasso":0,"Recycle":0,
                     'Weaponskill Damage':0, 'Weaponskill Bonus':0, "Weaponskill Trait":0, 'Skillchain Bonus':12, 'ftp':0, 'TP Bonus':0, 'Weaponskill Accuracy':0,
                     'Delay1':0, 'Delay2':0, 'Delay':0, 'Ammo Delay':0, "Ranged Delay":0,
                     'DMG1':0, 'DMG2':0, 'Ammo DMG':0, "Ranged DMG":0,
                     'Light Elemental Bonus':0, 'Dark Elemental Bonus':0, 'Fire Elemental Bonus':0,'Earth Elemental Bonus':0, 'Water Elemental Bonus':0, 'Wind Elemental Bonus':0,'Ice Elemental Bonus':0, 'Thunder Elemental Bonus':0,'Elemental Bonus':0, 'Weaponskill Accuracy':0,
                     'Light Affinity':0, 'Dark Affinity':0, 'Fire Affinity':0,'Earth Affinity':0, 'Water Affinity':0, 'Wind Affinity':0,'Ice Affinity':0, 'Thunder Affinity':0,
                     "Magic Crit Rate II":0,"PDT":0,"MDT":0,"DT":0,"PDT2":0,"Magic Evasion":36,"Evasion":42,"Magic Def":0,"Subtle Blow":35,"Subtle Blow II":0,
                     }
        elif mainjob == "BLU":  # Master Level 20 Blue Mage stats. Traits are added later to make it easier to adjust them with a drop-down menu based on spells used.
            self.playerstats = {'STR':107, 'DEX':107, 'VIT':107, 'AGI':107, 'INT':107, 'MND':107, 'CHR':107,
                     'Katana Skill':0+16, 'Dagger Skill':0+16, 'Sword Skill':444+16, 'Hand-to-Hand Skill':0+16, 'Great Katana Skill':0+16, 'Club Skill':408+16, 'Throwing Skill':0+16,
                     'Axe Skill':0+16,'Great Axe Skill':0+16,'Polearm Skill':0+16,'Scythe Skill':0+16,'Staff Skill':0+16,'Great Sword Skill':0+16,'Archery Skill':0+16,'Marksmanship Skill':0+16,
                     'Ninjutsu Skill':0+16, "Elemental Magic Skill":0+16, "Evasion Skill":388+16,
                     'Accuracy1':36, 'Accuracy2':36, 'Attack1':70, 'Attack2':70,
                     'Ranged Accuracy':36, 'Ranged Attack':70,
                     'Magic Accuracy':26+20, 'Magic Attack':26, 'Magic Damage':0, 'Magic Accuracy Skill':0, 'Ninjutsu Magic Attack':0, 'Ninjutsu Damage':0, 'Magic Crit Rate':0,
                     'Magic Burst Damage':0, 'Magic Burst Damage II':0, 'Magic Burst Damage Trait':0, "Magic Burst Accuracy":0,
                     "Quick Draw":0,"Quick Draw II":0,
                     'Daken':0, 'QA':0, 'TA':0, 'DA':0, 'OA8':0, 'OA7':0, 'OA6':0, 'OA5':0, 'OA4':0, 'OA3':0, 'OA2':0,"Double Shot":0,"Triple Shot":0,
                     "Kick Attacks":0,"Kick Attacks Attack":0,"Kick Attacks Accuracy":0,
                     'Crit Rate':10, 'Crit Damage':8, 'DA DMG':0, 'TA DMG':0,"Sneak Attack":0,"Trick Attack":0,"Flourish Bonus":0,"Ranged Crit Damage":0,
                     'Store TP':0, "True Shot":0,"Double Shot Damage":0,"Triple Shot Damage":0,"Double Shot DMG":0,"Triple Shot DMG":0,
                     'PDL':0, 'PDL Trait':0,
                     'Dual Wield':0, 'Magic Haste':0, 'Gear Haste':0, 'JA Haste':0,"Martial Arts":0,
                     'Zanshin':0, "Zanshin OA2":0, "Fencer":0,"Fencer TP Bonus":0,"Hasso":0,"Recycle":0,
                     'Weaponskill Damage':0, 'Weaponskill Bonus':0, "Weaponskill Trait":0, 'Skillchain Bonus':0, 'ftp':0, 'TP Bonus':0, 'Weaponskill Accuracy':0,
                     'Delay1':0, 'Delay2':0, 'Delay':0, 'Ammo Delay':0, "Ranged Delay":0,
                     'DMG1':0, 'DMG2':0, 'Ammo DMG':0, "Ranged DMG":0,
                     'Light Elemental Bonus':0, 'Dark Elemental Bonus':0, 'Fire Elemental Bonus':0,'Earth Elemental Bonus':0, 'Water Elemental Bonus':0, 'Wind Elemental Bonus':0,'Ice Elemental Bonus':0, 'Thunder Elemental Bonus':0,'Elemental Bonus':0, 'Weaponskill Accuracy':0,
                     'Light Affinity':0, 'Dark Affinity':0, 'Fire Affinity':0,'Earth Affinity':0, 'Water Affinity':0, 'Wind Affinity':0,'Ice Affinity':0, 'Thunder Affinity':0,
                     "Magic Crit Rate II":0,"PDT":0,"MDT":0,"DT":0,"PDT2":0,"Magic Evasion":36,"Evasion":36,"Magic Def":0,"Subtle Blow":0,"Subtle Blow II":0,
                     }
        elif mainjob == "DNC":  # Master Level 20 Dancer stats. +15 Accuracy and Evasion when facing an enemy (5/5 Closed Position merits)
            self.playerstats = {'STR':110, 'DEX':113, 'VIT':107, 'AGI':115, 'INT':104, 'MND':104, 'CHR':115,
                     'Katana Skill':0+16, 'Dagger Skill':444+16, 'Sword Skill':354+16, 'Hand-to-Hand Skill':354+16, 'Great Katana Skill':0+16, 'Club Skill':0+16, 'Throwing Skill':444+16,
                     'Axe Skill':0+16,'Great Axe Skill':0+16,'Polearm Skill':0+16,'Scythe Skill':0+16,'Staff Skill':0+16,'Great Sword Skill':0+16,'Archery Skill':0+16,'Marksmanship Skill':0+16,
                     'Ninjutsu Skill':0+16, "Elemental Magic Skill":0+16, "Evasion Skill":424+16,
                     'Accuracy1':64+15+35, 'Accuracy2':64+15+35, 'Attack1':42, 'Attack2':42,
                     'Ranged Accuracy':64+35, 'Ranged Attack':42,
                     'Magic Accuracy':26, 'Magic Attack':0, 'Magic Damage':0, 'Magic Accuracy Skill':0, 'Ninjutsu Magic Attack':0, 'Ninjutsu Damage':0, 'Magic Crit Rate':0,
                     'Magic Burst Damage':0, 'Magic Burst Damage II':0, 'Magic Burst Damage Trait':0, "Magic Burst Accuracy":0,
                     "Quick Draw":0,"Quick Draw II":0,
                     'Daken':0, 'QA':0, 'TA':0, 'DA':0, 'OA8':0, 'OA7':0, 'OA6':0, 'OA5':0, 'OA4':0, 'OA3':0, 'OA2':0,"Double Shot":0,"Triple Shot":0,
                     "Kick Attacks":0,"Kick Attacks Attack":0,"Kick Attacks Accuracy":0,
                     'Crit Rate':10, 'Crit Damage':8+11, 'DA DMG':0, 'TA DMG':0,"Sneak Attack":0,"Trick Attack":0,"Flourish Bonus":20,"Ranged Crit Damage":0,
                     'Store TP':0, "True Shot":0,"Double Shot Damage":0,"Triple Shot Damage":0,"Double Shot DMG":0,"Triple Shot DMG":0,
                     'PDL':0, 'PDL Trait':20,
                     'Dual Wield':5+30, 'Magic Haste':0, 'Gear Haste':0, 'JA Haste':10,"Martial Arts":0, # +10 JA Haste assuming haste samba with 5/5 merits
                     'Zanshin':0, "Zanshin OA2":0, "Fencer":0,"Fencer TP Bonus":0,"Hasso":0,"Recycle":0,
                     'Weaponskill Damage':0, 'Weaponskill Bonus':0, "Weaponskill Trait":0, 'Skillchain Bonus':0, 'ftp':0, 'TP Bonus':0, 'Weaponskill Accuracy':0,
                     'Delay1':0, 'Delay2':0, 'Delay':0, 'Ammo Delay':0, "Ranged Delay":0,
                     'DMG1':0, 'DMG2':0, 'Ammo DMG':0, "Ranged DMG":0,
                     'Light Elemental Bonus':0, 'Dark Elemental Bonus':0, 'Fire Elemental Bonus':0,'Earth Elemental Bonus':0, 'Water Elemental Bonus':0, 'Wind Elemental Bonus':0,'Ice Elemental Bonus':0, 'Thunder Elemental Bonus':0,'Elemental Bonus':0, 'Weaponskill Accuracy':0,
                     'Light Affinity':0, 'Dark Affinity':0, 'Fire Affinity':0,'Earth Affinity':0, 'Water Affinity':0, 'Wind Affinity':0,'Ice Affinity':0, 'Thunder Affinity':0,
                     "Magic Crit Rate II":0,"PDT":0,"MDT":0,"DT":0,"PDT2":0,"Magic Evasion":36,"Evasion":64+48+15,"Magic Def":0,"Subtle Blow":32,"Subtle Blow II":0,
                     }
        elif mainjob == "BST":  # Master Level THF TODO: BST stats. Smite and Fencer are added later. BST gets +50 accuracy from Tandem Strike.
            self.playerstats = {'STR':110, 'DEX':117, 'VIT':110, 'AGI':115, 'INT':113, 'MND':101, 'CHR':101,
                     'Katana Skill':0+16, 'Dagger Skill':398+16, 'Sword Skill':320+16, 'Hand-to-Hand Skill':0+16, 'Great Katana Skill':0+16, 'Club Skill':354+16, 'Throwing Skill':0+16,
                     'Axe Skill':444+16,'Great Axe Skill':0+16,'Polearm Skill':0+16,'Scythe Skill':388+16,'Staff Skill':0+16,'Great Sword Skill':0+16,'Archery Skill':0+16,'Marksmanship Skill':0+16,
                     'Ninjutsu Skill':0+16, "Elemental Magic Skill":0+16, "Evasion Skill":393+16,
                     'Accuracy1':36+50, 'Accuracy2':36+50, 'Attack1':70, 'Attack2':70,
                     'Ranged Accuracy':36, 'Ranged Attack':70,
                     'Magic Accuracy':36, 'Magic Attack':0, 'Magic Damage':0, 'Magic Accuracy Skill':0, 'Ninjutsu Magic Attack':0, 'Ninjutsu Damage':0, 'Magic Crit Rate':0,
                     'Magic Burst Damage':0, 'Magic Burst Damage II':0, 'Magic Burst Damage Trait':0, "Magic Burst Accuracy":0,
                     "Quick Draw":0,"Quick Draw II":0,
                     'Daken':0, 'QA':0, 'TA':0, 'DA':0, 'OA8':0, 'OA7':0, 'OA6':0, 'OA5':0, 'OA4':0, 'OA3':0, 'OA2':0,"Double Shot":0,"Triple Shot":0,
                     "Kick Attacks":0,"Kick Attacks Attack":0,"Kick Attacks Accuracy":0,
                     'Crit Rate':10, 'Crit Damage':0, 'DA DMG':0, 'TA DMG':0,"Sneak Attack":0,"Trick Attack":0,"Flourish Bonus":0,"Ranged Crit Damage":0,
                     'Store TP':0, "True Shot":0,"Double Shot Damage":0,"Triple Shot Damage":0,"Double Shot DMG":0,"Triple Shot DMG":0,
                     'PDL':0,"PDL Trait":20,
                     'Dual Wield':0, 'Magic Haste':0, 'Gear Haste':0, 'JA Haste':0,"Martial Arts":0,
                     'Zanshin':0, "Zanshin OA2":0, "Fencer":0, "Fencer TP Bonus":230,"Hasso":0,"Recycle":0,
                     'Weaponskill Damage':0, 'Weaponskill Bonus':0, "Weaponskill Trait":0, 'Skillchain Bonus':0, 'ftp':0, 'TP Bonus':0, 'Weaponskill Accuracy':0,
                     'Delay1':0, 'Delay2':0, 'Delay':0, 'Ammo Delay':0, "Ranged Delay":0,
                     'DMG1':0, 'DMG2':0, 'Ammo DMG':0, "Ranged DMG":0,
                     'Light Elemental Bonus':0, 'Dark Elemental Bonus':0, 'Fire Elemental Bonus':0, 'Earth Elemental Bonus':0, 'Water Elemental Bonus':0, 'Wind Elemental Bonus':0, 'Ice Elemental Bonus':0, 'Thunder Elemental Bonus':0,'Elemental Bonus':0,
                     'Light Affinity':0, 'Dark Affinity':0, 'Fire Affinity':0,'Earth Affinity':0, 'Water Affinity':0, 'Wind Affinity':0,'Ice Affinity':0, 'Thunder Affinity':0,
                     "Magic Crit Rate II":0,"PDT":0,"MDT":0,"DT":0,"PDT2":0,"Magic Evasion":36,"Evasion":36,"Magic Def":0,"Subtle Blow":0,"Subtle Blow II":0,
                     }
        elif mainjob == "GEO":  # Master Level 20 Geomancer stats
            self.playerstats = {'STR':104, 'DEX':110, 'VIT':110, 'AGI':107, 'INT':115, 'MND':115, 'CHR':107,
                     'Katana Skill':0+16, 'Dagger Skill':388+16, 'Sword Skill':0+16, 'Hand-to-Hand Skill':0+16, 'Great Katana Skill':0+16, 'Club Skill':424+16, 'Throwing Skill':0+16,
                     'Axe Skill':0+16,'Great Axe Skill':0+16,'Polearm Skill':0+16,'Scythe Skill':0+16,'Staff Skill':398+16,'Great Sword Skill':0+16,'Archery Skill':0+16,'Marksmanship Skill':0+16,
                     'Ninjutsu Skill':0+16, "Elemental Magic Skill":424+16+23, "Evasion Skill":354+16,
                     'Accuracy1':0, 'Accuracy2':0, 'Attack1':0, 'Attack2':0,
                     'Ranged Accuracy':0, 'Ranged Attack':0,
                     'Magic Accuracy':50+20, 'Magic Attack':42+20, 'Magic Damage':13, 'Magic Accuracy Skill':0, 'Ninjutsu Magic Attack':0, 'Ninjutsu Damage':0, 'Magic Crit Rate':0,
                     'Magic Burst Damage':0, 'Magic Burst Damage II':0, 'Magic Burst Damage Trait':0, "Magic Burst Accuracy":0,
                     "Quick Draw":0,"Quick Draw II":0,
                     'Daken':0, 'QA':0, 'TA':0, 'DA':0, 'OA8':0, 'OA7':0, 'OA6':0, 'OA5':0, 'OA4':0, 'OA3':0, 'OA2':0,"Double Shot":0,"Triple Shot":0,
                     "Kick Attacks":0,"Kick Attacks Attack":0,"Kick Attacks Accuracy":0,
                     'Crit Rate':10, 'Crit Damage':0, 'DA DMG':0, 'TA DMG':0,"Sneak Attack":0,"Trick Attack":0,"Flourish Bonus":0,"Ranged Crit Damage":0,
                     'Store TP':0, "True Shot":0,"Double Shot Damage":0,"Triple Shot Damage":0,"Double Shot DMG":0,"Triple Shot DMG":0,
                     'PDL':0,"PDL Trait":0,
                     'Dual Wield':0, 'Magic Haste':0, 'Gear Haste':0, 'JA Haste':0,"Martial Arts":0,
                     'Zanshin':0, "Zanshin OA2":0, "Fencer":0,"Fencer TP Bonus":0,"Hasso":0,"Recycle":0,
                     'Weaponskill Damage':0, 'Weaponskill Bonus':0, "Weaponskill Trait":0, 'Skillchain Bonus':0, 'ftp':0, 'TP Bonus':0, 'Weaponskill Accuracy':0,
                     'Delay1':0, 'Delay2':0, 'Delay':0, 'Ammo Delay':0, "Ranged Delay":0,
                     'DMG1':0, 'DMG2':0, 'Ammo DMG':0, "Ranged DMG":0,
                     'Light Elemental Bonus':0, 'Dark Elemental Bonus':0, 'Fire Elemental Bonus':0, 'Earth Elemental Bonus':0, 'Water Elemental Bonus':0, 'Wind Elemental Bonus':0, 'Ice Elemental Bonus':0, 'Thunder Elemental Bonus':0,'Elemental Bonus':0,
                     'Light Affinity':0, 'Dark Affinity':0, 'Fire Affinity':0,'Earth Affinity':0, 'Water Affinity':0, 'Wind Affinity':0,'Ice Affinity':0, 'Thunder Affinity':0,
                     "Magic Crit Rate II":0,"PDT":0,"MDT":0,"DT":0,"PDT2":0,"Magic Evasion":50,"Evasion":0,"Magic Def":0,"Subtle Blow":0,"Subtle Blow II":0,
                     }
        elif mainjob == "PLD":  # Master Level 20 Paladin stats
            self.playerstats = {'STR':115, 'DEX':107, 'VIT':117, 'AGI':101, 'INT':101, 'MND':113, 'CHR':113,
                     'Katana Skill':0+16, 'Dagger Skill':388+16, 'Sword Skill':444+16, 'Hand-to-Hand Skill':0+16, 'Great Katana Skill':0+16, 'Club Skill':437+16, 'Throwing Skill':0+16,
                     'Axe Skill':0+16,'Great Axe Skill':0+16,'Polearm Skill':320+16,'Scythe Skill':0+16,'Staff Skill':437+16,'Great Sword Skill':418+16,'Archery Skill':0+16,'Marksmanship Skill':0+16,
                     'Ninjutsu Skill':0+16, "Elemental Magic Skill":0+16, "Evasion Skill":393+16,
                     'Accuracy1':28, 'Accuracy2':28, 'Attack1':28, 'Attack2':28,
                     'Ranged Accuracy':28, 'Ranged Attack':28,
                     'Magic Accuracy':42, 'Magic Attack':0, 'Magic Damage':0, 'Magic Accuracy Skill':0, 'Ninjutsu Magic Attack':0, 'Ninjutsu Damage':0, 'Magic Crit Rate':0,
                     'Magic Burst Damage':0, 'Magic Burst Damage II':0, 'Magic Burst Damage Trait':0, "Magic Burst Accuracy":0,
                     "Quick Draw":0,"Quick Draw II":0,
                     'Daken':0, 'QA':0, 'TA':0, 'DA':0, 'OA8':0, 'OA7':0, 'OA6':0, 'OA5':0, 'OA4':0, 'OA3':0, 'OA2':0,"Double Shot":0,"Triple Shot":0,
                     "Kick Attacks":0,"Kick Attacks Attack":0,"Kick Attacks Accuracy":0,
                     'Crit Rate':10, 'Crit Damage':0, 'DA DMG':0, 'TA DMG':0,"Sneak Attack":0,"Trick Attack":0,"Flourish Bonus":0,"Ranged Crit Damage":0,
                     'Store TP':0, "True Shot":0,"Double Shot Damage":0,"Triple Shot Damage":0,"Double Shot DMG":0,"Triple Shot DMG":0,
                     'PDL':0,"PDL Trait":0,
                     'Dual Wield':0, 'Magic Haste':0, 'Gear Haste':0, 'JA Haste':0,"Martial Arts":0,
                     'Zanshin':0, "Zanshin OA2":0, "Fencer":0,"Fencer TP Bonus":0,"Hasso":0,"Recycle":0,
                     'Weaponskill Damage':0, 'Weaponskill Bonus':0, "Weaponskill Trait":0, 'Skillchain Bonus':0, 'ftp':0, 'TP Bonus':0, 'Weaponskill Accuracy':0,
                     'Delay1':0, 'Delay2':0, 'Delay':0, 'Ammo Delay':0, "Ranged Delay":0,
                     'DMG1':0, 'DMG2':0, 'Ammo DMG':0, "Ranged DMG":0,
                     'Light Elemental Bonus':0, 'Dark Elemental Bonus':0, 'Fire Elemental Bonus':0, 'Earth Elemental Bonus':0, 'Water Elemental Bonus':0, 'Wind Elemental Bonus':0, 'Ice Elemental Bonus':0, 'Thunder Elemental Bonus':0,'Elemental Bonus':0,
                     'Light Affinity':0, 'Dark Affinity':0, 'Fire Affinity':0,'Earth Affinity':0, 'Water Affinity':0, 'Wind Affinity':0,'Ice Affinity':0, 'Thunder Affinity':0,
                     "Magic Crit Rate II":0,"PDT":0,"MDT":0,"DT":0,"PDT2":0,"Magic Evasion":42,"Evasion":22,"Magic Def":0,"Subtle Blow":0,"Subtle Blow II":0,
                     }
        elif mainjob == "RUN":  # Master Level 20 Rune Fencer stats
            self.playerstats = {'STR':113, 'DEX':110, 'VIT':107, 'AGI':115, 'INT':110, 'MND':110, 'CHR':104,
                     'Katana Skill':0+16, 'Dagger Skill':0+16, 'Sword Skill':437+16, 'Hand-to-Hand Skill':0+16, 'Great Katana Skill':0+16, 'Club Skill':388+16, 'Throwing Skill':0+16,
                     'Axe Skill':408+16,'Great Axe Skill':418+16,'Polearm Skill':0+16,'Scythe Skill':0+16,'Staff Skill':0+16,'Great Sword Skill':444+16,'Archery Skill':0+16,'Marksmanship Skill':0+16,
                     'Ninjutsu Skill':0+16, "Elemental Magic Skill":0+16, "Evasion Skill":424+16,
                     'Accuracy1':56+35, 'Accuracy2':56+35, 'Attack1':50, 'Attack2':50,
                     'Ranged Accuracy':56+35, 'Ranged Attack':50,
                     'Magic Accuracy':26, 'Magic Attack':0, 'Magic Damage':0, 'Magic Accuracy Skill':0, 'Ninjutsu Magic Attack':0, 'Ninjutsu Damage':0, 'Magic Crit Rate':0,
                     'Magic Burst Damage':0, 'Magic Burst Damage II':0, 'Magic Burst Damage Trait':0, "Magic Burst Accuracy":0,
                     "Quick Draw":0,"Quick Draw II":0,
                     'Daken':0, 'QA':0, 'TA':0, 'DA':0, 'OA8':0, 'OA7':0, 'OA6':0, 'OA5':0, 'OA4':0, 'OA3':0, 'OA2':0,"Double Shot":0,"Triple Shot":0,
                     "Kick Attacks":0,"Kick Attacks Attack":0,"Kick Attacks Accuracy":0,
                     'Crit Rate':10, 'Crit Damage':0, 'DA DMG':0, 'TA DMG':0,"Sneak Attack":0,"Trick Attack":0,"Flourish Bonus":0,"Ranged Crit Damage":0,
                     'Store TP':0, "True Shot":0,"Double Shot Damage":0,"Triple Shot Damage":0,"Double Shot DMG":0,"Triple Shot DMG":0,
                     'PDL':0,"PDL Trait":0,
                     'Dual Wield':0, 'Magic Haste':0, 'Gear Haste':0, 'JA Haste':0,"Martial Arts":0,
                     'Zanshin':0, "Zanshin OA2":0, "Fencer":0,"Fencer TP Bonus":0,"Hasso":0,"Recycle":0,
                     'Weaponskill Damage':0, 'Weaponskill Bonus':0, "Weaponskill Trait":0, 'Skillchain Bonus':0, 'ftp':0, 'TP Bonus':0, 'Weaponskill Accuracy':0,
                     'Delay1':0, 'Delay2':0, 'Delay':0, 'Ammo Delay':0, "Ranged Delay":0,
                     'DMG1':0, 'DMG2':0, 'Ammo DMG':0, "Ranged DMG":0,
                     'Light Elemental Bonus':0, 'Dark Elemental Bonus':0, 'Fire Elemental Bonus':0, 'Earth Elemental Bonus':0, 'Water Elemental Bonus':0, 'Wind Elemental Bonus':0, 'Ice Elemental Bonus':0, 'Thunder Elemental Bonus':0,'Elemental Bonus':0,
                     'Light Affinity':0, 'Dark Affinity':0, 'Fire Affinity':0,'Earth Affinity':0, 'Water Affinity':0, 'Wind Affinity':0,'Ice Affinity':0, 'Thunder Affinity':0,
                     "Magic Crit Rate II":0,"PDT":0,"MDT":0,"DT":0,"PDT2":0,"Magic Evasion":70,"Evasion":56,"Magic Def":22,"Subtle Blow":0,"Subtle Blow II":0,
                     }
        elif mainjob == "RNG":  # Master Level 20 Ranger stats. +45 Ranged Crit from Dead Aim traits
            self.playerstats = {'STR':107, 'DEX':110, 'VIT':110, 'AGI':117, 'INT':107, 'MND':110, 'CHR':107,
                     'Katana Skill':0+16, 'Dagger Skill':408+16, 'Sword Skill':354+16, 'Hand-to-Hand Skill':0+16, 'Great Katana Skill':0+16, 'Club Skill':320+16, 'Throwing Skill':388+16,
                     'Axe Skill':408+16,'Great Axe Skill':0+16,'Polearm Skill':0+16,'Scythe Skill':0+16,'Staff Skill':0+16,'Great Sword Skill':0+16,'Archery Skill':444+16,'Marksmanship Skill':444+16,
                     'Ninjutsu Skill':0+16, "Elemental Magic Skill":0+16, "Evasion Skill":320+16,
                     'Accuracy1':70+73, 'Accuracy2':70+73, 'Attack1':70, 'Attack2':70,
                     'Ranged Accuracy':70+73, 'Ranged Attack':70,
                     'Magic Accuracy':26, 'Magic Attack':0, 'Magic Damage':0, 'Magic Accuracy Skill':0, 'Ninjutsu Magic Attack':0, 'Ninjutsu Damage':0, 'Magic Crit Rate':0,
                     'Magic Burst Damage':0, 'Magic Burst Damage II':0, 'Magic Burst Damage Trait':0, "Magic Burst Accuracy":0,
                     "Quick Draw":0,"Quick Draw II":0,
                     'Daken':0, 'QA':0, 'TA':0, 'DA':0, 'OA8':0, 'OA7':0, 'OA6':0, 'OA5':0, 'OA4':0, 'OA3':0, 'OA2':0,"Double Shot":20,"Triple Shot":0,
                     "Kick Attacks":0,"Kick Attacks Attack":0,"Kick Attacks Accuracy":0,
                     'Crit Rate':10, 'Crit Damage':0, 'DA DMG':0, 'TA DMG':0,"Sneak Attack":0,"Trick Attack":0,"Flourish Bonus":0,"Ranged Crit Damage":8+45,
                     'Store TP':0, "True Shot":8+7,"Double Shot Damage":0,"Triple Shot Damage":0,"Double Shot DMG":0,"Triple Shot DMG":0,
                     'PDL':0,"PDL Trait":30,
                     'Dual Wield':0, 'Magic Haste':0, 'Gear Haste':0, 'JA Haste':0,"Martial Arts":0,
                     'Zanshin':0, "Zanshin OA2":0, "Fencer":0,"Fencer TP Bonus":0,"Hasso":0,"Recycle":30+25,
                     'Weaponskill Damage':0, 'Weaponskill Bonus':0, "Weaponskill Trait":0, 'Skillchain Bonus':0, 'ftp':0, 'TP Bonus':0, 'Weaponskill Accuracy':0,
                     'Delay1':0, 'Delay2':0, 'Delay':0, 'Ammo Delay':0, "Ranged Delay":0,
                     'DMG1':0, 'DMG2':0, 'Ammo DMG':0, "Ranged DMG":0,
                     'Light Elemental Bonus':0, 'Dark Elemental Bonus':0, 'Fire Elemental Bonus':0, 'Earth Elemental Bonus':0, 'Water Elemental Bonus':0, 'Wind Elemental Bonus':0, 'Ice Elemental Bonus':0, 'Thunder Elemental Bonus':0,'Elemental Bonus':0,
                     'Light Affinity':0, 'Dark Affinity':0, 'Fire Affinity':0,'Earth Affinity':0, 'Water Affinity':0, 'Wind Affinity':0,'Ice Affinity':0, 'Thunder Affinity':0,
                     "Magic Crit Rate II":0,"PDT":0,"MDT":0,"DT":0,"PDT2":0,"Magic Evasion":36,"Evasion":14,"Magic Def":0,"Subtle Blow":0,"Subtle Blow II":0,
                     }
        elif mainjob == "PUP":  # Master Level 20 Puppetmaster stats
            self.playerstats = {'STR':107, 'DEX':115, 'VIT':110, 'AGI':113, 'INT':107, 'MND':104, 'CHR':113,
                     'Katana Skill':0+16, 'Dagger Skill':388+16, 'Sword Skill':0+16, 'Hand-to-Hand Skill':444+16, 'Great Katana Skill':0+16, 'Club Skill':354+16, 'Throwing Skill':398+16,
                     'Axe Skill':0+16,'Great Axe Skill':0+16,'Polearm Skill':0+16,'Scythe Skill':0+16,'Staff Skill':0+16,'Great Sword Skill':0+16,'Archery Skill':0+16,'Marksmanship Skill':0+16,
                     'Ninjutsu Skill':0+16, "Elemental Magic Skill":0+16, "Evasion Skill":418+16,
                     'Accuracy1':36, 'Accuracy2':36, 'Attack1':30, 'Attack2':30,
                     'Ranged Accuracy':36, 'Ranged Attack':30,
                     'Magic Accuracy':36, 'Magic Attack':0, 'Magic Damage':0, 'Magic Accuracy Skill':0, 'Ninjutsu Magic Attack':0, 'Ninjutsu Damage':0, 'Magic Crit Rate':0,
                      'Magic Burst Damage':0, 'Magic Burst Damage II':0, 'Magic Burst Damage Trait':0, "Magic Burst Accuracy":0,
                     "Quick Draw":0,"Quick Draw II":0,
                     'Daken':0, 'QA':0, 'TA':0, 'DA':0, 'OA8':0, 'OA7':0, 'OA6':0, 'OA5':0, 'OA4':0, 'OA3':0, 'OA2':0,"Double Shot":0,"Triple Shot":0,
                     "Kick Attacks":0,"Kick Attacks Attack":0,"Kick Attacks Accuracy":0,
                     'Crit Rate':10, 'Crit Damage':0, 'DA DMG':0, 'TA DMG':0,"Sneak Attack":0,"Trick Attack":0,"Flourish Bonus":0,"Ranged Crit Damage":0,
                     'Store TP':0, "True Shot":0,"Double Shot Damage":0,"Triple Shot Damage":0,"Double Shot DMG":0,"Triple Shot DMG":0,
                     'PDL':0,"PDL Trait":0,
                     'Dual Wield':0, 'Magic Haste':0, 'Gear Haste':0, 'JA Haste':0,"Martial Arts":205,
                     'Zanshin':0, "Zanshin OA2":0, "Fencer":0,"Fencer TP Bonus":0,"Hasso":0,"Recycle":0,
                     'Weaponskill Damage':0, 'Weaponskill Bonus':0, "Weaponskill Trait":0, 'Skillchain Bonus':0, 'ftp':0, 'TP Bonus':0, 'Weaponskill Accuracy':0,
                     'Delay1':0, 'Delay2':0, 'Delay':0, 'Ammo Delay':0, "Ranged Delay":0,
                     'DMG1':0, 'DMG2':0, 'Ammo DMG':0, "Ranged DMG":0,
                     'Light Elemental Bonus':0, 'Dark Elemental Bonus':0, 'Fire Elemental Bonus':0, 'Earth Elemental Bonus':0, 'Water Elemental Bonus':0, 'Wind Elemental Bonus':0, 'Ice Elemental Bonus':0, 'Thunder Elemental Bonus':0,'Elemental Bonus':0,
                     'Light Affinity':0, 'Dark Affinity':0, 'Fire Affinity':0,'Earth Affinity':0, 'Water Affinity':0, 'Wind Affinity':0,'Ice Affinity':0, 'Thunder Affinity':0,
                     "Magic Crit Rate II":0,"PDT":0,"MDT":0,"DT":0,"PDT2":0,"Magic Evasion":36,"Evasion":56+48,"Magic Def":0,"Subtle Blow":0,"Subtle Blow II":0,
                     }



        # Add job-specific bonuses.

        two_handed = ["Great Sword", "Great Katana", "Great Axe", "Polearm", "Scythe", "Staff", "Hand-to-Hand"]
        one_handed = ["Axe", "Club", "Dagger", "Sword", "Katana"] # Excluding H2H since H2H get smite bonuses, it's easier to include them in two_handed in this file.
        ranged_skills = ["Marksmanship","Archery"]

        smite_bonus = 0.
        building_flourish = 0.
        wyvern_bonus = False # This will only apply for DRG main job later.
        last_resort_bonus = 0. # Currently only for DRK main job

        # Add Smite bonuses now. We check for 2-handed weapon later
        if mainjob in ["DRK","WAR","MNK","DRG","PUP"]:
            smite_bonuses = {"DRK":304./1024, "WAR":204./1024, "MNK":152./1024, "DRG":152./1024, "PUP":100./1024}
            smite_bonus = smite_bonuses[mainjob]

        # Add Fencer trait bonuses now.
        if mainjob in ["WAR","BST","BRD"]:
            if self.gear["sub"]["Type"] != "Weapon" and self.gear["main"]["Skill Type"] not in two_handed:
                fencer_bonuses = {"WAR":5, "BST":3, "BRD":2}
                self.playerstats["Fencer"] += fencer_bonuses[mainjob]


        # Add specific Blue Magic bonuses now. Assuming the "Zahak Reborn" spellset from the ffxiah guide: https://www.ffxiah.com/forum/topic/30626/the-beast-within-a-guide-to-blue-mage/
        if mainjob == "BLU":
            self.playerstats["Accuracy1"] += 48
            self.playerstats["Accuracy2"] += 48
            self.playerstats["Ranged Accuracy"] += 48
            self.playerstats["Magic Accuracy"] += 36
            self.playerstats["Store TP"] += 30
            self.playerstats["Dual Wield"] += 25
            self.playerstats["TA"] += 5
            self.playerstats["Crit Damage"] += 11
            self.playerstats["Skillchain Bonus"] += 16
            self.playerstats["STR"] += 5+4+3+2-3
            self.playerstats["DEX"] += 8+6+2+4+4+1+8+4
            self.playerstats["VIT"] += 4+7+4
            self.playerstats["AGI"] += 5+2+1
            self.playerstats["MND"] += 4+2
            self.playerstats["INT"] += 4-1
            self.playerstats["CHR"] += 1+5-2


        if mainjob == "SAM": # Add Hasso stats
            if self.gear['main'].get('Skill Type', 'None') in two_handed:
                self.playerstats["STR"] += 14
                self.playerstats["STR"] += 20 # Job point category while using Hasso
                self.playerstats['JA Haste'] += 10
                self.playerstats['Accuracy1'] += 10
                self.playerstats['Accuracy2'] += 10

        if mainjob == "DRK": # Check for Last Resort
            if self.gear['main'].get('Skill Type', 'None') in two_handed:
                if job_abilities.get("Last Resort",False):
                    self.playerstats["Attack1"] += 40
                    self.playerstats["Attack2"] += 40
                    last_resort_bonus += 356./1024
                    self.playerstats["JA Haste"] += 25
        elif mainjob == "RNG": # Add hover shot and velocity shot bonuses
            if job_abilities.get("Velocity Shot",True):
                self.playerstats["Ranged Attack"] += 40
                self.playerstats["Magic Haste"] -= 0.15
            hover_shot = job_abilities.get("Hover Shot",0) # Hover shot not implemented.
            hover_shot = 100 if hover_shot > 100 else (0 if hover_shot < 0 else hover_shot)
            if hover_shot > 0:
                self.playerstats["Ranged Accuracy"] += hover_shot
                self.playerstats["Magic Accuracy"] += hover_shot
                # Hover shot direct damage bonus is applied in the main wsdist.py code. This code only adds to the player stats.

        elif mainjob == "MNK": # Add Impetus bonuses
            impetus_potency = 0.9
            self.playerstats["Attack1"] += 100*impetus_potency*impetus # Add 90% of the impetus here. # TODO: Find a better place for it.
            self.playerstats["Attack2"] += 100*impetus_potency*impetus
            self.playerstats["Crit Rate"] += 50*impetus_potency*impetus # 90% impetus potency = +45% crit rate and +90 attack.
            self.playerstats["Crit Damage"] += 50*impetus_potency*impetus*("Bhikku Cyclas" in gear["body"]["Name"]) # Impetus on and "Bhikku Cyclas" equipped is an extra 50% crit damage.
            if self.gear["main"]["Skill Type"] != "Hand-to-Hand": # Kick attacks only proc if using a h2h weapon
                self.playerstats["Kick Attacks"] = 0

        elif mainjob == "DRG": # DRG bonus stats for having a Wyvern out and fully leveled up.
            wyvern_bonus = True # This represents the +20% attack that will be applied later for having a wyvern out. Additive bonus with smite, berserk, chaos roll, etc.
            self.playerstats["Weaponskill Trait"] += 10 # Wyvern bonus. Applies to all WS hits, so it goes in the "Weaponskill Trait" stat.
            self.playerstats["JA Haste"] += 10
            self.playerstats["DA"] += 15

        elif mainjob == "DNC": # Bonus stats from building flourish.
            if job_abilities.get("Building Flourish",False):
                self.playerstats["Crit Rate"] += 10
                self.playerstats["Accuracy1"] += 40
                self.playerstats["Accuracy2"] += 40
                self.playerstats["Ranged Accuracy"] += 40
                self.playerstats["Weaponskill Damage"] += 20 # from job point categories
                building_flourish = 0.25

        # Special stats for main jobs are finished now.


        # Add bonuses from subjob stats

        if subjob == "WAR": # Master Level 20 bonus stats from Lv53 WAR subjob
            self.playerstats['STR'] += 15
            self.playerstats['DEX'] += 12
            self.playerstats['VIT'] += 10
            self.playerstats['AGI'] += 12
            self.playerstats['INT'] += 7
            self.playerstats['MND'] += 7
            self.playerstats['CHR'] += 9
        elif subjob == "MNK":
            self.playerstats["STR"] += 12
            self.playerstats["DEX"] += 13
            self.playerstats["VIT"] += 15
            self.playerstats["AGI"] += 7
            self.playerstats["INT"] += 6
            self.playerstats["MND"] += 10
            self.playerstats["CHR"] += 9
        elif subjob == "WHM":
            self.playerstats["STR"] += 10
            self.playerstats["DEX"] += 7
            self.playerstats["VIT"] += 10
            self.playerstats["AGI"] += 9
            self.playerstats["INT"] += 9
            self.playerstats["MND"] += 15
            self.playerstats["CHR"] += 12
        elif subjob == "BLM":
            self.playerstats["STR"] += 7
            self.playerstats["DEX"] += 12
            self.playerstats["VIT"] += 7
            self.playerstats["AGI"] += 12
            self.playerstats["INT"] += 15
            self.playerstats["MND"] += 9
            self.playerstats["CHR"] += 10
        elif subjob == "RDM":
            self.playerstats["STR"] += 10
            self.playerstats["DEX"] += 10
            self.playerstats["VIT"] += 9
            self.playerstats["AGI"] += 9
            self.playerstats["INT"] += 12
            self.playerstats["MND"] += 12
            self.playerstats["CHR"] += 10
        elif subjob == "THF":
            self.playerstats["STR"] += 10
            self.playerstats["DEX"] += 15
            self.playerstats["VIT"] += 10
            self.playerstats["AGI"] += 13
            self.playerstats["INT"] += 12
            self.playerstats["MND"] += 6
            self.playerstats["CHR"] += 6
        elif subjob == "PLD":
            self.playerstats["STR"] += 13
            self.playerstats["DEX"] += 9
            self.playerstats["VIT"] += 15
            self.playerstats["AGI"] += 6
            self.playerstats["INT"] += 6
            self.playerstats["MND"] += 12
            self.playerstats["CHR"] += 12
        elif subjob == "DRK":
            self.playerstats["STR"] += 15
            self.playerstats["DEX"] += 12
            self.playerstats["VIT"] += 12
            self.playerstats["AGI"] += 10
            self.playerstats["INT"] += 12
            self.playerstats["MND"] += 6
            self.playerstats["CHR"] += 6
        elif subjob == "BST":
            self.playerstats["STR"] += 0 # I have no idea what stats BST and BRD give. Mine are Lv1
            self.playerstats["DEX"] += 0
            self.playerstats["VIT"] += 0
            self.playerstats["AGI"] += 0
            self.playerstats["INT"] += 0
            self.playerstats["MND"] += 0
            self.playerstats["CHR"] += 0
        elif subjob == "BRD":
            self.playerstats["STR"] += 0 # I have no idea what stats BST and BRD give. Mine are Lv1
            self.playerstats["DEX"] += 0
            self.playerstats["VIT"] += 0
            self.playerstats["AGI"] += 0
            self.playerstats["INT"] += 0
            self.playerstats["MND"] += 0
            self.playerstats["CHR"] += 0
        elif subjob == "RNG":
            self.playerstats["STR"] += 9
            self.playerstats["DEX"] += 10
            self.playerstats["VIT"] += 10
            self.playerstats["AGI"] += 15
            self.playerstats["INT"] += 9
            self.playerstats["MND"] += 10
            self.playerstats["CHR"] += 9
        elif subjob == "SAM":
            if self.gear['main'].get('Skill Type', 'None') in two_handed:
                self.playerstats["STR"] += 7
                self.playerstats['JA Haste'] += 10
                self.playerstats['Accuracy1'] += 10
                self.playerstats['Accuracy2'] += 10
            self.playerstats["STR"] += 12
            self.playerstats["DEX"] += 12
            self.playerstats["VIT"] += 12
            self.playerstats["AGI"] += 10
            self.playerstats["INT"] += 9
            self.playerstats["MND"] += 9
            self.playerstats["CHR"] += 10
        elif subjob == "NIN":
            self.playerstats["STR"] += 12
            self.playerstats["DEX"] += 13
            self.playerstats["VIT"] += 12
            self.playerstats["AGI"] += 13
            self.playerstats["INT"] += 10
            self.playerstats["MND"] += 6
            self.playerstats["CHR"] += 7
        elif subjob == "DRG":
            self.playerstats["STR"] += 13
            self.playerstats["DEX"] += 10
            self.playerstats["VIT"] += 12
            self.playerstats["AGI"] += 10
            self.playerstats["INT"] += 7
            self.playerstats["MND"] += 9
            self.playerstats["CHR"] += 12
        elif subjob == "SMN":
            self.playerstats["STR"] += 7
            self.playerstats["DEX"] += 9
            self.playerstats["VIT"] += 7
            self.playerstats["AGI"] += 10
            self.playerstats["INT"] += 13
            self.playerstats["MND"] += 13
            self.playerstats["CHR"] += 13
        elif subjob == "BLU":
            self.playerstats["STR"] += 9
            self.playerstats["DEX"] += 9
            self.playerstats["VIT"] += 9
            self.playerstats["AGI"] += 9
            self.playerstats["INT"] += 9
            self.playerstats["MND"] += 9
            self.playerstats["CHR"] += 9
        elif subjob == "COR":
            self.playerstats["STR"] += 9
            self.playerstats["DEX"] += 12
            self.playerstats["VIT"] += 9
            self.playerstats["AGI"] += 13
            self.playerstats["INT"] += 12
            self.playerstats["MND"] += 9
            self.playerstats["CHR"] += 9
        elif subjob == "PUP":
            self.playerstats["STR"] += 9
            self.playerstats["DEX"] += 13
            self.playerstats["VIT"] += 10
            self.playerstats["AGI"] += 12
            self.playerstats["INT"] += 9
            self.playerstats["MND"] += 7
            self.playerstats["CHR"] += 12
        elif subjob == "DNC":
            self.playerstats['JA Haste'] += 5 # +5% JA haste from full-time Haste Samba
            self.playerstats["STR"] += 10
            self.playerstats["DEX"] += 12
            self.playerstats["VIT"] += 9
            self.playerstats["AGI"] += 13
            self.playerstats["INT"] += 7
            self.playerstats["MND"] += 7
            self.playerstats["CHR"] += 13
        elif subjob == "SCH": # Lv49 SCH subjob. Need to update to Lv53 TODO
            self.playerstats['STR'] += 7
            self.playerstats['DEX'] += 9
            self.playerstats['VIT'] += 8
            self.playerstats['AGI'] += 9
            self.playerstats['INT'] += 13
            self.playerstats['MND'] += 9
            self.playerstats['CHR'] += 11
            self.playerstats["Elemental Magic Skill"] = max(self.playerstats["Elemental Magic Skill"], 440+16) # Dark Arts enhances elemental magic skill to B+ rank, plus 16 from merits
            self.playerstats["Magic Accuracy"] += 15 # fulltime klimaform
        elif subjob == "GEO":
            self.playerstats["STR"] += 7
            self.playerstats["DEX"] += 10
            self.playerstats["VIT"] += 10
            self.playerstats["AGI"] += 9
            self.playerstats["INT"] += 13
            self.playerstats["MND"] += 13
            self.playerstats["CHR"] += 9
        elif subjob == "RUN":
            self.playerstats["STR"] += 12
            self.playerstats["DEX"] += 10
            self.playerstats["VIT"] += 9
            self.playerstats["AGI"] += 13
            self.playerstats["INT"] += 10
            self.playerstats["MND"] += 10
            self.playerstats["CHR"] += 7

        # Subjob stats are finished. Now do subjob traits. This organization makes it easier to update subjobs to Lv55 later.

        smite1_jobs = ["DRK","WAR","MNK","DRG"] # +100/1024 attack
        smite2_jobs = ["DRK"] # +152/1024 attack
        smite3_jobs = ["DRK"] # +204/1024 attack (55drk)
        if subjob in smite2_jobs and mainjob not in smite1_jobs:
            smite_bonus = 152./1024
        elif subjob in smite1_jobs and mainjob not in smite1_jobs:
            smite_bonus = 100./1024

        pdl1_jobs = ["DRK","MNK","RNG","DRG","WAR","SAM","BST","PUP","DNC","THF","NIN","RDM"] # +0.1 PDL
        pdl2_jobs = ["DRK"] # +0.2 PDL
        pdl3_jobs = ["DRK"] # +0.3 PDL (55drk)
        if subjob in pdl2_jobs and mainjob not in pdl1_jobs: # TODO: Rewrite the logic here. Right now PUP/DRK (pup with drk subjob) is only getting Smite1, despite /DRK boosting this to Smite2
            self.playerstats["PDL Trait"] += 20
        elif subjob in pdl1_jobs and mainjob not in pdl1_jobs:
            self.playerstats["PDL Trait"] += 10

        attack1_jobs = ["DRK","DRG","WAR"] # +10 attack
        attack3_jobs = ["DRK"] # +35 attack
        if subjob in attack3_jobs and mainjob not in attack1_jobs:
            self.playerstats["Attack1"] += 35
            self.playerstats["Attack2"] += 35
            self.playerstats["Ranged Attack"] += 35
        elif subjob in attack1_jobs and mainjob not in attack1_jobs:
            self.playerstats["Attack1"] += 10
            self.playerstats["Attack2"] += 10
            self.playerstats["Ranged Attack"] += 10

        acc1_jobs = ["RNG","DRG","DNC","RUN"] # +10 accuracy
        acc3_jobs = ["RNG"] # +35 accuracy
        if subjob in acc3_jobs and mainjob not in acc1_jobs:
            self.playerstats["Accuracy1"] += 35
            self.playerstats["Accuracy2"] += 35
            self.playerstats["Ranged Accuracy"] += 35
        elif subjob in acc1_jobs and mainjob not in acc1_jobs:
            self.playerstats["Accuracy1"] += 10
            self.playerstats["Accuracy2"] += 10
            self.playerstats["Ranged Accuracy"] += 10

        matk2_jobs = ["BLM","RDM"] # +24 magic attack
        matk3_jobs = ["BLM"] # +28 magic attack
        if subjob in matk3_jobs and mainjob not in matk2_jobs:
            self.playerstats["Magic Attack"] += 28
        if subjob in matk2_jobs and mainjob not in matk2_jobs:
            self.playerstats["Magic Attack"] += 24

        burst1_jobs = ["BLM"] # +5% magic burst bonus
        if subjob in burst1_jobs and mainjob not in burst1_jobs:
            self.playerstats["Magic Burst Damage Trait"] += 5

        martialarts2_jobs = ["MNK","PUP"] # Martial Arts = 100
        martialarts4_jobs = ["MNK"] # Martial Arts = 140
        if subjob in martialarts4_jobs and mainjob not in martialarts2_jobs:
            self.playerstats["Martial Arts"] = 480-340
        elif subjob in martialarts2_jobs and mainjob not in martialarts2_jobs:
            self.playerstats["Martial Arts"] = 480-380

        kickattacks1_jobs = ["MNK"] # +10% kick attacks (h2h mainhand only). We zero-out Kick Attacks later if no h2h equipped.
        if subjob in kickattacks1_jobs and mainjob not in kickattacks1_jobs:
            self.playerstats["Kick Attacks"] += 10

        fencer1_jobs = ["WAR"] # +1 Fencer
        if subjob in fencer1_jobs and self.gear["sub"]["Type"] != "Weapon" and self.gear["main"]["Skill Type"] not in two_handed and mainjob not in fencer1_jobs: # Fencer trait (+1)
            self.playerstats["Fencer"] += 1 # Fencer I from subjob WAR.
                                            # Fencer from gear is applied after we've updated playerstats with gear stats.
                                            # We'll apply the Fencer bonus stats after we've added up all Fencer+ from gear and traits.

        da2_jobs = ["WAR"] # +12% DA
        if subjob in da2_jobs and mainjob not in da2_jobs:
            self.playerstats["DA"] += 12

        # deadaim1_jobs = ["RNG"] # +10% ranged crit damage
        # if subjob in deadaim1_jobs and mainjob not in deadaim1_jobs:
        #     self.playerstats["Ranged Crit Damage"] += 10

        zanshin3_jobs = ["SAM"] # +35 zanshin
        if subjob in zanshin3_jobs and mainjob not in zanshin3_jobs:
            self.playerstats["Zanshin"] += 35

        # ta1_jobs = ["THF"] # TA+5% (55thf)
        # if subjob in ta1_jobs and mainjob not in ta1_jobs:
        #     self.playerstats["TA"] += 5

        storetp3_jobs = ["SAM"] # +20 store tp
        if subjob in storetp3_jobs and mainjob not in storetp3_jobs:
            self.playerstats["Store TP"] += 20

        wstrait1_jobs = ["DRG"] # +7% WSD (all hits)
        # wstrait2_jobs = ["DRG"] # +10% WSD (all hits) (55drg)
        if subjob in wstrait1_jobs and mainjob not in wstrait1_jobs:
            self.playerstats["Weaponskill Trait"] += 7

        skillchain1_jobs = ["DNC"] # +8% Skill chain damage
        if subjob in skillchain1_jobs and mainjob not in skillchain1_jobs:
            self.playerstats["Skillchain Bonus"] += 8

        evasion2_jobs = ["THF","DNC","PUP"] # +22 evasion
        evasion3_jobs = ["THF"] # +35 evasion
        if subjob in evasion3_jobs and mainjob not in evasion2_jobs:
            self.playerstats["Evasion"] += 35
        elif subjob in evasion2_jobs and mainjob not in evasion2_jobs:
            self.playerstats["Evasion"] += 22

        mdef2_jobs = ["RUN","WHM","RDM"] # +12 Magic Def
        mdef3_jobs = ["RUN","WHM"] # +14 Magic Def
        if subjob in mdef3_jobs and mainjob not in mdef2_jobs:
            self.playerstats["Magic Def"] += 14
        elif subjob in mdef2_jobs and mainjob not in mdef2_jobs:
            self.playerstats["Magic Def"] += 12

        subtleblow2_jobs = ["MNK","NIN","DNC"] # +10 Subtle Blow
        subtleblow3_jobs = ["MNK","NIN"] # +15 Subtle Blow
        if subjob in subtleblow3_jobs and mainjob not in subtleblow2_jobs:
            self.playerstats["Subtle Blow"] += 15
        elif subjob in subtleblow2_jobs and mainjob not in subtleblow2_jobs:
            self.playerstats["Subtle Blow"] += 10

        dualwield_jobs3 = ["NIN"] # +10 Subtle Blow
        dualwield_jobs2 = ["DNC","NIN"] # +15 Subtle Blow
        if subjob in dualwield_jobs3 and mainjob not in dualwield_jobs2:
            self.playerstats["Dual Wield"] += 25
        elif subjob in dualwield_jobs2 and mainjob not in dualwield_jobs2:
            self.playerstats["Dual Wield"] += 15



        # Do set bonuses!
        # Count the number of set-bonus gear equipped.
        self.set_bonuses = {'Crit Rate':0, 'STR':0, 'DEX':0, 'AGI':0, 'VIT':0, "MND":0, 'CHR':0, "Accuracy":0, "Ranged Accuracy":0, "Magic Accuracy":0, "Magic Attack":0, "Weaponskill Damage":0, "Attack":0}
        adhemar_count = 0    # Adhemar +1 gives Crit Rate
        mummu_count = 0      # Mummu +2 with the Mummu Ring gives DEX/AGI/VIT/CHR
        regal_ring_count = 0 # Regal Ring with AF+3 gear gives Accuracy/Ranged Accuracy/Magic Accuracy.
        flamma_count = 0     # Flamma +2 with the Flamma Ring gives STR/DEX/VIT
        ayanmo_count = 0     # Flamma +2 with the Flamma Ring gives STR/VIT/MND
        amalric_count = 0    # +10 Magic Attack for every piece of Amalric equipped after the first
        lustratio_count = 0    # +2 WSD for every piece of Amalric equipped after the first
        ryuo_count = 0    # +10 attack for every piece of Ryuo equipped after the first
        af_armor = {"war":"pummeler","mnk":"anchorite","whm":"theophany","blm":"spaekona","rdm":"atrophy","thf":"pillager","pld":"reverence","drk":"ignominy","bst":"totomic","brd":"brioso","rng":"orion","sam":"wakido","nin":"hachiya","drg":"vishap","smn":"convoker","blu":"assimilator","cor":"laksamana","pup":"foire","dnc":"maxixi","sch":"academic","geo":"geomancy","run":"runeist"}
        for slot in gear:
            if "adhemar" in gear[slot]['Name'].lower() and "+1" in gear[slot]['Name'].lower():
                adhemar_count += 1
            if "Amalric" in gear[slot]["Name"]:
                amalric_count += 1
            if "Lustratio" in gear[slot]["Name"]:
                lustratio_count += 1
            if "Ryuo" in gear[slot]["Name"]:
                ryuo_count += 1

            if "regal ring" == gear['ring1']['Name'].lower() or "regal ring" == gear['ring2']['Name'].lower():
                if af_armor[mainjob.lower()] in gear[slot]['Name'].lower():
                    if regal_ring_count == 4:
                        continue
                    regal_ring_count += 1

            if "flamma ring" == gear['ring1']['Name'].lower() or "flamma ring" == gear['ring2']['Name'].lower():
                if "flamma" in gear[slot]['Name'].lower() and "+2" in gear[slot]['Name']:
                    flamma_count += 1
            if "ayanmo ring" == gear['ring1']['Name'].lower() or "ayanmo ring" == gear['ring2']['Name'].lower():
                if "ayanmo" in gear[slot]['Name'].lower() and "+2" in gear[slot]['Name']:
                    ayanmo_count += 1
            if gear["ring1"]['Name'] == "Mummu Ring" or gear["ring2"]['Name'] == "Mummu Ring":
                if "mummu" in gear[slot]['Name'].lower() and "+2" in gear[slot]['Name']:
                    mummu_count += 1

        self.set_bonuses['Crit Rate'] += adhemar_count*2 if adhemar_count > 1 else 0
        self.set_bonuses['DEX'] += (mummu_count)*8 if mummu_count >= 2 else 0
        self.set_bonuses['AGI'] += (mummu_count)*8 if mummu_count >= 2 else 0
        self.set_bonuses['VIT'] += (mummu_count)*8 if mummu_count >= 2 else 0
        self.set_bonuses['CHR'] += (mummu_count)*8 if mummu_count >= 2 else 0
        self.set_bonuses['Accuracy'] += (regal_ring_count)*15
        self.set_bonuses['Ranged Accuracy'] += (regal_ring_count)*15
        self.set_bonuses['Magic Accuracy']  += (regal_ring_count)*15
        self.set_bonuses['DEX'] += (flamma_count)*8 if flamma_count >= 2 else 0
        self.set_bonuses['VIT'] += (flamma_count)*8 if flamma_count >= 2 else 0
        self.set_bonuses['STR'] += (flamma_count)*8 if flamma_count >= 2 else 0
        self.set_bonuses['Magic Attack'] += (amalric_count)*10 if amalric_count >= 2 else 0
        self.set_bonuses['STR'] += (ayanmo_count)*8 if ayanmo_count >= 2 else 0
        self.set_bonuses['VIT'] += (ayanmo_count)*8 if ayanmo_count >= 2 else 0
        self.set_bonuses['MND'] += (ayanmo_count)*8 if ayanmo_count >= 2 else 0 # TODO: confirm and remove the ring requirement for ambu gear.
        self.set_bonuses['Weaponskill Damage'] += (lustratio_count)*2 if lustratio_count >= 2 else 0 # TODO: confirm and remove the ring requirement for ambu gear.
        self.set_bonuses['Attack'] += (ryuo_count)*10 if ryuo_count >= 2 else 0

        # Details:
        # Your gear stats start out as all zero. Your player stats start out as whatever base values you have from traits/gifts/etc
        # This next code block applies set bonuses to your gearstats and playerstats together, but skips accuracy since that gets treated specifically later.
        # This should also skip attack, but there are no set bonuses that give attack added to the code yet.

        # TODO: We should just ignore playerstats until just before adding buffs. Only add to gear stats together, then loop over gearstats, adding to playerstats right before we add buffs.
        # We kind of already do this, just it looks bad.

        # Add set bonuses to gearstats
        for stat in self.set_bonuses:
            self.gearstats[stat] += self.set_bonuses[stat] # Stats from gear get set bonuses from gear
            if stat in ["Attack","Accuracy"]: # Skip the Accuracy stat for the "playerstats." Accuracy is added to "gearstats" on the line above, then converted to Accuracy1 and Accuracy2 in "playerstats" later.
                continue
            else:
                self.playerstats[stat] += self.set_bonuses[stat]


        # Now loop over all of the gear equipped and add the stats to the gearstats dictionary. Set bonuses were already added to both gearstats and playerstats above.

        # Build the gearstat dictionary from the provided gear set.
        for stat in self.gearstats: # stat = stat name as seen in the gearstats dictionary: "STR", "TA", "Crit Rate", etc
            for k in self.gear.values(): # k = Dictionary containing the stats for a single piece of gear for all slots one slot at a time: {'Name': 'Gere Ring', 'STR': 10, 'Attack': 16, 'TA': 5}. key=slot, value=item
                if stat in k.keys(): # If the stat in gearstats exists on the piece of gear being checked.
                    self.gearstats[stat] += k[stat] # Add the stat from the gear to the gearstats dictionary.




        main_wpn_skill = self.gear['main'].get('Skill Type', 'None') + ' Skill' # Record the type of weapon being used in the main hand. "Katana Skill" for example # TODO we redefine this later for some reason
        sub_wpn_skill = self.gear['sub'].get('Skill Type', 'None') + ' Skill' # Same for off-hand
        rng_wpn_skill = self.gear['ranged'].get('Skill Type', 'None') + ' Skill' # Same for ranged slot

        # Increase playerstats dictionary values by the amount listed on gear.
        for slot in self.gear: # slot = 'head', 'neck', 'ear1', etc
            for stat in gear[slot]: # stat = The stats on a piece of gear: "STR", "Double Attack", etc
                if stat not in self.gearstats or stat not in self.playerstats: # Skill stats on gear that I haven't yet added to the playerstats dictionary. Things like "Accuracy" and "Attack" in gearstats are called "Accuracy1" "Accuracy2" "Attack1" and "Attack2" in the playerstats and won't be found on gear. Skip them here
                    continue # Keep in mind, "Jobs" and "Type" etc are all stats that need to be skipped here
                if (slot == "main" and stat == main_wpn_skill) or (slot == "sub" and stat == sub_wpn_skill): # Skip adding skill+ stats from main+sub weapons for now. These get converted into attack and accuracy later. This skips skill from grips too, but only a few relatively useless grips have skill+ on them, so we'll ignore this issue for now.
                    # If we add "Katana Skill" from main and sub now, then they'll get confused later when we need ONLY main katana skill to calculate main katana accuracy/attack.
                    continue
                self.playerstats[stat] += self.gear[slot][stat] # This line already adds gear stat skills "Scythe Skill" from Empyrean +3 head for example is added here
                # self.gearstats[stat] += self.gear[slot][stat] # This line is adding stats to gearstats. but i dont think i even use gearstats anymore i could probably delete it entirely TODO

        # print(self.playerstats)
        # At this point, the playerstats dictionary should have all the player's gear stats added to the player's base stats, except attack1, attack2, accuracy1, and accuracy2

        # Stats from gear have now been applied to playerstats.
        # Check for trait enhancements from gear now (Fencer+1 for example)
        if self.gear["sub"]["Type"] != "Weapon" and self.gear["main"]["Skill Type"] not in two_handed: # Apply Fencer bonuses based on Fencer+ gear.
            fencer_bonus = get_fencer_bonus(self.playerstats["Fencer"])
            self.playerstats["TP Bonus"] += fencer_bonus[0] + self.playerstats["Fencer TP Bonus"]
            self.playerstats["Crit Rate"] += fencer_bonus[1]

        # Zero Kick Attacks if not using a Hand-to-Hand weapon. TODO: remove this and treat it the same as daken in the main code
        if self.gear["main"]["Skill Type"] != "Hand-to-Hand":
            self.playerstats["Kick Attacks"] = 0
        # Zero Daken if not using Shuriken.
        if self.gear["ammo"]["Type"] != "Shuriken":
            self.playerstats["Daken"] = 0

        # Limit Subtle BlowI and II to 50 each.
        # self.playerstats["Subtle Blow"] = 50 if self.playerstats["Subtle Blow"] > 50 else self.playerstats["Subtle Blow"]
        # self.playerstats["Subtle Blow II"] = 50 if self.playerstats["Subtle Blow II"] > 50 else self.playerstats["Subtle Blow II"]


        # Calculate ron. Traits are already included in playerstats, so we just need to add evasion from skill and half of AGI
        def get_skill_evasion(evasion_skill):
            #
            # Evasion skill over 300 is only worth 0.8 evasion based on my incredibly incomplete testing.
            #
            if evasion_skill >= 300:
                evasion = 300 + 0.8*(evasion_skill - 300)
            else:
                evasion = evasion_skill

            return(evasion)

        self.playerstats["Evasion"] += int(self.playerstats["AGI"]/2) + get_skill_evasion(self.playerstats["Evasion Skill"])

        # Stats from food are used to calculate Attack and Accuracy before any % bonuses such as Chaos Roll or GEO's Fury bubble
        # Add food stat bonuses here
        if buffs["food"]:
            self.playerstats['STR'] += buffs["food"].get('STR',0)
            self.playerstats['DEX'] += buffs["food"].get('DEX',0)
            self.playerstats['VIT'] += buffs["food"].get('VIT',0)
            self.playerstats['AGI'] += buffs["food"].get('AGI',0)
            self.playerstats['INT'] += buffs["food"].get('INT',0)
            self.playerstats['MND'] += buffs["food"].get('MND',0)
            self.playerstats['CHR'] += buffs["food"].get('CHR',0)

        # Add WHM "Boost-STAT" bonus, BRD etudes, and GEO stats
        if buffs["whm"]:
                self.playerstats['STR'] += buffs["whm"].get("STR", 0)
                self.playerstats['DEX'] += buffs["whm"].get("DEX", 0)
                self.playerstats['VIT'] += buffs["whm"].get("VIT", 0)
                self.playerstats['AGI'] += buffs["whm"].get("AGI", 0)
                self.playerstats['INT'] += buffs["whm"].get("INT", 0)
                self.playerstats['MND'] += buffs["whm"].get("MND", 0)
                self.playerstats['CHR'] += buffs["whm"].get("CHR", 0)
                self.playerstats['Magic Haste'] += buffs["whm"].get("Haste",0)
        if buffs["brd"]:
                self.playerstats['STR'] += buffs["brd"].get("STR", 0)
                self.playerstats['DEX'] += buffs["brd"].get("DEX", 0)
                self.playerstats['VIT'] += buffs["brd"].get("VIT", 0)
                self.playerstats['AGI'] += buffs["brd"].get("AGI", 0)
                self.playerstats['INT'] += buffs["brd"].get("INT", 0)
                self.playerstats['MND'] += buffs["brd"].get("MND", 0)
                self.playerstats['CHR'] += buffs["brd"].get("CHR", 0)
        if buffs["geo"]:
                self.playerstats['STR'] += buffs["geo"].get("STR", 0)
                self.playerstats['DEX'] += buffs["geo"].get("DEX", 0)
                self.playerstats['VIT'] += buffs["geo"].get("VIT", 0)
                self.playerstats['AGI'] += buffs["geo"].get("AGI", 0)
                self.playerstats['INT'] += buffs["geo"].get("INT", 0)
                self.playerstats['MND'] += buffs["geo"].get("MND", 0)
                self.playerstats['CHR'] += buffs["geo"].get("CHR", 0)


        # Add skill levels from armor. See Hachiya Tekko +3: "Throwing Skill +14"
        main_weapon_skill_type = self.gear['main'].get('Skill Type','None') + ' Skill'
        sub_weapon_skill_type = self.gear['sub'].get('Skill Type','None')  + ' Skill' if dual_wield else False
        ranged_weapon_skill_type = self.gear['ranged'].get('Skill Type','None')  + ' Skill' # TODO: this is already defined as rng_wpn_skill
        ammo_weapon_skill_type = self.gear['ammo'].get('Skill Type','None') + ' Skill'

        # Increase player Attack and Ranged Attack based on gear and base character stats.
        # Main hand =  Attack1 = 8+GearSkill+STR+Attack+MainWeaponSkill
        # Sub hand = Attack2 = 8+GearSkill+0.5*STR+Attack+SubWeaponSkill
        # Ranged attack = 8 + skill + STR + RangedAttack. Ranged/Ammo slot skill was already counted just above. no need to add it separately here.
        self.playerstats['Attack1'] += 8 + self.playerstats.get(self.gear['main'].get('Skill Type','None') + ' Skill', 0) + self.playerstats['STR'] + self.gearstats['Attack'] + self.gear['main'].get(self.gear['main'].get('Skill Type','None') + ' Skill', 0)
        self.playerstats['Attack2'] += 8 + self.playerstats.get(self.gear['sub'].get('Skill Type','None')  + ' Skill', 0) + int(0.5*(self.playerstats['STR'])) + self.gearstats['Attack'] + self.gear['sub'].get(self.gear['sub'].get('Skill Type','None')  + ' Skill', 0) if dual_wield else 0
        if self.gear["ranged"].get("Skill Type", "None") in ["Marksmanship","Archery"]:
            self.playerstats['Ranged Attack'] += 8 + self.playerstats.get(self.gear['ranged'].get('Skill Type','None') + ' Skill',0) + self.playerstats['STR'] # Ranged attack DOES exist in gearstats, so no need to add it on here.
        elif self.gear["ammo"].get("Skill Type", "None") == "Throwing": # For Shuriken
            self.playerstats['Ranged Attack'] += 8 + self.playerstats.get(self.gear['ammo'].get('Skill Type','None') + ' Skill',0) + self.playerstats['STR'] # Ranged attack DOES exist in gearstats, so no need to add it on here.


        # Now add in the additive buffs from BRD songs
        if buffs['brd']:
            self.playerstats['Attack1'] += buffs['brd'].get('Attack',0)
            self.playerstats['Attack2'] += buffs['brd'].get('Attack',0) if dual_wield else 0
            self.playerstats['Ranged Attack'] += buffs['brd'].get('Attack',0)

            if buffs["brd"].get("Attack",0) > 0 and mainjob=="BRD":
                # +20 attack when under the effects of minuet (job point category)
                self.playerstats["Attack1"] += 20
                self.playerstats["Attack2"] += 20
                self.playerstats["Ranged Attack"] += 20

        # Now multiply each attack by the sum of the %-based attack boosts like COR GEO and Kikoku's Attack+10%
        # First collect the individual attack% boosts and add them together.
        percent_attack_buff = 0.0 # Kikoku/Guttler AM
        percent_rangedattack_buff = 0.0 # Annihilator AM
        velocity_shot_ranged_bonus = 0.0 # Velocity shot exclusive
        velocity_shot_melee_bonus = 0.0 # Velocity shot exclusive
        if mainjob == "RNG":
            if job_abilities.get("Velocity Shot",False):
                velocity_shot_ranged_bonus += 152./1024
                velocity_shot_melee_bonus -= 152./1024
                if gear["body"]["Name2"] == "Amini Caban +3":
                    velocity_shot_ranged_bonus += 112./1024
                if gear["back"]["Name"] == "Belenus's Cape":
                    velocity_shot_ranged_bonus += 20./1024
        naegling_attack_bonus = 0.0
        if buffs['cor']:
            percent_attack_buff += buffs['cor'].get('Attack',0) # Chaos roll
        if buffs['geo']:
            percent_attack_buff += buffs['geo'].get('Attack',0) # Fury
        if gear['main']['Name'] in ["Kikoku","Guttler"]:
            percent_attack_buff += 100./1024.  # +10% Attack boost from Kikoku/Guttler Aftermath is applied as a sum with GEO and COR % boosts
        if gear['main']['Name'] in ["Annihilator"]:
            percent_rangedattack_buff += 100./1024.  # +10% Ranged Attack boost from Annihilator Aftermath is applied as a sum with GEO and COR % boosts
        if gear['main']['Name'] == "Gungnir":
            percent_attack_buff += 50./1024.  # +5% Attack boost from Gungnir Aftermath
        if gear['main']['Name'] == 'Naegling':
            nbuffs = 8 # Assume 8 buffs: pro, shell, haste, utsu, kakka, yonin, food, signet
            nbuffs += 4 if buffs['brd'] else 0 # If BRD in party, assume +4 buffs from songs
            nbuffs += 2 if buffs['cor'] else 0 # If COR in party, assume +2 buffs from rolls
            nbuffs += 1 if buffs['geo'] else 0 # If GEO in party, assume +1 buff from bubble
            naegling_attack_bonus += 10.*nbuffs/1024.

        smite_bonus = 0 if self.gear['main'].get('Skill Type','None') not in ["Scythe", "Great Sword", "Hand-to-Hand", "Polearm", "Great Axe", "Great Katana", "Staff"] else smite_bonus

        # Berserk/Warcry would also go here, but there is no real benefit to including them in a simulation (in my opinion).
        percent_attack_buff += ws_atk_bonus

        self.playerstats['Attack1'] *= (1+percent_attack_buff + smite_bonus + 0.2*wyvern_bonus + naegling_attack_bonus + velocity_shot_melee_bonus + last_resort_bonus)
        self.playerstats['Attack2'] *= (1+percent_attack_buff + velocity_shot_melee_bonus + last_resort_bonus) if dual_wield else 1.0 # Smite only applies to main hand, and only when using 2-handed weapons anyway...
        self.playerstats['Ranged Attack'] *= (1 + percent_attack_buff + percent_rangedattack_buff + velocity_shot_ranged_bonus) # Smite does not apply to ranged attacks.

        # Convert the attack values to integers.
        self.playerstats['Attack1'] = int(self.playerstats['Attack1'])
        self.playerstats['Attack2'] = int(self.playerstats['Attack2']) if dual_wield else 0
        self.playerstats['Ranged Attack'] = int(self.playerstats['Ranged Attack'])



        # Now work on accuracy1, accuracy2, and ranged accuracy stats
        def get_skill_accuracy(wpn, slot):
            #
            # Calculate accuracy from weapon-type skill.
            # The contribution from skill changes with different skill levels. We need to add the contributions separately
            #
            skill = self.playerstats.get(wpn.get('Skill Type','None') + ' Skill',0) + wpn.get(wpn.get('Skill Type','None') + ' Skill',0)*(slot != "ammo")*(slot != "ranged") # We've already added skill from ranged+ammo slots. Do not add them again.
            skill += 13
            skill_accuracy = 0
            if skill > 200:
                skill_accuracy += int((min(skill,400)-200)*0.9) + 200
            else:
                skill_accuracy += skill
            if skill > 400:
                skill_accuracy += int((min(skill,600)-400)*0.8)
            if skill > 600:
                skill_accuracy += int((skill-600)*0.9)

            return(skill_accuracy)

        # Increase player Accuracy and Ranged Accuracy based on gear and base character stats.
        self.playerstats['Accuracy1'] += int(0.75*(self.playerstats['DEX'])) + self.gearstats['Accuracy'] + get_skill_accuracy(self.gear['main'], 'main')
        self.playerstats['Accuracy2'] += int(0.75*(self.playerstats['DEX'])) + self.gearstats['Accuracy'] + get_skill_accuracy(self.gear['sub'], 'sub') if dual_wield else 0
        if self.gear["ranged"].get("Skill Type", "None") in ["Marksmanship","Archery"]:
            self.playerstats['Ranged Accuracy'] += int(0.75*(self.playerstats['AGI'])) + get_skill_accuracy(self.gear["ranged"], "ranged")
        elif self.gear["ammo"].get("Skill Type", "None") == "Throwing": # For Shuriken
            self.playerstats['Ranged Accuracy'] += int(0.75*(self.playerstats['AGI'])) + get_skill_accuracy(self.gear['ammo'], 'ammo')


        # Add in the additive accuracy buffs, which includes things like BRD madrigals, COR Hunter's Roll, GEO Precision, and Mjollnir Aftermath

        if buffs["brd"]:
            self.playerstats['Accuracy1'] += buffs['brd'].get('Accuracy',0)
            self.playerstats['Accuracy2'] += buffs['brd'].get('Accuracy',0) if dual_wield else 0
            self.playerstats['Ranged Accuracy'] += buffs['brd'].get('Ranged Accuracy',0)
        if buffs["geo"]:
            self.playerstats['Accuracy1'] += buffs["geo"].get('Accuracy',0)
            self.playerstats['Accuracy2'] += buffs["geo"].get('Accuracy',0) if dual_wield else 0
            self.playerstats['Ranged Accuracy'] += buffs["geo"].get('Ranged Accuracy',0)
        if buffs["cor"]:
            self.playerstats['Accuracy1'] += buffs["cor"].get('Accuracy',0)
            self.playerstats['Accuracy2'] += buffs["cor"].get('Accuracy',0) if dual_wield else 0
            self.playerstats['Ranged Accuracy'] += buffs["cor"].get('Ranged Accuracy',0)


        # Now add extra stat buffs like Store TP and Magic stuff.
        # Magic Accuracy should get it's own section later to include magic accuracy from INT, but this is currently handled in the nuking.py file for now. TODO
        if buffs["geo"]:
            self.playerstats['Magic Accuracy'] += buffs["geo"].get('Magic Accuracy',0)
            self.playerstats['Magic Attack'] += buffs["geo"].get('Magic Attack',0)
            self.playerstats['Magic Haste'] += buffs['geo'].get('Haste',0)
        if buffs["cor"]:
            self.playerstats['Store TP'] += buffs["cor"].get('Store TP', 0)
            self.playerstats['Magic Accuracy'] += buffs["cor"].get('Magic Accuracy', 0)
            self.playerstats['Magic Attack'] += buffs["cor"].get('Magic Attack', 0)
            self.playerstats['DA'] += buffs["cor"].get('DA', 0)
            self.playerstats['Crit Rate'] += buffs["cor"].get('Crit Rate', 0)
        if buffs["brd"]:
            self.playerstats['Magic Haste'] += buffs['brd'].get('Haste',0)


        # Finally, after normal spell buffs, food buffs to accuracy and attack take effect
        if buffs["food"]:
            self.playerstats['Attack1'] += buffs['food'].get('Attack',0)
            self.playerstats['Attack2'] += buffs['food'].get('Attack',0) if dual_wield else 0
            self.playerstats['Ranged Attack'] += buffs['food'].get('Attack',0)
            self.playerstats['Ranged Accuracy'] += buffs['food'].get('Accuracy',0)
            self.playerstats['Accuracy1'] += buffs['food'].get('Accuracy',0)
            self.playerstats['Accuracy2'] += buffs['food'].get('Accuracy',0) if dual_wield else 0
            self.playerstats['Magic Accuracy'] += buffs['food'].get('Magic Accuracy',0)
            self.playerstats['Magic Attack'] += buffs['food'].get('Magic Attack',0)
            self.playerstats['Store TP'] += buffs['food'].get('Store TP',0)

        if gear["ranged"].get("Skill Type","None") not in ["Marksmanship","Archery"] and gear["ammo"].get("Skill Type","None") != "Throwing":
            self.playerstats["Ranged Attack"] = 0
            self.playerstats["Ranged Accuracy"] = 0

        # Adjust main/sub/ammo weapon delays and damage
        self.playerstats['Delay1'] += self.gear['main']['Delay']
        self.playerstats['Delay2'] += self.gear['sub']['Delay'] if dual_wield else 0
        self.playerstats['Delay'] = self.gear['main']['Delay'] + self.gear['sub'].get('Delay',0)
        self.playerstats['Ammo Delay'] += self.gear['ammo'].get('Delay',0)

        self.playerstats['DMG1'] = self.gear['main']['DMG']
        self.playerstats['DMG2'] = self.gear['sub']['DMG'] if dual_wield else 0
        self.playerstats["Ranged DMG"] = self.gear["ranged"].get("DMG",0)
        self.playerstats["Ranged Delay"] = self.gear["ranged"].get("Delay",0)
        self.playerstats['Ammo DMG'] = self.gear['ammo'].get('DMG',0)

    def equipment(self):
        # Define a function that simply stores the names of each piece of gear equipped in each slot.
        for k in self.gear:
            self.equipped = {
            'main': self.gear['main']['Name'],
            'sub':  self.gear['sub']['Name'],
            'ranged':  self.gear['ranged']['Name'],
            'ammo':  self.gear['ammo']['Name'],
            'head':  self.gear['head']['Name'],
            'neck':  self.gear['neck']['Name'],
            'ear1':  self.gear['ear1']['Name'],
            'ear2':  self.gear['ear2']['Name'],
            'body':  self.gear['body']['Name'],
            'hands':  self.gear['hands']['Name'],
            'ring1':  self.gear['ring1']['Name'],
            'ring2':  self.gear['ring2']['Name'],
            'back':  self.gear['back']['Name'],
            'waist':  self.gear['waist']['Name'],
            'legs':  self.gear['legs']['Name'],
            'feet':  self.gear['feet']['Name'],
            }
        return(self.equipped)
