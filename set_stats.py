#
# Created by Kastra on Asura.
# Feel free to /tell in game or send a PM on FFXIAH you have questions, comments, or suggestions.
#
# Version date: 2021 August 22
#
# This code holds the methods for building a player's stats.
#
from buffs import *
from gear import *
from init import *

import sys

class set_gear:

    #
    # Python class used to build a dictionary of player stats from gear, buffs, and food.
    # First create zero'd gear stat dictionary, containing all of the offensive stats from the provided gear set
    # Then create a base-player stat dictionary, containing all of the offensive stats a player would have at Lv99 master NIN without a subjob, but with merits
    # Add stats and traits from the selected subjob
    # Check the gear set for set bonuses, then apply those to the gearstats dictionary
    # Build the gearstats dictionary using stats from the provided gearset
    # Build the playerstats dictionary using the stats from the provided gearset. But the playerstats dictionary doesnt have "Attack" or "Accuracy". We need to calculation "Attack1" and "Accuracy2", later for main- and off-hand
    #
    # This does not read in skill from armor, only weapons
    # Need to adjust it to allow, for example, hands: throwing skill +242 (see NIN AF hands)
    #

    def __init__(self, buffs, gear, ws_atk_bonus=0.0):

        self.gear = gear

        mainjob = main_job.upper()
        subjob = sub_job.upper()

        sub_type = gear['sub'].get('Type', 'None') # Check if the item equipped in the sub slot is a weapon or a grip or nothing. If the item doesn't have a "Type" Key then return "None", meaning nothing is equipped.
        dual_wield = sub_type == 'Weapon'

        # Initialize empty gearset for modification.
        # This will contain all stats that come from gear only. Player stats are defined later.
        self.gearstats = {'STR': 0, 'DEX': 0, 'VIT': 0, 'AGI': 0, 'INT': 0, 'MND': 0, 'CHR': 0,
                 'Accuracy': 0, 'Attack': 0, 'Ranged Accuracy': 0, 'Ranged Attack': 0,
                 'Magic Accuracy': 0, 'Magic Attack': 0, 'Magic Damage': 0,
                 'DA': 0, 'TA': 0, 'QA': 0,
                 'OA8': 0, 'OA7': 0, 'OA6': 0, 'OA5': 0, 'OA4': 0, 'OA3': 0, 'OA2': 0,
                 'Crit Rate': 0, 'Crit Damage': 0, 'STP': 0, 'TP Bonus': 0,
                 'Katana Skill': 0, 'Dagger Skill': 0, 'Sword Skill': 0,
                 'PDL': 0, 'Dual Wield': 0, 'Weaponskill Damage': 0, 'Weaponskill Bonus': 0, 'TA DMG': 0,
                 'Ninjutsu Skill': 0, 'Daken': 0, 'Throwing Skill': 0, 'Skillchain Bonus': 0,
                 'Magic Accuracy Skill': 0, 'ftp': 0, 'Ninjutsu Magic Attack': 0,
                 'Zanshin':0, 'Magic Crit Rate':0, 'Magic Burst Damage':0,
                 'Delay1':0, 'Delay2':0, 'Delay':0, 'Ammo Delay':0, 'Haste':0,
                 'DMG1':0, 'DMG2':0, 'Ammo DMG':0, 'Club Skill':0,
                 'Light Affinity':0, 'Dark Affinity':0, 'Fire Affinity':0,
                 'Earth Affinity':0, 'Water Affinity':0, 'Wind Affinity':0,
                 'Ice Affinity':0, 'Thunder Affinity':0,
                 'Light Elemental Bonus':0, 'Dark Elemental Bonus':0, 'Fire Elemental Bonus':0,
                 'Earth Elemental Bonus':0, 'Water Elemental Bonus':0, 'Wind Elemental Bonus':0,
                 'Ice Elemental Bonus':0, 'Thunder Elemental Bonus':0,
                 'Elemental Bonus': 0, 'Weaponskill Accuracy':0}




        # Initialize base player stats with no gear and no subjob.
        # Subjob stats and gear stats will be added later
        # Base 5% crit rate, +5% from merits
        if mainjob == "NIN":
            # Ninja gets +5% WSD from job gifts
            self.playerstats = {'STR': 93, 'DEX': 95, 'VIT': 93, 'AGI': 95, 'INT': 90, 'MND': 81, 'CHR': 84,
                     'Accuracy1': 56, 'Accuracy2': 56, 'Attack1': 70, 'Attack2': 70,
                     'Ranged Accuracy': 56, 'Ranged Attack': 70,
                     'Magic Accuracy': 50, 'Magic Attack': 28, 'Magic Damage': 0,
                     'DA': 0, 'TA': 0, 'QA': 0,
                     'OA8': 0, 'OA7': 0, 'OA6': 0, 'OA5': 0, 'OA4': 0, 'OA3': 0, 'OA2': 0,
                     'Crit Rate': 10, 'Crit Damage': 0, 'STP': 0, 'TP Bonus': 0,
                     'Katana Skill': 440, 'Dagger Skill': 394, 'Sword Skill': 389, 'Great Katana Skill':384,
                     'PDL': 0, 'PDL Trait':0.1, 'Dual Wield': 0.35, 'Weaponskill Damage': 0.05, 'Weaponskill Bonus': 0, 'TA DMG': 0,
                     'Ninjutsu Skill':469, 'Daken': 0.54, 'Throwing Skill': 440, 'Skillchain Bonus': 0.12,
                     'Magic Accuracy Skill': 0, 'ftp': 0, 'Ninjutsu Magic Attack': 0,
                     'Zanshin':0, 'Magic Crit Rate':0, 'Magic Burst Damage':0,
                     'Delay1':0, 'Delay2':0, 'Delay': 0, 'Ammo Delay':0, 'Haste':0,
                     'DMG1':0, 'DMG2':0, 'Ammo DMG':0, 'Club Skill': 316,
                     'Light Affinity':0, 'Dark Affinity':0, 'Fire Affinity':0,
                     'Earth Affinity':0, 'Water Affinity':0, 'Wind Affinity':0,
                     'Ice Affinity':0, 'Thunder Affinity':0,
                     'Light Elemental Bonus':0, 'Dark Elemental Bonus':0, 'Fire Elemental Bonus':0,
                     'Earth Elemental Bonus':0, 'Water Elemental Bonus':0, 'Wind Elemental Bonus':0,
                     'Ice Elemental Bonus':0, 'Thunder Elemental Bonus':0,
                     'Elemental Bonus': 0, 'Weaponskill Accuracy':0}


        if mainjob == "SAM":
            # Using +20 STR from Hasso JP and another +14 STR for having Hasso up. Essentially assuming that Hasso is always up.
            # Using WS damage +19% from 5/5 Overwhelm Merits. This will only apply to first WS hit and also incorrectly applies to ranged weapon skills, but this code does not handle ranged weapon skills yet anyway.
            # If Overwhelm merits apply to ALL HITS, then change "Weaponskill Damage" to 0, and change "Weaponskill Bonus" to 0.19. I don't play SAM so I have no idea if it's all hits or first hit.
            # Notice that there is no "Katana Skill" for example. This will cause the code to throw an error if you use SAM main job but try to equip a weapon that has "Katana Skill +" stat, since there is no "Katana Skill" stat here to be improved.
            self.playerstats = {'STR': 93+34, 'DEX': 93, 'VIT': 93, 'AGI': 90, 'INT': 87, 'MND': 87, 'CHR': 90,
                     'Accuracy1': 36, 'Accuracy2': 36, 'Attack1': 70, 'Attack2': 70,
                     'Ranged Accuracy': 36, 'Ranged Attack': 70,
                     'Magic Accuracy': 36, 'Magic Attack': 0, 'Magic Damage': 0,
                     'DA': 0, 'TA': 0, 'QA': 0,
                     'OA8': 0, 'OA7': 0, 'OA6': 0, 'OA5': 0, 'OA4': 0, 'OA3': 0, 'OA2': 0,
                     'Crit Rate': 5, 'Crit Damage': 0, 'STP': 38, 'TP Bonus': 0,
                     'Great Katana Skill': 440, 'Polearm Skill': 404, 'Archery Skill': 394,
                     'PDL': 0, 'PDL Trait':0.2, 'Dual Wield': 0, 'Weaponskill Damage': 0.19, 'Weaponskill Bonus': 0, 'TA DMG': 0,
                     'Skillchain Bonus': 0.24, 'Magic Accuracy Skill': 0, 'ftp': 0,
                     'Zanshin':0, 'Magic Crit Rate':0, 'Magic Burst Damage':0,
                     'Delay1':0, 'Delay2':0, 'Delay': 0, 'Ranged Delay':0, 'Ammo Delay':0, 'Haste':0, 'Haste2':0.1,
                     'DMG1':0, 'DMG2':0, 'Ranged DMG':0, 'Ammo DMG':0,
                     'Light Affinity':0, 'Dark Affinity':0, 'Fire Affinity':0,
                     'Earth Affinity':0, 'Water Affinity':0, 'Wind Affinity':0,
                     'Ice Affinity':0, 'Thunder Affinity':0,
                     'Elemental Bonus': 1.0, 'Weaponskill Accuracy':0}

        # Add stats in from your subjob. This can get complicated if your main job has a better version trait that your subjob would give. For example: DRK main job has a higher "Attack Bonus" trait than subjob WAR, so when DRK/WAR, don't add the Attack bonus from /WAR traits.
        if subjob == "WAR":
            if mainjob != "DRK":
                self.playerstats['Attack1'] += 10
                self.playerstats['Attack2'] += 10
                self.playerstats['Ranged Attack'] += 10
            self.playerstats['DA'] += 10
            self.playerstats['STR'] += 14
            self.playerstats['DEX'] += 11
            self.playerstats['VIT'] += 9
            self.playerstats['AGI'] += 11
            self.playerstats['INT'] += 7
            self.playerstats['MND'] += 7
            self.playerstats['CHR'] += 8
        if subjob == "SAM":
            self.playerstats['STR'] += 11
            self.playerstats['DEX'] += 11
            self.playerstats['VIT'] += 11
            self.playerstats['AGI'] += 9
            self.playerstats['INT'] += 8
            self.playerstats['MND'] += 8
            self.playerstats['CHR'] += 9
            self.playerstats['STP'] += 15
        if subjob == "COR":
            self.playerstats['STR'] += 8
            self.playerstats['DEX'] += 11
            self.playerstats['VIT'] += 8
            self.playerstats['AGI'] += 12
            self.playerstats['INT'] += 11
            self.playerstats['MND'] += 7
            self.playerstats['CHR'] += 8

        self.set_bonuses = {'Crit Rate':0, 'DEX':0, 'AGI':0, 'VIT':0, 'CHR':0, "Accuracy":0, "Ranged Accuracy":0, "Magic Accuracy":0, 'STR':0, 'VIT':0}
        adhemar_count = 0
        mummu_count = 0
        regal_ring_count = 0
        flamma_count = 0
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
        self.set_bonuses['DEX'] += (mummu_count-1)*8 if mummu_count >= 2 else 0
        self.set_bonuses['AGI'] += (mummu_count-1)*8 if mummu_count >= 2 else 0
        self.set_bonuses['VIT'] += (mummu_count-1)*8 if mummu_count >= 2 else 0
        self.set_bonuses['CHR'] += (mummu_count-1)*8 if mummu_count >= 2 else 0
        self.set_bonuses['Accuracy'] += (regal_ring_count)*15
        self.set_bonuses['Ranged Accuracy'] += (regal_ring_count)*15
        self.set_bonuses['Magic Accuracy'] += (regal_ring_count)*15
        self.set_bonuses['DEX'] += (flamma_count-1)*8 if flamma_count >= 2 else 0
        self.set_bonuses['VIT'] += (flamma_count-1)*8 if flamma_count >= 2 else 0
        self.set_bonuses['STR'] += (flamma_count-1)*8 if flamma_count >= 2 else 0

        # Add set bonuses to gearstats
        for stat in self.set_bonuses:
            self.gearstats[stat] += self.set_bonuses[stat]
            if stat == 'Accuracy': # Skip the Accuracy stat for the "playerstats." Accuracy is added to "gearstats" on the line above, then converted to Accuracy1 and Accuracy2 in "playerstats" later.
                continue
            else:
                self.playerstats[stat] += self.set_bonuses[stat]

        # Build the gearstat dictionary from the provided gear set.
        for stat in self.gearstats:
            for k in self.gear.values():
                if stat in k.keys():
                    self.gearstats[stat] += k[stat]

        for slot in self.gear:
            for stat in gear[slot]:
                if stat not in self.gearstats or stat not in self.playerstats: # Skill stats on gear that I haven't yet added to the playerstats dictionary. Things like "Accuracy" and "Attack" in gearstats are called "Accuracy1" "Accuracy2" "Attack1" and "Attack2" in the playerstats, so skip them here
                    continue
                main_wpn_skill = self.gear['main'].get('Skill Type', 'None') + ' Skill'
                sub_wpn_skill = self.gear['sub'].get('Skill Type', 'None') + ' Skill'
                if (slot == "main" and stat == main_wpn_skill) or (slot == "sub" and stat == sub_wpn_skill): # Skip adding skill+ stats from weapons for now. These get converted into attack and accuracy later. This skips skill from grips too, but only a few relatively useless grips have skill+ on them
                    continue
                self.gearstats[stat] += self.gear[slot][stat]
                self.playerstats[stat] += self.gear[slot][stat]

        # At this point, the playerstats dictionary should have all of the player's gear's stats except attack1, attack2, accuracy1, and accuracy2

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

        # Manually increase player Attack and Ranged Attack based on gear and base character stats.
        # Main hand Attack1 = 8+Skill+STR+Attack
        # Sub hand Attack2 = 8+skill+0.5*STR+Attack
        # Ranged attack = 8+skill + STR + RangedAttack
        self.playerstats['Attack1'] += 8 + self.playerstats[self.gear['main']['Skill Type'] + ' Skill'] + self.playerstats['STR'] + self.gearstats['Attack'] + self.gear['main'][self.gear['main']['Skill Type'] + ' Skill']
        self.playerstats['Attack2'] += 8 + self.playerstats[self.gear['sub']['Skill Type'] + ' Skill'] + int(0.5*(self.playerstats['STR'])) + self.gearstats['Attack'] + self.gear['sub'][self.gear['sub']['Skill Type'] + ' Skill'] if dual_wield else 0
        self.playerstats['Ranged Attack'] += 8 + self.playerstats.get(self.gear['ammo'].get('Skill Type','None') + ' Skill',0) + self.playerstats['STR'] # Ranged attack DOES exist in gearstats, so no need to add it on here

        # Now add in the additive buffs from BRD songs and potentially other sources
        if buffs['brd']:
            self.playerstats['Attack1'] += buffs['brd'].get('Attack',0)
            self.playerstats['Attack2'] += buffs['brd'].get('Attack',0) if dual_wield else 0
            self.playerstats['Ranged Attack'] += buffs['brd'].get('Attack',0)

        # Now multiply each attack by the sum of the %-based attack boosts like COR GEO and Kikoku's Attack+10%
        percent_attack_buff = 0.0
        if buffs['cor']:
            percent_attack_buff += buffs['cor'].get('Attack',0)
        if buffs['geo']:
            percent_attack_buff += buffs['geo'].get('Attack',0)
        if gear['main']['Name'] == "Kikoku":
            percent_attack_buff += 100./1024.  # +10% Attack boost from Kikoku Aftermath is applied as a sum to GEO and COR % boosts
        if gear['main']['Name'] == 'Naegling':
            nbuffs = 8 # (pro, shell, haste, utsu, kakka, yonin, food, signet)
            nbuffs += 4 if buffs['brd'] else 0
            nbuffs += 2 if buffs['cor'] else 0
            nbuffs += 1 if buffs['geo'] else 0
            percent_attack_buff += 10*nbuffs/1024.

        percent_attack_buff += ws_atk_bonus

        self.playerstats['Attack1'] *= (1+percent_attack_buff)
        self.playerstats['Attack2'] *= (1+percent_attack_buff) if dual_wield else 1.0
        self.playerstats['Ranged Attack'] *= (1+percent_attack_buff)

        # INTegerize the attack values
        self.playerstats['Attack1'] = int(self.playerstats['Attack1'])
        self.playerstats['Attack2'] = int(self.playerstats['Attack2']) if dual_wield else 0 # This line zeros out your off-hand attack if not dual wielding.
        self.playerstats['Ranged Attack'] = int(self.playerstats['Ranged Attack'])

        # Now work on accuracy1, accuracy2, and ranged accuracy stats

        # Define the accuracy case statement from BG wiki
        def get_skill_accuracy(wpn, slot):
            # skill = slot[slot['Skill Type'] + ' Skill'] + self.playerstats[slot['Skill Type'] + ' Skill']
            skill = self.playerstats.get(wpn.get('Skill Type','None') + ' Skill',0) + wpn.get(wpn.get('Skill Type','None')+' Skill',0)*(slot != "ammo")
            if skill >= 601:
                skill_accuracy = int((skill-600)*0.9)+540
            elif skill >= 401:
                skill_accuracy = int((skill-400)*0.8)+380
            elif skill >= 201:
                skill_accuracy = int((skill-200)*0.9)+200
            else:
                skill_accuracy = skill
            return(skill_accuracy)

        # Manually increase player Accuracy and Ranged Accuracy based on gear and base character stats.
        self.playerstats['Accuracy1'] += int(0.75*(self.playerstats['DEX'])) + self.gearstats['Accuracy'] + get_skill_accuracy(self.gear['main'], 'main')
        self.playerstats['Accuracy2'] += int(0.75*(self.playerstats['DEX'])) + self.gearstats['Accuracy'] + get_skill_accuracy(self.gear['sub'], 'sub') if dual_wield else 0
        self.playerstats['Ranged Accuracy'] += int(0.75*(self.playerstats['AGI'])) + get_skill_accuracy(self.gear['ammo'], 'ammo')


        # Now add in the additive accuracy buffs, which includes things like BRD madrigals, COR Hunter's Roll, GEO Precision, and Mjollnir Aftermath

        if buffs["brd"]:
            self.playerstats['Accuracy1'] += buffs['brd'].get('Accuracy',0)
            self.playerstats['Accuracy2'] += buffs['brd'].get('Accuracy',0) if dual_wield else 0
            self.playerstats['Ranged Accuracy'] += buffs['brd'].get('Accuracy',0)
        if buffs["geo"]:
            self.playerstats['Accuracy1'] += buffs["geo"].get('Accuracy',0)
            self.playerstats['Accuracy2'] += buffs["geo"].get('Accuracy',0) if dual_wield else 0
            self.playerstats['Ranged Accuracy'] += buffs["geo"].get('Accuracy',0)
        if buffs["cor"]:
            self.playerstats['Accuracy1'] += buffs["cor"].get('Accuracy',0)
            self.playerstats['Accuracy2'] += buffs["cor"].get('Accuracy',0) if dual_wield else 0
            self.playerstats['Ranged Accuracy'] += buffs["cor"].get('Accuracy',0)


        # Finally, after normal spell buffs, food buffs take effect
        if buffs["food"]:
            self.playerstats['Attack1'] += buffs['food'].get('Attack',0)
            self.playerstats['Attack2'] += buffs['food'].get('Attack',0) if dual_wield else 0
            self.playerstats['Ranged Attack'] += buffs['food'].get('Attack',0)
            self.playerstats['Accuracy1'] += buffs['food'].get('Accuracy',0)
            self.playerstats['Accuracy2'] += buffs['food'].get('Accuracy',0) if dual_wield else 0
            self.playerstats['Ranged Accuracy'] += buffs['food'].get('Accuracy',0)
            self.playerstats['Magic Attack'] += buffs['food'].get('Magic Attack',0)
            self.playerstats['STP'] += buffs['food'].get('STP',0)

        # Manually adjust main/sub/ammo weapon delays and damage
        self.playerstats['Delay1'] += self.gear['main']['Delay']
        self.playerstats['Delay2'] += self.gear['sub']['Delay'] if dual_wield else 0
        self.playerstats['Delay'] = self.gear['main']['Delay'] + self.gear['sub'].get('Delay',0)
        self.playerstats['Ammo Delay'] += self.gear['ammo'].get('Delay',0)

        self.playerstats['DMG1'] = self.gear['main']['DMG']
        self.playerstats['DMG2'] = self.gear['sub']['DMG'] if dual_wield else 0
        self.playerstats['Ammo DMG'] = self.gear['ammo'].get('DMG',0)


    def equipment(self):
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
