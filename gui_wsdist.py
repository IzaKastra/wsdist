import PySimpleGUI as sg
import numpy as np
import traceback # https://stackoverflow.com/questions/3702675/how-to-catch-and-print-the-full-exception-traceback-without-halting-exiting-the


sg.Window.get_screen_size() # https://github.com/PySimpleGUI/PySimpleGUI/issues/1996
w, h = sg.Window.get_screen_size()

random_theme = np.random.choice(sg.theme_list())
random_theme = np.random.choice([k for k in sg.theme_list() if "Mono" in k])

sg.theme(random_theme)

def get_warnings(values):
    #
    # This would print warnings, but it doesn't correctly read the status of selected items.
    # Will fix later. The user just needs to know that they shouldn't try to use Liberator in their Blade: Shun set...
    #
    selected_mains = [] # Currently enabled main weapons
    selected_subs = []
    for k in values:
        if "main: " in str(k) and values[k]: # If the "main" gear slot item is enabled:
            selected_mains.append( " ".join(k.split()[1:]) )
        if "sub: " in str(k) and values[k]: # If the "sub" gear slot item is enabled:
            selected_subs.append( " ".join(k.split()[1:]) )

    if "Blade:" in values["select weaponskill"]:
        selected_ws_type = "Katana"
    elif "Tachi:" in values["select weaponskill"]:
        selected_ws_type = "Great Katana"
    elif values["select weaponskill"] in ["Insurgency", "Cross Reaper", "Entropy", "Infernal Scythe", "Catastrophe", "Quietus"]:
        selected_ws_type = "Scythe"
    elif values["select weaponskill"] in ["Torcleaver", "Resolution", "Scourge"]:
        selected_ws_type = "Great Sword"
    elif values["select weaponskill"] in ["Savage Blade", "Requiescat", "Chant du Cygne ", "Death Blossom"]:
        selected_ws_type = "Sword"
    elif values["select weaponskill"] in ["Evisceration", "Mercy Stroke", "Mandalic Stab", "Rudra's Storm", "Exenterator"]:
        selected_ws_type = "Dagger"



    active_warnings = []
    two_handed = ["Great Sword", "Great Katana", "Great Axe", "Polearm", "Scythe", "Staff"]
    one_handed = ["Axe", "Club", "Dagger", "Sword", "Katana"]
    for k in selected_mains:
        for l in mains:
            wname = l["Name2"] if "Name2" in l else l["Name"]
            if k==wname:
                if l["Skill Type"] != selected_ws_type:
                    active_warnings.append("Main:["+wname+"]" + warning_messages["Incorrect main"] + "["+values["select weaponskill"]+"]")

                for k2 in selected_subs:
                    for l2 in subs+grips:
                        wname2 = l2["Name2"] if "Name2" in l2 else l2["Name"]
                        if k2==wname2:
                            if l2["Type"] == "Grip" and l["Skill Type"] not in two_handed:
                                active_warnings.append("Sub:["+wname2+"]" + warning_messages["Incorrect sub"] + "Main:["+wname+"]")
                            if l2["Type"] == "Weapon" and l["Skill Type"] in two_handed:
                                active_warnings.append("Sub:["+wname2+"]" + warning_messages["Incorrect sub"] + "Main:["+wname+"]")
    window["ws warnings"].update("\n".join(active_warnings),visible=True)


def name2dictionary(name, all_gear):
    #
    # Given an item name ("Adhemar Bonnet +1A"), find the dictionary (adhemar_bonnet_A) which containts that item's stats.
    # This will be used often, may as well make it a function, even if it is inefficient.
    # First check Name2, then check Name. This is so you don't mix up different augment paths.
    # Name is mostly for finding the icon anyway.
    #
    for i,k in enumerate(all_gear):
        gear_name = k["Name2"] if "Name2" in k else k["Name"]
        if name == gear_name:
            return(all_gear[i])
    return(Empty)

from tab_inputs import * # Load the inputs tab
from tab_select_gear import *  # Load the select_gear tab
from tab_outputs import * # Load the outputs tab.

# Add a menu bar for the user to adjust font size and stuff.
font_size_options = [f"&{k:>3d}::font{k}" for k in [l for l in range(6,16)]]
# https://csveda.com/python-menu-button-menu-and-option-menu-with-pysimplegui/
menu_def=[['&Edit', ['&Font Size',font_size_options, '&Theme','---', '!&Save Defaults']]]

layout = [
          [
          [sg.Menu(menu_def, font='Verdana', pad=(10,10),key="menubar_select")],
          sg.TabGroup([
                        [
                         sg.Tab("Inputs", input_tab),
                         sg.Tab("Select Gear", select_gear_tab),
                         sg.Tab("Outputs", ws_tab),
                         ]
                       ],key="tab group")
          ]
         ]

# window_styles = ["default", "winnative", "clam", "alt", "classic", "vista", "xpnative"] # https://old.reddit.com/r/learnpython/comments/k0m9on/how_can_i_change_the_ui_style_in_pysimplegui/
window_styles = ["default", "alt"] # https://old.reddit.com/r/learnpython/comments/k0m9on/how_can_i_change_the_ui_style_in_pysimplegui/
random_style = np.random.choice(window_styles)
window = sg.Window(f"Kastra WS Damage Simulator (2022 November 18) - Theme:{random_theme} - Style:{random_style}",layout,size=(700,850),resizable=True,alpha_channel=1.0,finalize=True,no_titlebar=False,ttk_theme=random_style)



while True:
    # Run the code within this while True block once.
    # Then wait for the user to perform an event before running another loop.


    # Read the window. Record the action that triggered the window to refresh as well as the key-value pairs associated with all variables throughout the window.
    event, values = window.read()


    # Exit the program if given exit or null command.
    if event in (None, "Exit"):
        break


    # # Allow the user to define their font size (lazy way of having the user try to fix their own UI formatting issues). Currently broken. Can't find a way to update all text programmatically yet
    if event[1:] in [k[2:] for k in font_size_options]:
        # This is not well-written yet. Some GUI elements do not have a font keyword in their .update() method.
        # Input.update() was just recently updated to include it, but Button (and others) are missing it still.
        # To update the font of elements missing the font keyword, I'm using the code from jason990420 (https://github.com/PySimpleGUI/PySimpleGUI/issues/6012)
        # It works, but there may be stuff that breaks because of it.
        new_size = event.strip().split("::")[0]
        new_font = ["Cascadia Mono", new_size]
        for value in values:
            if window[value].Font == ['Cascadia Mono', 9]:
                try:
                    window[value].update(font=new_font)
                except:
                    window[value].Widget.configure(font=new_font)    # state is 'normal', 'readonly' or 'disabled'

    try:
        # If the user selects a new enemy from the enemy drop down list, then automatically update the enemy stats.
        if event == "enemy_name":
            enemy = values["enemy_name"]
            if enemy == "Custom":
                window["enemy_location"].update("")
            else:
                window["enemy_level"].update(f"{preset_enemies[enemy]['Level']}")
                window["enemy_evasion"].update(f"{preset_enemies[enemy]['Evasion']}")
                window["enemy_defense"].update(f"{preset_enemies[enemy]['Defense']}")
                window["enemy_mdefense"].update(f"{preset_enemies[enemy]['Magic Defense']}")
                window["enemy_vit"].update(f"{preset_enemies[enemy]['VIT']}")
                window["enemy_agi"].update(f"{preset_enemies[enemy]['AGI']}")
                window["enemy_int"].update(f"{preset_enemies[enemy]['INT']}")
                window["enemy_location"].update(f"({preset_enemies[enemy]['Location']})")



        # Update the drop down menus for BRD songs when the user selects a song that is already selected somewhere else.
        if event in ["song1","song2","song3","song4"]:
            songs = {"song1":values["song1"], "song2":values["song2"], "song3":values["song3"], "song4":values["song4"]}
            song1 = values["song1"]
            song2 = values["song2"]
            song3 = values["song3"]
            song4 = values["song4"]
            i = int(event[-1])
            for j in [k+1 for k in range(4) if (k+1)!=i]:
                if songs[f"song{i}"] == songs[f"song{j}"]:
                    window[f"song{j}"].update(value="None")

        # Update the drop down menus for COR rolls when the user selects a roll that is already selected in the other slot.
        if event in ["roll1","roll2"]:
            rolls = {"roll1":values["roll1"], "roll2":values["roll2"]}
            roll1 = values["roll1"]
            roll2 = values["roll2"]
            i = int(event[-1])
            for j in [k+1 for k in range(2) if (k+1)!=i]:
                if rolls[f"roll{i}"] == rolls[f"roll{j}"]:
                    window[f"roll{j}"].update(value="None")

        # Update the drop down menus for GEO entrusts when the user selects an entrust bubble that is already selected as an indi- or geo-bubble.
        if event in ["entrust","indibuff","geobuff"]:
            indibubble = values["indibuff"].split("-")[-1]
            geobubble = values["geobuff"].split("-")[-1]
            entrustbubble = values["entrust"].split("-")[-1]
            if (entrustbubble == indibubble) or (entrustbubble == geobubble):
                window["entrust"].update(value="None")

            if event == "indibuff":
                if indibubble == geobubble:
                    window["geobuff"].update(value="None")
            if event == "geobuff":
                if geobubble == indibubble:
                    window["indibuff"].update(value="None")



        # Unlock Light Shot if COR is selected.
        if event == "cor_on":
            if values["cor_on"]:
                window["LIGHTSHOT"].update(disabled=False)
                window["Crooked Cards"].update(disabled=False)
            else:
                window["LIGHTSHOT"].update(False)
                window["LIGHTSHOT"].update(disabled=True)
                window["Crooked Cards"].update(False)
                window["Crooked Cards"].update(disabled=True)

        # Unlock Bolster and Blaze of Glory if GEO is selected.
        if event == "geo_on":
            if values["geo_on"]:
                window["bolster"].update(disabled=False)
                window["geo_bog"].update(disabled=False)
            else:
                window["bolster"].update(False)
                window["bolster"].update(disabled=True)
                window["geo_bog"].update(False)
                window["geo_bog"].update(disabled=True)

        # Automatically turn off and disable Blaze of Glory if Bolster is turned on.
        if event == "bolster":
            if values["bolster"]:
                if values["geo_bog"]:
                    window["geo_bog"].update(False)
                window["geo_bog"].update(disabled=True)
            else:
                window["geo_bog"].update(disabled=False)

        # Unlock Soul Voice if BRD is selected.
        if event == "brd_on":
            if values["brd_on"]:
                window["soulvoice"].update(disabled=False)
                window["marcato"].update(disabled=False)
            else:
                window["soulvoice"].update(False)
                window["soulvoice"].update(disabled=True)
                window["marcato"].update(False)
                window["marcato"].update(disabled=True)

        # Automatically turn off Marcato if Soul Voice is turned on.
        if event == "soulvoice":
            if values["soulvoice"]:
                if values["marcato"]:
                    window["marcato"].update(False)
                window["marcato"].update(disabled=True)
            else:
                window["marcato"].update(disabled=False)

        # Setup the buttons which display/hide gear lists on the gear tab.
        if event in ["display main","display sub","display ammo","display head","display body","display neck","display ear1","display ear2","display body","display hands","display ring1","display ring2","display back","display waist","display legs","display feet",]:
            slot = event.split()[-1]
            for k in ["main","sub","ammo","head","body","neck","ear1","ear2","body","hands","ring1","ring2","back","waist","legs","feet",]:
                if slot==k:
                    window[f"{k} display"].update(visible=True)
                else:
                    window[f"{k} display"].update(visible=False)

        # Setup buttons to automatically select everything in the displayed list.
        if event == "select all gear":
            for k in ["main","sub","ammo","head","body","neck","ear1","ear2","body","hands","ring1","ring2","back","waist","legs","feet",]:
                if window[f"{k} display"].visible:
                    slot = k
                    break
            for k in values:
                if type(k) == str:
                    if k.split()[0][:-1] == slot:
                        window[k].update(True)

        # Setup buttons to automatically unselect everything in the displayed list.
        if event == "unselect all gear":
            for k in ["main","sub","ammo","head","body","neck","ear1","ear2","body","hands","ring1","ring2","back","waist","legs","feet",]:
                if window[f"{k} display"].visible:
                    slot = k
                    break
            for k in values:
                if type(k) == str:
                    if k.split()[0][:-1] == slot:
                        window[k].update(False)


        if event == "select all main":
            gear_map = {"main":mains, # Map the slot name to the list of gear to be considered in that slot.
                        "sub":subs + grips,
                        "ammo":ammos,
                        "head":heads,
                        "neck":necks,
                        "ear1":ears,
                        "ear2":ears2,
                        "body":bodies,
                        "hands":hands,
                        "ring1":rings,
                        "ring2":rings2,
                        "back":capes,
                        "waist":waists,
                        "legs":legs,
                        "feet":feet}
            main_job = values["mainjob"].lower()
            for k in ["main","sub","ammo","head","body","neck","ear1","ear2","body","hands","ring1","ring2","back","waist","legs","feet",]:
                if window[f"{k} display"].visible:
                    slot = k
                    displayed_equipment_list = gear_map[slot]
                    break
            for k in values:
                if type(k) == str:
                    if k.split()[0][:-1] == slot:
                        for l in displayed_equipment_list:
                            if main_job in l.get("Jobs",[]):
                                window[f"{slot}: {l['Name2']}"].update(True)
                            else:
                                window[f"{slot}: {l['Name2']}"].update(False)


        # Setup buttons to show/hide radio buttons on the starting gearset tab.
        # Clicking the "main" slot will show the radio buttons for the "main" gear on the right while hiding all other slot radio buttons
        if event.split()[0] == "showstart":
            slot = event.split()[-1]
            if slot == "---":
                continue
            for k in ["main","sub","ammo","head","body","neck","ear1","ear2","body","hands","ring1","ring2","back","waist","legs","feet",]:
                if k == slot:
                    if not window[f"{k} start radio"].visible:
                        window[f"{k} start radio"].update(visible=True)
                else:
                    if window[f"{k} start radio"].visible:
                        window[f"{k} start radio"].update(visible=False)

        # Setup fancy pictures on the buttons when you select a radio button on starting set tab.
        if event[:5] == "start":
            slot = event.split(":")[0][5:]
            item = event.split(":")[1][1:]
            item_name = all_names_map[item]
            window[f"showstart {slot}"].update(image_data=item2image(item_name))
            window[f"showstart {slot}"].set_tooltip(item)


        # Begin collecting variables to pass into the main code. There will be a lot of variables.
        if event == "Run" or event == "quicklook":

            main_job = values["mainjob"]
            sub_job = values["subjob"]


            # Define weapon skill and TP range.
            ws_name = values["select weaponskill"]
            min_tp = int(values["mintp"])
            max_tp = int(values["maxtp"])


            # New window to show output?
            # window2 = sg.Window(f"{main_job}/{sub_job}  {ws_name}  {min_tp}-{max_tp}",[[[sg.Push(),sg.Output(size=(150, 60),font=font_choice),sg.Push()]]],size=(800 ,500),resizable=True,alpha_channel=1.0,finalize=True,no_titlebar=False,ttk_theme=random_style)


            fitn = 2 # Fit two slots simultaneously. Hard-coded because 3 isn't worth the time and 1 occasionally results in incorrect sets

            # How many simulations in the final plot?
            n_sims = int(values["n_sims"]) if int(values["n_sims"]) > 100 else 100


            # How many maximum iterations before assuming converged? Currently hard-coded to 10 and 0. 0 means "do not find best set."
            n_iter = 10 if values["find set"] else 0


            # Define the starting gearset.
            for k in values:
                if type(k)==str:
                    if k[:5] == "start" and ":" in k: # If the key is a "start_____: " key for a starting item
                        if values[k]: # if the start item is set to true
                            slot = k.split(":")[0][5:] # The slot is recorded in the key
                            item_name2 = k.split(":")[1][1:] # The item name is also recorded in the key
                            starting_gearset[slot] = name2dictionary(item_name2,all_gear)


            # Define buffs
            from buffs import *

            # Define BRD buffs
            brd_on = values["brd_on"]
            active_songs = [values[k] for k in values if "song"==k[:4]]
            marcato = values["marcato"]
            soulvoice = values["soulvoice"]
            nsong = int(values["nsong"].split()[-1])

            brd_min5_attack  = ((brd["Minuet V"]["Attack"][0] + min(8,nsong)*brd["Minuet V"]["Attack"][1])*(1.0+0.5*marcato if values["song1"]=="Minuet V" else 1.0) if "Minuet V" in active_songs else 0)*(1.0+1.0*soulvoice)
            brd_min4_attack  = ((brd["Minuet IV"]["Attack"][0] + min(8,nsong)*brd["Minuet IV"]["Attack"][1])*(1.0+0.5*marcato if values["song1"]=="Minuet IV" else 1.0) if "Minuet IV" in active_songs else 0)*(1.0+1.0*soulvoice)
            brd_min3_attack  = ((brd["Minuet III"]["Attack"][0] + min(8,nsong)*brd["Minuet III"]["Attack"][1])*(1.0+0.5*marcato if values["song1"]=="Minuet III" else 1.0) if "Minuet III" in active_songs else 0)*(1.0+1.0*soulvoice)

            brd_hm_accuracy        = ((brd["Honor March"]["Accuracy"][0] + min(8,nsong)*brd["Honor March"]["Accuracy"][1])*(1.0+0.5*marcato if values["song1"]=="Honor March" else 1.0) if "Honor March" in active_songs else 0)*(1.0+1.0*soulvoice)
            brd_hm_rangedaccuracy  = ((brd["Honor March"]["Ranged Accuracy"][0] + min(8,nsong)*brd["Honor March"]["Ranged Accuracy"][1])*(1.0+0.5*marcato if values["song1"]=="Honor March" else 1.0) if "Honor March" in active_songs else 0)*(1.0+1.0*soulvoice)
            brd_hm_attack          = ((brd["Honor March"]["Attack"][0] + min(8,nsong)*brd["Honor March"]["Attack"][1])*(1.0+0.5*marcato if values["song1"]=="Honor March" else 1.0) if "Honor March" in active_songs else 0)*(1.0+1.0*soulvoice)
            brd_hm_rangedattack    = ((brd["Honor March"]["Ranged Attack"][0] + min(8,nsong)*brd["Honor March"]["Ranged Attack"][1])*(1.0+0.5*marcato if values["song1"]=="Honor March" else 1.0) if "Honor March" in active_songs else 0)*(1.0+1.0*soulvoice)
            brd_hm_haste           = ((brd["Honor March"]["Haste"][0] + min(8,nsong)*brd["Honor March"]["Haste"][1])*(1.0+0.5*marcato if values["song1"]=="Honor March" else 1.0) if "Honor March" in active_songs else 0)*(1.0+1.0*soulvoice)


            brd_swordmad_accuracy  = ((brd["Sword Madrigal"]["Accuracy"][0] + min(8,nsong)*brd["Sword Madrigal"]["Accuracy"][1])*(1.0+0.5*marcato if values["song1"]=="Sword Madrigal" else 1.0) if "Sword Madrigal" in active_songs else 0)*(1.0+1.0*soulvoice)
            brd_blademad_accuracy  = ((brd["Blade Madrigal"]["Accuracy"][0] + min(8,nsong)*brd["Blade Madrigal"]["Accuracy"][1])*(1.0+0.5*marcato if values["song1"]=="Blade Madrigal" else 1.0) if "Blade Madrigal" in active_songs else 0)*(1.0+1.0*soulvoice)

            brd_vmarch_haste  = ((brd["Victory March"]["Haste"][0] + min(8,nsong)*brd["Victory March"]["Haste"][1])*(1.0+0.5*marcato if values["song1"]=="Victory March" else 1.0) if "Victory March" in active_songs else 0)*(1.0+1.0*soulvoice)
            brd_amarch_haste  = ((brd["Advancing March"]["Haste"][0] + min(8,nsong)*brd["Advancing March"]["Haste"][1])*(1.0+0.5*marcato if values["song1"]=="Advancing March" else 1.0) if "Advancing March" in active_songs else 0)*(1.0+1.0*soulvoice)


            brd_attack = brd_on*int(brd_min5_attack + brd_min4_attack + brd_min3_attack + brd_hm_attack)
            brd_accuracy = brd_on*int(brd_hm_accuracy + brd_swordmad_accuracy + brd_blademad_accuracy)
            brd_rangedaccuracy = brd_on*int(brd_hm_accuracy)


            # Define COR buffs: Total bonus stat obtained from a Lucky roll with "Rolls +nroll" bonus from gear.
            cor_on = values["cor_on"]
            active_rolls = [values["roll1"], values["roll2"]]
            nroll = int(values["nroll"].split()[-1])
            cor_sam = cor["Samurai"]["Store TP"][0] + nroll*cor["Samurai"]["Store TP"][1] if "Samurai" in active_rolls else 0
            cor_chaos = cor["Chaos"]["Attack"][0] + nroll*cor["Chaos"]["Attack"][1] if "Chaos" in active_rolls else 0
            cor_hunter = cor["Hunter"]["Accuracy"][0] + nroll*cor["Hunter"]["Accuracy"][1] if "Hunter's" in active_rolls else 0
            cor_rogue = cor["Rogue"]["Crit Rate"][0] + nroll*cor["Rogue"]["Crit Rate"][1] if "Rogue's" in active_rolls else 0
            cor_wizard = cor["Wizard"]["Magic Attack"][0] + nroll*cor["Wizard"]["Magic Attack"][1] if "Wizard's" in active_rolls else 0
            cor_fighter = cor["Fighter"]["DA"][0] + nroll*cor["Fighter"]["DA"][1] if "Fighter's" in active_rolls else 0
            crooked = values["Crooked Cards"]
            cor_stp = cor_on*cor_sam*(1.0+0.2*crooked if values["roll1"]=="Samurai" else 1.0)
            cor_attack = cor_on*cor_chaos*(1.0+0.2*crooked if values["roll1"]=="Chaos" else 1.0)
            cor_accuracy = cor_on*cor_hunter*(1.0+0.2*crooked if values["roll1"]=="Hunter's" else 1.0)
            cor_critrate = cor_on*cor_rogue*(1.0+0.2*crooked if values["roll1"]=="Rogue's" else 1.0)
            cor_magicattack = cor_on*cor_wizard*(1.0+0.2*crooked if values["roll1"]=="Wizard's" else 1.0)
            cor_da = cor_on*cor_fighter*(1.0+0.2*crooked if values["roll1"]=="Fighter's" else 1.0)


            # Define GEO buffs
            geo_on = values["geo_on"]
            nbubble = int(values["nbubble"].split()[-1])
            indibubble = values["indibuff"]
            geobubble = values["geobuff"]
            geomancy_potency = float(values["geomancy_potency"])/100
            geomancy_potency = 0 if geomancy_potency < 0 else geomancy_potency
            geomancy_potency = 1 if geomancy_potency > 1 else geomancy_potency
            active_bubbles = [indibubble.split("-")[-1],geobubble.split("-")[-1]]
            entrust = values["entrust"]
            blazeofglory = values["geo_bog"]
            bolster = values["bolster"]
            geo_attack = geo_on*((geo["Fury"]["Attack"][0] + nbubble*geo["Fury"]["Attack"][1] if "Fury" in active_bubbles else 0)*(1.0+0.5*blazeofglory*(geobubble=="Geo-Fury"))*(1.0+1.0*bolster) + (geo["Fury"]["Attack"][0] if entrust == "Entrust-Fury" else 0))
            geo_accuracy = geo_on*((geo["Precision"]["Accuracy"][0] + nbubble*geo["Precision"]["Accuracy"][1] if "Precision" in active_bubbles else 0)*(1.0+0.5*blazeofglory*(geobubble=="Geo-Precision"))*(1.0+1.0*bolster) + (geo["Precision"]["Accuracy"][0] if entrust == "Entrust-Precision" else 0))
            geo_haste = geo_on*((geo["Haste"]["Haste"][0] + nbubble*geo["Haste"]["Haste"][1] if "Haste" in active_bubbles else 0)*(1.0+0.5*blazeofglory*(geobubble=="Geo-Haste"))*(1.0+1.0*bolster) + (geo["Haste"]["Haste"][0] if entrust == "Entrust-Haste" else 0))
            geo_magicaccuracy = geo_on*((geo["Focus"]["Magic Accuracy"][0] + nbubble*geo["Focus"]["Magic Accuracy"][1] if "Focus" in active_bubbles else 0)*(1.0+0.5*blazeofglory*(geobubble=="Geo-Focus"))*(1.0+1.0*bolster) + (geo["Focus"]["Magic Accuracy"][0] if entrust == "Entrust-Focus" else 0))
            geo_magicattack = geo_on*((geo["Acumen"]["Magic Attack"][0] + nbubble*geo["Acumen"]["Magic Attack"][1] if "Acumen" in active_bubbles else 0)*(1.0+0.5*blazeofglory*(geobubble=="Geo-Acumen"))*(1.0+1.0*bolster) + (geo["Acumen"]["Magic Attack"][0] if entrust == "Entrust-Acumen" else 0))
            geo_str = geo_on*((geo["STR"]["STR"][0] + nbubble*geo["STR"]["STR"][1] if "STR" in active_bubbles else 0)*(1.0+0.5*blazeofglory*(geobubble=="Geo-STR"))*(1.0+1.0*bolster) + (geo["STR"]["STR"][0] if entrust == "Entrust-STR" else 0))
            geo_dex = geo_on*((geo["DEX"]["DEX"][0] + nbubble*geo["DEX"]["DEX"][1] if "DEX" in active_bubbles else 0)*(1.0+0.5*blazeofglory*(geobubble=="Geo-DEX"))*(1.0+1.0*bolster) + (geo["DEX"]["DEX"][0] if entrust == "Entrust-DEX" else 0))
            geo_vit = geo_on*((geo["VIT"]["VIT"][0] + nbubble*geo["VIT"]["VIT"][1] if "VIT" in active_bubbles else 0)*(1.0+0.5*blazeofglory*(geobubble=="Geo-VIT"))*(1.0+1.0*bolster) + (geo["VIT"]["VIT"][0] if entrust == "Entrust-VIT" else 0))
            geo_agi = geo_on*((geo["AGI"]["AGI"][0] + nbubble*geo["AGI"]["AGI"][1] if "AGI" in active_bubbles else 0)*(1.0+0.5*blazeofglory*(geobubble=="Geo-AGI"))*(1.0+1.0*bolster) + (geo["AGI"]["AGI"][0] if entrust == "Entrust-AGI" else 0))
            geo_int = geo_on*((geo["INT"]["INT"][0] + nbubble*geo["INT"]["INT"][1] if "INT" in active_bubbles else 0)*(1.0+0.5*blazeofglory*(geobubble=="Geo-INT"))*(1.0+1.0*bolster) + (geo["INT"]["INT"][0] if entrust == "Entrust-INT" else 0))
            geo_mnd = geo_on*((geo["MND"]["MND"][0] + nbubble*geo["MND"]["MND"][1] if "MND" in active_bubbles else 0)*(1.0+0.5*blazeofglory*(geobubble=="Geo-MND"))*(1.0+1.0*bolster) + (geo["MND"]["MND"][0] if entrust == "Entrust-MND" else 0))
            geo_chr = geo_on*((geo["CHR"]["CHR"][0] + nbubble*geo["CHR"]["CHR"][1] if "CHR" in active_bubbles else 0)*(1.0+0.5*blazeofglory*(geobubble=="Geo-CHR"))*(1.0+1.0*bolster) + (geo["CHR"]["CHR"][0] if entrust == "Entrust-CHR" else 0))

            frailty_potency = (geomancy_potency)*(geo_on*((geo["Frailty"]["Defense"][0] + nbubble*geo["Frailty"]["Defense"][1] if "Frailty" in active_bubbles else 0)*(1.0+0.5*blazeofglory*(geobubble=="Geo-Frailty"))*(1.0+1.0*bolster) + (geo["Frailty"]["Defense"][0] if entrust == "Entrust-Frailty" else 0)))
            malaise_potency = (geomancy_potency)*(geo_on*((geo["Malaise"]["Magic Defense"][0] + nbubble*geo["Malaise"]["Magic Defense"][1] if "Malaise" in active_bubbles else 0)*(1.0+0.5*blazeofglory*(geobubble=="Geo-Malaise"))*(1.0+1.0*bolster) + (geo["Malaise"]["Magic Defense"][0] if entrust == "Entrust-Malaise" else 0)))
            torpor_potency = (geomancy_potency)*(geo_on*((geo["Torpor"]["Evasion"][0] + nbubble*geo["Torpor"]["Evasion"][1] if "Torpor" in active_bubbles else 0)*(1.0+0.5*blazeofglory*(geobubble=="Geo-Torpor"))*(1.0+1.0*bolster) + (geo["Torpor"]["Evasion"][0] if entrust == "Entrust-Torpor" else 0)))


            # Define buffs from white magic:
            whm_on = values["whm_on"]
            whm_haste = whm["Haste"]["Haste"]*(values["nhaste"] == "Haste") + whm["Haste II"]["Haste"]*(values["nhaste"] == "Haste II")
            whm_str = whm["Boost-STR"]["STR"]*(values["whm_boost"]=="Boost-STR")
            whm_dex = whm["Boost-DEX"]["DEX"]*(values["whm_boost"]=="Boost-DEX")
            whm_vit = whm["Boost-VIT"]["VIT"]*(values["whm_boost"]=="Boost-VIT")
            whm_agi = whm["Boost-AGI"]["AGI"]*(values["whm_boost"]=="Boost-AGI")
            whm_int = whm["Boost-INT"]["INT"]*(values["whm_boost"]=="Boost-INT")
            whm_mnd = whm["Boost-MND"]["MND"]*(values["whm_boost"]=="Boost-MND")
            whm_chr = whm["Boost-CHR"]["CHR"]*(values["whm_boost"]=="Boost-CHR")

            # Define Dia
            dia_dictionary = {"None":0,
                              "Dia": 104./1024+(28./1024*values["LIGHTSHOT"]),
                              "Dia II": 156./1024+(28./1024*values["LIGHTSHOT"]),
                              "Dia III": 208./1024+(28./1024*values["LIGHTSHOT"]),
            }
            dia_potency = dia_dictionary[values["ndia"]] if whm_on else 0.0


            for food in all_food:
                if food["Name"] == values["food"]:
                    food_attack = food.get("Attack",0)
                    food_rangedattack = food.get("Ranged Attack",0)
                    food_accuracy = food.get("Accuracy",0)
                    food_rangedaccuracy = food.get("Ranged Accuracy",0)
                    food_magicaccuracy = food.get("Magic Accuracy",0)
                    food_magicattack = food.get("Magic Attack",0)
                    food_str = food.get("STR",0)
                    food_dex = food.get("DEX",0)
                    food_vit = food.get("VIT",0)
                    food_agi = food.get("AGI",0)
                    food_int = food.get("INT",0)
                    food_mnd = food.get("MND",0)
                    food_chr = food.get("CHR",0)
                    food_found = True
            if not food_found:
                attack,food_rangedattack,food_accuracy,food_rangedaccuracy,food_magicaccuracy,food_magicattack,food_str,food_dex,food_vit,food_agi,food_int,food_mnd,food_chr = [0 for k in range(13)]



            # Collect all of the buffs into a single dictionary which gets looped over in the main code to add towards your final stats.
            buffs = {"food": {"Attack": food_attack, "Ranged Attack": food_attack, "Accuracy": food_accuracy, "Ranged Accuracy":food_accuracy, "Magic Attack":food_magicattack, "Magic Accuracy":food_magicaccuracy, "STR":food_str,"DEX":food_dex, "VIT":food_vit, "AGI":food_agi, "INT":food_int, "MND":food_mnd, "CHR":food_chr,},
                     "brd": {"Attack": brd_attack, "Accuracy": brd_accuracy, "Ranged Accuracy": brd_rangedaccuracy, "Ranged Attack": brd_attack},
                     "cor": {"Attack": cor_attack, "Ranged Attack": cor_attack, "Store TP": cor_stp, "Accuracy": cor_accuracy, "Magic Attack": cor_magicattack, "DA":cor_da, "Crit Rate": cor_critrate},
                     "geo": {"Attack": geo_attack, "Ranged Attack": geo_attack, "Accuracy": geo_accuracy, "Ranged Accuracy":geo_accuracy, "Magic Accuracy":geo_magicaccuracy, "Magic Attack":geo_magicattack, "STR":geo_str,"DEX":geo_dex, "VIT":geo_vit, "AGI":geo_agi, "INT":geo_int, "MND":geo_mnd, "CHR":geo_chr,},
                     "whm": {"Haste": whm_haste, "STR":whm_str,"DEX":whm_dex, "VIT":whm_vit, "AGI":whm_agi, "INT":whm_int, "MND":whm_mnd, "CHR":whm_chr}, # WHM buffs like boost-STR. Not tested
                     }


            # Define your enemy stats based on the enemy tab.
            enemy = {"Defense":int(values["enemy_defense"]),
                     "Evasion":int(values["enemy_evasion"]),
                     "Magic Defense":int(values["enemy_mdefense"]),
                     "VIT":int(values["enemy_vit"]),
                     "INT":int(values["enemy_int"]),
                     "AGI":int(values["enemy_agi"]),
                    }

            # Decrease enemy stats based on debuffs selected.
            enemy["Defense"] *= (1-(dia_potency + frailty_potency)) if (1-(dia_potency + frailty_potency)) > 0.01 else 0.01
            enemy["Magic Defense"] = (enemy["Magic Defense"] - malaise_potency) if (enemy["Magic Defense"]- malaise_potency) > -50 else -50
            enemy["Evasion"] -= torpor_potency


            # We need to transfer the list of gear to check into a list of lists now. This will be used by the main code to check each piece, slot by slot.
            check_gear = [] # List of lists, containing dictionaries for items to be checked. This gets appended to later using the items in the GUI with checkboxes marked.
            check_slots = ["main","sub","ammo","head","neck","ear1","ear2","body","hands","ring1","ring2","back","waist","legs","feet"] # Slot names to check. This gets filtered later with .remove()
            remove_slots = []
            for s in check_slots:
                gear_to_check = []
                for val in values: # Format: value = <slot>: <itemname>
                    if type(val) == str:
                        # print(slot, val, val.split(":")[0],values[val])
                        if val.split(":")[0] == s and values[val]:
                            item_name = " ".join(val.split()[1:])
                            gear_to_check.append(name2dictionary(item_name,all_gear))
                if len(gear_to_check) > 0:
                    check_gear.append(gear_to_check)
                else:
                    remove_slots.append(s)
            for s in remove_slots:
                check_slots.remove(s)


            if event == "quicklook":
                from wsdist import weaponskill
                from set_stats import *
                gearset = set_gear(buffs, starting_gearset, main_job ,sub_job)
                quicklook_damage = weaponskill(main_job, sub_job, ws_name, enemy, gearset, np.average([min_tp, max_tp]), buffs, starting_gearset)[0]
                window["quickaverage"].update(f"{'Average =':>10s} {int(quicklook_damage):>6d} damage")
            else:
                from wsdist import run_weaponskill

                show_final_plot = values["show final plot"]
                best_set = run_weaponskill(main_job, sub_job, ws_name, min_tp, max_tp, n_iter, n_sims, check_gear, check_slots, buffs, enemy, starting_gearset, show_final_plot)
                window["copy best set"].update(disabled=False)
        # Copy the best set to the initial set tab for convenience:
        if event == "copy best set":
            window["tab group"].Widget.select(0) # https://github.com/PySimpleGUI/PySimpleGUI/issues/415
            for val in values:
                if type(val) == str:
                    if "start" == val[:5]:
                        window[val].update(False)
            for slot in best_set:
                if slot == "ranged":
                    continue
                # print(slot, best_set[slot]["Name2"],values[f"start{slot}: {best_set[slot]['Name2']}"])
                window[f"showstart {slot}"].update(image_data=item2image(best_set[slot]["Name"]))
                window[f"start{slot}: {best_set[slot]['Name2']}"].update(True)
                window[f"showstart {slot}"].set_tooltip(best_set[slot]["Name2"])

    except Exception as err:

        # Automatically move to the "Output" if something returns an error.
        window["tab group"].Widget.select(2) # https://github.com/PySimpleGUI/PySimpleGUI/issues/415

        traceback.print_exc() # print the most recent error to the output tab.
                              # this is only the most recent. if you have a chain of errors, then you'll have to work your way up one at a time.

    # This bit is useless until I add the Nuke Tab
    # nuke = False
    # spell = "Doton: Ichi"
    # burst = False
    # futae = False


# window.set_min_size(window.size)
window.close()
