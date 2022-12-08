#
# Created by Kastra on Asura.
# Feel free to /tell in game or send a PM on FFXIAH you have questions, comments, or suggestions.
#
# Version date: 2022 December 04
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

    def __init__(self, buffs, gear, main_job, sub_job, ws_atk_bonus=0.0):

        self.gear = gear

        mainjob = main_job.upper()
        subjob = sub_job.upper()

        sub_type = gear['sub'].get('Type', 'None') # Check if the item equipped in the sub slot is a weapon, a grip, or nothing. If the item doesn't have a "Type" Key then return "None", meaning nothing is equipped.
        dual_wield = sub_type == 'Weapon'
        ranged_type = gear["ranged"].get("Skill Type", "None") # Not sure if we'll need this, but adding it now just in case.

        # Initialize empty gearset for modification.
        # This will contain all stats that come from gear only. Player stats are defined later.
        self.gearstats = {
                 'STR':0, 'DEX':0, 'VIT':0, 'AGI':0, 'INT':0, 'MND':0, 'CHR':0,
                 'Katana Skill':0, 'Dagger Skill':0, 'Sword Skill':0, 'Hand-to-Hand Skill':0, 'Great Katana Skill':0, 'Club Skill':0, 'Throwing Skill':0,
                 'Axe Skill':0,'Great Axe Skill':0,'Polearm Skill':0,'Scythe Skill':0,'Staff Skill':0,'Great Sword Skill':0,'Archery Skill':0,'Marksmanship Skill':0,
                 'Ninjutsu Skill':0, 'Great Sword Skill':0, 'Marksmanship Skill':0, "Elemental Magic Skill":0,
                 'Accuracy':0, 'Attack':0,
                 'Ranged Accuracy':0, 'Ranged Attack':0,
                 'Magic Accuracy':0, 'Magic Attack':0, 'Magic Damage':0, 'Magic Accuracy Skill':0, 'Ninjutsu Magic Attack':0, 'Ninjutsu Damage':0, 'Magic Crit Rate':0, 'Magic Burst Damage':0, 'Magic Burst Damage II':0, "Magic Burst Accuracy":0,
                 'Daken':0, 'QA':0, 'TA':0, 'DA':0, 'OA8':0, 'OA7':0, 'OA6':0, 'OA5':0, 'OA4':0, 'OA3':0, 'OA2':0,
                 'Crit Rate':0, 'Crit Damage':0,'DA DMG':0, 'TA DMG':0,
                 'Store TP':0,
                 'PDL':0,
                 'Dual Wield':0, 'Magic Haste':0, 'Gear Haste':0, 'JA Haste':0,
                 'Zanshin':0,"Fencer":0,
                 'Weaponskill Damage':0, 'Weaponskill Bonus':0, 'Skillchain Bonus':0, 'ftp':0, 'TP Bonus':0, 'Weaponskill Accuracy':0,
                 'Delay1':0, 'Delay2':0, 'Delay':0, 'Ammo Delay':0, "Ranged Delay":0,
                 'DMG1':0, 'DMG2':0, 'Ammo DMG':0, "Ranged DMG":0,
                 'Light Elemental Bonus':0, 'Dark Elemental Bonus':0, 'Fire Elemental Bonus':0, 'Earth Elemental Bonus':0, 'Water Elemental Bonus':0, 'Wind Elemental Bonus':0, 'Ice Elemental Bonus':0, 'Thunder Elemental Bonus':0,'Elemental Bonus':0,
                 'Light Affinity':0, 'Dark Affinity':0, 'Fire Affinity':0,'Earth Affinity':0, 'Water Affinity':0, 'Wind Affinity':0,'Ice Affinity':0, 'Thunder Affinity':0,
                 }


        # Initialize base player stats with no gear and no subjob.
        # Subjob stats and gear stats will be added later in another part of the code.
        # Base 5% crit rate (0+5), +5 for 5/5 crit merits for 0+5+5

        if mainjob == "NIN":  # Master Level 20 Ninja stats
            # Ninja gets +5% WSD from job gifts
            self.playerstats = {'STR':113, 'DEX':115, 'VIT':113, 'AGI':115, 'INT':110, 'MND':101, 'CHR':104,
                     'Katana Skill':444+16, 'Dagger Skill':398+16, 'Sword Skill':393+16, 'Hand-to-Hand Skill':320+16, 'Great Katana Skill':388+16, 'Club Skill':320+16, 'Throwing Skill':444+16,
                     'Axe Skill':0+16,'Great Axe Skill':0+16,'Polearm Skill':0+16,'Scythe Skill':0+16,'Staff Skill':0+16,'Great Sword Skill':0+16,'Archery Skill':320+16,'Marksmanship Skill':393+16,
                     'Ninjutsu Skill':473+16, "Elemental Magic Skill":0+16,
                     'Accuracy1':56, 'Accuracy2':56, 'Attack1':70, 'Attack2':70,
                     'Ranged Accuracy':56, 'Ranged Attack':70,
                     'Magic Accuracy':50, 'Magic Attack':28, 'Magic Damage':40, 'Magic Accuracy Skill':0, 'Ninjutsu Magic Attack':0, 'Ninjutsu Damage':0, 'Magic Crit Rate':0, 'Magic Burst Damage':0, 'Magic Burst Damage II':7, "Magic Burst Accuracy":0,
                     'Daken':54, 'QA':0, 'TA':0, 'DA':0, 'OA8':0, 'OA7':0, 'OA6':0, 'OA5':0, 'OA4':0, 'OA3':0, 'OA2':0,
                     'Crit Rate':0+5+5, 'Crit Damage':0, 'DA DMG':0, 'TA DMG':0,
                     'Store TP':0,
                     'PDL':0, 'PDL Trait':10,
                     'Dual Wield':35, 'Magic Haste':0, 'Gear Haste':0, 'JA Haste':0,
                     'Zanshin':0, "Fencer":0,
                     'Weaponskill Damage':5, 'Weaponskill Bonus':0, 'Skillchain Bonus':12, 'ftp':0, 'TP Bonus':0, 'Weaponskill Accuracy':0,
                     'Delay1':0, 'Delay2':0, 'Delay':0, 'Ammo Delay':0, "Ranged Delay":0,
                     'DMG1':0, 'DMG2':0, 'Ammo DMG':0, "Ranged DMG":0,
                     'Light Elemental Bonus':0, 'Dark Elemental Bonus':0, 'Fire Elemental Bonus':0,'Earth Elemental Bonus':0, 'Water Elemental Bonus':0, 'Wind Elemental Bonus':0,'Ice Elemental Bonus':0, 'Thunder Elemental Bonus':0,'Elemental Bonus':0, 'Weaponskill Accuracy':0,
                     'Light Affinity':0, 'Dark Affinity':0, 'Fire Affinity':0,'Earth Affinity':0, 'Water Affinity':0, 'Wind Affinity':0,'Ice Affinity':0, 'Thunder Affinity':0,
                     }
        elif mainjob == "DRK":  # Master Level 20 Dark Knight stats
            self.playerstats = {'STR':117, 'DEX':113, 'VIT':113, 'AGI':110, 'INT':113, 'MND':101, 'CHR':101,
                     'Scythe Skill':444+16, 'Dagger Skill':393+16, 'Sword Skill':408+16, 'Hand-to-Hand Skill':0+16, 'Great Katana Skill':0+16, 'Club Skill':388+16, 'Throwing Skill':0+16,
                     'Katana Skill':0+16, 'Axe Skill':408+16,'Great Axe Skill':408+16,'Polearm Skill':0+16,'Staff Skill':0+16,'Great Sword Skill':437+16,'Archery Skill':0+16,'Marksmanship Skill':320+16,
                     'Ninjutsu Skill':0, 'Dark Magic Skill':473+16, "Elemental Magic Skill":424+16,
                     'Accuracy1':22, 'Accuracy2':22, 'Attack1':202, 'Attack2':202,
                     'Ranged Accuracy':22, 'Ranged Attack':202,
                     'Magic Accuracy':30, 'Magic Attack':0, 'Magic Damage':0, 'Magic Accuracy Skill':0, 'Ninjutsu Magic Attack':0, 'Magic Crit Rate':0, 'Magic Burst Damage':0,'Magic Burst Damage II':0, "Magic Burst Accuracy":0,
                     'Daken':0, 'QA':0, 'TA':0, 'DA':0, 'OA8':0, 'OA7':0, 'OA6':0, 'OA5':0, 'OA4':0, 'OA3':0, 'OA2':0,
                     'Crit Rate':0+5, 'Crit Damage':8, 'DA DMG':0, 'TA DMG':0,
                     'Store TP':0,
                     'PDL':0, 'PDL Trait':50,
                     'Dual Wield':0, 'Magic Haste':0, 'Gear Haste':0, 'JA Haste':0,
                     'Zanshin':0, "Fencer":0,
                     'Weaponskill Damage':8, 'Weaponskill Bonus':0, 'Skillchain Bonus':12, 'ftp':0, 'TP Bonus':0, 'Weaponskill Accuracy':0,
                     'Delay1':0, 'Delay2':0, 'Delay':0, 'Ammo Delay':0, "Ranged Delay":0,
                     'DMG1':0, 'DMG2':0, 'Ammo DMG':0, "Ranged DMG":0,
                     'Light Elemental Bonus':0, 'Dark Elemental Bonus':0, 'Fire Elemental Bonus':0,'Earth Elemental Bonus':0, 'Water Elemental Bonus':0, 'Wind Elemental Bonus':0,'Ice Elemental Bonus':0, 'Thunder Elemental Bonus':0,'Elemental Bonus':0, 'Weaponskill Accuracy':0,
                     'Light Affinity':0, 'Dark Affinity':0, 'Fire Affinity':0,'Earth Affinity':0, 'Water Affinity':0, 'Wind Affinity':0,'Ice Affinity':0, 'Thunder Affinity':0,
                     }
        elif mainjob == "SAM":  # Master Level 20 Dark Knight stats. Update to SAM later
            self.playerstats = {'STR':117, 'DEX':113, 'VIT':113, 'AGI':110, 'INT':113, 'MND':101, 'CHR':101,
                     'Scythe Skill':0+16, 'Dagger Skill':320+16, 'Sword Skill':398+16, 'Hand-to-Hand Skill':0+16, 'Great Katana Skill':444+16, 'Club Skill':320+16, 'Throwing Skill':398+16,
                     'Katana Skill':0+16, 'Axe Skill':0+16,'Great Axe Skill':0+16,'Polearm Skill':408+16,'Staff Skill':0+16,'Great Sword Skill':0+16,'Archery Skill':398+16,'Marksmanship Skill':0+16,
                     'Ninjutsu Skill':0, "Elemental Magic Skill":0,
                     'Accuracy1':36, 'Accuracy2':36, 'Attack1':70, 'Attack2':70,
                     'Ranged Accuracy':36, 'Ranged Attack':70,
                     'Magic Accuracy':26, 'Magic Attack':0, 'Magic Damage':0, 'Magic Accuracy Skill':0, 'Ninjutsu Magic Attack':0, 'Magic Crit Rate':0, 'Magic Burst Damage':0,'Magic Burst Damage II':0,
                     'Daken':0, 'QA':0, 'TA':0, 'DA':0, 'OA8':0, 'OA7':0, 'OA6':0, 'OA5':0, 'OA4':0, 'OA3':0, 'OA2':0,
                     'Crit Rate':0+5, 'Crit Damage':8, 'DA DMG':0, 'TA DMG':0,
                     'Store TP':8,
                     'PDL':0, 'PDL Trait':0,
                     'Dual Wield':0, 'Magic Haste':0, 'Gear Haste':0, 'JA Haste':0,
                     'Zanshin':18, "Fencer":0, # Not sure how to do Zanshin yet. May as well keep track of it now, though.
                     'Weaponskill Damage':8, 'Weaponskill Bonus':0, 'Skillchain Bonus':8, 'ftp':0, 'TP Bonus':0, 'Weaponskill Accuracy':0,
                     'Delay1':0, 'Delay2':0, 'Delay':0, 'Ammo Delay':0, "Ranged Delay":0,
                     'DMG1':0, 'DMG2':0, 'Ammo DMG':0, "Ranged DMG":0,
                     'Light Elemental Bonus':0, 'Dark Elemental Bonus':0, 'Fire Elemental Bonus':0,'Earth Elemental Bonus':0, 'Water Elemental Bonus':0, 'Wind Elemental Bonus':0,'Ice Elemental Bonus':0, 'Thunder Elemental Bonus':0,'Elemental Bonus':0, 'Weaponskill Accuracy':0,
                     'Light Affinity':0, 'Dark Affinity':0, 'Fire Affinity':0,'Earth Affinity':0, 'Water Affinity':0, 'Wind Affinity':0,'Ice Affinity':0, 'Thunder Affinity':0,
                     }
        elif mainjob == "DRG":  # Master Level 20 Dragoon stats. copied from SAM, which was copied from DRK
            self.playerstats = {'STR':117, 'DEX':113, 'VIT':113, 'AGI':110, 'INT':113, 'MND':101, 'CHR':101,
                     'Scythe Skill':0+16, 'Dagger Skill':320+16, 'Sword Skill':388+16, 'Hand-to-Hand Skill':0+16, 'Great Katana Skill':0+16, 'Club Skill':320+16, 'Throwing Skill':0+16,
                     'Katana Skill':0+16, 'Axe Skill':0+16,'Great Axe Skill':0+16,'Polearm Skill':444+16,'Staff Skill':408+16,'Great Sword Skill':0+16,'Archery Skill':0+16,'Marksmanship Skill':0+16,
                     'Ninjutsu Skill':0, "Elemental Magic Skill":0,
                     'Accuracy1':64, 'Accuracy2':64, 'Attack1':55, 'Attack2':55,
                     'Ranged Accuracy':64, 'Ranged Attack':55,
                     'Magic Accuracy':26, 'Magic Attack':0, 'Magic Damage':0, 'Magic Accuracy Skill':0, 'Ninjutsu Magic Attack':0, 'Magic Crit Rate':0, 'Magic Burst Damage':0,'Magic Burst Damage II':0, "Magic Burst Accuracy":0,
                     'Daken':0, 'QA':0, 'TA':0, 'DA':0, 'OA8':0, 'OA7':0, 'OA6':0, 'OA5':0, 'OA4':0, 'OA3':0, 'OA2':0,
                     'Crit Rate':0+5, 'Crit Damage':8, 'DA DMG':0, 'TA DMG':0,
                     'Store TP':0,
                     'PDL':0, 'PDL Trait':0,
                     'Dual Wield':0, 'Magic Haste':0, 'Gear Haste':0, 'JA Haste':0,
                     'Zanshin':0, "Fencer":0, # Not sure how to do Zanshin yet. May as well keep track of it now, though.
                     'Weaponskill Damage':0, 'Weaponskill Bonus':0, 'Skillchain Bonus':8, 'ftp':0, 'TP Bonus':0, 'Weaponskill Accuracy':0,
                     'Delay1':0, 'Delay2':0, 'Delay':0, 'Ammo Delay':0, "Ranged Delay":0,
                     'DMG1':0, 'DMG2':0, 'Ammo DMG':0, "Ranged DMG":0,
                     'Light Elemental Bonus':0, 'Dark Elemental Bonus':0, 'Fire Elemental Bonus':0,'Earth Elemental Bonus':0, 'Water Elemental Bonus':0, 'Wind Elemental Bonus':0,'Ice Elemental Bonus':0, 'Thunder Elemental Bonus':0,'Elemental Bonus':0, 'Weaponskill Accuracy':0,
                     'Light Affinity':0, 'Dark Affinity':0, 'Fire Affinity':0,'Earth Affinity':0, 'Water Affinity':0, 'Wind Affinity':0,'Ice Affinity':0, 'Thunder Affinity':0,
                     }
        elif mainjob == "BLM":  # Master Level 20 Black Mage stats.
            self.playerstats = {'STR':104, 'DEX':113, 'VIT':104, 'AGI':113, 'INT':117, 'MND':117, 'CHR':110,
                     'Katana Skill':0+16, 'Dagger Skill':354+16, 'Sword Skill':0+16, 'Hand-to-Hand Skill':0+16, 'Great Katana Skill':0+16, 'Club Skill':398+16, 'Throwing Skill':354+16,
                     'Axe Skill':0+16,'Great Axe Skill':0+16,'Polearm Skill':0+16,'Scythe Skill':320+16,'Staff Skill':408+16,'Great Sword Skill':0+16,'Archery Skill':0+16,'Marksmanship Skill':0+16,
                     'Ninjutsu Skill':0+16, "Elemental Magic Skill":480+16,
                     'Accuracy1':0, 'Accuracy2':0, 'Attack1':0, 'Attack2':0,
                     'Ranged Accuracy':0, 'Ranged Attack':0,
                     'Magic Accuracy':62, 'Magic Attack':50, 'Magic Damage':43, 'Magic Accuracy Skill':0, 'Ninjutsu Magic Attack':0, 'Ninjutsu Damage':0, 'Magic Crit Rate':0, 'Magic Burst Damage':0, 'Magic Burst Damage II':43, "Magic Burst Accuracy":0,
                     'Daken':0, 'QA':0, 'TA':0, 'DA':0, 'OA8':0, 'OA7':0, 'OA6':0, 'OA5':0, 'OA4':0, 'OA3':0, 'OA2':0,
                     'Crit Rate':5+5, 'Crit Damage':0, 'DA DMG':0, 'TA DMG':0,
                     'Store TP':0,
                     'PDL':0, 'PDL Trait':0,
                     'Dual Wield':0, 'Magic Haste':0, 'Gear Haste':0, 'JA Haste':0,
                     'Zanshin':0, "Fencer":0,
                     'Weaponskill Damage':0, 'Weaponskill Bonus':0, 'Skillchain Bonus':0, 'ftp':0, 'TP Bonus':0, 'Weaponskill Accuracy':0,
                     'Delay1':0, 'Delay2':0, 'Delay':0, 'Ammo Delay':0, "Ranged Delay":0,
                     'DMG1':0, 'DMG2':0, 'Ammo DMG':0, "Ranged DMG":0,
                     'Light Elemental Bonus':0, 'Dark Elemental Bonus':0, 'Fire Elemental Bonus':0,'Earth Elemental Bonus':0, 'Water Elemental Bonus':0, 'Wind Elemental Bonus':0,'Ice Elemental Bonus':0, 'Thunder Elemental Bonus':0,'Elemental Bonus':0, 'Weaponskill Accuracy':0,
                     'Light Affinity':0, 'Dark Affinity':0, 'Fire Affinity':0,'Earth Affinity':0, 'Water Affinity':0, 'Wind Affinity':0,'Ice Affinity':0, 'Thunder Affinity':0,
                     }
        elif mainjob == "RDM":  # Master Level 20 Red Mage stats
            self.playerstats = {'STR':113, 'DEX':115, 'VIT':113, 'AGI':115, 'INT':110, 'MND':101, 'CHR':104, # Stats are copy/pasted from NIN. TODO: fix
                     'Katana Skill':0+16, 'Dagger Skill':418+16, 'Sword Skill':418+16, 'Hand-to-Hand Skill':0+16, 'Great Katana Skill':0+16, 'Club Skill':354+16, 'Throwing Skill':285+16,
                     'Axe Skill':0+16,'Great Axe Skill':0+16,'Polearm Skill':0+16,'Scythe Skill':0+16,'Staff Skill':0+16,'Great Sword Skill':0+16,'Archery Skill':354+16,'Marksmanship Skill':0+16,
                     'Ninjutsu Skill':0+16, "Elemental Magic Skill":398+16,
                     'Accuracy1':32, 'Accuracy2':32, 'Attack1':0, 'Attack2':0,
                     'Ranged Accuracy':22, 'Ranged Attack':0,
                     'Magic Accuracy':90, 'Magic Attack':48, 'Magic Damage':0, 'Magic Accuracy Skill':0, 'Ninjutsu Magic Attack':0, 'Ninjutsu Damage':0, 'Magic Crit Rate':0, 'Magic Burst Damage':0, 'Magic Burst Damage II':43, "Magic Burst Accuracy":0,
                     'Daken':0, 'QA':0, 'TA':0, 'DA':0, 'OA8':0, 'OA7':0, 'OA6':0, 'OA5':0, 'OA4':0, 'OA3':0, 'OA2':0,
                     'Crit Rate':5+5, 'Crit Damage':0, 'DA DMG':0, 'TA DMG':0,
                     'Store TP':0,
                     'PDL':0, 'PDL Trait':0, # PDL trait is added in the merits and traits section later
                     'Dual Wield':0, 'Magic Haste':0, 'Gear Haste':0, 'JA Haste':0,
                     'Zanshin':0, "Fencer":0,
                     'Weaponskill Damage':0, 'Weaponskill Bonus':0, 'Skillchain Bonus':0, 'ftp':0, 'TP Bonus':0, 'Weaponskill Accuracy':0,
                     'Delay1':0, 'Delay2':0, 'Delay':0, 'Ammo Delay':0, "Ranged Delay":0,
                     'DMG1':0, 'DMG2':0, 'Ammo DMG':0, "Ranged DMG":0,
                     'Light Elemental Bonus':0, 'Dark Elemental Bonus':0, 'Fire Elemental Bonus':0,'Earth Elemental Bonus':0, 'Water Elemental Bonus':0, 'Wind Elemental Bonus':0,'Ice Elemental Bonus':0, 'Thunder Elemental Bonus':0,'Elemental Bonus':0, 'Weaponskill Accuracy':0,
                     'Light Affinity':0, 'Dark Affinity':0, 'Fire Affinity':0,'Earth Affinity':0, 'Water Affinity':0, 'Wind Affinity':0,'Ice Affinity':0, 'Thunder Affinity':0,
                     }
        elif mainjob == "SCH":  # Master Level 20 Scholar stats
            self.playerstats = {'STR':104, 'DEX':110, 'VIT':107, 'AGI':110, 'INT':115, 'MND':110, 'CHR':113, # Stats are copy/pasted from NIN. TODO: fix
                     'Katana Skill':0+16, 'Dagger Skill':354+16, 'Sword Skill':0+16, 'Hand-to-Hand Skill':0+16, 'Great Katana Skill':0+16, 'Club Skill':398+16, 'Throwing Skill':354+16,
                     'Axe Skill':0+16,'Great Axe Skill':0+16,'Polearm Skill':0+16,'Scythe Skill':0+16,'Staff Skill':398+16,'Great Sword Skill':0+16,'Archery Skill':0+16,'Marksmanship Skill':0+16,
                     'Ninjutsu Skill':0+16, "Elemental Magic Skill":460+16,
                     'Accuracy1':0, 'Accuracy2':0, 'Attack1':0, 'Attack2':0,
                     'Ranged Accuracy':0, 'Ranged Attack':0,
                     'Magic Accuracy':27, 'Magic Attack':26, 'Magic Damage':0, 'Magic Accuracy Skill':0, 'Ninjutsu Magic Attack':0, 'Ninjutsu Damage':0, 'Magic Crit Rate':0, 'Magic Burst Damage':0, 'Magic Burst Damage II':13, "Magic Burst Accuracy":0,
                     'Daken':0, 'QA':0, 'TA':0, 'DA':0, 'OA8':0, 'OA7':0, 'OA6':0, 'OA5':0, 'OA4':0, 'OA3':0, 'OA2':0,
                     'Crit Rate':5+5, 'Crit Damage':0, 'DA DMG':0, 'TA DMG':0,
                     'Store TP':0,
                     'PDL':0, 'PDL Trait':0, # PDL trait is added in the merits and traits section later
                     'Dual Wield':0, 'Magic Haste':0, 'Gear Haste':0, 'JA Haste':0,
                     'Zanshin':0, "Fencer":0,
                     'Weaponskill Damage':0, 'Weaponskill Bonus':0, 'Skillchain Bonus':0, 'ftp':0, 'TP Bonus':0, 'Weaponskill Accuracy':0,
                     'Delay1':0, 'Delay2':0, 'Delay':0, 'Ammo Delay':0, "Ranged Delay":0,
                     'DMG1':0, 'DMG2':0, 'Ammo DMG':0, "Ranged DMG":0,
                     'Light Elemental Bonus':0, 'Dark Elemental Bonus':0, 'Fire Elemental Bonus':0,'Earth Elemental Bonus':0, 'Water Elemental Bonus':0, 'Wind Elemental Bonus':0,'Ice Elemental Bonus':0, 'Thunder Elemental Bonus':0,'Elemental Bonus':0, 'Weaponskill Accuracy':0,
                     'Light Affinity':0, 'Dark Affinity':0, 'Fire Affinity':0,'Earth Affinity':0, 'Water Affinity':0, 'Wind Affinity':0,'Ice Affinity':0, 'Thunder Affinity':0,
                     }

        two_handed = ["Great Sword", "Great Katana", "Great Axe", "Polearm", "Scythe", "Staff"]
        one_handed = ["Axe", "Club", "Dagger", "Sword", "Katana"] # H2H goes here?
        ranged_skills = ["Marksmanship","Archery"]

        smite_bonus = 0.
        wyvern_bonus = False # This will only apply for DRG main later.
        # Add special bonuses here, just to keep them separate from the main stats. # TODO: move DRK and NIN traits here. New stuff goes here by default
        if mainjob == "DRK":
            smite_bonus = 304./1024
        elif mainjob == "BLM":
            self.playerstats["Magic Burst Damage II"] += 13 # Magic Burst Bonus V trait
            self.playerstats["Magic Attack"] += 40 # Magic Attack Bonus VI trait
            self.playerstats["Magic Attack"] += 10 # Assuming 5/5 elemental potency merits in each element.
        elif mainjob == "RDM":
            self.playerstats["Magic Burst Damage II"] += 7 # Magic Burst Bonus II trait
            self.playerstats["Magic Attack"] += 28 # Magic Attack Bonus III trait
            self.playerstats["Magic Accuracy"] += 15 # Assuming 5/5 elemental magic accuracy merits in each element.
            self.playerstats["Magic Accuracy"] += 25 # Assuming 5/5 magic accuracy group2 merits.
            self.playerstats["PDL Trait"] += 10 # PDL limit I trait
            self.playerstats["TA"] += 35 # Assume +35% TA from full-time Temper2 with a good enhancing magic set at ML20 RDM
        elif mainjob == "SCH":
            self.playerstats["Magic Burst Damage II"] += 9 # Magic Burst Bonus III trait
            self.playerstats["Magic Accuracy"] += 15 # Full time Klimaform
        elif mainjob == "SAM":
            self.playerstats["Store TP"] += 30 # Store TP V trait
            self.playerstats["Store TP"] += 10 # 5/5 Group1 merits
            self.playerstats["Skillchain Bonus"] += 16 # Skillchain Bonus III trait
            self.playerstats["PDL Trait"] += 20  # PDL limit II trait
            self.playerstats["Zanshin"] += 50 # Zanshin V trait
            self.playerstats["Weaponskill Damage"] += 19 # 5/5 Overwhelm merits TODO: This doesn't apply to ranged WSs apparently
            if self.gear['main'].get('Skill Type', 'None') in two_handed:
                self.playerstats["STR"] += 14 # Normal Hasso STR bonus
                self.playerstats["STR"] += 20 # Job point category while using Hasso
                self.playerstats['JA Haste'] += 10 # +10 JA haste from Hasso
                self.playerstats['Accuracy1'] += 10
                self.playerstats['Accuracy2'] += 10
        elif mainjob == "DRG":
            self.playerstats["Weaponskill Bonus"] += 21 # WS Damage Boost trait. Assuming it applies to all hits. TODO: WSD trait is a third WS term, not combined with rema augments
            self.playerstats["Accuracy1"] += 35 # Accuracy Boost III trait
            self.playerstats["Accuracy2"] += 35 # Accuracy Boost III trait
            self.playerstats["PDL Trait"] += 30  # PDL limit III trait
            self.playerstats["Attack1"] += 22 # Attack Boost II trait
            self.playerstats["Attack2"] += 22 # Attack Boost II trait
            smite_bonus = 152./1024 # Smite II trait. We check if using 2h weapon later.
            wyvern_bonus = True # This represents the +20% attack that will be applied later for having a wyvern out (added with smite and stuff)
            self.playerstats["JA Haste"] += 10
            self.playerstats["DA"] += 15
            self.playerstats["Weaponskill Bonus"] += 10 # Wyvern bonus
        elif mainjob == "WAR":
            if self.gear["sub"]["Type"] != "Weapon" and self.gear["main"]["Skill Type"] not in two_handed:
                self.playerstats["Fencer"] += 5 # Fencer V native, plus gear
                fencer_bonus = get_fencer_bonus(self.playerstats["Fencer"])
                self.playerstats["TP Bonus"] += fencer_bonus[0]
                self.playerstats["Crit Rate"] += fencer_bonus[1]

        # Add stats in from your subjob
        # This can get complicated if your main job has a better version of a trait that your subjob would give. For example: DRK main job has a higher "Attack Bonus" trait than subjob WAR. So when DRK/WAR, don't add the Attack bonus from /WAR traits.
        if subjob == "WAR": # Master Level 20 bonus stats from Lv53 WAR subjob
            if mainjob not in ["DRK", "WAR", "DRG", "BLU"]:
                self.playerstats['Attack1'] += 10 # Attack Bonus I trait
                self.playerstats['Attack2'] += 10 # Attack Bonus I trait
                self.playerstats['Ranged Attack'] += 10 # Attack Bonus I trait
            if mainjob not in ["WAR","BST","BRD"]:
                if self.gear["sub"]["Type"] != "Weapon" and self.gear["main"]["Skill Type"] not in two_handed:
                    self.playerstats["Fencer"] += 1 # Fencer I from subjob WAR. 
                                                    # Fencer from gear is applied after we've updated playerstats with gear stats.
                                                    # We'll apply the Fencer bonus stats after we've added up all Fencer+ from gear and traits.
            self.playerstats['DA']  += 12 # Double Attack II trait
            self.playerstats['STR'] += 15
            self.playerstats['DEX'] += 12
            self.playerstats['VIT'] += 10
            self.playerstats['AGI'] += 12
            self.playerstats['INT'] += 7
            self.playerstats['MND'] += 7
            self.playerstats['CHR'] += 9
            if mainjob not in ["DRK", "WAR", "DRG", "MNK", "PUP"]:
                smite_bonus = 100/1024
            if mainjob not in ["DRK", "MNK", "RNG", "DRG", "WAR", "SAM", "BST", "PUP", "DNC", "THF", "NIN", "RDM"]:
                self.playerstats["PDL Trait"] += 10  # PDL limit I trait
                
        elif subjob == "SAM": # Master Level 20 bonus stats from Lv53 SAM subjob
            if self.gear['main'].get('Skill Type', 'None') in two_handed:
                self.playerstats["STR"] += 7 # +7 from full-time Hasso. Remove Hasso for casting on DRK, but keep it on for TP and WS
                self.playerstats['JA Haste'] += 10 # +10 JA haste from Hasso
                self.playerstats['Accuracy1'] += 10
                self.playerstats['Accuracy2'] += 10
            self.playerstats['STR'] += 12
            self.playerstats['DEX'] += 12
            self.playerstats['VIT'] += 12
            self.playerstats['AGI'] += 10
            self.playerstats['INT'] += 9
            self.playerstats['MND'] += 9
            self.playerstats['CHR'] += 10
            self.playerstats["Store TP"] += 20 # Store TP III trait
            if mainjob not in ["DRK","MNK","RNG","DRG","WAR","SAM","BST","PUP","DNC","THF","NIN","RDM"]: # Exclude jobs that get better or equal values TODO: Should also remove weaker values first. This is not an issue right now though
                self.playerstats["PDL Trait"] += 10

        elif subjob == "RDM": # Master Level 20 bonus stats from Lv53 RDM subjob.
            self.playerstats['STR'] += 10
            self.playerstats['DEX'] += 10
            self.playerstats['VIT'] += 9
            self.playerstats['AGI'] += 9
            self.playerstats['INT'] += 12
            self.playerstats['MND'] += 12
            self.playerstats['CHR'] += 10
            if mainjob not in ["BLM","RDM","BLU"]:
                self.playerstats['Magic Attack'] += 24

        elif subjob == "SCH": # Master Level 20 bonus stats from Lv49 SCH subjob. TODO: /53SCH
            self.playerstats['STR'] += 7
            self.playerstats['DEX'] += 9
            self.playerstats['VIT'] += 8
            self.playerstats['AGI'] += 9
            self.playerstats['INT'] += 13
            self.playerstats['MND'] += 9
            self.playerstats['CHR'] += 11
            self.playerstats["Elemental Magic Skill"] = max(self.playerstats["Elemental Magic Skill"], 440+16) # Dark Arts enhances elemental magic skill to B+ rank (then +16 for merits)
            self.playerstats["Magic Accuracy"] += 15 # fulltime klimaform

        elif subjob == "DRG": # Master Level 20 bonus stats from Lv53 DRG subjob. Not yet implemented; copy/pasted /sam stuff
            self.playerstats['STR'] += 12
            self.playerstats['DEX'] += 12
            self.playerstats['VIT'] += 12
            self.playerstats['AGI'] += 10
            self.playerstats['INT'] += 9
            self.playerstats['MND'] += 9
            self.playerstats['CHR'] += 10
            self.playerstats["Weaponskill Bonus"] += 7 # WS Damage Boost I trait. Assuming it applies to all hits.
            if mainjob not in ["DRK", "WAR", "DRG", "BLU"]:
                self.playerstats['Attack1'] += 10 # Attack Bonus I trait
                self.playerstats['Attack2'] += 10 # Attack Bonus I trait
                self.playerstats['Ranged Attack'] += 10 # Attack Bonus I trait
            if mainjob not in ["DRK", "WAR", "DRG", "MNK", "PUP"]:
                smite_bonus = 100./1024 # Smite I trait
            if mainjob not in ["RNG", "DRG", "DNC", "RUN", "BLU"]:
                self.playerstats['Accuracy1'] += 10 # Accuracy Bonus I trait
                self.playerstats['Accuracy2'] += 10 # Accuracy Bonus I trait
                self.playerstats['Ranged Accuracy'] += 10 # Accuracy Bonus I trait
            if mainjob not in ["DRK", "MNK", "RNG", "DRG", "WAR", "SAM", "BST", "PUP", "DNC", "THF", "NIN", "RDM"]:
                self.playerstats["PDL Trait"] += 10  # PDL limit I trait

        elif subjob == "NIN": # Master Level 20 bonus stats from Lv53 NIN subjob. Not yet implemented; copy/pasted /sam stuff
            self.playerstats['STR'] += 12
            self.playerstats['DEX'] += 12
            self.playerstats['VIT'] += 12
            self.playerstats['AGI'] += 10
            self.playerstats['INT'] += 9
            self.playerstats['MND'] += 9
            self.playerstats['CHR'] += 10
            if mainjob not in ["DRK", "MNK", "RNG", "DRG", "WAR", "SAM", "BST", "PUP", "DNC", "THF", "NIN", "RDM"]:
                self.playerstats["PDL Trait"] += 10  # PDL limit I trait

        elif subjob == "DRK": # Master Level 20 bonus stats from Lv53 NIN subjob. Not yet implemented; copy/pasted /sam stuff
            self.playerstats['STR'] += 12
            self.playerstats['DEX'] += 12
            self.playerstats['VIT'] += 12
            self.playerstats['AGI'] += 10
            self.playerstats['INT'] += 9
            self.playerstats['MND'] += 9
            self.playerstats['CHR'] += 10
            if mainjob not in ["DRK", "MNK", "RNG", "DRG", "WAR", "SAM", "BST", "PUP", "DNC", "THF", "NIN", "RDM"]:
                self.playerstats["PDL Trait"] += 20  # PDL limit II trait
            if mainjob not in ["DRK", "WAR", "DRG", "BLU"]:
                self.playerstats['Attack1'] += 35 # Attack Bonus I trait
                self.playerstats['Attack2'] += 35 # Attack Bonus I trait
                self.playerstats['Ranged Attack'] += 35 # Attack Bonus I trait
            if mainjob not in ["DRK", "WAR", "DRG", "MNK", "PUP"]:
                smite_bonus = 152./1024 # Smite II trait
     
        # Traits are done now.

        # Do set bonuses!
        # Count the number of set-bonus gear equipped.
        self.set_bonuses = {'Crit Rate':0, 'STR':0, 'DEX':0, 'AGI':0, 'VIT':0, "MND":0, 'CHR':0, "Accuracy":0, "Ranged Accuracy":0, "Magic Accuracy":0, "Magic Attack":0}
        adhemar_count = 0    # Adhemar +1 gives Crit Rate
        mummu_count = 0      # Mummu +2 with the Mummu Ring gives DEX/AGI/VIT/CHR
        regal_ring_count = 0 # Regal Ring with AF+3 gear gives Accuracy/Ranged Accuracy/Magic Accuracy.
        flamma_count = 0     # Flamma +2 with the Flamma Ring gives STR/DEX/VIT
        ayanmo_count = 0     # Flamma +2 with the Flamma Ring gives STR/VIT/MND
        amalric_count = 0    # +10 Magic Attack for every piece of Amalric equipped after the first
        for slot in gear:
            if "adhemar" in gear[slot]['Name'].lower() and "+1" in gear[slot]['Name'].lower():
                adhemar_count += 1
            if gear["ring1"]['Name'] == "Mummu Ring" or gear["ring2"]['Name'] == "Mummu Ring":
                if "mummu" in gear[slot]['Name'].lower() and "+2" in gear[slot]['Name']:
                    mummu_count += 1
            if "regal ring" == gear['ring1']['Name'].lower() or "regal ring" == gear['ring2']['Name'].lower():
                if "hachiya" in gear[slot]['Name'].lower() or "wakido" in gear[slot]['Name']:
                    if regal_ring_count == 4:
                        continue
                    regal_ring_count += 1
            if "flamma ring" == gear['ring1']['Name'].lower() or "flamma ring" == gear['ring2']['Name'].lower():
                if "flamma" in gear[slot]['Name'].lower() and "+2" in gear[slot]['Name']:
                    flamma_count += 1
            if "ayanmo ring" == gear['ring1']['Name'].lower() or "ayanmo ring" == gear['ring2']['Name'].lower():
                if "ayanmo" in gear[slot]['Name'].lower() and "+2" in gear[slot]['Name']:
                    ayanmo_count += 1
            if "Amalric" in gear[slot]["Name"]:
                amalric_count += 1
        self.set_bonuses['Crit Rate'] += adhemar_count*2 if adhemar_count > 1 else 0
        self.set_bonuses['DEX'] += (mummu_count)*8 if mummu_count >= 2 else 0
        self.set_bonuses['AGI'] += (mummu_count)*8 if mummu_count >= 2 else 0
        self.set_bonuses['VIT'] += (mummu_count)*8 if mummu_count >= 2 else 0
        self.set_bonuses['CHR'] += (mummu_count)*8 if mummu_count >= 2 else 0
        self.set_bonuses['Accuracy']        += (regal_ring_count)*15
        self.set_bonuses['Ranged Accuracy'] += (regal_ring_count)*15
        self.set_bonuses['Magic Accuracy']  += (regal_ring_count)*15
        self.set_bonuses['DEX'] += (flamma_count)*8 if flamma_count >= 2 else 0
        self.set_bonuses['VIT'] += (flamma_count)*8 if flamma_count >= 2 else 0
        self.set_bonuses['STR'] += (flamma_count)*8 if flamma_count >= 2 else 0
        self.set_bonuses['Magic Attack'] += (amalric_count)*10 if amalric_count >= 2 else 0
        self.set_bonuses['STR'] += (ayanmo_count)*8 if ayanmo_count >= 2 else 0
        self.set_bonuses['VIT'] += (ayanmo_count)*8 if ayanmo_count >= 2 else 0
        self.set_bonuses['MND'] += (ayanmo_count)*8 if ayanmo_count >= 2 else 0 # TODO: confirm and remove the ring requirement for ambu gear.

        # Add set bonuses to gearstats
        for stat in self.set_bonuses:
            self.gearstats[stat] += self.set_bonuses[stat]
            if stat == 'Accuracy': # Skip the Accuracy stat for the "playerstats." Accuracy is added to "gearstats" on the line above, then converted to Accuracy1 and Accuracy2 in "playerstats" later.
                continue
            else:
                self.playerstats[stat] += self.set_bonuses[stat]

        # Build the gearstat dictionary from the provided gear set.
        for stat in self.gearstats: # stat = stat name as seen in the gearstats dictionary: "STR", "TA", "Crit Rate", etc
            for k in self.gear.values(): # k = Dictionary containing the stats for a single piece of gear for all slots one slot at a time: {'Name': 'Gere Ring', 'STR': 10, 'Attack': 16, 'TA': 5}
                if stat in k.keys(): # If the stat in gearstats exists on the piece of gear being checked.
                    self.gearstats[stat] += k[stat] # Add the stat from the gear to the gearstats dictionary.

        # Increase playerstats dictionary values by the amount listed on gear.
        for slot in self.gear: # slot = 'head', 'neck', 'ear1', etc
            for stat in gear[slot]: # stat = The stats on a piece of gear: "STR", "Double Attack", etc
                if stat not in self.gearstats or stat not in self.playerstats: # Skill stats on gear that I haven't yet added to the playerstats dictionary. Things like "Accuracy" and "Attack" in gearstats are called "Accuracy1" "Accuracy2" "Attack1" and "Attack2" in the playerstats and won't be found on gear, which uses "Accuracy." Skip them here
                    continue
                main_wpn_skill = self.gear['main'].get('Skill Type', 'None') + ' Skill' # Record the type of weapon being used in the main hand. "Katana Skill" for example
                sub_wpn_skill = self.gear['sub'].get('Skill Type', 'None') + ' Skill' # Same for off-hand
                rng_wpn_skill = self.gear['ranged'].get('Skill Type', 'None') + ' Skill' # Same for ranged slot
                if (slot == "main" and stat == main_wpn_skill) or (slot == "sub" and stat == sub_wpn_skill): # Skip adding skill+ stats from weapons for now. These get converted into attack and accuracy later. This skips skill from grips too, but only a few relatively useless grips have skill+ on them, so we'll ignore this issue for now.
                    continue
                self.playerstats[stat] += self.gear[slot][stat]
                # self.gearstats[stat] += self.gear[slot][stat] # This line is re-adding stuff already added above. Commenting it out for now.

        # print(self.playerstats)
        # At this point, the playerstats dictionary should have all the player's gear stats except attack1, attack2, accuracy1, and accuracy2

        # Stats from gear have now been applied to playerstats.
        # Check for trait enhancements from gear now (Fencer+1 for example)
        if self.gear["sub"]["Type"] != "Weapon" and self.gear["main"]["Skill Type"] not in two_handed: # Apply Fencer bonuses based on Fencer+ gear.
            fencer_bonus = get_fencer_bonus(self.playerstats["Fencer"])
            self.playerstats["TP Bonus"] += fencer_bonus[0]
            self.playerstats["Crit Rate"] += fencer_bonus[1]

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

        # Add WHM "Boost-STAT" bonus here
        if buffs["whm"]:
                self.playerstats['STR'] += buffs["whm"].get("STR", 0)
                self.playerstats['DEX'] += buffs["whm"].get("DEX", 0)
                self.playerstats['VIT'] += buffs["whm"].get("VIT", 0)
                self.playerstats['AGI'] += buffs["whm"].get("AGI", 0)
                self.playerstats['INT'] += buffs["whm"].get("INT", 0)
                self.playerstats['MND'] += buffs["whm"].get("MND", 0)
                self.playerstats['CHR'] += buffs["whm"].get("CHR", 0)
                self.playerstats['Magic Haste'] += buffs["whm"].get("Haste",0)


        # Add skill levels from armor. See Hachiya Tekko +3: "Throwing Skill +14"
        main_weapon_skill_type = self.gear['main'].get('Skill Type','None') + ' Skill'
        sub_weapon_skill_type = self.gear['sub'].get('Skill Type','None')  + ' Skill' if dual_wield else False
        ammo_weapon_skill_type = self.gear['ammo'].get('Skill Type','None') + ' Skill'
        main_gear_skill, sub_gear_skill, ammo_gear_skill = [0 for k in range(3)]
        for slot in self.gear:
            if slot == 'main' or slot == 'sub':
                continue
            main_gear_skill += self.gear[slot].get(main_weapon_skill_type, 0)
            if dual_wield:
                sub_gear_skill += self.gear[slot].get(sub_weapon_skill_type, 0)
            ammo_gear_skill += self.gear[slot].get(ammo_weapon_skill_type, 0)

        # Increase player Attack and Ranged Attack based on gear and base character stats.
        # Main hand =  Attack1 = 8+GearSkill+STR+Attack+MainWeaponSkill
        # Sub hand = Attack2 = 8+GearSkill+0.5*STR+Attack+SubWeaponSkill
        # Ranged attack = 8+skill + STR + RangedAttack  ~ Assume only using Shuriken so only check Ammo skill and ignore Ranged slot. I'm not interested in NIN Empyreal Arrow sets.
        self.playerstats['Attack1'] += 8 + self.playerstats.get(self.gear['main'].get('Skill Type','None') + ' Skill', 0) + self.playerstats['STR'] + self.gearstats['Attack'] + self.gear['main'].get(self.gear['main'].get('Skill Type','None') + ' Skill', 0) + main_gear_skill
        self.playerstats['Attack2'] += 8 + self.playerstats.get(self.gear['sub'].get('Skill Type','None')  + ' Skill', 0) + int(0.5*(self.playerstats['STR'])) + self.gearstats['Attack'] + self.gear['sub'].get(self.gear['sub'].get('Skill Type','None')  + ' Skill', 0) + sub_gear_skill if dual_wield else 0
        self.playerstats['Ranged Attack'] += 8 + self.playerstats.get(self.gear['ammo'].get('Skill Type','None') + ' Skill',0) + self.playerstats['STR'] + ammo_gear_skill # Ranged attack DOES exist in gearstats, so no need to add it on here.

        # Now add in the additive buffs from BRD songs
        if buffs['brd']:
            self.playerstats['Attack1'] += buffs['brd'].get('Attack',0)
            self.playerstats['Attack2'] += buffs['brd'].get('Attack',0) if dual_wield else 0
            self.playerstats['Ranged Attack'] += buffs['brd'].get('Attack',0)

        # Now multiply each attack by the sum of the %-based attack boosts like COR GEO and Kikoku's Attack+10%
        # First collect the individual attack% boosts and add them together.
        percent_attack_buff = 0.0
        if buffs['cor']:
            percent_attack_buff += buffs['cor'].get('Attack',0) # Chaos roll
        if buffs['geo']:
            percent_attack_buff += buffs['geo'].get('Attack',0) # Fury
        if gear['main']['Name'] == "Kikoku":
            percent_attack_buff += 100./1024.  # +10% Attack boost from Kikoku Aftermath is applied as a sum with GEO and COR % boosts
        if gear['main']['Name'] == "Gungnir":
            percent_attack_buff += 50./1024.  # +5% Attack boost from Gungnir Aftermath
        if gear['main']['Name'] == 'Naegling':
            nbuffs = 8 # Assume 8 buffs: pro, shell, haste, utsu, kakka, yonin, food, signet
            nbuffs += 4 if buffs['brd'] else 0 # If BRD in party, assume +4 buffs from songs
            nbuffs += 2 if buffs['cor'] else 0 # If COR in party, assume +2 buffs from rolls
            nbuffs += 1 if buffs['geo'] else 0 # If GEO in party, assume +1 buff from bubble
            percent_attack_buff += 10.*nbuffs/1024.

        smite_bonus = 0 if self.gear['main'].get('Skill Type','None') not in ["Scythe", "Great Sword", "Hand-to-Hand", "Polearm", "Great Axe", "Great Katana", "Staff"] else smite_bonus

        # Berserk/Warcry would also go here, but there is no real benefit to including them in a simulation (in my opinion).
        percent_attack_buff += ws_atk_bonus

        self.playerstats['Attack1'] *= (1+percent_attack_buff + smite_bonus + 0.2*wyvern_bonus)
        self.playerstats['Attack2'] *= (1+percent_attack_buff) if dual_wield else 1.0 # Smite only applies to main hand, and only when using 2-handed weapons anyway...
        self.playerstats['Ranged Attack'] *= (1+percent_attack_buff) # Smite does not apply to ranged attacks.

        # Convert the attack values to integers.
        self.playerstats['Attack1'] = int(self.playerstats['Attack1'])
        self.playerstats['Attack2'] = int(self.playerstats['Attack2']) if dual_wield else 0
        self.playerstats['Ranged Attack'] = int(self.playerstats['Ranged Attack'])



        # Now work on accuracy1, accuracy2, and ranged accuracy stats

        # Define the accuracy case statement from BG wiki
        def get_skill_accuracy(wpn, slot, gear_skill):
            skill = self.playerstats.get(wpn.get('Skill Type','None') + ' Skill',0) + wpn.get(wpn.get('Skill Type','None')+' Skill',0)*(slot != "ammo") + gear_skill # Example: skill = "Katana_Skill_(armor) + Katana_Skill_(weapon)"; "wpn" == off-hand OR main-hand
            if skill >= 601:
                skill_accuracy = int((skill-600)*0.9)+540
            elif skill >= 401:
                skill_accuracy = int((skill-400)*0.8)+380
            elif skill >= 201:
                skill_accuracy = int((skill-200)*0.9)+200
            else:
                skill_accuracy = skill
            return(skill_accuracy)

        # Increase player Accuracy and Ranged Accuracy based on gear and base character stats.
        self.playerstats['Accuracy1'] += int(0.75*(self.playerstats['DEX'])) + self.gearstats['Accuracy'] + get_skill_accuracy(self.gear['main'], 'main', main_gear_skill)
        self.playerstats['Accuracy2'] += int(0.75*(self.playerstats['DEX'])) + self.gearstats['Accuracy'] + get_skill_accuracy(self.gear['sub'], 'sub', sub_gear_skill) if dual_wield else 0
        self.playerstats['Ranged Accuracy'] += int(0.75*(self.playerstats['AGI'])) + get_skill_accuracy(self.gear['ammo'], 'ammo', ammo_gear_skill)


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



        base_delay = 480 # Before any Martial Arts traits

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
