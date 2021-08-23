#
# Created by Kastra on Asura.
# Feel free to /tell in game or send a PM on FFXIAH you have questions, comments, or suggestions.
#
# Version date: 2021 August 22
#
# This file contains most of the lines that you'd want to change when running the code.
# Stuff like job, weapon skill, buffs, gear, TP ranges, number of simulations, file paths, etc
#
from buffs import *
from gear import *

import os

main_job = "NIN" # Only NIN and SAM are completed for main jobs. See the set_stats.py file for examples on how to add your own jobs in
sub_job = "WAR" # Only WAR, SAM, and COR are completed for sub jobs. See the set_stats.py file for examples on how to add your own subjobs in.

WS_name = 'Blade: Chi' # Weapon skill to test
shortname = 'BladeChi' # Shortened weapon skill name. Used as filenames for output files


# Define upper and lower TP limits. Must remain as a list with at least 1 entry.
tp1_list = [1000,1500,2000] # Minimum TP values to check
tp2_list = [1300,1800,2300] # Maximum TP values to check. Same length as "tp1_list"


# Starting gearset for simulations.
starting_gearset = {
                'main' : Heishi,
                'sub' : Kunimitsu,
                'ranged' : Empty,
                'ammo' : Seki,
                'head' : Adhemar_Bonnet_A,
                'body' : Kendatsuba_Samue,
                'hands' : Adhemar_Wristbands_B,
                'legs' : Kendatsuba_Hakama,
                'feet' : Herculean_Boots_QA,
                'neck' : Ninja_Nodowa,
                'waist' : Windbuffet_Belt,
                'ear1' : Dedition_Earring,
                'ear2' : Telos_Earring,
                'ring1' : Gere_Ring,
                'ring2' : Hetairoi_Ring,
                'back' : Andartia_STP}
# starting_gearset = Haste30_TP.copy()

all_gear = [mains, subs, ammos, heads, necks, ears, ears2, bodies, hands, rings, rings2, capes, belts, legs, feet] # List containing lists of gear to check in each slot. Modify the lists in gear.py to change which items are included in "heads" for example.
names = ["main", "sub", "ammo", "head", "neck", "ear1", "ear2", "body", "hands", "ring1", "ring2", "back", "waist", "legs", "feet"] # Names for each slot. Should match length of "all_gear" and uses same format at in-game /equip

fit2 = True # Simultaneously swap up to two equipment pieces at once? This increases runtime significantly, but improves accuracy of finding the best sets when you're dealing with incredibly rare edge cases like set bonuses and being significantly under accuracy cap.


ntrials = 50000 # Number of simulations to be completed to build the final distribution.

savepath = "output/" # Where to save the output image and text file.
savetext = True # Save the output text file?
save_img = True # Save the output distribution image?


items_file = "C:/Users/Meissa/Documents/My Games/FFXI/Windower/res/items.lua" # Location of your items.lua file within your Windower/res/ directory. Used for the final plot.
icons_path = "C:/Users/Meissa/Documents/My Games/FFXI/Windower/addons/equipviewer/icons/" # File path for the icons for each piece of gear. I use equipviewer for this, so I give it the path for the equipviewer/icons/ directory.


# Create the "savepath" directory if it does not exist
if not os.path.exists(savepath):
    os.makedirs(savepath)

# Define your buffs and their potency. See buffs.py file for details on each.
nsong = 7 # Song+
nroll = 7 # Rolls+
nbubble = 6 # Geomancy+
cor_sam = cor['Samurai']['STP'][0] + nroll*cor['Samurai']['STP'][1]
cor_chaos = cor['Chaos']['Attack'][0] + nroll*cor['Chaos']['Attack'][1]
brd_min5 = brd['Minuet V']['Attack'][0] + nsong*brd['Minuet V']['Attack'][1]
brd_min4 = brd['Minuet IV']['Attack'][0] + nsong*brd['Minuet IV']['Attack'][1]
brd_victory = brd['Victory March']['Haste'][0] + nsong*brd['Victory March']['Haste'][1]
brd_hm_attack = brd['Honor March']['Attack'][0] + 4*brd['Honor March']['Attack'][1]
brd_hm_haste = brd['Honor March']['Haste'][0] + 4*brd['Honor March']['Haste'][1]
brd_hm_acc = brd['Honor March']['Accuracy'][0] + 4*brd['Honor March']['Accuracy'][1]
geo_fury = geo['Fury']['Attack'][0] + nbubble*geo['Fury']['Attack'][1]

geo_on = False # Use GEO buffs (defined above)?
cor_on = True # Use COR buffs (defined above)?
brd_on = True # Use BRD buffs (defined above)?

# Define your debuffs.
dia_potency = 2 # Dia potency? (0, 1, 2, 3, 4)
malaise = False # Use Malaise?
frailty = False # Use Frailty?

# Compile the bonuses obtained from buffs.
brd_attack = brd_on*int(brd_min5 + brd_min4 + brd_hm_attack) # Total attack bonus from BRD
brd_accuracy = brd_on*int(brd_hm_acc) # Total accuracy bonus from BRD
cor_attack = cor_on*cor_chaos # Total attack bonus from COR
cor_stp = cor_on*cor_sam # Total STP bonus from COR
geo_attack = geo_on*geo_fury # Total attack bonus from GEO
food = Grape_Daifuku # Load stat bonuses from food, defined in the "gear.py" file. Set to food=False to turn off food.

attack_cap = False # Artifically place attack at 99999? Might not work as intended right now. This is a relic of an earlier version that I never messed with. It's easier to just modify the enemy defense stat to 1


buffs = {"food": food,
         "brd": {"Attack": brd_attack, "Accuracy": brd_accuracy},
         "cor": {"Attack": cor_attack, 'STP': cor_stp},
         "geo": {"Attack": geo_attack},
         "whm": False, # WHM buffs like boost-STR. Not tested
         }


dia = {0: 0,
       1: 104./1024,
       2: 156./1024,
       3: 208./1024,
       4: 236./1024}

# Apex Toad enemy stats defined here.
# Will need to modify the main code to change enemies. Just search for "apex_toad". I might fix this later.
# If your target has some MDT or takes more elemental damage, then you'll need to modify the main code. Search for "enemy_mdt"
# https://w.atwiki.jp/barlett3/pages/327.html
e_mdef = 0-malaise*(15+3*nbubble) if 0-malaise*(15+3*nbubble) > -50 else -50
apex_toad = {'Level': [131, 132, 133],
             'Defense': [1206*(1-dia[dia_potency]-frailty*(0.148+0.027*nbubble)), 1239*(1-dia[dia_potency]-frailty*(0.148+0.027*nbubble)), 1272*(1-dia[dia_potency]-frailty*(0.148+0.027*nbubble))],
             'Evasion': [1103, 1133, 1163],
             'VIT': [264, 270, 276],
             'AGI': [354, 356, 358], # AGI roughly measured using Scoreboard on two different toads.
             'MND': [218, 224, 228],
             'INT': [285, 293, 299],
             'CHR': [270, 277, 284],
             'Magic Defense': [e_mdef, e_mdef, e_mdef]} # Enemy Magic Defense has a floor of 50



buff_list = [] # Construct a list of buffs being used. This list is then used to create a string used in output file names to keep everything organized.
if food:
    buff_list.append(f"{''.join(food['Name'].split())}")
if dia[dia_potency] != 0:
    buff_list.append(f'Dia{dia_potency}')
if brd_on:
    buff_list.append('BRD')
if cor_on:
    buff_list.append('COR')
if geo_on:
    buff_list.append('GEO')
if frailty:
    buff_list.append('Frailty')
if malaise:
    buff_list.append('Malaise')

output_file_suffix = ""
for b in buff_list:
    output_file_suffix += f"_{b}"
