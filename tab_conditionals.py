#
# Created by Kastra on Asura.
# Feel free to /tell in game or send a PM on FFXIAH you have questions, comments, or suggestions.
#
# Version date: 2023 January 16
#
# This file contains a the GUI tab "Outputs".
# This will be renamed later to "WS Outputs" when I add TP sets and nuking.
#
import PySimpleGUI as sg
sg.Window.get_screen_size() # https://github.com/PySimpleGUI/PySimpleGUI/issues/1996
w, h = sg.Window.get_screen_size()

fontsize = 9
font_choice = ["Cascadia Mono", fontsize]



conditional_frame = sg.vtop(sg.Frame("Gearset conditions",[
    [sg.Text(f"{'PDT:':<20s}",font=font_choice,size=(25,1)),sg.Input("0",key="pdt_req",size=(5,1),tooltip="PDT requirement for gearset.\nPositive is good.\nCaps at 50",font=font_choice)],
    [sg.Text(f"{'MDT:':<20s}",font=font_choice,size=(25,1)),sg.Input("0",key="mdt_req",size=(5,1),tooltip="MDT requirement for gearset.\nPositive is good.\nCaps at 50",font=font_choice)],
    [sg.Text(f"{'Subtle Blow:':<20s}",font=font_choice,size=(25,1)),sg.Input("0",key="sb_req",size=(5,1),tooltip="Subtle Blow requirement for gearset.\nCaps at 50.",font=font_choice)],
    [sg.Text(f"{'Subtle Blow II:':<20s}",font=font_choice,size=(25,1)),sg.Input("0",key="sb2_req",size=(5,1),tooltip="Subtle Blow II requirement for gearset.\nCaps at 50.",font=font_choice)],
    [sg.Text(f"{'Magic Evasion:':<20s}",font=font_choice,size=(25,1)),sg.Input("0",key="meva_req",size=(5,1),tooltip="Magic Evasion requirement for gearset",font=font_choice)],
    [sg.Text(f"{'Magic Defense:':<20s}",font=font_choice,size=(25,1)),sg.Input("0",key="mdef_req",size=(5,1),tooltip="Magic Defense requirement for gearset",font=font_choice)],
    ]))

conditional_tab = [[conditional_frame]]
