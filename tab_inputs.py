#
# Created by Kastra on Asura.
# Feel free to /tell in game or send a PM on FFXIAH you have questions, comments, or suggestions.
#
# Version date: 2022 November 15
#
# This file contains a the GUI tab "Inputs".
#
import PySimpleGUI as sg
import numpy as np # Just to randomly choose the starting gear set
import os

font_choice = "Courier 12"

main_jobs = ["NIN", "DRK"]
sub_jobs = ["WAR", "SAM"]

player_column = [
  [sg.Text("Main Job:",size=(10,1),font=font_choice), sg.Combo(values=main_jobs, default_value=main_jobs[0], readonly=True, key="mainjob",size=(10,1),font=font_choice,tooltip="Select main job.",disabled=True)],
  [sg.Text("Sub Job:",size=(10,1),font=font_choice), sg.Combo(values=sub_jobs, default_value=sub_jobs[0], readonly=True, key="subjob",size=(10,1),font=font_choice,tooltip="Select sub job.",disabled=True)],
]

ws_list = sorted(
           ["Blade: Chi", "Blade: Hi", "Blade: Kamu", "Blade: Metsu", "Blade: Shun", "Blade: Ten", "Blade: Ku",
           "Tachi: Rana", "Tachi: Fudo", "Tachi: Kaiten", "Tachi: Shoha", "Tachi: Kasha", "Tachi: Gekko", "Tachi: Jinpu",
           "Evisceration",
           "Savage Blade",
           "Insurgency", "Cross Reaper", "Entropy", "Quietus", "Catastrophe"])

ws_column = [ # Copy pasted out of player_column for now.
  [sg.Text("Weapon skill:",size=(14,1),font=font_choice,justification="r",key="ws label")],[sg.Combo(values=ws_list, default_value="Blade: Shun", readonly=True, k="select weaponskill",font=font_choice,enable_events=True)],
  [sg.Text("Min.TP:",font=font_choice,key="minTP label"), sg.Input("1500",key="mintp",size=(5,1),font=font_choice,tooltip="Lower limit for weapon skill TP.")],
  [sg.Text("Max.TP:",font=font_choice,key="maxTP label"), sg.Input("1800",key="maxtp",size=(5,1),font=font_choice,tooltip="Upper limit for weapon skill TP.")]
]

from gear import all_food
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
  [sg.Text("GEO nerf: ",font=font_choice,tooltip="0 = -0% potency\n37 = -37% potency\n100 = -100% potency"),sg.Input("0",size=(3,1),pad=(1,1),font=font_choice,key="geomancy_nerf",tooltip="0 = -0% potency\n37 = -37% potency\n100 = -100% potency")],

]

input_length = [5,1]
text_length = [15,1]
stat_length = [5,1]
bwidth = 1
nopad = [1,2]
from enemies import *
default_enemy = "Apex Toad" # Just a default value so the fields are populated on start up.
enemy_stat_column = [
  [sg.Text("Enemy:", font=font_choice, size=[6,2],justification="r"), sg.Column([[sg.Combo(values=tuple(list(preset_enemies.keys())+["Custom"]), default_value=preset_enemies[default_enemy]["Name"], readonly=True, k="enemy_name", size=[20,1],font=font_choice,enable_events=True)],
  [sg.Text(f"({preset_enemies[default_enemy]['Location']})",font=font_choice,key="enemy_location")]])],
  [sg.Text("Level:",size=text_length,font=font_choice,justification="r",border_width=bwidth,pad=nopad),sg.Input(preset_enemies[default_enemy]["Level"],size=input_length,pad=nopad,border_width=bwidth,font=font_choice,key="enemy_level"),],
  [sg.Text("Evasion:",size=text_length,font=font_choice,justification="r",border_width=bwidth,pad=nopad),sg.Input(preset_enemies[default_enemy]["Evasion"],size=input_length,pad=nopad,border_width=bwidth,font=font_choice,key="enemy_evasion"),sg.Text("AGI:",size=stat_length,font=font_choice,justification="r",border_width=bwidth,pad=nopad),sg.Input(preset_enemies[default_enemy]["AGI"],size=input_length,pad=nopad,border_width=bwidth,font=font_choice,key="enemy_agi")],
  [sg.Text("Defense:",size=text_length,font=font_choice,justification="r",border_width=bwidth,pad=nopad),sg.Input(preset_enemies[default_enemy]["Defense"],size=input_length,pad=nopad,border_width=bwidth,font=font_choice,key="enemy_defense"),sg.Text("VIT:",size=stat_length,font=font_choice,justification="r",border_width=bwidth,pad=nopad),sg.Input(preset_enemies[default_enemy]["VIT"],size=input_length,pad=nopad,border_width=bwidth,font=font_choice,key="enemy_vit")],
  [sg.Text("Magic Defense:",size=text_length,font=font_choice,justification="r",border_width=bwidth,pad=nopad),sg.Input(preset_enemies[default_enemy]["Magic Defense"],size=input_length,pad=nopad,border_width=bwidth,font=font_choice,key="enemy_mdefense"), sg.Text("INT:",size=stat_length,font=font_choice,justification="r",border_width=bwidth,pad=nopad),sg.Input(preset_enemies[default_enemy]["INT"],size=input_length,pad=nopad,border_width=bwidth,font=font_choice,key="enemy_int")],
]













import PySimpleGUI as sg
from gear import *
import numpy as np
import base64
from PIL import Image

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


font_choice = "Courier 12"

items = np.loadtxt('item_list.txt',dtype=str, delimiter=";", unpack=True)


# Randomly select the initial gear set.
random_main = np.random.choice([k for k in mains if k["Skill Type"] in ["Katana"]])
random_sub = np.random.choice([k for k in subs if k["Skill Type"] in ["Katana","Dagger"]])
random_ammo = np.random.choice(ammos)
random_head = np.random.choice(heads)
random_body = np.random.choice(bodies)
random_hands = np.random.choice(hands)
random_legs = np.random.choice(legs)
random_feet = np.random.choice(feet)
random_neck = np.random.choice(necks)
random_waist = np.random.choice(waists)
random_ear1 = np.random.choice(ears)
random_ear2 = np.random.choice(ears2)
random_ring1 = np.random.choice(rings)
random_ring2 = np.random.choice(rings2)
random_back = np.random.choice(capes)


while random_sub["Name2"] == random_main["Name2"]:
    random_sub = np.random.choice([k for k in mains if k["Skill Type"] in ["Katana","Dagger"]]),
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

# Define a dictionary containing slot:item_name pairs. The item_name is used to search item_list.txt for item IDs, which are then pulled from icons32/ and displayed in the GUI.
default_images = dict([[k,starting_gearset[k]["Name"]] for k in starting_gearset] )

start_main,start_sub,start_ammo,start_head,start_neck,start_ear1,start_ear2,start_body,start_hands,start_ring1,start_ring2,start_back,start_waist,start_legs,start_feet = [[] for k in range(15)]

main_names = [k['Name2'] if 'Name2' in k else k['Name'] for k in mains]
for k in sorted(main_names):
    start_main.append([sg.Radio(k,"main",font=font_choice,size=(50,1),key="startmain: "+k,enable_events=True)])

sub_names = [k['Name2'] if 'Name2' in k else k['Name'] for k in subs+grips]
for k in sorted(sub_names):
    start_sub.append([sg.Radio(k,"sub",font=font_choice,size=(50,1),key="startsub: "+k,enable_events=True)])

ammo_names = [k['Name2'] if 'Name2' in k else k['Name'] for k in ammos]
for k in sorted(ammo_names):
    start_ammo.append([sg.Radio(k,"ammo",font=font_choice,size=(50,1),key="startammo: "+k,enable_events=True)])

head_names = [k['Name2'] if 'Name2' in k else k['Name'] for k in heads]
for k in sorted(head_names):
    start_head.append([sg.Radio(k,"head",font=font_choice,size=(50,1),key="starthead: "+k,enable_events=True)])

neck_names = [k['Name2'] if 'Name2' in k else k['Name'] for k in necks]
for k in sorted(neck_names):
    start_neck.append([sg.Radio(k,"neck",font=font_choice,size=(50,1),key="startneck: "+k,enable_events=True)])

ear1_names = [k['Name2'] if 'Name2' in k else k['Name'] for k in ears]
for k in sorted(ear1_names):
    start_ear1.append([sg.Radio(k,"ear1",font=font_choice,size=(50,1),key="startear1: "+k,enable_events=True)])

ear2_names = [k['Name2'] if 'Name2' in k else k['Name'] for k in ears2]
for k in sorted(ear2_names):
    start_ear2.append([sg.Radio(k,"ear2",font=font_choice,size=(50,1),key="startear2: "+k,enable_events=True)])

body_names = [k['Name2'] if 'Name2' in k else k['Name'] for k in bodies]
for k in sorted(body_names):
    start_body.append([sg.Radio(k,"body",font=font_choice,size=(50,1),key="startbody: "+k,enable_events=True)])

hands_names = [k['Name2'] if 'Name2' in k else k['Name'] for k in hands]
for k in sorted(hands_names):
    start_hands.append([sg.Radio(k,"hands",font=font_choice,size=(50,1),key="starthands: "+k,enable_events=True)])

ring1_names = [k['Name2'] if 'Name2' in k else k['Name'] for k in rings]
for k in sorted(ring1_names):
    start_ring1.append([sg.Radio(k,"ring1",font=font_choice,size=(50,1),key="startring1: "+k,enable_events=True)])

ring2_names = [k['Name2'] if 'Name2' in k else k['Name'] for k in rings2]
for k in sorted(ring2_names):
    start_ring2.append([sg.Radio(k,"ring2",font=font_choice,size=(50,1),key="startring2: "+k,enable_events=True)])

back_names = [k['Name2'] if 'Name2' in k else k['Name'] for k in capes]
for k in sorted(back_names):
    start_back.append([sg.Radio(k,"back",font=font_choice,size=(50,1),key="startback: "+k,enable_events=True)])

waist_names = [k['Name2'] if 'Name2' in k else k['Name'] for k in waists]
for k in sorted(waist_names):
    start_waist.append([sg.Radio(k,"waist",font=font_choice,size=(50,1),key="startwaist: "+k,enable_events=True)])

legs_names = [k['Name2'] if 'Name2' in k else k['Name'] for k in legs]
for k in sorted(legs_names):
    start_legs.append([sg.Radio(k,"legs",font=font_choice,size=(50,1),key="startlegs: "+k,enable_events=True)])

feet_names = [k['Name2'] if 'Name2' in k else k['Name'] for k in feet]
for k in sorted(feet_names):
    start_feet.append([sg.Radio(k,"feet",font=font_choice,size=(50,1),key="startfeet: "+k,enable_events=True)])

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
radio_tab = [
          sg.Frame("Select starting main-hand", [[sg.Column(start_main,size=framesize,scrollable=True,vertical_scroll_only=True)]],font=font_choice,visible=True,key="main start radio"),
          sg.Frame("Select starting off-hand",  [[sg.Column(start_sub,size=framesize,scrollable=True,vertical_scroll_only=True)]],font=font_choice,visible=False,key="sub start radio"),
          sg.Frame("Select starting ammo", [[sg.Column(start_ammo,size=framesize,scrollable=True,vertical_scroll_only=True)]],font=font_choice,visible=False,key="ammo start radio"),
          sg.Frame("Select starting head", [[sg.Column(start_head,size=framesize,scrollable=True,vertical_scroll_only=True)]],font=font_choice,visible=False,key="head start radio"),
          sg.Frame("Select starting neck", [[sg.Column(start_neck,size=framesize,scrollable=True,vertical_scroll_only=True)]],font=font_choice,visible=False,key="neck start radio"),
          sg.Frame("Select starting left ear", [[sg.Column(start_ear1,size=framesize,scrollable=True,vertical_scroll_only=True)]],font=font_choice,visible=False,key="ear1 start radio"),
          sg.Frame("Select starting ring ear", [[sg.Column(start_ear2,size=framesize,scrollable=True,vertical_scroll_only=True)]],font=font_choice,visible=False,key="ear2 start radio"),
          sg.Frame("Select starting body", [[sg.Column(start_body,size=framesize,scrollable=True,vertical_scroll_only=True)]],font=font_choice,visible=False,key="body start radio"),
          sg.Frame("Select starting hands", [[sg.Column(start_hands,size=framesize,scrollable=True,vertical_scroll_only=True)]],font=font_choice,visible=False,key="hands start radio"),
          sg.Frame("Select starting left ring", [[sg.Column(start_ring1,size=framesize,scrollable=True,vertical_scroll_only=True)]],font=font_choice,visible=False,key="ring1 start radio"),
          sg.Frame("Select starting right ring", [[sg.Column(start_ring2,size=framesize,scrollable=True,vertical_scroll_only=True)]],font=font_choice,visible=False,key="ring2 start radio"),
          sg.Frame("Select starting back", [[sg.Column(start_back,size=framesize,scrollable=True,vertical_scroll_only=True)]],font=font_choice,visible=False,key="back start radio"),
          sg.Frame("Select starting waist", [[sg.Column(start_waist,size=framesize,scrollable=True,vertical_scroll_only=True)]],font=font_choice,visible=False,key="waist start radio"),
          sg.Frame("Select starting legs", [[sg.Column(start_legs,size=framesize,scrollable=True,vertical_scroll_only=True)]],font=font_choice,visible=False,key="legs start radio"),
          sg.Frame("Select starting feet", [[sg.Column(start_feet,size=framesize,scrollable=True,vertical_scroll_only=True)]],font=font_choice,visible=False,key="feet start radio"),
         ]













input_tab = [
          [sg.vtop(sg.Frame("Basic inputs",[[sg.vtop(sg.Column(player_column))],[sg.Column(ws_column)]],size=[250,200])),sg.Push(),sg.vtop(sg.Frame("Enemy inputs",[[sg.Column(enemy_stat_column)]],))],
          [sg.vtop(sg.Frame("Buffs", [[sg.vtop(sg.Column(buffs_whm_column,)), sg.vtop(sg.Column(buffs_brd_column,)), sg.vtop(sg.Column(buffs_cor_column,)), sg.vtop(sg.Column(buffs_geo_column,))]]))],
          [sg.vtop(sg.Frame("Initial gearset",[[sg.Push(),sg.vcenter(sg.Column([[sg.Column(starting_set_tab)],[sg.Button("Quick-look",key="quicklook")],[sg.Text(f"{'Average =':>10s} ------ damage",key="quickaverage",font=font_choice)]])),sg.Push(),sg.Column([radio_tab])],],size=[800,350]))]
          # [sg.vtop(sg.Frame("Initial gearset",[[sg.Column([[sg.Column(starting_set_tab)],[sg.Button("test")]]),sg.Column([radio_tab])],],size=[600,275]))]
         ]
