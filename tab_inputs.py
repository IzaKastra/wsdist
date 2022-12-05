#
# Created by Kastra on Asura.
# Feel free to /tell in game or send a PM on FFXIAH you have questions, comments, or suggestions.
#
# Version date: 2022 December 04
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

main_jobs = sorted(["NIN", "DRK", "SCH", "RDM", "BLM", "SAM", "DRG"])
sub_jobs = sorted(["WAR", "SAM", "SCH", "RDM", "NIN", "DRK", "DRG"]) + ["None"]

player_column = [
  [sg.Text("Main Job:",size=(10,1),font=font_choice), sg.Combo(values=main_jobs, default_value="NIN", readonly=True, key="mainjob",size=(10,1),font=font_choice,tooltip="Select main job.",disabled=False,enable_events=True)],
  [sg.Text("Sub Job:",size=(10,1),font=font_choice), sg.Combo(values=sub_jobs, default_value="WAR", readonly=True, key="subjob",size=(10,1),font=font_choice,tooltip="Select sub job.",disabled=False,enable_events=True)],
]

ws_list = sorted(
           ["Blade: Chi", "Blade: Hi", "Blade: Kamu", "Blade: Metsu", "Blade: Shun", "Blade: Ten", "Blade: Ku",
           "Tachi: Rana", "Tachi: Fudo", "Tachi: Kaiten", "Tachi: Shoha", "Tachi: Kasha", "Tachi: Gekko", "Tachi: Jinpu",
           "Evisceration", "Exenterator",
           "Savage Blade", "Death Blossom", "Chant du Cygne", "Knights of Round",
           "Insurgency", "Cross Reaper", "Entropy", "Quietus", "Catastrophe",
           "Torcleaver", "Scourge", "Resolution",
           "Stardiver", "Impulse Drive", "Penta Thrust", "Geirskogul", "Drakesbane", "Camlann's Torment",
           "Black Halo", "Judgment", "Hexa Strike", "Realmrazer"])

spell_list = ["Stone","Stone II","Stone III","Stone IV","Stone V","Stone VI","Stoneja","Doton: Ichi","Doton: Ni","Doton: San",
              "Water","Water II","Water III","Water IV","Water V","Water VI","Waterja","Suiton: Ichi","Suiton: Ni","Suiton: San",
              "Aero","Aero II","Aero III","Aero IV","Aero V","Aero VI","Aeroja","Huton: Ichi","Huton: Ni","Huton: San",
              "Fire","Fire II","Fire III","Fire IV","Fire V","Fire VI","Firaja","Katon: Ichi","Katon: Ni","Katon: San",
              "Blizzard","Blizzard II","Blizzard III","Blizzard IV","Blizzard V","Blizzard VI","Blizzaja","Hyoton: Ichi","Hyoton: Ni","Hyoton: San",
              "Thunder","Thunder II","Thunder III","Thunder IV","Thunder V","Thunder VI","Thundaja","Raiton: Ichi","Raiton: Ni","Raiton: San",
]
non_nin_spells = [k for k in spell_list if ":" not in k]
# spell_list = [k for k in spell_list if ":" in k] if main_job == "NIN" else [k for k in spell_list if ":" not in k]
# Same for weapon skill; filter to only show weapon skills that the selected main weapon can equip

ws_column = [
  [sg.Text("Weapon skill:",size=(14,1),font=font_choice,justification="r",key="ws label"),sg.Push()],
  [sg.Text("Min.TP:",font=font_choice,key="minTP label"), sg.Input("1500",key="mintp",size=(5,1),font=font_choice,tooltip="Lower limit for weapon skill TP.")],
  [sg.Text("Max.TP:",font=font_choice,key="maxTP label"), sg.Input("1800",key="maxtp",size=(5,1),font=font_choice,tooltip="Upper limit for weapon skill TP.")]
]


ws_column2 = [
  [sg.Column([
  [sg.Text("Weapon skill:",size=(14,1),font=font_choice,justification="r",key="ws label"),sg.Push()],[sg.Combo(values=ws_list, default_value="Blade: Shun", readonly=True, k="select weaponskill",font=font_choice,enable_events=True)],
  [sg.Text("Min.TP:",font=font_choice,key="minTP label"), sg.Input("1500",key="mintp",size=(5,1),font=font_choice,tooltip="Lower limit for weapon skill TP.")],
  [sg.Text("Max.TP:",font=font_choice,key="maxTP label"), sg.Input("1800",key="maxtp",size=(5,1),font=font_choice,tooltip="Upper limit for weapon skill TP.")]
  ]),sg.Push(),
  sg.Column([
  [sg.Text("Spell:",size=(15,1),font=font_choice,justification="r"),sg.Push()],[sg.Combo(values=spell_list, default_value="Doton: San", readonly=True, k="select spell",font=font_choice,enable_events=True)],
  [sg.Checkbox("Magic Burst",font=font_choice,key="magic burst toggle")],
  [sg.Checkbox("Futae",font=font_choice,key="futae toggle")],
  ])


]]


food_list = sorted([k["Name"] for k in all_food]) + ["None"] # Reads "all_food" from gear.py
buffs_whm_column = [
  [sg.Checkbox("WHM",size=(15,1),tooltip="Use White Magic buffs?",key="whm_on",default=False,font=font_choice)],
  [sg.Combo(values=("Dia","Dia II","Dia III","None"), default_value="Dia II", readonly=True, k="ndia",size=(15,1),font=font_choice)],
  [sg.Combo(values=("Haste","Haste II","None"), default_value="Haste", readonly=True, key="nhaste",size=(15,1),font=font_choice)],
  [sg.Combo(values=("Boost-STR","Boost-DEX","Boost-VIT","Boost-AGI","Boost-INT","Boost-MND","Boost-CHR","None"), default_value="None", readonly=True, key="whm_boost",size=(15,1),font=font_choice)],
  [sg.Text("Food:",font=font_choice)],
  [sg.Combo(values=food_list, default_value="Grape Daifuku", readonly=True, key="food",size=(15,1),font=font_choice)],
  [sg.Text("",font=font_choice)]
]




song_list = ["Blade Madrigal","Sword Madrigal","Minuet V","Minuet IV","Minuet III","Honor March","Victory March","Adv. March"]
song1 = "Honor March"
song2 = "Victory March"
song3 = "Minuet V"
song4 = "None"
# BRD buffs column
buffs_brd_column = [
  [sg.Checkbox("BRD",size=(15,1),tooltip="Use Bard buffs?",key="brd_on",default=False,font=font_choice,enable_events=True)],
  [sg.Combo(values=("Songs +8","Songs +7","Songs +6","Songs +5","Songs +4","Songs +3","Songs +2","Songs +1","Songs +0"), default_value="Songs +7", readonly=True, k="nsong",size=(15,1),font=font_choice)],
  [sg.Combo(values=song_list + ["None"], default_value=song1, readonly=True,enable_events=True, k="song1",size=(15,1),font=font_choice)],
  [sg.Combo(values=song_list + ["None"], default_value=song2, readonly=True,enable_events=True, k="song2",size=(15,1),font=font_choice)],
  [sg.Combo(values=song_list + ["None"], default_value=song3, readonly=True,enable_events=True, k="song3",size=(15,1),font=font_choice)],
  [sg.Combo(values=song_list + ["None"], default_value=song4, readonly=True,enable_events=True, k="song4",size=(15,1),font=font_choice)],
  [sg.Checkbox("Marcato*",size=(15,1),font=font_choice,disabled=True,k="marcato",enable_events=True,tooltip="Marcato applies to the first song.")],
  [sg.Checkbox("Soul Voice",size=(15,1),font=font_choice,disabled=True,k="soulvoice",enable_events=True)],
]




rolls_list = ["Chaos", "Fighter's", "Hunter's", "Rogue's", "Samurai", "Wizard's"]
roll1 = "Chaos"
roll2 = "Samurai"
# COR buffs column
buffs_cor_column = [
  [sg.Checkbox("COR",size=(14,1),tooltip="Use Corsair buffs?",key="cor_on",default=False,enable_events=True,font=font_choice)],
  [sg.Combo(values=("Rolls +8","Rolls +7","Rolls +6","Rolls +5","Rolls +3","Rolls +0"), default_value="Rolls +7", readonly=True, k="nroll",size=(14,1),font=font_choice)],
  [sg.Combo(values=rolls_list + ["None"], default_value=roll1, readonly=True, k="roll1",size=(14,1),font=font_choice,enable_events=True)],
  [sg.Combo(values=rolls_list + ["None"], default_value=roll2, readonly=True, k="roll2",size=(14,1),font=font_choice,enable_events=True)],
  [sg.Checkbox("Light Shot",size=(14,1),font=font_choice,disabled=True,k="LIGHTSHOT")],
  [sg.Checkbox("Crooked\nCards*",size=(14,2),font=font_choice,disabled=True,k="Crooked Cards",tooltip="Crooked Cards applies to the first roll.")],
  [sg.Text("",font=font_choice)], # Blank line with the same font so that the formatting lines up with other buffs
  [sg.Text("",font=font_choice)], # Blank line with the same font so that the formatting lines up with other buffs

]

geo_spells = sorted(["Acumen", "Fury", "Precision", "Focus", "Haste", "STR", "DEX", "VIT", "AGI", "INT", "MND", "CHR", "Frailty", "Torpor", "Malaise"])
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
  [sg.Text("GEO potency: ",font=font_choice,tooltip="0 = -0% potency\n37 = -37% potency\n100 = -100% potency"),sg.Input("100",size=(4,1),pad=(1,1),font=font_choice,key="geomancy_potency",tooltip="0 = 0% potency\n37 = 37% potency\n100 = 100% potency")],

]

input_length = [5,1]
text_length = [15,1]
stat_length = [5,1]
bwidth = 1
nopad = [1,2]

default_enemy = "Apex Toad" # Just a default value so the fields are populated on start up.
enemy_stat_column = [
  [sg.Text("Enemy:", font=font_choice, size=[6,2],justification="r"), sg.Column([[sg.Combo(values=tuple(list(preset_enemies.keys())+["Custom"]), default_value=preset_enemies[default_enemy]["Name"], readonly=True, k="enemy_name", size=[20,1],font=font_choice,enable_events=True)],
  [sg.Text(f"({preset_enemies[default_enemy]['Location']})",font=font_choice,key="enemy_location")]])],
  [sg.Text("Level:",size=text_length,font=font_choice,justification="r",border_width=bwidth,pad=nopad),sg.Input(preset_enemies[default_enemy]["Level"],size=input_length,pad=nopad,border_width=bwidth,font=font_choice,key="enemy_level"),],
  [sg.Text("Evasion:",size=text_length,font=font_choice,justification="r",border_width=bwidth,pad=nopad),sg.Input(preset_enemies[default_enemy]["Evasion"],size=input_length,pad=nopad,border_width=bwidth,font=font_choice,key="enemy_evasion"),sg.Text("AGI:",size=stat_length,font=font_choice,justification="r",border_width=bwidth,pad=nopad),sg.Input(preset_enemies[default_enemy]["AGI"],size=input_length,pad=nopad,border_width=bwidth,font=font_choice,key="enemy_agi")],
  [sg.Text("Defense:",size=text_length,font=font_choice,justification="r",border_width=bwidth,pad=nopad),sg.Input(preset_enemies[default_enemy]["Defense"],size=input_length,pad=nopad,border_width=bwidth,font=font_choice,key="enemy_defense"),sg.Text("VIT:",size=stat_length,font=font_choice,justification="r",border_width=bwidth,pad=nopad),sg.Input(preset_enemies[default_enemy]["VIT"],size=input_length,pad=nopad,border_width=bwidth,font=font_choice,key="enemy_vit")],
  [sg.Text("Magic Defense:",size=text_length,font=font_choice,justification="r",border_width=bwidth,pad=nopad),sg.Input(preset_enemies[default_enemy]["Magic Defense"],size=input_length,pad=nopad,border_width=bwidth,font=font_choice,key="enemy_mdefense"), sg.Text("INT:",size=stat_length,font=font_choice,justification="r",border_width=bwidth,pad=nopad),sg.Input(preset_enemies[default_enemy]["INT"],size=input_length,pad=nopad,border_width=bwidth,font=font_choice,key="enemy_int")],
  [sg.Text("Magic Evasion:",size=text_length,font=font_choice,justification="r",border_width=bwidth,pad=nopad),sg.Input(preset_enemies[default_enemy]["Magic Evasion"],size=input_length,pad=nopad,border_width=bwidth,font=font_choice,key="enemy_mevasion")],
]








def item2image(item_name):
    #
    # Use base64 to convert image data
    #
    path32 = "icons32/"
    path64 = "icons64/"
    use_32x32_icons = False
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


items = np.loadtxt('item_list.txt',dtype=str, delimiter=";", unpack=True)


# Randomly select the initial gear set.
random_main = np.random.choice([k for k in mains if k["Skill Type"] in ["Katana"]])
random_sub = np.random.choice([k for k in subs if k["Skill Type"] in ["Katana","Dagger"]])
random_ammo = np.random.choice([k for k in ammos if "nin" in k["Jobs"]])
random_head = np.random.choice([k for k in heads if "nin" in k["Jobs"]])
random_body = np.random.choice([k for k in bodies if "nin" in k["Jobs"]])
random_hands = np.random.choice([k for k in hands if "nin" in k["Jobs"]])
random_legs = np.random.choice([k for k in legs if "nin" in k["Jobs"]])
random_feet = np.random.choice([k for k in feet if "nin" in k["Jobs"]])
random_neck = np.random.choice([k for k in necks if "nin" in k["Jobs"]])
random_waist = np.random.choice([k for k in waists if "nin" in k["Jobs"]])
random_ear1 = np.random.choice([k for k in ears if "nin" in k["Jobs"]])
random_ear2 = np.random.choice([k for k in ears2 if "nin" in k["Jobs"]])
random_ring1 = np.random.choice([k for k in rings if "nin" in k["Jobs"]])
random_ring2 = np.random.choice([k for k in rings2 if "nin" in k["Jobs"]])
random_back = np.random.choice([k for k in capes if "nin" in k["Jobs"]])


while random_sub["Name2"] == random_main["Name2"]:
    random_sub = np.random.choice([k for k in subs if k["Skill Type"] in ["Katana","Dagger"]])
while random_ring2["Name2"] == random_ring1["Name2"]:
    random_ring2 = np.random.choice(rings2)
while random_ear2["Name2"] == random_ear1["Name2"]:
    random_ear2 = np.random.choice(ears2)

starting_gearset = {
                    'main' : random_main,
                    'sub' : random_sub,
                    'ranged' : Empty,
                    'ammo' : random_ammo,
                    'head' : random_head,
                    'body' : random_body,
                    'hands' : random_hands,
                    'legs' : random_legs,
                    'feet' : random_feet,
                    'neck' : random_neck,
                    'waist' : random_waist,
                    'ear1' : random_ear1,
                    'ear2' : random_ear2,
                    'ring1' : random_ring1,
                    'ring2' : random_ring2,
                    'back' : random_back,
        }

# starting_gearset = {
#                     'main' : Hitaki,
#                     'sub' : Empty,
#                     'ranged' : Empty,
#                     'ammo' : Empty,
#                     'head' : Empty,
#                     'body' : Empty,
#                     'hands' : Empty,
#                     'legs' : Empty,
#                     'feet' : Empty,
#                     'neck' : Empty,
#                     'waist' : Empty,
#                     'ear1' : Empty,
#                     'ear2' : Empty,
#                     'ring1' : Empty,
#                     'ring2' : Empty,
#                     'back' : Empty,
#         }

# Define a dictionary containing slot:item_name pairs. The item_name is used to search item_list.txt for item IDs, which are then pulled from icons32/ and displayed in the GUI.
default_images = dict([[k,starting_gearset[k]["Name"]] for k in starting_gearset] )

def setup_radio_list(main_job):
    start_main,start_sub,start_ammo,start_head,start_neck,start_ear1,start_ear2,start_body,start_hands,start_ring1,start_ring2,start_back,start_waist,start_legs,start_feet = [[] for k in range(15)]

    main_names = [k['Name2'] if 'Name2' in k else k['Name'] for k in mains if main_job.lower() in k["Jobs"]]
    for k in sorted(main_names):
        start_main.append([sg.Radio(k,"main",font=font_choice,size=(50,1),key="startmain: "+k+";;"+main_job,enable_events=True)])

    sub_names = [k['Name2'] if 'Name2' in k else k['Name'] for k in subs+grips if main_job.lower() in k["Jobs"]]
    for k in sorted(sub_names):
        start_sub.append([sg.Radio(k,"sub",font=font_choice,size=(50,1),key="startsub: "+k+";;"+main_job,enable_events=True)])

    ammo_names = [k['Name2'] if 'Name2' in k else k['Name'] for k in ammos if main_job.lower() in k["Jobs"]]
    for k in sorted(ammo_names):
        start_ammo.append([sg.Radio(k,"ammo",font=font_choice,size=(50,1),key="startammo: "+k+";;"+main_job,enable_events=True)])

    head_names = [k['Name2'] if 'Name2' in k else k['Name'] for k in heads if main_job.lower() in k["Jobs"]]
    for k in sorted(head_names):
        start_head.append([sg.Radio(k,"head",font=font_choice,size=(50,1),key="starthead: "+k+";;"+main_job,enable_events=True)])

    neck_names = [k['Name2'] if 'Name2' in k else k['Name'] for k in necks if main_job.lower() in k["Jobs"]]
    for k in sorted(neck_names):
        start_neck.append([sg.Radio(k,"neck",font=font_choice,size=(50,1),key="startneck: "+k+";;"+main_job,enable_events=True)])

    ear1_names = [k['Name2'] if 'Name2' in k else k['Name'] for k in ears if main_job.lower() in k["Jobs"]]
    for k in sorted(ear1_names):
        start_ear1.append([sg.Radio(k,"ear1",font=font_choice,size=(50,1),key="startear1: "+k+";;"+main_job,enable_events=True)])

    ear2_names = [k['Name2'] if 'Name2' in k else k['Name'] for k in ears2 if main_job.lower() in k["Jobs"]]
    for k in sorted(ear2_names):
        start_ear2.append([sg.Radio(k,"ear2",font=font_choice,size=(50,1),key="startear2: "+k+";;"+main_job,enable_events=True)])

    body_names = [k['Name2'] if 'Name2' in k else k['Name'] for k in bodies if main_job.lower() in k["Jobs"]]
    for k in sorted(body_names):
        start_body.append([sg.Radio(k,"body",font=font_choice,size=(50,1),key="startbody: "+k+";;"+main_job,enable_events=True)])

    hands_names = [k['Name2'] if 'Name2' in k else k['Name'] for k in hands if main_job.lower() in k["Jobs"]]
    for k in sorted(hands_names):
        start_hands.append([sg.Radio(k,"hands",font=font_choice,size=(50,1),key="starthands: "+k+";;"+main_job,enable_events=True)])

    ring1_names = [k['Name2'] if 'Name2' in k else k['Name'] for k in rings if main_job.lower() in k["Jobs"]]
    for k in sorted(ring1_names):
        start_ring1.append([sg.Radio(k,"ring1",font=font_choice,size=(50,1),key="startring1: "+k+";;"+main_job,enable_events=True)])

    ring2_names = [k['Name2'] if 'Name2' in k else k['Name'] for k in rings2 if main_job.lower() in k["Jobs"]]
    for k in sorted(ring2_names):
        start_ring2.append([sg.Radio(k,"ring2",font=font_choice,size=(50,1),key="startring2: "+k+";;"+main_job,enable_events=True)])

    back_names = [k['Name2'] if 'Name2' in k else k['Name'] for k in capes if main_job.lower() in k["Jobs"]]
    for k in sorted(back_names):
        start_back.append([sg.Radio(k,"back",font=font_choice,size=(50,1),key="startback: "+k+";;"+main_job,enable_events=True)])

    waist_names = [k['Name2'] if 'Name2' in k else k['Name'] for k in waists if main_job.lower() in k["Jobs"]]
    for k in sorted(waist_names):
        start_waist.append([sg.Radio(k,"waist",font=font_choice,size=(50,1),key="startwaist: "+k+";;"+main_job,enable_events=True)])

    legs_names = [k['Name2'] if 'Name2' in k else k['Name'] for k in legs if main_job.lower() in k["Jobs"]]
    for k in sorted(legs_names):
        start_legs.append([sg.Radio(k,"legs",font=font_choice,size=(50,1),key="startlegs: "+k+";;"+main_job,enable_events=True)])

    feet_names = [k['Name2'] if 'Name2' in k else k['Name'] for k in feet if main_job.lower() in k["Jobs"]]
    for k in sorted(feet_names):
        start_feet.append([sg.Radio(k,"feet",font=font_choice,size=(50,1),key="startfeet: "+k+";;"+main_job,enable_events=True)])

    return(start_main, start_sub, start_ammo, start_head, start_neck, start_ear1, start_ear2, start_body, start_hands, start_ring1, start_ring2, start_back, start_waist, start_legs, start_feet)

# We can't dynamically update a radio button list with PySimpleGUI without destroying and recreating the window every time.
# We can, however, create a million frames, one for each situation, and simply hide the ones we don't want to show.
start_radio = {k:setup_radio_list(k) for k in main_jobs}
# start_radio = {
#     "NIN":setup_radio_list("NIN"),
#     "DRK":setup_radio_list("DRK"),}
start_main, start_sub, start_ammo, start_head, start_neck, start_ear1, start_ear2, start_body, start_hands, start_ring1, start_ring2, start_back, start_waist, start_legs, start_feet = setup_radio_list("DRK")
framesize = [300,300]

starting_set_tab = [
          [sg.Column([
            [sg.Button(image_data=item2image(default_images["main"]),font=font_choice,pad=(1,1),border_width=0,size=(1,1),key="showstart main",tooltip=starting_gearset["main"]["Name2"] if "Name2" in starting_gearset["main"] else starting_gearset["main"]["Name"]),
            sg.Button(image_data=item2image(default_images["sub"]),font=font_choice,pad=(1,1),border_width=0,size=(1,1),key="showstart sub",tooltip=starting_gearset["sub"]["Name2"] if "Name2" in starting_gearset["sub"] else starting_gearset["sub"]["Name"]),
            sg.Button(image_data=item2image(default_images["ranged"]),font=font_choice,pad=(1,1),border_width=0,size=(1,1),key="showstart ---",tooltip="Empty"),
            sg.Button(image_data=item2image(default_images["ammo"]),font=font_choice,pad=(1,1),border_width=0,size=(1,1),key="showstart ammo",tooltip=starting_gearset["ammo"]["Name2"] if "Name2" in starting_gearset["ammo"] else starting_gearset["ammo"]["Name"]),],
            [sg.Button(image_data=item2image(default_images["head"]),font=font_choice,pad=(1,1),border_width=0,size=(1,1),key="showstart head",tooltip=starting_gearset["head"]["Name2"] if "Name2" in starting_gearset["head"] else starting_gearset["head"]["Name"]),
            sg.Button(image_data=item2image(default_images["neck"]),font=font_choice,pad=(1,1),border_width=0,size=(1,1),key="showstart neck",tooltip=starting_gearset["neck"]["Name2"] if "Name2" in starting_gearset["neck"] else starting_gearset["neck"]["Name"]),
            sg.Button(image_data=item2image(default_images["ear1"]),font=font_choice,pad=(1,1),border_width=0,size=(1,1),key="showstart ear1",tooltip=starting_gearset["ear1"]["Name2"] if "Name2" in starting_gearset["ear1"] else starting_gearset["ear1"]["Name"]),
            sg.Button(image_data=item2image(default_images["ear2"]),font=font_choice,pad=(1,1),border_width=0,size=(1,1),key="showstart ear2",tooltip=starting_gearset["ear2"]["Name2"] if "Name2" in starting_gearset["ear2"] else starting_gearset["ear2"]["Name"]),],
            [sg.Button(image_data=item2image(default_images["body"]),font=font_choice,pad=(1,1),border_width=0,size=(1,1),key="showstart body",tooltip=starting_gearset["body"]["Name2"] if "Name2" in starting_gearset["body"] else starting_gearset["body"]["Name"]),
            sg.Button(image_data=item2image(default_images["hands"]),font=font_choice,pad=(1,1),border_width=0,size=(1,1),key="showstart hands",tooltip=starting_gearset["hands"]["Name2"] if "Name2" in starting_gearset["hands"] else starting_gearset["hands"]["Name"]),
            sg.Button(image_data=item2image(default_images["ring1"]),font=font_choice,pad=(1,1),border_width=0,size=(1,1),key="showstart ring1",tooltip=starting_gearset["ring1"]["Name2"] if "Name2" in starting_gearset["ring1"] else starting_gearset["ring1"]["Name"]),
            sg.Button(image_data=item2image(default_images["ring2"]),font=font_choice,pad=(1,1),border_width=0,size=(1,1),key="showstart ring2",tooltip=starting_gearset["ring2"]["Name2"] if "Name2" in starting_gearset["ring2"] else starting_gearset["ring2"]["Name"]),],
            [sg.Button(image_data=item2image(default_images["back"]),font=font_choice,pad=(1,1),border_width=0,size=(1,1),key="showstart back",tooltip=starting_gearset["back"]["Name2"] if "Name2" in starting_gearset["back"] else starting_gearset["back"]["Name"]),
            sg.Button(image_data=item2image(default_images["waist"]),font=font_choice,pad=(1,1),border_width=0,size=(1,1),key="showstart waist",tooltip=starting_gearset["waist"]["Name2"] if "Name2" in starting_gearset["waist"] else starting_gearset["waist"]["Name"]),
            sg.Button(image_data=item2image(default_images["legs"]),font=font_choice,pad=(1,1),border_width=0,size=(1,1),key="showstart legs",tooltip=starting_gearset["legs"]["Name2"] if "Name2" in starting_gearset["legs"] else starting_gearset["legs"]["Name"]),
            sg.Button(image_data=item2image(default_images["feet"]),font=font_choice,pad=(1,1),border_width=0,size=(1,1),key="showstart feet",tooltip=starting_gearset["feet"]["Name2"] if "Name2" in starting_gearset["feet"] else starting_gearset["feet"]["Name"]),],
          ]),]]

# radio_tab = [
#           sg.Frame("Select starting main-hand", [[sg.Column(start_radio["NIN"][0],size=framesize,scrollable=True,vertical_scroll_only=True)]],font=font_choice,visible=True,key="main start radio NIN"),
#           sg.Frame("Select starting off-hand",  [[sg.Column(start_radio["NIN"][1],size=framesize,scrollable=True,vertical_scroll_only=True)]],font=font_choice,visible=False,key="sub start radio NIN"),
#           sg.Frame("Select starting ammo", [[sg.Column(start_radio["NIN"][2],size=framesize,scrollable=True,vertical_scroll_only=True)]],font=font_choice,visible=False,key="ammo start radio NIN"),
#           sg.Frame("Select starting head", [[sg.Column(start_radio["NIN"][3],size=framesize,scrollable=True,vertical_scroll_only=True)]],font=font_choice,visible=False,key="head start radio NIN"),
#           sg.Frame("Select starting neck", [[sg.Column(start_radio["NIN"][4],size=framesize,scrollable=True,vertical_scroll_only=True)]],font=font_choice,visible=False,key="neck start radio NIN"),
#           sg.Frame("Select starting left ear", [[sg.Column(start_radio["NIN"][5],size=framesize,scrollable=True,vertical_scroll_only=True)]],font=font_choice,visible=False,key="ear1 start radio NIN"),
#           sg.Frame("Select starting ring ear", [[sg.Column(start_radio["NIN"][6],size=framesize,scrollable=True,vertical_scroll_only=True)]],font=font_choice,visible=False,key="ear2 start radio NIN"),
#           sg.Frame("Select starting body", [[sg.Column(start_radio["NIN"][7],size=framesize,scrollable=True,vertical_scroll_only=True)]],font=font_choice,visible=False,key="body start radio NIN"),
#           sg.Frame("Select starting hands", [[sg.Column(start_radio["NIN"][8],size=framesize,scrollable=True,vertical_scroll_only=True)]],font=font_choice,visible=False,key="hands start radio NIN"),
#           sg.Frame("Select starting left ring", [[sg.Column(start_radio["NIN"][9],size=framesize,scrollable=True,vertical_scroll_only=True)]],font=font_choice,visible=False,key="ring1 start radio NIN"),
#           sg.Frame("Select starting right ring", [[sg.Column(start_radio["NIN"][10],size=framesize,scrollable=True,vertical_scroll_only=True)]],font=font_choice,visible=False,key="ring2 start radio NIN"),
#           sg.Frame("Select starting back", [[sg.Column(start_radio["NIN"][11],size=framesize,scrollable=True,vertical_scroll_only=True)]],font=font_choice,visible=False,key="back start radio NIN"),
#           sg.Frame("Select starting waist", [[sg.Column(start_radio["NIN"][12],size=framesize,scrollable=True,vertical_scroll_only=True)]],font=font_choice,visible=False,key="waist start radio NIN"),
#           sg.Frame("Select starting legs", [[sg.Column(start_radio["NIN"][13],size=framesize,scrollable=True,vertical_scroll_only=True)]],font=font_choice,visible=False,key="legs start radio NIN"),
#           sg.Frame("Select starting feet", [[sg.Column(start_radio["NIN"][14],size=framesize,scrollable=True,vertical_scroll_only=True)]],font=font_choice,visible=False,key="feet start radio NIN"),

#           sg.Frame("Select starting main-hand", [[sg.Column(start_radio["DRK"][0],size=framesize,scrollable=True,vertical_scroll_only=True)]],font=font_choice,visible=False,key="main start radio DRK"),
#           sg.Frame("Select starting off-hand",  [[sg.Column(start_radio["DRK"][1],size=framesize,scrollable=True,vertical_scroll_only=True)]],font=font_choice,visible=False,key="sub start radio DRK"),
#           sg.Frame("Select starting ammo", [[sg.Column(start_radio["DRK"][2],size=framesize,scrollable=True,vertical_scroll_only=True)]],font=font_choice,visible=False,key="ammo start radio DRK"),
#           sg.Frame("Select starting head", [[sg.Column(start_radio["DRK"][3],size=framesize,scrollable=True,vertical_scroll_only=True)]],font=font_choice,visible=False,key="head start radio DRK"),
#           sg.Frame("Select starting neck", [[sg.Column(start_radio["DRK"][4],size=framesize,scrollable=True,vertical_scroll_only=True)]],font=font_choice,visible=False,key="neck start radio DRK"),
#           sg.Frame("Select starting left ear", [[sg.Column(start_radio["DRK"][5],size=framesize,scrollable=True,vertical_scroll_only=True)]],font=font_choice,visible=False,key="ear1 start radio DRK"),
#           sg.Frame("Select starting ring ear", [[sg.Column(start_radio["DRK"][6],size=framesize,scrollable=True,vertical_scroll_only=True)]],font=font_choice,visible=False,key="ear2 start radio DRK"),
#           sg.Frame("Select starting body", [[sg.Column(start_radio["DRK"][7],size=framesize,scrollable=True,vertical_scroll_only=True)]],font=font_choice,visible=False,key="body start radio DRK"),
#           sg.Frame("Select starting hands", [[sg.Column(start_radio["DRK"][8],size=framesize,scrollable=True,vertical_scroll_only=True)]],font=font_choice,visible=False,key="hands start radio DRK"),
#           sg.Frame("Select starting left ring", [[sg.Column(start_radio["DRK"][9],size=framesize,scrollable=True,vertical_scroll_only=True)]],font=font_choice,visible=False,key="ring1 start radio DRK"),
#           sg.Frame("Select starting right ring", [[sg.Column(start_radio["DRK"][10],size=framesize,scrollable=True,vertical_scroll_only=True)]],font=font_choice,visible=False,key="ring2 start radio DRK"),
#           sg.Frame("Select starting back", [[sg.Column(start_radio["DRK"][11],size=framesize,scrollable=True,vertical_scroll_only=True)]],font=font_choice,visible=False,key="back start radio DRK"),
#           sg.Frame("Select starting waist", [[sg.Column(start_radio["DRK"][12],size=framesize,scrollable=True,vertical_scroll_only=True)]],font=font_choice,visible=False,key="waist start radio DRK"),
#           sg.Frame("Select starting legs", [[sg.Column(start_radio["DRK"][13],size=framesize,scrollable=True,vertical_scroll_only=True)]],font=font_choice,visible=False,key="legs start radio DRK"),
#           sg.Frame("Select starting feet", [[sg.Column(start_radio["DRK"][14],size=framesize,scrollable=True,vertical_scroll_only=True)]],font=font_choice,visible=False,key="feet start radio DRK"),
#          ]

# The above commented block can be reduced to the following two lines to cover all slots and all jobs at once.
# The first element is printed on screen. The 2nd element is used by the code to organize things.
# Allowing a dynamic radio list required a lot of changes. If things appear unreasonably broken, then simply download the Github versions from 2022 December 03 titled " Better output tab. " which are the save state before this big change.
radio_slots = [["main-hand","main"], ["off-hand","sub"], ["ammo","ammo"], ["head","head"], ["neck","neck"], ["left ear","ear1"], ["right ear","ear2"], ["body","body"], ["hands","hands"], ["left ring","ring1"], ["right ring","ring2"], ["back","back"], ["waist","waist"], ["legs","legs"], ["feet","feet"]]
radio_tab = [sg.Frame(f"Select starting {l[0]}", [[sg.Column(start_radio[k][m],size=framesize,scrollable=True,vertical_scroll_only=True)]],font=font_choice,visible=True if k=="NIN" and l[1]=="main" else False,key=f"{l[1]} start radio {k}") for k in main_jobs for m,l in enumerate(radio_slots)]
#radio_tab = [sg.Frame(f"Select starting {l[0]}", [[sg.Column(start_radio[k][m],size=framesize,scrollable=True,vertical_scroll_only=True)]],font=font_choice,visible=False,key=f"{l[1]} start radio {k}") for k in main_jobs for m,l in enumerate(radio_slots)]

# k = main_job
# l = [used in the frame header display, used in the code for organization]
# m = 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14 (slot index)










input_tab = [
          [sg.vtop(sg.Frame("Basic inputs",[[sg.vtop(sg.Column(player_column,))],[sg.Column(ws_column2)]],size=[350,220])),sg.Push(),sg.vtop(sg.Frame("Enemy inputs",[[sg.Column(enemy_stat_column)]],))],
          [sg.Push(),sg.vtop(sg.Frame("Buffs", [[sg.vtop(sg.Column(buffs_whm_column,)), sg.vtop(sg.Column(buffs_brd_column,)), sg.vtop(sg.Column(buffs_cor_column,)), sg.vtop(sg.Column(buffs_geo_column,))]])),sg.Push()],
          [sg.Push(),sg.vtop(sg.Frame("Initial gearset",[[sg.Push(),sg.vcenter(sg.Column([[sg.Column(starting_set_tab)],[sg.Button("Quick-look WS",key="quicklook"),sg.Button("Quick-look Magic",key="quicklook magic", disabled=False)],
          [sg.Push(),sg.Button("Quick-look TP",key="quicklook TP",disabled=True),sg.Button("Calculate Stats",key="get stats", disabled=False),sg.Push()],
          [sg.Text(f"{'Average =':>10s} ------ damage",key="quickaverage",font=font_choice)]])),sg.Push(),sg.Column([radio_tab])],],size=[800,350])),sg.Push()]
          # [sg.vtop(sg.Frame("Initial gearset",[[sg.Column([[sg.Column(starting_set_tab)],[sg.Button("test")]]),sg.Column([radio_tab])],],size=[600,275]))]
         ]
