#
# Created by Kastra on Asura.
# Feel free to /tell in game or send a PM on FFXIAH you have questions, comments, or suggestions.
#
# Version date: 2023 February 14
#
# This file contains a the GUI tab "Outputs".
# This will be renamed later to "WS Outputs" when I add TP sets and nuking.
#
import PySimpleGUI as sg
sg.Window.get_screen_size() # https://github.com/PySimpleGUI/PySimpleGUI/issues/1996
w, h = sg.Window.get_screen_size()

fontsize = 9
font_choice = ["Cascadia Mono", fontsize]



base_stats = sg.vtop(sg.Frame("Base",[
    [sg.Text(f"{'STR:':<5s} {'----':>4s}",font=font_choice,size=(10,1),key="str stat")],
    [sg.Text(f"{'DEX:':<5s} {'----':>4s}",font=font_choice,size=(10,1),key="dex stat")],
    [sg.Text(f"{'VIT:':<5s} {'----':>4s}",font=font_choice,size=(10,1),key="vit stat")],
    [sg.Text(f"{'AGI:':<5s} {'----':>4s}",font=font_choice,size=(10,1),key="agi stat")],
    [sg.Text(f"{'INT:':<5s} {'----':>4s}",font=font_choice,size=(10,1),key="int stat")],
    [sg.Text(f"{'MND:':<5s} {'----':>4s}",font=font_choice,size=(10,1),key="mnd stat")],
    [sg.Text(f"{'CHR:':<5s} {'----':>4s}",font=font_choice,size=(10,1),key="chr stat")],]))


physical = sg.vtop(sg.Frame("Physical",[
    [sg.Text(f"{'Accuracy1:':<16s} {'----':>4s}",font=font_choice,size=(22,1),key="acc1 stat",tooltip="Main-hand accuracy.")],
    [sg.Text(f"{'Accuracy2:':<16s} {'----':>4s}",font=font_choice,size=(22,1),key="acc2 stat",tooltip="Off-hand accuracy.")],
    [sg.Text(f"{'Attack1:':<16s} {'----':>4s}",font=font_choice,size=(22,1),key="atk1 stat",tooltip="Main-hand attack.")],
    [sg.Text(f"{'Attack2:':<16s} {'----':>4s}",font=font_choice,size=(22,1),key="atk2 stat",tooltip="Off-hand attack.")],
    [sg.Text(f"{'Ranged Accuracy:':<16s} {'----':>4s}",font=font_choice,size=(22,1),key="racc stat")],
    [sg.Text(f"{'Ranged Attack:':<16s} {'----':>4s}",font=font_choice,size=(22,1),key="ratk stat")],
    ]))

magical = sg.vtop(sg.Frame("Magical",[
    [sg.Text(f"{'Magic Accuracy:':<20s} {'----':>4s}",font=font_choice,size=(26,1),key="macc stat", tooltip="Magic Accuracy from traits and gear. dINT not included.")],
    [sg.Text(f"{'Magic Accuracy Skill:':<21s} {'---':>3s}",font=font_choice,size=(26,1),key="macc skill stat", tooltip="Magic Accuracy Skill from gear.")],
    [sg.Text(f"{'Magic Attack:':<20s} {'----':>4s}",font=font_choice,size=(26,1),key="matk stat")],
    [sg.Text(f"{'Magic Damage:':<20s} {'----':>4s}",font=font_choice,size=(26,1),key="mdmg stat")],
    [sg.Text(f"{'Magic Burst Bonus:':<21s} {'---':>3s}",font=font_choice,size=(26,1),key="mbb stat",tooltip="Caps at 40.\nAdditive with other Magic Burst Damage sources")],
    [sg.Text(f"{'Magic Burst Bonus II:':<21s} {'---':>3s}",font=font_choice,size=(26,1),key="mbb2 stat",tooltip="Only includes gear. No cap confirmed.\nAdditive with other Magic Burst Damage sources.")],
    [sg.Text(f"{'Magic Burst Traits:':<21s} {'---':>3s}",font=font_choice,size=(26,1),key="mbb3 stat",tooltip="Includes Traits, Job Points, and Job Gifts.\nAdditive with other Magic Burst Damage sources.")],
    ]))

tp = sg.vtop(sg.Frame("TP",[
    [sg.Text(f"{'Store TP:':<16s} {'---':>4s}",font=font_choice,size=(22,1),key="stp stat")],
    [sg.Text(f"{'Dual Wield:':<16s} {'----':>4s}",font=font_choice,size=(22,1),key="dw stat",tooltip="Dual wield will reduce TP gain per hit, but increases attack speed.")],
    [sg.Text(f"{'Martial Arts:':<16s} {'----':>4s}",font=font_choice,size=(22,1),key="marts stat", tooltip="Additive delay reduction when using Hand-to-Hand weapons.\nSubtract this value from 480+Weapon_Delay.\nReduces TP gained per hit.")],
    [sg.Text(f"{'Gear Haste:':<16s} {'----':>4s}",font=font_choice,size=(22,1),key="gear haste stat", tooltip="Caps at 256/1024 = 25%")],
    [sg.Text(f"{'Magic Haste:':<15s} {'-----':>5s}",font=font_choice,size=(22,1),key="magic haste stat", tooltip="Caps at 448/1024 = 43.75%")],
    [sg.Text(f"{'JA Haste:':<16s} {'----':>4s}",font=font_choice,size=(22,1),key="ja haste stat", tooltip="Caps at 256/1024 = 25%")],
    [sg.Text(f"{'Delay Reduction:':<16s} {'----':>4s}",font=font_choice,size=(22,1),key="delay reduction stat", tooltip="Caps at 80%")],
    [sg.Text(f"{'Daken:':<16s} {'----':>4s}",font=font_choice,size=(22,1),key="daken stat", tooltip="Chance to throw a Shuriken while TPing.\nMust have a Shuriken equipped.")],
    [sg.Text(f"{'Kick Attacks:':<16s} {'----':>4s}",font=font_choice,size=(22,1),key="kickattack stat", tooltip="Chance of a bonus kick attack while TPing.\nMust be using a hand-to-hand weapon.")],
    [sg.Text(f"{'Physical DT:':<16s} {'----':>4s}",font=font_choice,size=(22,1),key="pdt stat", tooltip="Physical damage taken. Caps at -50% + Burtgang. \nIncludes \"Damage Taken\" stat bonuses.")],
    [sg.Text(f"{'Magical DT:':<16s} {'----':>4s}",font=font_choice,size=(22,1),key="mdt stat", tooltip="Magical damage taken. Caps at -50%.\nIncludes \"Damage Taken\" stat bonuses.\nShell V provides -29.3% and is included if WHM is selected.")],
    [sg.Text(f"{'Evasion:':<16s} {'----':>4s}",font=font_choice,size=(22,1),key="eva stat", tooltip="Total player evasion.\nIncludes gear, traits, gifts, etc.")],
    [sg.Text(f"{'Magic Evasion:':<16s} {'----':>4s}",font=font_choice,size=(22,1),key="meva stat", tooltip="Total player magic evasion.\nIncludes gear, traits, gifts, etc.")],
    [sg.Text(f"{'Magic Def:':<16s} {'----':>4s}",font=font_choice,size=(22,1),key="mdef stat", tooltip="Total player magic defense.\nIncludes gear, traits, gifts, etc.")],
    ]))

two_handed = ["Great Sword", "Great Katana", "Great Axe", "Polearm", "Scythe", "Staff"]
one_handed = ["Axe", "Club", "Dagger", "Sword", "Katana","Hand-to-Hand"]
magic = ["Elemental Magic", "Ninjutsu"]
ranged_skills = ["Throwing", "Marksmanship", "Archery"]
skills = sg.vtop(sg.Frame("Skill Levels",[
    [sg.Text(f"{k+':':<16s} {'----':>4s}",font=font_choice,size=(22,1),key=f"{k} skill display")] for k in sorted(one_handed+two_handed)+ranged_skills+magic
]))

other = sg.vtop(sg.Frame("Other",[
    [sg.Text(f"{'Crit. Rate:':<21s} {'---':>3s}",font=font_choice,size=(26,1),key="crit rate stat",tooltip="Crit. Rate only applies for Critical Hit weapon skills or when Shining One is equipped.")],
    [sg.Text(f"{'Crit. Damage:':<21s} {'---':>3s}",font=font_choice,size=(26,1),key="crit damage stat",)],
    [sg.Text(f"{'Double Attack:':<21s} {'---':>3s}",font=font_choice,size=(26,1),key="da stat")],
    [sg.Text(f"{'Triple Attack:':<21s} {'---':>3s}",font=font_choice,size=(26,1),key="ta stat")],
    [sg.Text(f"{'Quad. Attack:':<21s} {'---':>3s}",font=font_choice,size=(26,1),key="qa stat")],
    [sg.Text(f"{'Zanshin:':<21s} {'---':>3s}",font=font_choice,size=(26,1),key="zanshin stat",tooltip="Zanshin total from gear and traits.\nHasso provides a 1.25 multiplier to this value if mainjob=SAM.\nSAM mainjob provides an additional +10% from gifts\nCaps at 100%")],
    [sg.Text(f"{'Weapon skill damage:':<21s} {'---':>3s}",font=font_choice,size=(26,1),key="wsd stat",tooltip="Weapon skill damage generally only applies to the first hit of a weapon skill.")],
    [sg.Text(f"{'Weapon skill trait:':<21s} {'---':>3s}",font=font_choice,size=(26,1),key="ws bonus stat",tooltip="Weaponskill damage from DRG or /DRG. Applies to all hits.\nDoes not include Ambuscade WS, Relic/Mythic or REMA augment bonuses")],
    [sg.Text(f"{'PDL (gear):':<20s} {'----':>4s}",font=font_choice,size=(26,1),key="pdl gear stat",tooltip="Multiplicative with PDIF cap for (weapon_base_PDIF + PDL_trait).")],
    [sg.Text(f"{'PDL (trait):':<20s} {'----':>4s}",font=font_choice,size=(26,1),key="pdl trait stat", tooltip="Additive with weapon base PDIF value.")],
    [sg.Text(f"{'TP Bonus:':<20s} {'----':>4s}",font=font_choice,size=(26,1),key="tp bonus stat")],
    ]))

ws_tab = [
          [sg.Text("Number of simulated weapon skills:",font=font_choice),sg.Input("2000",key="n_sims",size=(10,1),tooltip="Number of weapon skill simulations used for the final plot\nAND for calculating damage statistics (min/median/mean/max).\nValues less than 10 are converted to 10.",font=font_choice)],
          [sg.Checkbox("Show final simulated damage distribution plot?",font=font_choice,size=(50,1),key="show final plot",enable_events=False,default=False,tooltip="Uses matplotlib.pyplot to show a final damage distribution.\nMagic simulations will never show plots.")],[sg.Checkbox("Find the best set?",font=font_choice,size=(50,1),key="find set",enable_events=False,default=True,tooltip="Enabled: Check every combination of selected gear (2 at a time) to find the best set automatically.\nDisabled: Calculate damage statistics and plot the initial set from the inputs tab without modifications.")],
          [sg.Text(f"{'DT requirement:':<16s}",font=font_choice,size=(16,1)),sg.Input("0",key="dt_req",size=(5,1),tooltip="DT requirement for gearset.\nFinding sets with DT requirements is slow.",font=font_choice)],
          [sg.Text(f"{'Ranged TP priority:':<16s}",font=font_choice,size=(19,1)),sg.Combo(values=["Damage > TP","TP > Damage", "TP only", "Damage only"], default_value="TP only", readonly=True, key="tp priority",size=(11,1),font=font_choice,tooltip="Damage: Maximizes (damage^2)*(tp_return)\nTP Return: Maximizes (damage)*(tp_return^2)",disabled=False,enable_events=False)],
          [sg.Button("Run WS",size=(5,2),tooltip="Run weapon skill damage simulator."),sg.Button("Run Magic",size=(5,2),tooltip="Run magic damage simulator.\nRanged attacks are included here."),sg.Button("Run TP",size=(5,2),tooltip="Run the TP set finder."),sg.Button("Copy best set",size=(6,2),pad=(15,0),key="copy best set",disabled=True,tooltip="Copies best set to the initial set in the inputs tab for quick look.\nUseful for making minor changes to the best set for comparisons.")],
          [base_stats,physical,magical],[tp,other,skills]
          # Comment out this next line if you want to use the terminal for outputs instead of the GUI. Doing so will prevent the GUI from crashing without any messages explaining why.
        #   [sg.Push(),sg.Output(size=(80, 23),font=font_choice),sg.Push()], # can only have one "sg.Output() since it takes the STDOUT"
]
