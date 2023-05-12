#
# Created by Kastra on Asura.
# Feel free to /tell in game or send a PM on FFXIAH you have questions, comments, or suggestions.
#
# Version date: 2023 May 12
#
# This file contains a the GUI tab "Inputs".
#
import PySimpleGUI as sg
import numpy as np # Just to randomly choose the starting gear set
import os
import numpy as np
import base64 # Used to convert image icons into image_data readable by the GUI
from PIL import Image # Imported only for image resizing. Useful for super high resolutions where showing a 32x32 icon is tiny...

from gear import all_food
from gear import *
from enemies import *


sg.Window.get_screen_size() # https://github.com/PySimpleGUI/PySimpleGUI/issues/1996
w, h = sg.Window.get_screen_size()

# https://stackoverflow.com/questions/67148741/pysimplegui-change-font-font-display-ubuntu-ugly-fonts
fontsize = 9
font_choice = ["Cascadia Mono", fontsize]

main_jobs = sorted(["NIN", "DRK", "SCH", "RDM", "BLM", "SAM", "DRG", "WHM", "WAR", "COR","BRD", "THF", "MNK", "DNC", "BST","RUN","RNG","PUP","BLU","GEO","PLD"]) # If you add jobs here, make sure to add them in the gui_wsdist.py and tab_select_gear.py files too.
sub_jobs = sorted(["WAR","MNK","WHM","BLM","RDM","THF","PLD","DRK","BST","BRD","RNG","SAM","NIN","DRG","SMN","BLU","COR","PUP","DNC","SCH","GEO","RUN"]) + ["None"]

player_column = [
  [sg.Text("Main Job:",size=(10,1),font=font_choice), sg.Combo(values=main_jobs, default_value="NIN", readonly=True, key="mainjob",size=(10,1),font=font_choice,tooltip="Select main job.",disabled=False,enable_events=True)],
  [sg.Text("Sub Job:",size=(10,1),font=font_choice), sg.Combo(values=sub_jobs, default_value="WAR", readonly=True, key="subjob",size=(10,1),font=font_choice,tooltip="Select sub job.",disabled=False,enable_events=True)],
]

# Copy pasted from gui_wsdist.py. This will be used to filter the selectable WSs based on main+ranged types.
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
            "Hand-to-Hand":["Raging Fists","Howling Fist","Dragon Kick","Asuran Fists","Tornado Kick","Shijin Spiral","Final Heaven","Victory Smite","Ascetic's Fury","Stringing Pummel","Spinning Attack","Combo","One Inch Punch"]}



spell_dict = {# This SHOULD be a copy/paste of the spell_dict in gui_wsdist.py
              "NIN":["Doton: Ichi","Doton: Ni","Doton: San","Suiton: Ichi","Suiton: Ni","Suiton: San","Huton: Ichi","Huton: Ni","Huton: San","Katon: Ichi","Katon: Ni","Katon: San","Hyoton: Ichi","Hyoton: Ni","Hyoton: San", "Raiton: Ichi","Raiton: Ni","Raiton: San","Ranged Attack"],
              "BLM":["Stone","Stone II","Stone III","Stone IV","Stone V","Stone VI","Stoneja",
                     "Water","Water II","Water III","Water IV","Water V","Water VI","Waterja",
                     "Aero","Aero II","Aero III","Aero IV","Aero V","Aero VI","Aeroja",
                     "Fire","Fire II","Fire III","Fire IV","Fire V","Fire VI","Firaja",
                     "Blizzard","Blizzard II","Blizzard III","Blizzard IV","Blizzard V","Blizzard VI","Blizzaja",
                     "Thunder","Thunder II","Thunder III","Thunder IV","Thunder V","Thunder VI", "Thundaja",
                     "Ranged Attack"],
              "RDM":["Stone","Stone II","Stone III","Stone IV","Stone V",
                     "Water","Water II","Water III","Water IV","Water V",
                     "Aero","Aero II","Aero III","Aero IV","Aero V",
                     "Fire","Fire II","Fire III","Fire IV","Fire V",
                     "Blizzard","Blizzard II","Blizzard III","Blizzard IV","Blizzard V",
                     "Thunder","Thunder II","Thunder III","Thunder IV","Thunder V",],
              "SCH":["Stone","Stone II","Stone III","Stone IV","Stone V","Geohelix II",
                     "Water","Water II","Water III","Water IV","Water V","Hydrohelix II",
                     "Aero","Aero II","Aero III","Aero IV","Aero V","Anemohelix II",
                     "Fire","Fire II","Fire III","Fire IV","Fire V","Pyrohelix II",
                     "Blizzard","Blizzard II","Blizzard III","Blizzard IV","Blizzard V","Cryohelix II",
                     "Thunder","Thunder II","Thunder III","Thunder IV","Thunder V","Ionohelix II",
                     "Luminohelix II", "Noctohelix II","Kaustra"],
              "DRK":["Stone","Stone II","Stone III",
                     "Water","Water II","Water III",
                     "Aero","Aero II","Aero III",
                     "Fire","Fire II","Fire III",
                     "Blizzard","Blizzard II","Blizzard III",
                     "Thunder","Thunder II","Thunder III",],
              "COR":["Earth Shot", "Water Shot", "Wind Shot", "Fire Shot", "Ice Shot", "Thunder Shot","Ranged Attack"],
              "RNG":["Ranged Attack"],
              "SAM":["Ranged Attack"],
              "THF":["Ranged Attack"],
             }
# spell_list = [k for k in spell_list if ":" in k] if main_job == "NIN" else [k for k in spell_list if ":" not in k]
# Same for weapon skill; filter to only show weapon skills that the selected main weapon can equip

ws_column = [
  [sg.Text("Weapon skill:",size=(14,1),font=font_choice,justification="r",key="ws label"),sg.Push()],
  [sg.Text("Min.TP:",font=font_choice,key="minTP label",size=(13,1)), sg.Input("1500",key="mintp",size=(5,1),font=font_choice,tooltip="Lower limit for weapon skill TP.")],
  [sg.Text("Max.TP:",font=font_choice,key="maxTP label",size=(13,1)), sg.Input("1800",key="maxtp",size=(5,1),font=font_choice,tooltip="Upper limit for weapon skill TP.")],
]

special_flourishes = ["Climactic Flourish", "Striking Flourish", "Ternary Flourish", "No Flourish"]
ws_column2 = [
  [sg.vtop(sg.Column([
#   [sg.Text("Weapon skill:",size=(20,1),font=font_choice,justification="r",key="ws label"),sg.Push()],
  [sg.Combo(values=sorted(ws_dict["Katana"]), default_value="Blade: Shun", size=(20,1),readonly=True, k="select weaponskill",font=font_choice,enable_events=True)],
  [sg.Text("Min.TP:",font=font_choice,key="minTP label",size=(13,1)), sg.Input("1500",key="mintp",size=(5,1),font=font_choice,tooltip="Lower limit for weapon skill TP.")],
  [sg.Text("Max.TP:",font=font_choice,key="maxTP label",size=(13,1)), sg.Input("1800",key="maxtp",size=(5,1),font=font_choice,tooltip="Upper limit for weapon skill TP.")],
  [sg.Text("Starting TP:",font=font_choice,key="starttp label",size=(13,1)), sg.Input("0",key="startingtp",size=(5,1),font=font_choice,tooltip="Starting TP value for estimating melee TP sets based on \"Time to WS\"")],
  [sg.Text("Aftermath Lv:",font=font_choice,size=(13,1)),sg.Combo(values=("0","1","2","3"), default_value="0", readonly=True, key="aftermath toggle",size=(3,1),font=font_choice,tooltip="Enable/Disable REMA aftermath effects.\nApplies to Melee and Ranged simultaneously.",visible=True)],
  ])),sg.Push(),
  sg.vtop(sg.Column([
#   [sg.Text("Spell:",size=(16,1),font=font_choice,justification="r"),sg.Push()],
  [sg.Combo(values=spell_dict["NIN"], size=(16,1),default_value=np.random.choice([k for k in spell_dict["NIN"] if "San" in k]), readonly=True, k="select spell",font=font_choice,enable_events=True)],
  [sg.Checkbox("Magic Burst",font=font_choice,key="magic burst toggle",visible=True),sg.Checkbox("Building Flourish",font=font_choice,key="building toggle",visible=False),sg.Checkbox("True Shot",font=font_choice,key="trueshot toggle",visible=False),sg.Checkbox("Blood Rage",font=font_choice,key="bloodrage toggle",visible=False),sg.Checkbox("Nat. Meditation",font=font_choice,key="nat.meditation toggle",visible=False)],
  [sg.Checkbox("Futae",font=font_choice,key="futae toggle",disabled=False,tooltip="Enhance Ninjutsu damage. NIN only.",visible=True),sg.Checkbox("Ebullience",font=font_choice,key="ebullience toggle",disabled=False,tooltip="Enhance Black Magic damage. SCH only.",visible=False),sg.Checkbox("Sneak Attack",font=font_choice,key="sa toggle",disabled=False,tooltip="Sneak Attack. THF only.",visible=False),sg.Checkbox("Footwork",font=font_choice,key="footwork toggle",disabled=False,tooltip="Footwork significantly enhances Kick Attacks (MNK only)\n(Dragon Kick and Tornado Kick).",visible=False),sg.Checkbox("Mighty Strikes",font=font_choice,key="mightystrikes toggle",visible=False),sg.Checkbox("Velocity Shot",font=font_choice,key="velocityshot toggle",disabled=False,tooltip="Velocity Shot toggle\n+15% Ranged Attack\n-15% Melee Attack\n-15% Magic Haste",visible=False),sg.Checkbox("Last Resort",font=font_choice,key="lastresort toggle",disabled=False,tooltip="Last Resort\n+25% Job Ability Haste\n+34.77% Attack",visible=False),sg.Checkbox("Triple Shot",font=font_choice,key="tripleshot toggle",disabled=False,tooltip="Triple Shot toggle\n+60% Triple Shot",visible=False)],
  [sg.Checkbox("Trick Attack",font=font_choice,key="ta toggle",disabled=False,tooltip="Trick Attack. THF only.",visible=False),sg.Checkbox("Impetus",font=font_choice,key="impetus toggle",disabled=False,tooltip="Assume 90% Impetus bonus:\nCrit Rate +45%\nAttack+90\nCrit Damage +45% (if using Bhikku Body)",visible=False),sg.Combo(values=special_flourishes, size=(20,1),default_value="No Flourish", readonly=True, k="select flourish",font=font_choice,enable_events=True, visible=False),sg.Checkbox("Hover Shot",font=font_choice,key="hovershot toggle",disabled=False,tooltip="Hover Shot toggle\n+100% Ranged Damage\n+100 Ranged Accuracy\n+100 Magic Accuracy",visible=False),sg.Checkbox("Endark II",font=font_choice,key="endark toggle",disabled=False,tooltip="+70 Attack (80\% of 600 Dark Magic Skill)\n+20 Accuracy from Job Points",visible=False)],
  [sg.Checkbox("Double Shot",font=font_choice,key="doubleshot toggle",disabled=False,tooltip="Double Shot toggle\n+60% Double Shot",visible=False),sg.Checkbox("Hasso",font=font_choice,key="hasso toggle",disabled=False,tooltip="+10% JA Haste\n+7 STR\n+10 Accuracy",visible=False)]
  ],))


]]


food_list = sorted([k["Name"] for k in all_food]) + ["None"] # Reads "all_food" from gear.py
food_list = [k["Name"] for k in all_food] + ["None"] # Reads "all_food" from gear.py
buffs_whm_column = [
  [sg.Checkbox("WHM",size=(15,1),tooltip="Use White Magic buffs?",key="whm_on",default=False,font=font_choice)],
  [sg.Combo(values=("Dia","Dia II","Dia III","None"), default_value="Dia II", readonly=True, k="ndia",size=(16,1),font=font_choice)],
  [sg.Combo(values=("Haste","Haste II","None"), default_value="Haste", readonly=True, key="nhaste",size=(16,1),font=font_choice)],
  [sg.Combo(values=("Boost-STR","Boost-DEX","Boost-VIT","Boost-AGI","Boost-INT","Boost-MND","Boost-CHR","None"), default_value="None", readonly=True, key="whm_boost",size=(16,1),font=font_choice)],
  [sg.Combo(values=("Sandstorm II","Rainstorm II","Windstorm II","Firestorm II","Hailstorm II","Thunderstorm II","Aurorastorm II","Voidstorm II","None"), default_value="None", readonly=True, key="sch_storm",size=(16,1),font=font_choice)],
  [sg.Text("Food:",font=font_choice,)],
  [sg.Combo(values=food_list, default_value="Grape Daifuku", readonly=True, key="food",size=(17,1),font=font_choice)],
  [sg.Text("",font=font_choice)]
]




song_list = ["Blade Madrigal","Sword Madrigal","Minuet V","Minuet IV","Minuet III","Honor March","Victory March","Adv. March","Hunter's Prelude","Archer's Prelude",
             "Sinewy Etude","Herculean Etude","Dextrous Etude","Uncanny Etude","Vivacious Etude","Vital Etude","Quick Etude","Swift Etude","Learned Etude","Sage Etude","Spirited Etude","Logical Etude","Enchanting Etude","Bewitching Etude"]
song1 = "Honor March"
song2 = "Victory March"
song3 = "Minuet V"
song4 = "None"
song5 = "None"
# BRD buffs column
buffs_brd_column = [
  [sg.Checkbox("BRD",size=(17,1),tooltip="Use Bard buffs?",key="brd_on",default=False,font=font_choice,enable_events=True)],
  [sg.Combo(values=("Songs +9","Songs +8","Songs +7","Songs +6","Songs +5","Songs +4","Songs +3","Songs +2","Songs +1","Songs +0"), default_value="Songs +7", readonly=True, k="nsong",size=(17,1),font=font_choice)],
  [sg.Combo(values=song_list + ["None"], default_value=song1, readonly=True,enable_events=True, k="song1",size=(17,1),font=font_choice)],
  [sg.Combo(values=song_list + ["None"], default_value=song2, readonly=True,enable_events=True, k="song2",size=(17,1),font=font_choice)],
  [sg.Combo(values=song_list + ["None"], default_value=song3, readonly=True,enable_events=True, k="song3",size=(17,1),font=font_choice)],
  [sg.Combo(values=song_list + ["None"], default_value=song4, readonly=True,enable_events=True, k="song4",size=(17,1),font=font_choice)],
  [sg.Combo(values=song_list + ["None"], default_value=song5, readonly=True,enable_events=True, k="song5",size=(17,1),font=font_choice)],
  [sg.Checkbox("Marcato*",size=(15,1),font=font_choice,disabled=True,k="marcato",enable_events=True,tooltip="Marcato applies to the first song.")],
  [sg.Checkbox("Soul Voice",size=(15,1),font=font_choice,disabled=True,k="soulvoice",enable_events=True)],
]


# "I","II","III","IV","V","VI","VII","VIII","IX","X","XI"
rolls_list = ["Chaos", "Fighter's", "Hunter's", "Rogue's", "Samurai", "Wizard's"]
roll1 = "Chaos"
roll2 = "Samurai"
# COR buffs column
buffs_cor_column = [
#   [sg.Checkbox("COR",size=(14,1),tooltip="Use Corsair buffs?",key="cor_on",default=False,enable_events=True,font=font_choice)],
#   [sg.Combo(values=("Rolls +8","Rolls +7","Rolls +6","Rolls +5","Rolls +3","Rolls +0"), default_value="Rolls +7", readonly=True, k="nroll",size=(14,1),font=font_choice)],
#   [sg.Combo(values=rolls_list + ["None"], default_value=roll1, readonly=True, k="roll1",size=(14,1),font=font_choice,enable_events=True)],
#   [sg.Combo(values=rolls_list + ["None"], default_value=roll2, readonly=True, k="roll2",size=(14,1),font=font_choice,enable_events=True)],
#   [sg.Checkbox("Light Shot",size=(14,1),font=font_choice,disabled=True,k="LIGHTSHOT")],
#   [sg.Checkbox("Crooked\nCards*",size=(14,2),font=font_choice,disabled=True,k="Crooked Cards",tooltip="Crooked Cards applies to the first roll.")],
#   [sg.Text("",font=font_choice)], # Blank line with the same font so that the formatting lines up with other buffs
#   [sg.Text("",font=font_choice)], # Blank line with the same font so that the formatting lines up with other buffs
  [sg.Checkbox("COR",size=(14,1),tooltip="Use Corsair buffs?",key="cor_on",default=False,enable_events=True,font=font_choice)],
  [sg.Combo(values=("Rolls +8","Rolls +7","Rolls +6","Rolls +5","Rolls +3","Rolls +0"), default_value="Rolls +7", readonly=True, k="nroll",size=(17,1),font=font_choice)],
  [sg.Combo(values=("1","2","3","4","5","6","7","8","9","10","11"), default_value="9", readonly=True, k="roll1 potency",size=(3,1),font=font_choice,tooltip="Dice roll value."),sg.Combo(values=rolls_list + ["None"], default_value=roll1, readonly=True, k="roll1",size=(10,1),font=font_choice,enable_events=True)],
  [sg.Combo(values=("1","2","3","4","5","6","7","8","9","10","11"), default_value="9", readonly=True, k="roll2 potency",size=(3,1),font=font_choice,tooltip="Dice roll value."),sg.Combo(values=rolls_list + ["None"], default_value=roll2, readonly=True, k="roll2",size=(10,1),font=font_choice,enable_events=True)],
  [sg.Checkbox("Job Bonuses",size=(14,1),font=font_choice,disabled=True,k="Job Bonus",tooltip="Include bonus stats for having the relevant jobs in party?\n(SAM roll gets an additional +10 STP for having a SAM in party)")],
  [sg.Checkbox("Light Shot",size=(14,1),font=font_choice,disabled=True,k="LIGHTSHOT")],
  [sg.Checkbox("Crooked\nCards*",size=(14,2),font=font_choice,disabled=True,k="Crooked Cards",tooltip="Crooked Cards applies to the first roll.")],
  [sg.Text("",font=font_choice)], # Blank line with the same font so that the formatting lines up with other buffs
  [sg.Text("",font=font_choice)], # Blank line with the same font so that the formatting lines up with other buffs

]

geo_spells = sorted(["Acumen", "Fury", "Precision", "Focus", "Haste", "STR", "DEX", "VIT", "AGI", "INT", "MND", "CHR", "Frailty", "Torpor", "Malaise","Languor"])
indispells = ["Indi-"+k for k in geo_spells] + ["None"]
geospells = ["Geo-"+k for k in geo_spells] + ["None"]
entrustspells = ["Entrust-"+k for k in geo_spells] + ["None"]
buffs_geo_column = [
  [sg.Checkbox("GEO",size=(10,1),tooltip="Use Geomancy buffs?",key="geo_on",default=False,font=font_choice,enable_events=True)],
  [sg.Combo(values=("Geomancy +10","Geomancy +7","Geomancy +6","Geomancy +5","Geomancy +0"), default_value="Geomancy +6", readonly=True, k="nbubble",size=(20,1),font=font_choice)],
  [sg.Combo(values=indispells, default_value="Indi-Fury", readonly=True, k="indibuff",size=(20,1),font=font_choice,enable_events=True)],
  [sg.Combo(values=geospells, default_value="Geo-Frailty", readonly=True, k="geobuff",size=(20,1),font=font_choice,enable_events=True)],
  [sg.Combo(values=entrustspells, default_value="None", readonly=True, k="entrust",size=(20,1),font=font_choice,enable_events=True,tooltip="Indi/Geo-bubbles overwrite the entrust bubble.")],
  [sg.Checkbox("Blaze of\nGlory*",size=(15,2),font=font_choice,disabled=True,k="geo_bog",tooltip="Blaze of Glory applies to the \"Geo-\" bubble.")],
  [sg.Checkbox("Bolster",size=(15,1),font=font_choice,disabled=True,k="bolster",enable_events=True)],
  [sg.Text("GEO potency: ",font=font_choice,tooltip="0 = 0% potency\n37 = 37% potency\n100 = 100% potency"),sg.Input("100",size=(4,1),pad=(1,1),font=font_choice,key="geomancy_potency",tooltip="0 = 0% potency\n37 = 37% potency\n100 = 100% potency")],

]

input_length = [5,1]
text_length = [15,1]
stat_length = [5,1]
bwidth = 1
nopad = [1,2]

default_enemy = "Apex Bat" # Just a default value so the fields are populated on start up.
enemy_stat_column = [
  [sg.Text("Enemy:", font=font_choice, size=[6,2],justification="r"), sg.Column([[sg.Combo(values=tuple(list(preset_enemies.keys())+["Custom"]), default_value=preset_enemies[default_enemy]["Name"], readonly=True, k="enemy_name", size=[25,1],font=font_choice,enable_events=True)],
  [sg.Text(f"{preset_enemies[default_enemy]['Location']}",size=(25,1),font=font_choice,key="enemy_location")]])],
  [sg.Text("Level:",size=text_length,font=font_choice,justification="r",border_width=bwidth,pad=nopad),sg.Input(preset_enemies[default_enemy]["Level"],size=input_length,pad=nopad,border_width=bwidth,font=font_choice,key="enemy_level"),],
  [sg.Text("Evasion:",size=text_length,font=font_choice,justification="r",border_width=bwidth,pad=nopad),sg.Input(preset_enemies[default_enemy]["Evasion"],size=input_length,pad=nopad,border_width=bwidth,font=font_choice,key="enemy_evasion"),sg.Text("AGI:",size=stat_length,font=font_choice,justification="r",border_width=bwidth,pad=nopad),sg.Input(preset_enemies[default_enemy]["AGI"],size=input_length,pad=nopad,border_width=bwidth,font=font_choice,key="enemy_agi")],
  [sg.Text("Defense:",size=text_length,font=font_choice,justification="r",border_width=bwidth,pad=nopad),sg.Input(preset_enemies[default_enemy]["Defense"],size=input_length,pad=nopad,border_width=bwidth,font=font_choice,key="enemy_defense"),sg.Text("VIT:",size=stat_length,font=font_choice,justification="r",border_width=bwidth,pad=nopad),sg.Input(preset_enemies[default_enemy]["VIT"],size=input_length,pad=nopad,border_width=bwidth,font=font_choice,key="enemy_vit")],
  [sg.Text("Magic Defense:",size=text_length,font=font_choice,justification="r",border_width=bwidth,pad=nopad),sg.Input(preset_enemies[default_enemy]["Magic Defense"],size=input_length,pad=nopad,border_width=bwidth,font=font_choice,key="enemy_mdefense"), sg.Text("INT:",size=stat_length,font=font_choice,justification="r",border_width=bwidth,pad=nopad),sg.Input(preset_enemies[default_enemy]["INT"],size=input_length,pad=nopad,border_width=bwidth,font=font_choice,key="enemy_int")],
  [sg.Text("Magic Evasion:",size=text_length,font=font_choice,justification="r",border_width=bwidth,pad=nopad),sg.Input(preset_enemies[default_enemy]["Magic Evasion"],size=input_length,pad=nopad,border_width=bwidth,font=font_choice,key="enemy_mevasion"),sg.Text("MND:",size=stat_length,font=font_choice,justification="r",border_width=bwidth,pad=nopad),sg.Input(preset_enemies[default_enemy]["MND"],size=input_length,pad=nopad,border_width=bwidth,font=font_choice,key="enemy_mnd")],
]








def item2image(item_name):
    #
    # Use base64 to convert image data
    #
    items = np.loadtxt('item_list.txt',dtype=str, delimiter=";", unpack=True)

    path32 = "icons32/"
    path64 = "icons64/"
    use_32x32_icons = False if h > 900 else True
    if use_32x32_icons:
        try:
            id = items[0][np.where(np.array([k.lower() for k in items[1]])==item_name.lower())][0]
            contents = open(f"{path32}/{id}.png", 'rb').read()
            encoded = base64.b64encode(contents)
        except IndexError:
            id = 65536
            contents = open(f"{path32}/{id}.png", 'rb').read()
            encoded = base64.b64encode(contents)
        except FileNotFoundError:
            id = items[0][np.where(np.array([k.lower() for k in items[1]])==item_name.lower())][0]
            print(f"File not found: icons32/{id}.png")
            print(f"Download the 32x32 icon for {item_name} and try again.")
            id = 65536
            contents = open(f"{path32}/{id}.png", 'rb').read()
            encoded = base64.b64encode(contents)
    else:
        try:
            id = items[0][np.where(np.array([k.lower() for k in items[1]])==item_name.lower())][0]
            if f"{id}.png" not in os.listdir(path64):
                image32 = Image.open(f"{path32}/{id}.png")
                image64 = image32.resize((48,48))
                image64.save(f"{path64}/{id}.png")
            contents = open(f"{path64}/{id}.png", 'rb').read()
        except IndexError:
            id = 65536
            if f"{id}.png" not in os.listdir(path64):
                image32 = Image.open(f"{path32}/{id}.png")
                image64 = image32.resize((48,48))
                image64.save(f"{path64}/{id}.png")
            contents = open(f"{path64}/{id}.png", 'rb').read()
        except FileNotFoundError:
            id = items[0][np.where(np.array([k.lower() for k in items[1]])==item_name.lower())][0]
            if f"{id}.png" not in os.listdir(path64):
                image32 = Image.open(f"{path32}/{id}.png")
                image64 = image32.resize((48,48))
                image64.save(f"{path64}/{id}.png")
            print(f"File not found: icons32/{id}.png")
            print(f"Download the 32x32 icon for {item_name} and try again.")
            id = 65536
            contents = open(f"{path64}/{id}.png", 'rb').read()
        encoded = base64.b64encode(contents)

    return(encoded)



starting_gearset = {
                'main' : Heishi,
                'sub' : Kunimitsu30,
                'ranged' : Empty,
                'ammo' : Seki,
                'head' : Malignance_Chapeau,
                'body' : Tatenashi_Haramaki,
                'hands' : Malignance_Gloves,
                'legs' : Samnuha_Tights,
                'feet' : Malignance_Boots,
                'neck' : Ninja_Nodowa,
                'waist' : Sailfi_Belt,
                'ear1' : Dedition_Earring,
                'ear2' : Telos_Earring,
                'ring1' : Gere_Ring,
                'ring2' : Epona_Ring,
                'back' : np.random.choice([k for k in capes if "nin" in k["Jobs"] and "Store TP" in k["Name2"]])}
# Define a dictionary containing slot:item_name pairs. The item_name is used to search item_list.txt for item IDs, which are then pulled from icons32/ and displayed in the GUI.
default_images = dict([[k,starting_gearset[k]["Name"]] for k in starting_gearset] )





gear_dict = {"main":mains,"sub":subs+grips,"ranged":ranged,"ammo":ammos,"head":heads,"neck":necks,"ear1":ears,"ear2":ears2,"body":bodies,"hands":hands,"ring1":rings,"ring2":rings2,"back":capes,"waist":waists,"legs":legs,"feet":feet}
for slot in gear_dict:
    gear_dict[slot] = sorted(gear_dict[slot], key=lambda d: d['Name2'])



# TODO: Throw this into a loop again.
start_main,start_sub,start_ranged,start_ammo,start_head,start_neck,start_ear1,start_ear2,start_body,start_hands,start_ring1,start_ring2,start_back,start_waist,start_legs,start_feet = [[] for k in range(16)]

for k in sorted([k['Name2'] for k in mains]):
    start_main.append([sg.Radio(k,"main",font=font_choice,size=(50,1),key="startmain:"+k,enable_events=True,visible=True)])

for k in sorted([k['Name2'] for k in subs+grips]):
    start_sub.append([sg.Radio(k,"sub",font=font_choice,size=(50,1),key="startsub:"+k,enable_events=True)])

for k in sorted([k['Name2'] for k in ranged]):
    start_ranged.append([sg.Radio(k,"ranged",font=font_choice,size=(50,1),key="startranged:"+k,enable_events=True)])

for k in sorted([k['Name2'] for k in ammos]):
    start_ammo.append([sg.Radio(k,"ammo",font=font_choice,size=(50,1),key="startammo:"+k,enable_events=True)])

for k in sorted([k['Name2'] for k in heads]):
    start_head.append([sg.Radio(k,"head",font=font_choice,size=(50,1),key="starthead:"+k,enable_events=True)])

for k in sorted([k['Name2'] for k in necks]):
    start_neck.append([sg.Radio(k,"neck",font=font_choice,size=(50,1),key="startneck:"+k,enable_events=True)])

for k in sorted([k['Name2'] for k in ears]):
    start_ear1.append([sg.Radio(k,"ear1",font=font_choice,size=(50,1),key="startear1:"+k,enable_events=True)])

for k in sorted([k['Name2'] for k in ears2]):
    start_ear2.append([sg.Radio(k,"ear2",font=font_choice,size=(50,1),key="startear2:"+k,enable_events=True)])

for k in sorted([k['Name2'] for k in bodies]):
    start_body.append([sg.Radio(k,"body",font=font_choice,size=(50,1),key="startbody:"+k,enable_events=True)])

for k in sorted([k['Name2'] for k in hands]):
    start_hands.append([sg.Radio(k,"hands",font=font_choice,size=(50,1),key="starthands:"+k,enable_events=True)])

for k in sorted([k['Name2'] for k in rings]):
    start_ring1.append([sg.Radio(k,"ring1",font=font_choice,size=(50,1),key="startring1:"+k,enable_events=True)])

for k in sorted([k['Name2'] for k in rings2]):
    start_ring2.append([sg.Radio(k,"ring2",font=font_choice,size=(50,1),key="startring2:"+k,enable_events=True)])

for k in sorted([k['Name2'] for k in capes]):
    start_back.append([sg.Radio(k,"back",font=font_choice,size=(50,1),key="startback:"+k,enable_events=True)])

for k in sorted([k['Name2'] for k in waists]):
    start_waist.append([sg.Radio(k,"waist",font=font_choice,size=(50,1),key="startwaist:"+k,enable_events=True)])

for k in sorted([k['Name2'] for k in legs]):
    start_legs.append([sg.Radio(k,"legs",font=font_choice,size=(50,1),key="startlegs:"+k,enable_events=True)])

for k in sorted([k['Name2'] for k in feet]):
    start_feet.append([sg.Radio(k,"feet",font=font_choice,size=(50,1),key="startfeet:"+k,enable_events=True)])

framesize = [300,300]


radio_tab = [
    sg.Frame(f"Select main-hand.", [[sg.Column(start_main,size=framesize,scrollable=True,key="radiobox_main_col")]],visible=True,key="radiobox_main"), # Main-hand weapon frame is visible by default
    sg.Frame(f"Select off-hand.", [[sg.Column(start_sub,size=framesize,scrollable=True,key="radiobox_sub_col")]],visible=False,key="radiobox_sub"),
    sg.Frame(f"Select ranged.", [[sg.Column(start_ranged,size=framesize,scrollable=True,key="radiobox_ranged_col")]],visible=False,key="radiobox_ranged"),
    sg.Frame(f"Select ammo.", [[sg.Column(start_ammo,size=framesize,scrollable=True,key="radiobox_ammo_col")]],visible=False,key="radiobox_ammo"),
    sg.Frame(f"Select head.", [[sg.Column(start_head,size=framesize,scrollable=True,key="radiobox_head_col")]],visible=False,key="radiobox_head"),
    sg.Frame(f"Select neck.", [[sg.Column(start_neck,size=framesize,scrollable=True,key="radiobox_neck_col")]],visible=False,key="radiobox_neck"),
    sg.Frame(f"Select ear1.", [[sg.Column(start_ear1,size=framesize,scrollable=True,key="radiobox_ear1_col")]],visible=False,key="radiobox_ear1"),
    sg.Frame(f"Select ear2.", [[sg.Column(start_ear2,size=framesize,scrollable=True,key="radiobox_ear2_col")]],visible=False,key="radiobox_ear2"),
    sg.Frame(f"Select body.", [[sg.Column(start_body,size=framesize,scrollable=True,key="radiobox_body_col")]],visible=False,key="radiobox_body"),
    sg.Frame(f"Select hands.", [[sg.Column(start_hands,size=framesize,scrollable=True,key="radiobox_hands_col")]],visible=False,key="radiobox_hands"),
    sg.Frame(f"Select ring1.", [[sg.Column(start_ring1,size=framesize,scrollable=True,key="radiobox_ring1_col")]],visible=False,key="radiobox_ring1"),
    sg.Frame(f"Select ring2.", [[sg.Column(start_ring2,size=framesize,scrollable=True,key="radiobox_ring2_col")]],visible=False,key="radiobox_ring2"),
    sg.Frame(f"Select back.", [[sg.Column(start_back,size=framesize,scrollable=True,key="radiobox_back_col")]],visible=False,key="radiobox_back"),
    sg.Frame(f"Select waist.", [[sg.Column(start_waist,size=framesize,scrollable=True,key="radiobox_waist_col")]],visible=False,key="radiobox_waist"),
    sg.Frame(f"Select legs.", [[sg.Column(start_legs,size=framesize,scrollable=True,key="radiobox_legs_col")]],visible=False,key="radiobox_legs"),
    sg.Frame(f"Select feet.", [[sg.Column(start_feet,size=framesize,scrollable=True,key="radiobox_feet_col")]],visible=False,key="radiobox_feet"),
    ]


# Create a dictionary containing the starting gearset slot: stats in text form for tooltips:
ignore_stats = ["Jobs","Name","Name2","Type","Skill Type","Rank"]
base_stats = ["STR", "DEX", "VIT", "AGI", "INT", "MND", "CHR"]
wpn_stats = ["DMG","Delay"]
main_stats = ["Accuracy","Attack","Ranged Accuracy","Ranged Attack","Magic Accuracy","Magic Damage","Magic Attack"]
bonus_stats = ["Blood Pact Damage", "Kick Attacks", "Kick Attacks Attack", "Martial Arts", "Sneak Attack", "Trick Attack", "Double Shot", "True Shot","Zanshin", "Hasso", "Quick Draw", "Quick Draw II", "Triple Shot","Magic Crit Rate II","Magic Burst Accuracy","Fencer","JA Haste","Accuracy", "AGI", "Attack", "Axe Skill", "CHR", "Club Skill", "Crit Damage", "Crit Rate", "DA", "DA DMG", "Dagger Skill", "Daken", "Dark Affinity", "Dark Elemental Bonus", "Delay", "DEX", "DMG", "Dual Wield", "Earth Affinity", "Earth Elemental Bonus", "Elemental Bonus", "Elemental Magic Skill", "Fire Affinity", "Fire Elemental Bonus", "ftp", "Gear Haste", "Great Axe Skill", "Great Katana Skill", "Great Sword Skill", "Hand-to-Hand Skill", "Ice Affinity", "Ice Elemental Bonus", "INT", "Katana Skill", "Light Affinity", "Light Elemental Bonus", "Magic Accuracy Skill", "Magic Accuracy", "Magic Attack", "Magic Burst Damage II", "Magic Burst Damage", "Magic Damage", "MND", "Name", "Name2", "Ninjutsu Damage", "Ninjutsu Magic Attack", "Ninjutsu Skill", "OA2", "OA3", "OA4", "OA5", "OA6", "OA7", "OA8", "PDL", "Polearm Skill", "QA", "Ranged Accuracy", "Ranged Attack", "Scythe Skill", "Skillchain Bonus", "Staff Skill", "Store TP", "STR", "Sword Skill", "TA", "TA DMG", "Throwing Skill", "Thunder Affinity", "Thunder Elemental Bonus", "TP Bonus", "VIT", "Water Affinity", "Water Elemental Bonus", "Weaponskill Accuracy", "Weaponskill Damage", "Weather", "Wind Affinity", "Wind Elemental Bonus","Polearm Skill","Marksmanship Skill","Archery Skill"]
def_stats = ["Evasion","Magic Evasion", "Magic Def","DT","MDT","PDT"]

default_tooltips = {}
for slot in gear_dict:
    default_tooltips[slot] = f"{starting_gearset[slot]['Name2']}\n" # Just a list of names right now.

    nl = False
    for k in wpn_stats:
        if starting_gearset[slot].get(k,False):
            default_tooltips[slot] += f"{k}:{starting_gearset[slot][k]},"
            nl = True
        if k=="Delay" and nl:
            default_tooltips[slot] += "\n"

    nl = False
    for k in base_stats:
        if starting_gearset[slot].get(k,False):
            default_tooltips[slot] += f"{k}:{starting_gearset[slot][k]},"
            nl = True
        if nl and k=="CHR":
            default_tooltips[slot] += "\n"

    nl = False
    for k in main_stats:
        if starting_gearset[slot].get(k,False):
            default_tooltips[slot] += f"{k}:{starting_gearset[slot][k]},"
            nl = True
        if "Attack" in k and nl:
            default_tooltips[slot] += "\n"
            nl = False
    for k in starting_gearset[slot]:
        if k in base_stats or k in ignore_stats or k in main_stats or k in wpn_stats or k in def_stats:
            continue
        default_tooltips[slot] += f"{k}:{starting_gearset[slot][k]}\n"

    nl = False
    for k in def_stats:
        if starting_gearset[slot].get(k,False):
            default_tooltips[slot] += f"{k}:{starting_gearset[slot][k]},"
            nl = True
        if "Def" in k and nl:
            default_tooltips[slot] += "\n"
            nl = False





# This is the grid of images that shows equipped gear.
starting_set_tab = [
          [sg.Column([
            [sg.Button(image_data=item2image(default_images["main"]),font=font_choice,pad=(1,1),border_width=0,size=(1,1),key="showradio main",tooltip=default_tooltips["main"]),
            sg.Button(image_data=item2image(default_images["sub"]),font=font_choice,pad=(1,1),border_width=0,size=(1,1),key="showradio sub",tooltip=default_tooltips["sub"]),
            sg.Button(image_data=item2image(default_images["ranged"]),font=font_choice,pad=(1,1),border_width=0,size=(1,1),key="showradio ranged",tooltip=default_tooltips["ranged"]),
            sg.Button(image_data=item2image(default_images["ammo"]),font=font_choice,pad=(1,1),border_width=0,size=(1,1),key="showradio ammo",tooltip=default_tooltips["ammo"]),],
            [sg.Button(image_data=item2image(default_images["head"]),font=font_choice,pad=(1,1),border_width=0,size=(1,1),key="showradio head",tooltip=default_tooltips["head"]),
            sg.Button(image_data=item2image(default_images["neck"]),font=font_choice,pad=(1,1),border_width=0,size=(1,1),key="showradio neck",tooltip=default_tooltips["neck"]),
            sg.Button(image_data=item2image(default_images["ear1"]),font=font_choice,pad=(1,1),border_width=0,size=(1,1),key="showradio ear1",tooltip=default_tooltips["ear1"]),
            sg.Button(image_data=item2image(default_images["ear2"]),font=font_choice,pad=(1,1),border_width=0,size=(1,1),key="showradio ear2",tooltip=default_tooltips["ear2"]),],
            [sg.Button(image_data=item2image(default_images["body"]),font=font_choice,pad=(1,1),border_width=0,size=(1,1),key="showradio body",tooltip=default_tooltips["body"]),
            sg.Button(image_data=item2image(default_images["hands"]),font=font_choice,pad=(1,1),border_width=0,size=(1,1),key="showradio hands",tooltip=default_tooltips["hands"]),
            sg.Button(image_data=item2image(default_images["ring1"]),font=font_choice,pad=(1,1),border_width=0,size=(1,1),key="showradio ring1",tooltip=default_tooltips["ring1"]),
            sg.Button(image_data=item2image(default_images["ring2"]),font=font_choice,pad=(1,1),border_width=0,size=(1,1),key="showradio ring2",tooltip=default_tooltips["ring2"]),],
            [sg.Button(image_data=item2image(default_images["back"]),font=font_choice,pad=(1,1),border_width=0,size=(1,1),key="showradio back",tooltip=default_tooltips["back"]),
            sg.Button(image_data=item2image(default_images["waist"]),font=font_choice,pad=(1,1),border_width=0,size=(1,1),key="showradio waist",tooltip=default_tooltips["waist"]),
            sg.Button(image_data=item2image(default_images["legs"]),font=font_choice,pad=(1,1),border_width=0,size=(1,1),key="showradio legs",tooltip=default_tooltips["legs"]),
            sg.Button(image_data=item2image(default_images["feet"]),font=font_choice,pad=(1,1),border_width=0,size=(1,1),key="showradio feet",tooltip=default_tooltips["feet"]),],
          ]),]]


if h > 900: # If screen height is greater than 900 pixels, then use a vertical (tall) layout
    input_tab = [
            [sg.vtop(sg.Frame("Basic inputs",[[sg.vtop(sg.Column(player_column,))],[sg.Column(ws_column2)]],size=[390,240])),sg.Push(),sg.vtop(sg.Frame("Enemy inputs",[[sg.Column(enemy_stat_column)]],))],
            [sg.Push(),sg.vtop(sg.Frame("Buffs", [[sg.vtop(sg.Column(buffs_whm_column,)), sg.vtop(sg.Column(buffs_brd_column,)), sg.vtop(sg.Column(buffs_cor_column,)), sg.vtop(sg.Column(buffs_geo_column,))]])),sg.Push()],
            [sg.Push(),sg.vtop(sg.Frame("Initial gearset",[[sg.Push(),sg.vcenter(sg.Column([[sg.Column(starting_set_tab)],[sg.Button("Quick-look WS",key="quicklook"),sg.Button("Quick-look Magic",key="quicklook magic", disabled=False)],
            [sg.Push(),sg.Button("Quick-look TP",key="quicklook TP",disabled=False),sg.Button("Calculate Stats",key="get stats", disabled=False),sg.Push()],
            [sg.Text(f"{'Average =':>10s} ------ damage",key="quickaverage",font=font_choice)]])),sg.Push(),sg.Column([radio_tab])],],size=[800,350])),sg.Push()]
            ]

else: # Else, use a horizontal (wide) layout
    input_tab = [[sg.Column([
            [sg.vtop(sg.Frame("Basic inputs",[[sg.vtop(sg.Column(player_column,))],[sg.Column(ws_column2)]],size=[390,230])),sg.Push(),sg.vtop(sg.Frame("Enemy inputs",[[sg.Column(enemy_stat_column)]],))],
            [sg.Push(),sg.vtop(sg.Frame("Buffs", [[sg.vtop(sg.Column(buffs_whm_column,)), sg.vtop(sg.Column(buffs_brd_column,)), sg.vtop(sg.Column(buffs_cor_column,)), sg.vtop(sg.Column(buffs_geo_column,))]])),sg.Push()]]),
            sg.Push(),
            sg.Column([
            [sg.Push(),sg.vtop(sg.Frame("Initial gearset",[[sg.Push(),sg.vcenter(sg.Column([[sg.Column(starting_set_tab)],[sg.Button("Quick-look WS",key="quicklook"),sg.Button("Quick-look Magic",key="quicklook magic", disabled=False)],
            [sg.Push(),sg.Button("Quick-look TP",key="quicklook TP",disabled=False),sg.Button("Calculate Stats",key="get stats", disabled=False),sg.Push()],
            [sg.Text(f"{'Average =':>10s} ------ damage",key="quickaverage",font=font_choice)]])),sg.Push(),sg.Column([radio_tab])],],size=[800,350])),sg.Push()]])
            ]]
