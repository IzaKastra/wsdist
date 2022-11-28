#
# Created by Kastra on Asura.
# Feel free to /tell in game or send a PM on FFXIAH you have questions, comments, or suggestions.
#
# Version date: 2022 November 15
#
# This file contains a the GUI tab "Select Gear".
#
import PySimpleGUI as sg
from gear import *
sg.Window.get_screen_size() # https://github.com/PySimpleGUI/PySimpleGUI/issues/1996
w, h = sg.Window.get_screen_size()


fontsize = 9
font_choice = ["Cascadia Mono", fontsize]

# --------------------------------------------------------------------------------
# Create the full list of checkboxes for each of 15 gear slots. Lots of hard-coding for now...
gear_main,gear_sub,gear_ammo,gear_head,gear_neck,gear_ear1,gear_ear2,gear_body,gear_hands,gear_ring1,gear_ring2,gear_back,gear_waist,gear_legs,gear_feet = [[] for k in range(15)]

all_gear = mains+subs+grips+ammos+heads+necks+ears+ears2+bodies+hands+rings+rings2+capes+waists+legs+feet
all_names_map = dict([[k['Name2'] if 'Name2' in k else k['Name'], k['Name']] for k in all_gear]) # Dictionary that maps name2s to names for images later. We can't find an image for "Heishi Shorinken R15" so map it to "Heishi Shoriken" here


main_names = [k['Name2'] if 'Name2' in k else k['Name'] for k in mains]
for k in sorted(main_names):
    gear_main.append([sg.Checkbox(k,font=font_choice,size=(50,1),key="main: "+k,enable_events=True)])

sub_names = [k['Name2'] if 'Name2' in k else k['Name'] for k in subs+grips]
sub_names2 = dict([[k['Name2'] if 'Name2' in k else k['Name'], k['Name']] for k in subs+grips]) # Dictionary that maps name2s to names for images later. We can't find an image for "Heishi Shorinken R15" so map it to "Heishi Shoriken" here
for k in sorted(sub_names):
    gear_sub.append([sg.Checkbox(k,font=font_choice,size=(50,1),key="sub: "+k,enable_events=True)])

ammo_names = [k['Name2'] if 'Name2' in k else k['Name'] for k in ammos]
ammo_names2 = dict([[k['Name2'] if 'Name2' in k else k['Name'], k['Name']] for k in ammos]) # Dictionary that maps name2s to names for images later. We can't find an image for "Heishi Shorinken R15" so map it to "Heishi Shoriken" here
for k in sorted(ammo_names):
    gear_ammo.append([sg.Checkbox(k,font=font_choice,size=(50,1),key="ammo: "+k,enable_events=True)])

head_names = [k['Name2'] if 'Name2' in k else k['Name'] for k in heads]
head_names2 = dict([[k['Name2'] if 'Name2' in k else k['Name'], k['Name']] for k in heads]) # Dictionary that maps name2s to names for images later. We can't find an image for "Heishi Shorinken R15" so map it to "Heishi Shoriken" here
for k in sorted(head_names):
    gear_head.append([sg.Checkbox(k,font=font_choice,size=(50,1),key="head: "+k,enable_events=True)])

neck_names = [k['Name2'] if 'Name2' in k else k['Name'] for k in necks]
neck_names2 = dict([[k['Name2'] if 'Name2' in k else k['Name'], k['Name']] for k in necks])
for k in sorted(neck_names):
    gear_neck.append([sg.Checkbox(k,font=font_choice,size=(50,1),key="neck: "+k,enable_events=True)])

ear1_names = [k['Name2'] if 'Name2' in k else k['Name'] for k in ears]
ear1_names2 = dict([[k['Name2'] if 'Name2' in k else k['Name'], k['Name']] for k in ears])
for k in sorted(ear1_names):
    gear_ear1.append([sg.Checkbox(k,font=font_choice,size=(50,1),key="ear1: "+k,enable_events=True)])

ear2_names = [k['Name2'] if 'Name2' in k else k['Name'] for k in ears2]
ear2_names2 = dict([[k['Name2'] if 'Name2' in k else k['Name'], k['Name']] for k in ears2])
for k in sorted(ear2_names):
    gear_ear2.append([sg.Checkbox(k,font=font_choice,size=(50,1),key="ear2: "+k,enable_events=True)])

body_names = [k['Name2'] if 'Name2' in k else k['Name'] for k in bodies]
body_names2 = dict([[k['Name2'] if 'Name2' in k else k['Name'], k['Name']] for k in bodies])
for k in sorted(body_names):
    gear_body.append([sg.Checkbox(k,font=font_choice,size=(50,1),key="body: "+k,enable_events=True)])

hands_names = [k['Name2'] if 'Name2' in k else k['Name'] for k in hands]
hands_names2 = dict([[k['Name2'] if 'Name2' in k else k['Name'], k['Name']] for k in hands])
for k in sorted(hands_names):
    gear_hands.append([sg.Checkbox(k,font=font_choice,size=(50,1),key="hands: "+k,enable_events=True)])

ring1_names = [k['Name2'] if 'Name2' in k else k['Name'] for k in rings]
ring1_names2 = dict([[k['Name2'] if 'Name2' in k else k['Name'], k['Name']] for k in rings])
for k in sorted(ring1_names):
    gear_ring1.append([sg.Checkbox(k,font=font_choice,size=(50,1),key="ring1: "+k,enable_events=True)])

ring2_names = [k['Name2'] if 'Name2' in k else k['Name'] for k in rings2]
ring2_names2 = dict([[k['Name2'] if 'Name2' in k else k['Name'], k['Name']] for k in rings2])
for k in sorted(ring2_names):
    gear_ring2.append([sg.Checkbox(k,font=font_choice,size=(50,1),key="ring2: "+k,enable_events=True)])

back_names = [k['Name2'] if 'Name2' in k else k['Name'] for k in capes]
back_names2 = dict([[k['Name2'] if 'Name2' in k else k['Name'], k['Name']] for k in capes])
for k in sorted(back_names):
    gear_back.append([sg.Checkbox(k,font=font_choice,size=(50,1),key="back: "+k,enable_events=True)])

waist_names = [k['Name2'] if 'Name2' in k else k['Name'] for k in waists]
waist_names2 = dict([[k['Name2'] if 'Name2' in k else k['Name'], k['Name']] for k in waists])
for k in sorted(waist_names):
    gear_waist.append([sg.Checkbox(k,font=font_choice,size=(50,1),key="waist: "+k,enable_events=True)])

legs_names = [k['Name2'] if 'Name2' in k else k['Name'] for k in legs]
legs_names2 = dict([[k['Name2'] if 'Name2' in k else k['Name'], k['Name']] for k in legs])
for k in sorted(legs_names):
    gear_legs.append([sg.Checkbox(k,font=font_choice,size=(50,1),key="legs: "+k,enable_events=True)])

feet_names = [k['Name2'] if 'Name2' in k else k['Name'] for k in feet]
feet_names2 = dict([[k['Name2'] if 'Name2' in k else k['Name'], k['Name']] for k in feet])
for k in sorted(feet_names):
    gear_feet.append([sg.Checkbox(k,font=font_choice,size=(50,1),key="feet: "+k,enable_events=True)])

from tab_inputs import item2image
framesize = [400,450]
# sg.Push()
# https://stackoverflow.com/questions/68929799/pysimplegui-right-justify-a-button-in-a-frame
gear_tab = [
  [sg.Column([
    [sg.Push(),sg.Button("Main",image_data=item2image("Empty"),font=font_choice,pad=(0,0),border_width=1,size=(7,1),key="display main"),sg.Button("Sub",image_data=item2image("Empty"),font=font_choice,pad=(0,0),border_width=1,size=(7,1),key="display sub"),sg.Button("---",image_data=item2image("Empty"),font=font_choice,pad=(0,0),border_width=1,size=(7,1),key="display ---"),sg.Button("Ammo",image_data=item2image("Empty"),font=font_choice,pad=(0,0),border_width=1,size=(7,1),key="display ammo"),sg.Push()],
    [sg.Push(),sg.Button("Head",image_data=item2image("Empty"),font=font_choice,pad=(0,0),border_width=1,size=(7,1),key="display head"),sg.Button("Neck",image_data=item2image("Empty"),font=font_choice,pad=(0,0),border_width=1,size=(7,1),key="display neck"),sg.Button("Ear1",image_data=item2image("Empty"),font=font_choice,pad=(0,0),border_width=1,size=(7,1),key="display ear1"),sg.Button("Ear2",image_data=item2image("Empty"),font=font_choice,pad=(0,0),border_width=1,size=(7,1),key="display ear2"),sg.Push()],
    [sg.Push(),sg.Button("Body",image_data=item2image("Empty"),font=font_choice,pad=(0,0),border_width=1,size=(7,1),key="display body"),sg.Button("Hands",image_data=item2image("Empty"),font=font_choice,pad=(0,0),border_width=1,size=(7,1),key="display hands"),sg.Button("Ring1",image_data=item2image("Empty"),font=font_choice,pad=(0,0),border_width=1,size=(7,1),key="display ring1"),sg.Button("Ring2",image_data=item2image("Empty"),font=font_choice,pad=(0,0),border_width=1,size=(7,1),key="display ring2"),sg.Push()],
    [sg.Push(),sg.Button("Back",image_data=item2image("Empty"),font=font_choice,pad=(0,0),border_width=1,size=(7,1),key="display back"),sg.Button("Waist",image_data=item2image("Empty"),font=font_choice,pad=(0,0),border_width=1,size=(7,1),key="display waist"),sg.Button("Legs",image_data=item2image("Empty"),font=font_choice,pad=(0,0),border_width=1,size=(7,1),key="display legs"),sg.Button("Feet",image_data=item2image("Empty"),font=font_choice,pad=(0,0),border_width=1,size=(7,1),key="display feet"),sg.Push()],
    [sg.Push(),sg.Text("",font=font_choice)],
    [sg.Push(),sg.Button("Select All",font=font_choice,pad=(0,0),border_width=1,size=(16,2),key="select all gear",tooltip="Select all items in the displayed list.",enable_events=True),sg.Button("Unselect All",font=font_choice,pad=(0,0),border_width=1,size=(16,2),key="unselect all gear",tooltip="Unselect all items in the displayed list.",enable_events=True)],
    [sg.Push(),sg.Button("Select All\nMain Job",font=font_choice,pad=(0,0),border_width=1,size=(16,2),key="select all main",tooltip="Select all items in the displayed list that your selected main job can equip.",enable_events=True,disabled=False),sg.Button("Select <ALL>\nMain Job",font=font_choice,pad=(0,0),border_width=1,size=(16,2),key="select ALL main",tooltip="Select all items in ALL LISTS that your selected main job can equip.",enable_events=True,disabled=False)]
  ],vertical_alignment="center",size=[370,450]),]]
checkbox_tab = [[sg.Column([[
  sg.Push(),
  sg.Frame("Select main-hand equipment", [[sg.Column([  k for k in gear_main  ],size=framesize,scrollable=True,vertical_scroll_only=True)],],font=font_choice,visible=True,key="main display",size=framesize),
  sg.Frame("Select off-hand equipment", [[sg.Column([  k for k in gear_sub  ],size=framesize,scrollable=True,vertical_scroll_only=True)],],font=font_choice,visible=False,key="sub display",size=framesize),
  sg.Frame('Select ammo equipment',[[sg.Column([  k for k in gear_ammo  ],size=framesize,scrollable=True,vertical_scroll_only=True)]],font=font_choice,visible=False,key='ammo display',size=framesize),
  sg.Frame("Select head equipment", [[sg.Column([  k for k in gear_head  ],size=framesize,scrollable=True,vertical_scroll_only=True)],],font=font_choice,visible=False,key="head display",size=framesize),
  sg.Frame("Select neck equipment", [[sg.Column([  k for k in gear_neck  ],size=framesize,scrollable=True,vertical_scroll_only=True)],],font=font_choice,visible=False,key="neck display",size=framesize),
  sg.Frame("Select left ear equipment", [[sg.Column([  k for k in gear_ear1  ],size=framesize,scrollable=True,vertical_scroll_only=True)],],font=font_choice,visible=False,key="ear1 display",size=framesize),
  sg.Frame("Select right ear equipment", [[sg.Column([  k for k in gear_ear2  ],size=framesize,scrollable=True,vertical_scroll_only=True)],],font=font_choice,visible=False,key="ear2 display",size=framesize),
  sg.Frame("Select body equipment", [[sg.Column([  k for k in gear_body  ],size=framesize,scrollable=True,vertical_scroll_only=True)],],font=font_choice,visible=False,key="body display",size=framesize),
  sg.Frame("Select hands equipment", [[sg.Column([  k for k in gear_hands  ],size=framesize,scrollable=True,vertical_scroll_only=True)],],font=font_choice,visible=False,key="hands display",size=framesize),
  sg.Frame("Select left ring equipment", [[sg.Column([  k for k in gear_ring1  ],size=framesize,scrollable=True,vertical_scroll_only=True)],],font=font_choice,visible=False,key="ring1 display",size=framesize),
  sg.Frame("Select right ring equipment", [[sg.Column([  k for k in gear_ring2  ],size=framesize,scrollable=True,vertical_scroll_only=True)],],font=font_choice,visible=False,key="ring2 display",size=framesize),
  sg.Frame("Select back equipment", [[sg.Column([  k for k in gear_back  ],size=framesize,scrollable=True,vertical_scroll_only=True)],],font=font_choice,visible=False,key="back display",size=framesize),
  sg.Frame("Select waist equipment", [[sg.Column([  k for k in gear_waist  ],size=framesize,scrollable=True,vertical_scroll_only=True)],],font=font_choice,visible=False,key="waist display",size=framesize),
  sg.Frame("Select legs equipment", [[sg.Column([  k for k in gear_legs ],size=framesize,scrollable=True,vertical_scroll_only=True)],],font=font_choice,visible=False,key="legs display",size=framesize),
  sg.Frame("Select feet equipment", [[sg.Column([  k for k in gear_feet  ],size=framesize,scrollable=True,vertical_scroll_only=True)],],font=font_choice,visible=False,key="feet display",size=framesize)]],)],
]

select_gear_tab = [[sg.Frame("Select equipment",[[sg.Push(),sg.vtop(sg.Column(gear_tab)),sg.Push(),sg.vtop(sg.Column(checkbox_tab))]],size=(800,500),)]]
          # [sg.vtop(sg.Frame("Initial gearset",[[sg.Push(),sg.vcenter(sg.Column(starting_set_tab)),sg.Push(),sg.Column([radio_tab])]],size=[600,275]))]
