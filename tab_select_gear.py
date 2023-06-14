#
# Created by Kastra on Asura.
# Feel free to /tell in game or send a PM on FFXIAH you have questions, comments, or suggestions.
#
# Version date: 2023 June 14
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
# Create the full list of checkboxes for each of 16 gear slots. TODO: put this back into a loop
gear_main,gear_sub,gear_ranged,gear_ammo,gear_head,gear_neck,gear_ear1,gear_ear2,gear_body,gear_hands,gear_ring1,gear_ring2,gear_back,gear_waist,gear_legs,gear_feet = [[] for k in range(16)]

for k in sorted([k['Name2'] for k in mains]):
    gear_main.append([sg.Checkbox(k,font=font_choice,size=(50,1),key="checkbox_main:"+k,enable_events=True)])

for k in sorted([k['Name2'] for k in subs+grips]):
    gear_sub.append([sg.Checkbox(k,font=font_choice,size=(50,1),key="checkbox_sub:"+k,enable_events=True)])

for k in sorted([k['Name2'] for k in ranged]):
    gear_ranged.append([sg.Checkbox(k,font=font_choice,size=(50,1),key="checkbox_ranged:"+k,enable_events=True)])

for k in sorted([k['Name2'] for k in ammos]):
    gear_ammo.append([sg.Checkbox(k,font=font_choice,size=(50,1),key="checkbox_ammo:"+k,enable_events=True)])

for k in sorted([k['Name2'] for k in heads]):
    gear_head.append([sg.Checkbox(k,font=font_choice,size=(50,1),key="checkbox_head:"+k,enable_events=True)])

for k in sorted([k['Name2'] for k in necks]):
    gear_neck.append([sg.Checkbox(k,font=font_choice,size=(50,1),key="checkbox_neck:"+k,enable_events=True)])

for k in sorted([k['Name2'] for k in ears]):
    gear_ear1.append([sg.Checkbox(k,font=font_choice,size=(50,1),key="checkbox_ear1:"+k,enable_events=True)])

for k in sorted([k['Name2'] for k in ears2]):
    gear_ear2.append([sg.Checkbox(k,font=font_choice,size=(50,1),key="checkbox_ear2:"+k,enable_events=True)])

for k in sorted([k['Name2'] for k in bodies]):
    gear_body.append([sg.Checkbox(k,font=font_choice,size=(50,1),key="checkbox_body:"+k,enable_events=True)])

for k in sorted([k['Name2'] for k in hands]):
    gear_hands.append([sg.Checkbox(k,font=font_choice,size=(50,1),key="checkbox_hands:"+k,enable_events=True)])

for k in sorted([k['Name2'] for k in rings]):
    gear_ring1.append([sg.Checkbox(k,font=font_choice,size=(50,1),key="checkbox_ring1:"+k,enable_events=True)])

for k in sorted([k['Name2'] for k in rings2]):
    gear_ring2.append([sg.Checkbox(k,font=font_choice,size=(50,1),key="checkbox_ring2:"+k,enable_events=True)])

for k in sorted([k['Name2'] for k in capes]):
    gear_back.append([sg.Checkbox(k,font=font_choice,size=(50,1),key="checkbox_back:"+k,enable_events=True)])

for k in sorted([k['Name2'] for k in waists]):
    gear_waist.append([sg.Checkbox(k,font=font_choice,size=(50,1),key="checkbox_waist:"+k,enable_events=True)])

for k in sorted([k['Name2'] for k in legs]):
    gear_legs.append([sg.Checkbox(k,font=font_choice,size=(50,1),key="checkbox_legs:"+k,enable_events=True)])

for k in sorted([k['Name2'] for k in feet]):
    gear_feet.append([sg.Checkbox(k,font=font_choice,size=(50,1),key="checkbox_feet:"+k,enable_events=True)])

framesize = [400,450]

checkbox_tab = [[sg.Column([[
  sg.Frame("Select main-hand equipment", [[sg.Column([  k for k in gear_main  ],size=framesize,scrollable=True,vertical_scroll_only=True,key="main display col")],],font=font_choice,visible=True,key="main display",size=framesize),
  sg.Frame("Select off-hand equipment", [[sg.Column([  k for k in gear_sub  ],size=framesize,scrollable=True,vertical_scroll_only=True,key="sub display col")],],font=font_choice,visible=False,key="sub display",size=framesize),
  sg.Frame("Select ranged equipment", [[sg.Column([  k for k in gear_ranged  ],size=framesize,scrollable=True,vertical_scroll_only=True,key="ranged display col")],],font=font_choice,visible=False,key="ranged display",size=framesize),
  sg.Frame('Select ammo equipment',[[sg.Column([  k for k in gear_ammo  ],size=framesize,scrollable=True,vertical_scroll_only=True,key="ammo display col")]],font=font_choice,visible=False,key='ammo display',size=framesize),
  sg.Frame("Select head equipment", [[sg.Column([  k for k in gear_head  ],size=framesize,scrollable=True,vertical_scroll_only=True,key="head display col")],],font=font_choice,visible=False,key="head display",size=framesize),
  sg.Frame("Select neck equipment", [[sg.Column([  k for k in gear_neck  ],size=framesize,scrollable=True,vertical_scroll_only=True,key="neck display col")],],font=font_choice,visible=False,key="neck display",size=framesize),
  sg.Frame("Select left ear equipment", [[sg.Column([  k for k in gear_ear1  ],size=framesize,scrollable=True,vertical_scroll_only=True,key="ear1 display col")],],font=font_choice,visible=False,key="ear1 display",size=framesize),
  sg.Frame("Select right ear equipment", [[sg.Column([  k for k in gear_ear2  ],size=framesize,scrollable=True,vertical_scroll_only=True,key="ear2 display col")],],font=font_choice,visible=False,key="ear2 display",size=framesize),
  sg.Frame("Select body equipment", [[sg.Column([  k for k in gear_body  ],size=framesize,scrollable=True,vertical_scroll_only=True,key="body display col")],],font=font_choice,visible=False,key="body display",size=framesize),
  sg.Frame("Select hands equipment", [[sg.Column([  k for k in gear_hands  ],size=framesize,scrollable=True,vertical_scroll_only=True,key="hands display col")],],font=font_choice,visible=False,key="hands display",size=framesize),
  sg.Frame("Select left ring equipment", [[sg.Column([  k for k in gear_ring1  ],size=framesize,scrollable=True,vertical_scroll_only=True,key="ring1 display col")],],font=font_choice,visible=False,key="ring1 display",size=framesize),
  sg.Frame("Select right ring equipment", [[sg.Column([  k for k in gear_ring2  ],size=framesize,scrollable=True,vertical_scroll_only=True,key="ring2 display col")],],font=font_choice,visible=False,key="ring2 display",size=framesize),
  sg.Frame("Select back equipment", [[sg.Column([  k for k in gear_back  ],size=framesize,scrollable=True,vertical_scroll_only=True,key="back display col")],],font=font_choice,visible=False,key="back display",size=framesize),
  sg.Frame("Select waist equipment", [[sg.Column([  k for k in gear_waist  ],size=framesize,scrollable=True,vertical_scroll_only=True,key="waist display col")],],font=font_choice,visible=False,key="waist display",size=framesize),
  sg.Frame("Select legs equipment", [[sg.Column([  k for k in gear_legs ],size=framesize,scrollable=True,vertical_scroll_only=True,key="legs display col")],],font=font_choice,visible=False,key="legs display",size=framesize),
  sg.Frame("Select feet equipment", [[sg.Column([  k for k in gear_feet  ],size=framesize,scrollable=True,vertical_scroll_only=True,key="feet display col")],],font=font_choice,visible=False,key="feet display",size=framesize)]],)],
]

from tab_inputs import item2image



# This bit is the 4x4 grid of buttons and the few "Select" buttons under it.
odyssey_rank_thing = [sg.Text("Odyssey Rank:",size=(15,1),font=font_choice,),sg.Combo(values=["None","0","15","20","25","30"], default_value="30", readonly=True, key="odyssey rank",size=(10,1),font=font_choice,tooltip="Auto-select Odyssey gear with this rank.",disabled=False,enable_events=False)]


tvr_ring_thing = [sg.Text("TVR Ring:",size=(15,1),font=font_choice,),sg.Combo(values=["Cornelia's","Ephramad's","Fickblix's","Gurebu-Ogurebu's","Lehko Habhoka's","Medada's","Ragelise's"], default_value="Cornelia's", readonly=True, key="tvr ring",size=(17,1),font=font_choice,tooltip="Only auto-select this one TVR ring.",disabled=False,enable_events=False)]

gear_tab = [
  [sg.Column([
    [sg.Push(),sg.Button("Main",image_data=item2image("Empty"),font=font_choice,pad=(0,0),border_width=1,size=(7,1),key="display main"),sg.Button("Sub",image_data=item2image("Empty"),font=font_choice,pad=(0,0),border_width=1,size=(7,1),key="display sub"),sg.Button("Ranged",image_data=item2image("Empty"),font=font_choice,pad=(0,0),border_width=1,size=(7,1),key="display ranged"),sg.Button("Ammo",image_data=item2image("Empty"),font=font_choice,pad=(0,0),border_width=1,size=(7,1),key="display ammo"),sg.Push()],
    [sg.Push(),sg.Button("Head",image_data=item2image("Empty"),font=font_choice,pad=(0,0),border_width=1,size=(7,1),key="display head"),sg.Button("Neck",image_data=item2image("Empty"),font=font_choice,pad=(0,0),border_width=1,size=(7,1),key="display neck"),sg.Button("Ear1",image_data=item2image("Empty"),font=font_choice,pad=(0,0),border_width=1,size=(7,1),key="display ear1"),sg.Button("Ear2",image_data=item2image("Empty"),font=font_choice,pad=(0,0),border_width=1,size=(7,1),key="display ear2"),sg.Push()],
    [sg.Push(),sg.Button("Body",image_data=item2image("Empty"),font=font_choice,pad=(0,0),border_width=1,size=(7,1),key="display body"),sg.Button("Hands",image_data=item2image("Empty"),font=font_choice,pad=(0,0),border_width=1,size=(7,1),key="display hands"),sg.Button("Ring1",image_data=item2image("Empty"),font=font_choice,pad=(0,0),border_width=1,size=(7,1),key="display ring1"),sg.Button("Ring2",image_data=item2image("Empty"),font=font_choice,pad=(0,0),border_width=1,size=(7,1),key="display ring2"),sg.Push()],
    [sg.Push(),sg.Button("Back",image_data=item2image("Empty"),font=font_choice,pad=(0,0),border_width=1,size=(7,1),key="display back"),sg.Button("Waist",image_data=item2image("Empty"),font=font_choice,pad=(0,0),border_width=1,size=(7,1),key="display waist"),sg.Button("Legs",image_data=item2image("Empty"),font=font_choice,pad=(0,0),border_width=1,size=(7,1),key="display legs"),sg.Button("Feet",image_data=item2image("Empty"),font=font_choice,pad=(0,0),border_width=1,size=(7,1),key="display feet"),sg.Push()],
    [sg.Push(),sg.Text("",font=font_choice)],
    [sg.Push(),sg.Button("Select All",font=font_choice,pad=(0,0),border_width=1,size=(16,2),key="select all gear",tooltip="Select all items in the displayed list.",enable_events=True),sg.Button("Unselect All",font=font_choice,pad=(0,0),border_width=1,size=(16,2),key="unselect all gear",tooltip="Unselect all items in the displayed list.",enable_events=True)],
    [sg.Push(),sg.Button("Select From\nFile",font=font_choice,pad=(0,0),border_width=1,size=(16,2),key="select file",tooltip="Open an input file to select gear.\nInput file format is based on the \"\\\\gs export all\" command.",enable_events=True,disabled=False),sg.Button("Select <ALL>\nMain Job",font=font_choice,pad=(0,0),border_width=1,size=(16,2),key="select ALL main",tooltip="Select all items in ALL LISTS that your selected main job can equip.",enable_events=True,disabled=False)],odyssey_rank_thing,tvr_ring_thing,
  ],vertical_alignment="center",size=[270,450]),]]


select_gear_tab = [[sg.Frame("Select equipment",[[sg.Push(),sg.vtop(sg.Column(gear_tab)),sg.Push(),sg.vtop(sg.Column(checkbox_tab))]],size=(800,500),)]]
