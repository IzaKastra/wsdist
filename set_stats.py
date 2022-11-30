#
# Created by Kastra on Asura.
# Feel free to /tell in game or send a PM on FFXIAH you have questions, comments, or suggestions.
#
# Version date: 2022 November 29
#
# This code holds the methods for building a player's stats.
#
from buffs import *
from gear import *

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

        # Initialize empty gearset for modification.
        # This will contain all stats that come from gear only. Player stats are defined later.
        self.gearstats = {
                 'STR':0, 'DEX':0, 'VIT':0, 'AGI':0, 'INT':0, 'MND':0, 'CHR':0,
                 'Katana Skill':0, 'Dagger Skill':0, 'Sword Skill':0, 'Hand-to-Hand Skill':0, 'Great Katana Skill':0, 'Club Skill':0, 'Throwing Skill':0,
                 'Axe Skill':0,'Great Axe Skill':0,'Polearm Skill':0,'Scythe Skill':0,'Staff Skill':0,'Great Sword Skill':0,'Archery Skill':0,'Marksmanship Skill':0,
                 'Ninjutsu Skill':0, 'Great Sword Skill':0, 'Marksmanship Skill':0, "Elemental Magic Skill":0,
                 'Accuracy':0, 'Attack':0,
                 'Ranged Accuracy':0, 'Ranged Attack':0,
                 'Magic Accuracy':0, 'Magic Attack':0, 'Magic Damage':0, 'Magic Accuracy Skill':0, 'Ninjutsu Magic Attack':0, 'Ninjutsu Damage':0, 'Magic Crit Rate':0, 'Magic Burst Damage':0, 'Magic Burst Damage II':0,
                 'Daken':0, 'QA':0, 'TA':0, 'DA':0, 'OA8':0, 'OA7':0, 'OA6':0, 'OA5':0, 'OA4':0, 'OA3':0, 'OA2':0,
                 'Crit Rate':0, 'Crit Damage':0,'DA DMG':0, 'TA DMG':0,
                 'Store TP':0,
                 'PDL':0,
                 'Dual Wield':0, 'Magic Haste':0, 'Gear Haste':0, 'JA Haste':0,
                 'Zanshin':0,
                 'Weaponskill Damage':0, 'Weaponskill Bonus':0, 'Skillchain Bonus':0, 'ftp':0, 'TP Bonus':0, 'Weaponskill Accuracy':0,
                 'Delay1':0, 'Delay2':0, 'Delay':0, 'Ammo Delay':0,
                 'DMG1':0, 'DMG2':0, 'Ammo DMG':0,
                 'Light Elemental Bonus':0, 'Dark Elemental Bonus':0, 'Fire Elemental Bonus':0, 'Earth Elemental Bonus':0, 'Water Elemental Bonus':0, 'Wind Elemental Bonus':0, 'Ice Elemental Bonus':0, 'Thunder Elemental Bonus':0,'Elemental Bonus':0,
                 'Light Affinity':0, 'Dark Affinity':0, 'Fire Affinity':0,'Earth Affinity':0, 'Water Affinity':0, 'Wind Affinity':0,'Ice Affinity':0, 'Thunder Affinity':0,
                 }


        # Initialize base player stats with no gear and no subjob.
        # Subjob stats and gear stats will be added later in another part of the code.
        # Base 5% crit rate (0+5), +5 for 5/5 crit merits for 0+5+5

        if mainjob == "NIN":  # Master Level 20 Ninja stats
            # Ninja gets +5% WSD from job gifts
            self.playerstats = {'STR':113, 'DEX':115, 'VIT':113, 'AGI':115, 'INT':110, 'MND':101, 'CHR':104,
                     'Katana Skill':460, 'Dagger Skill':414, 'Sword Skill':409, 'Hand-to-Hand Skill':336, 'Great Katana Skill':404, 'Club Skill':336, 'Throwing Skill':460,
                     'Axe Skill':0,'Great Axe Skill':0,'Polearm Skill':0,'Scythe Skill':0,'Staff Skill':0,'Great Sword Skill':0,'Archery Skill':0,'Marksmanship Skill':0,
                     'Ninjutsu Skill':489, "Elemental Magic Skill":0,
                     'Accuracy1':56, 'Accuracy2':56, 'Attack1':70, 'Attack2':70,
                     'Ranged Accuracy':56, 'Ranged Attack':70,
                     'Magic Accuracy':50, 'Magic Attack':28, 'Magic Damage':40, 'Magic Accuracy Skill':0, 'Ninjutsu Magic Attack':0, 'Ninjutsu Damage':0, 'Magic Crit Rate':0, 'Magic Burst Damage':0, 'Magic Burst Damage II':7,
                     'Daken':54, 'QA':0, 'TA':0, 'DA':0, 'OA8':0, 'OA7':0, 'OA6':0, 'OA5':0, 'OA4':0, 'OA3':0, 'OA2':0,
                     'Crit Rate':0+5+5, 'Crit Damage':0, 'DA DMG':0, 'TA DMG':0,
                     'Store TP':0,
                     'PDL':0, 'PDL Trait':10,
                     'Dual Wield':35, 'Magic Haste':0, 'Gear Haste':0, 'JA Haste':0,
                     'Zanshin':0,
                     'Weaponskill Damage':5, 'Weaponskill Bonus':0, 'Skillchain Bonus':12, 'ftp':0, 'TP Bonus':0, 'Weaponskill Accuracy':0,
                     'Delay1':0, 'Delay2':0, 'Delay':0, 'Ammo Delay':0,
                     'DMG1':0, 'DMG2':0, 'Ammo DMG':0,
                     'Light Elemental Bonus':0, 'Dark Elemental Bonus':0, 'Fire Elemental Bonus':0,'Earth Elemental Bonus':0, 'Water Elemental Bonus':0, 'Wind Elemental Bonus':0,'Ice Elemental Bonus':0, 'Thunder Elemental Bonus':0,'Elemental Bonus':0, 'Weaponskill Accuracy':0,
                     'Light Affinity':0, 'Dark Affinity':0, 'Fire Affinity':0,'Earth Affinity':0, 'Water Affinity':0, 'Wind Affinity':0,'Ice Affinity':0, 'Thunder Affinity':0,
                     }
        elif mainjob == "DRK":  # Master Level 20 Dark Knight stats
            self.playerstats = {'STR':117, 'DEX':113, 'VIT':113, 'AGI':110, 'INT':113, 'MND':101, 'CHR':101,
                     'Scythe Skill':460, 'Dagger Skill':409, 'Sword Skill':424, 'Hand-to-Hand Skill':0, 'Great Katana Skill':0, 'Club Skill':404, 'Throwing Skill':0,
                     'Katana Skill':0, 'Axe Skill':0,'Great Axe Skill':0,'Polearm Skill':0,'Staff Skill':0,'Great Sword Skill':0,'Archery Skill':0,'Marksmanship Skill':0,
                     'Ninjutsu Skill':0, 'Great Sword Skill':453, 'Marksmanship Skill':336, 'Dark Magic Skill':489, 'Axe Skill':424, 'Great Axe Skill':424, "Elemental Magic Skill":0,
                     'Accuracy1':22, 'Accuracy2':22, 'Attack1':202, 'Attack2':202,
                     'Ranged Accuracy':22, 'Ranged Attack':202,
                     'Magic Accuracy':30, 'Magic Attack':0, 'Magic Damage':0, 'Magic Accuracy Skill':0, 'Ninjutsu Magic Attack':0, 'Magic Crit Rate':0, 'Magic Burst Damage':0,'Magic Burst Damage II':0,
                     'Daken':0, 'QA':0, 'TA':0, 'DA':0, 'OA8':0, 'OA7':0, 'OA6':0, 'OA5':0, 'OA4':0, 'OA3':0, 'OA2':0,
                     'Crit Rate':0+5, 'Crit Damage':8, 'DA DMG':0, 'TA DMG':0,
                     'Store TP':0,
                     'PDL':0, 'PDL Trait':50,
                     'Dual Wield':0, 'Magic Haste':0, 'Gear Haste':0, 'JA Haste':0,
                     'Zanshin':0,
                     'Weaponskill Damage':8, 'Weaponskill Bonus':0, 'Skillchain Bonus':12, 'ftp':0, 'TP Bonus':0, 'Weaponskill Accuracy':0,
                     'Delay1':0, 'Delay2':0, 'Delay':0, 'Ammo Delay':0,
                     'DMG1':0, 'DMG2':0, 'Ammo DMG':0,
                     'Light Elemental Bonus':0, 'Dark Elemental Bonus':0, 'Fire Elemental Bonus':0,'Earth Elemental Bonus':0, 'Water Elemental Bonus':0, 'Wind Elemental Bonus':0,'Ice Elemental Bonus':0, 'Thunder Elemental Bonus':0,'Elemental Bonus':0, 'Weaponskill Accuracy':0,
                     'Light Affinity':0, 'Dark Affinity':0, 'Fire Affinity':0,'Earth Affinity':0, 'Water Affinity':0, 'Wind Affinity':0,'Ice Affinity':0, 'Thunder Affinity':0,
                     }
        elif mainjob == "BLM":  # Master Level 40 Black Mage stats
            self.playerstats = {'STR':113, 'DEX':115, 'VIT':113, 'AGI':115, 'INT':110, 'MND':101, 'CHR':104,
                     'Katana Skill':460, 'Dagger Skill':414, 'Sword Skill':409, 'Hand-to-Hand Skill':336, 'Great Katana Skill':404, 'Club Skill':336, 'Throwing Skill':460,
                     'Axe Skill':0,'Great Axe Skill':0,'Polearm Skill':0,'Scythe Skill':0,'Staff Skill':0,'Great Sword Skill':0,'Archery Skill':0,'Marksmanship Skill':0,
                     'Ninjutsu Skill':489, "Elemental Magic Skill":0,
                     'Accuracy1':56, 'Accuracy2':56, 'Attack1':70, 'Attack2':70,
                     'Ranged Accuracy':56, 'Ranged Attack':70,
                     'Magic Accuracy':50, 'Magic Attack':28, 'Magic Damage':0, 'Magic Accuracy Skill':0, 'Ninjutsu Magic Attack':0, 'Ninjutsu Damage':0, 'Magic Crit Rate':0, 'Magic Burst Damage':0, 'Magic Burst Damage II':7,
                     'Daken':54, 'QA':0, 'TA':0, 'DA':0, 'OA8':0, 'OA7':0, 'OA6':0, 'OA5':0, 'OA4':0, 'OA3':0, 'OA2':0,
                     'Crit Rate':0+5+5, 'Crit Damage':0, 'DA DMG':0, 'TA DMG':0,
                     'Store TP':0,
                     'PDL':0, 'PDL Trait':10,
                     'Dual Wield':35, 'Magic Haste':0, 'Gear Haste':0, 'JA Haste':0,
                     'Zanshin':0,
                     'Weaponskill Damage':5, 'Weaponskill Bonus':0, 'Skillchain Bonus':12, 'ftp':0, 'TP Bonus':0, 'Weaponskill Accuracy':0,
                     'Delay1':0, 'Delay2':0, 'Delay':0, 'Ammo Delay':0,
                     'DMG1':0, 'DMG2':0, 'Ammo DMG':0,
                     'Light Elemental Bonus':0, 'Dark Elemental Bonus':0, 'Fire Elemental Bonus':0,'Earth Elemental Bonus':0, 'Water Elemental Bonus':0, 'Wind Elemental Bonus':0,'Ice Elemental Bonus':0, 'Thunder Elemental Bonus':0,'Elemental Bonus':0, 'Weaponskill Accuracy':0,
                     'Light Affinity':0, 'Dark Affinity':0, 'Fire Affinity':0,'Earth Affinity':0, 'Water Affinity':0, 'Wind Affinity':0,'Ice Affinity':0, 'Thunder Affinity':0,
                     }
        # Add stats in from your subjob
        # This can get complicated if your main job has a better version of a trait that your subjob would give. For example: DRK main job has a higher "Attack Bonus" trait than subjob WAR. So when DRK/WAR, don't add the Attack bonus from /WAR traits.
        if subjob == "WAR": # Master Level 20 bonus stats from Lv53 WAR subjob
            self.playerstats['Attack1'] += 10 # Attack Bonus I trait
            self.playerstats['Attack2'] += 10 # Attack Bonus I trait
            self.playerstats['Ranged Attack'] += 10 # Attack Bonus I trait
            self.playerstats['DA']  += 12 # Double Attack II trait
            self.playerstats['STR'] += 15
            self.playerstats['DEX'] += 12
            self.playerstats['VIT'] += 10
            self.playerstats['AGI'] += 12
            self.playerstats['INT'] += 7
            self.playerstats['MND'] += 7
            self.playerstats['CHR'] += 9
        elif subjob == "SAM": # Master Level 20 bonus stats from Lv53 SAM subjob
            self.playerstats['STR'] += 12+7 # +7 from full-time Hasso (Assuming using 2h weapons for now, no DRK Savage Blade yet)
            self.playerstats['DEX'] += 12
            self.playerstats['VIT'] += 12
            self.playerstats['AGI'] += 10
            self.playerstats['INT'] += 9
            self.playerstats['MND'] += 9
            self.playerstats['CHR'] += 10
            self.playerstats['Accuracy1'] += 10
            self.playerstats['Accuracy2'] += 10
            self.playerstats['JA Haste'] += 10
        elif subjob == "RDM": # Master Level 20 bonus stats from Lv53 RDM subjob. Not yet implemented; copy/pasted /sam stuff
            self.playerstats['STR'] += 12+7
            self.playerstats['DEX'] += 12
            self.playerstats['VIT'] += 12
            self.playerstats['AGI'] += 10
            self.playerstats['INT'] += 9
            self.playerstats['MND'] += 9
            self.playerstats['CHR'] += 10
            self.playerstats['Accuracy1'] += 10
            self.playerstats['Accuracy2'] += 10
            self.playerstats['JA Haste'] += 10
        elif subjob == "SCH": # Master Level 20 bonus stats from Lv53 SCH subjob. Not yet implemented; copy/pasted /sam stuff
            self.playerstats['STR'] += 12+7
            self.playerstats['DEX'] += 12
            self.playerstats['VIT'] += 12
            self.playerstats['AGI'] += 10
            self.playerstats['INT'] += 9
            self.playerstats['MND'] += 9
            self.playerstats['CHR'] += 10
            self.playerstats['Accuracy1'] += 10
            self.playerstats['Accuracy2'] += 10
            self.playerstats['JA Haste'] += 10


        # Count the number of set-bonus gear equipped.
        self.set_bonuses = {'Crit Rate':0, 'DEX':0, 'AGI':0, 'VIT':0, 'CHR':0, "Accuracy":0, "Ranged Accuracy":0, "Magic Accuracy":0, 'STR':0, 'VIT':0}
        adhemar_count = 0    # Adhemar +1 gives Crit Rate
        mummu_count = 0      # Mummu +2 with the Mummu Ring gives DEX/AGI/VIT/CHR
        regal_ring_count = 0 # Regal Ring with AF+3 gear gives Accuracy/Ranged Accuracy/Magic Accuracy
        flamma_count = 0     # Flamma +2 with the Flamma Ring gives STR/DEX/VIT
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
                if (slot == "main" and stat == main_wpn_skill) or (slot == "sub" and stat == sub_wpn_skill): # Skip adding skill+ stats from weapons for now. These get converted into attack and accuracy later. This skips skill from grips too, but only a few relatively useless grips have skill+ on them, so we'll ignore this issue for now.
                    continue
                self.playerstats[stat] += self.gear[slot][stat]
                # self.gearstats[stat] += self.gear[slot][stat] # This line is re-adding stuff already added above. Commenting it out for now.


        # At this point, the playerstats dictionary should have all the player's gear stats except attack1, attack2, accuracy1, and accuracy2

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
        main_weapon_skill_type = self.gear['main']['Skill Type'] + ' Skill'
        sub_weapon_skill_type = self.gear['sub']['Skill Type'] + ' Skill' if dual_wield else False
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
        self.playerstats['Attack1'] += 8 + self.playerstats[self.gear['main']['Skill Type'] + ' Skill'] + self.playerstats['STR'] + self.gearstats['Attack'] + self.gear['main'][self.gear['main']['Skill Type'] + ' Skill'] + main_gear_skill
        self.playerstats['Attack2'] += 8 + self.playerstats[self.gear['sub']['Skill Type'] + ' Skill'] + int(0.5*(self.playerstats['STR'])) + self.gearstats['Attack'] + self.gear['sub'][self.gear['sub']['Skill Type'] + ' Skill'] + sub_gear_skill if dual_wield else 0
        self.playerstats['Ranged Attack'] += 8 + self.playerstats.get(self.gear['ammo'].get('Skill Type','None') + ' Skill',0) + self.playerstats['STR'] + ammo_gear_skill # Ranged attack DOES exist in gearstats, so no need to add it on here.

        # Now add in the additive buffs from BRD songs
        if buffs['brd']:
            self.playerstats['Attack1'] += buffs['brd'].get('Attack',0)
            self.playerstats['Attack2'] += buffs['brd'].get('Attack',0) if dual_wield else 0
            self.playerstats['Ranged Attack'] += buffs['brd'].get('Attack',0)
            self.playerstats['Magic Haste'] += buffs['brd'].get('Haste',0)

        # Now multiply each attack by the sum of the %-based attack boosts like COR GEO and Kikoku's Attack+10%
        percent_attack_buff = 0.0
        if buffs['cor']:
            percent_attack_buff += buffs['cor'].get('Attack',0)
        if buffs['geo']:
            percent_attack_buff += buffs['geo'].get('Attack',0)
        if gear['main']['Name'] == "Kikoku":
            percent_attack_buff += 100./1024.  # +10% Attack boost from Kikoku Aftermath is applied as a sum with GEO and COR % boosts
        if gear['main']['Name'] == 'Naegling':
            nbuffs = 8 # Assume 8 buffs: pro, shell, haste, utsu, kakka, yonin, food, signet
            nbuffs += 4 if buffs['brd'] else 0 # If BRD in party, assume +4 buffs from songs
            nbuffs += 2 if buffs['cor'] else 0 # If COR in party, assume +2 buffs from rolls
            nbuffs += 1 if buffs['geo'] else 0 # If GEO in party, assume +1 buff from bubble
            percent_attack_buff += 10.*nbuffs/1024.
        percent_attack_buff += ws_atk_bonus

        self.playerstats['Attack1'] *= (1+percent_attack_buff)
        self.playerstats['Attack2'] *= (1+percent_attack_buff) if dual_wield else 1.0
        self.playerstats['Ranged Attack'] *= (1+percent_attack_buff)

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
            self.playerstats['Ranged Attack'] += buffs['brd'].get('Ranged Attack',0)
        if buffs["geo"]:
            self.playerstats['Accuracy1'] += buffs["geo"].get('Accuracy',0)
            self.playerstats['Accuracy2'] += buffs["geo"].get('Accuracy',0) if dual_wield else 0
            self.playerstats['Ranged Accuracy'] += buffs["geo"].get('Ranged Accuracy',0)
            self.playerstats['Ranged Attack'] += buffs["geo"].get('Ranged Attack',0)
            self.playerstats['Magic Accuracy'] += buffs["geo"].get('Magic Accuracy',0)
            self.playerstats['Magic Attack'] += buffs["geo"].get('Magic Attack',0)
        if buffs["cor"]:
            self.playerstats['Accuracy1'] += buffs["cor"].get('Accuracy',0)
            self.playerstats['Accuracy2'] += buffs["cor"].get('Accuracy',0) if dual_wield else 0
            self.playerstats['Ranged Accuracy'] += buffs["cor"].get('Ranged Accuracy',0)
            self.playerstats['Store TP'] += buffs["cor"].get('Store TP', 0)
            self.playerstats['Magic Accuracy'] += buffs["cor"].get('Magic Accuracy', 0)
            self.playerstats['Magic Attack'] += buffs["cor"].get('Magic Attack', 0)
            self.playerstats['DA'] += buffs["cor"].get('DA', 0)
            self.playerstats['Crit Rate'] += buffs["cor"].get('Crit Rate', 0)



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




        # Adjust main/sub/ammo weapon delays and damage
        self.playerstats['Delay1'] += self.gear['main']['Delay']
        self.playerstats['Delay2'] += self.gear['sub']['Delay'] if dual_wield else 0
        self.playerstats['Delay'] = self.gear['main']['Delay'] + self.gear['sub'].get('Delay',0)
        self.playerstats['Ammo Delay'] += self.gear['ammo'].get('Delay',0)

        self.playerstats['DMG1'] = self.gear['main']['DMG']
        self.playerstats['DMG2'] = self.gear['sub']['DMG'] if dual_wield else 0
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
