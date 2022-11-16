#
# Created by Kastra on Asura.
# Feel free to /tell in game or send a PM on FFXIAH you have questions, comments, or suggestions.
#
# Version date: 2022 November 15
#
# This file contains a the GUI tab "Outputs".
# This will be renamed later to "WS Outputs" when I add TP sets and nuking.
#
import PySimpleGUI as sg

font_choice = "Courier 12"


warning_messages = {"Incorrect main":" can not use ",
                  "Incorrect sub":" not compatible with "}



active_warnings = [] # Default no warnings
ws_tab = [
          [sg.Text("Number of simulations for the final plot:",font=font_choice),sg.Input("0",key="n_sims",size=(10,1),tooltip="Number of weapon skill simulations used for the final plot\nand for calculating damage statistics.\nValues less than 10 are converted to 10.",font=font_choice)],
          [sg.Checkbox("Show final simulated damage distribution plot?",font=font_choice,size=(50,1),key="show final plot",enable_events=False,default=False)],[sg.Checkbox("Find the best set?",font=font_choice,size=(50,1),key="find set",enable_events=False,default=True,tooltip="Enabled: Check every combination of selected gear (2 at a time) to find the best set.\nDisabled: Calculate damage statistics and plot the initial set from the inputs tab.")],[sg.Button("Run",size=(5,2)),sg.Button("Copy best set",size=(6,2),pad=(15,0),key="copy best set",disabled=True,tooltip="Copies best set to the initial set in the inputs tab for quick look.\nUseful for making minor changes to the best set for comparisons.")],
          # [sg.Frame("Active warnings",[[sg.Text("\n".join(active_warnings),key="ws warnings",font=font_choice,text_color="orange",size=(200,8))]],font=font_choice,visible=True,)], # This line should go in the "Select Gear" tab later.

          # Comment out this next line if you want to use the terminal for outputs instead of the GUI. Doing so will prevent the GUI from crashing without any messages explaining why.
          [sg.Push(),sg.Output(size=(80, 23),font=font_choice),sg.Push()], # can only have one "sg.Output() since it takes the STDOUT"

]
