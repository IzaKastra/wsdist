import PySimpleGUI as sg
import numpy as np
import traceback # https://stackoverflow.com/questions/3702675/how-to-catch-and-print-the-full-exception-traceback-without-halting-exiting-the


sg.Window.get_screen_size() # https://github.com/PySimpleGUI/PySimpleGUI/issues/1996
w, h = sg.Window.get_screen_size()

random_theme = np.random.choice(sg.theme_list())
random_theme = np.random.choice([k for k in sg.theme_list() if "Mono" in k])
random_theme = "BlueMono"


sg.theme(random_theme)

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
# from tab_conditionals import * # Load the conditionals tab.

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
                        #  sg.Tab("Conditions", conditional_tab),
                         ]
                       ],key="tab group")
          ]
         ]

# window_styles = ["default", "winnative", "clam", "alt", "classic", "vista", "xpnative"] # https://old.reddit.com/r/learnpython/comments/k0m9on/how_can_i_change_the_ui_style_in_pysimplegui/
window_styles = ["default", "alt"] # https://old.reddit.com/r/learnpython/comments/k0m9on/how_can_i_change_the_ui_style_in_pysimplegui/
random_style = np.random.choice(window_styles)
random_style = "default"

# Build the window.
window = sg.Window(f"Kastra FFXI Damage Simulator (2023 February 22)",layout,size=(700,930) if h>930 else (700+500,600),resizable=True,alpha_channel=1.0,finalize=True,no_titlebar=False,ttk_theme=random_style)




# Define some variables/lists/dictionaries that the GUI will use.
all_gear = mains+subs+grips+ranged+ammos+heads+necks+ears+ears2+bodies+hands+rings+rings2+capes+waists+legs+feet
all_names_map = dict([[k['Name2'], k['Name']] for k in all_gear]) # Dictionary that maps name2s to names for images later. We can't find an image for "Heishi Shorinken R15" so map it to "Heishi Shoriken" here

# Sort the gear lists by name. https://stackoverflow.com/questions/72899/how-do-i-sort-a-list-of-dictionaries-by-a-value-of-the-dictionary
gear_dict = {"main":mains,"sub":subs+grips,"ranged":ranged,"ammo":ammos,"head":heads,"neck":necks,"ear1":ears,"ear2":ears2,"body":bodies,"hands":hands,"ring1":rings,"ring2":rings2,"back":capes,"waist":waists,"legs":legs,"feet":feet}
for slot in gear_dict:
    gear_dict[slot] = sorted(gear_dict[slot], key=lambda d: d['Name2'])

default_job = "nin"
# Make sure the gear lists only show NIN gear to start
for slot in gear_dict:
    # First loop once to hide everything.
    for equipment in gear_dict[slot]:
        window[f"checkbox_{slot}:{equipment['Name2']}"].hide_row()
        window[f"start{slot}:{equipment['Name2']}"].hide_row()
    # Now loop once again and unhide things in alphabetical order. Without the first hide all loop, things get thrown in at the bottom and would be out of order.
    for equipment in gear_dict[slot]:
        if default_job in equipment["Jobs"]:
            window[f"checkbox_{slot}:{equipment['Name2']}"].unhide_row()
            window[f"start{slot}:{equipment['Name2']}"].unhide_row()


# Dictionary of spells that each job has access to. This SHOULD be a copy/paste of the spell_dict in tab_inputs.py
spell_dict = {
    "NIN":["Doton: Ichi","Doton: Ni","Doton: San","Suiton: Ichi","Suiton: Ni","Suiton: San","Huton: Ichi","Huton: Ni","Huton: San","Katon: Ichi","Katon: Ni","Katon: San","Hyoton: Ichi","Hyoton: Ni","Hyoton: San", "Raiton: Ichi","Raiton: Ni","Raiton: San","Ranged Attack"],
    "BLM":["Stone","Stone II","Stone III","Stone IV","Stone V","Stone VI","Stoneja",
            "Water","Water II","Water III","Water IV","Water V","Water VI","Waterja",
            "Aero","Aero II","Aero III","Aero IV","Aero V","Aero VI","Aeroja",
            "Fire","Fire II","Fire III","Fire IV","Fire V","Fire VI","Firaja",
            "Blizzard","Blizzard II","Blizzard III","Blizzard IV","Blizzard V","Blizzard VI","Blizzaja",
            "Thunder","Thunder II","Thunder III","Thunder IV","Thunder V","Thunder VI","Thundaja"],
    "RDM":["Stone","Stone II","Stone III","Stone IV","Stone V",
            "Water","Water II","Water III","Water IV","Water V",
            "Aero","Aero II","Aero III","Aero IV","Aero V",
            "Fire","Fire II","Fire III","Fire IV","Fire V",
            "Blizzard","Blizzard II","Blizzard III","Blizzard IV","Blizzard V",
            "Thunder","Thunder II","Thunder III","Thunder IV","Thunder V",
            "Ranged Attack"],
    "GEO":["Stone","Stone II","Stone III","Stone IV","Stone V",
            "Water","Water II","Water III","Water IV","Water V",
            "Aero","Aero II","Aero III","Aero IV","Aero V",
            "Fire","Fire II","Fire III","Fire IV","Fire V",
            "Blizzard","Blizzard II","Blizzard III","Blizzard IV","Blizzard V",
            "Thunder","Thunder II","Thunder III","Thunder IV","Thunder V",],
    "SCH":["Stone","Stone II","Stone III","Stone IV","Stone V","Geohelix II",
            "Water","Water II","Water III","Water IV","Water V","Hydrohelix II",
            "Aero","Aero II","Aero III","Aero IV","Aero V","Anemohelix II",
            "Fire","Fire II","Fire III","Fire IV","Fire V","Pyrohelix",
            "Blizzard","Blizzard II","Blizzard III","Blizzard IV","Blizzard V","Cryohelix II",
            "Thunder","Thunder II","Thunder III","Thunder IV","Thunder V","Ionohelix II",
            "Luminohelix II", "Noctohelix II","Kaustra"],
    "DRK":["Stone","Stone II","Stone III",
            "Water","Water II","Water III",
            "Aero","Aero II","Aero III",
            "Fire","Fire II","Fire III",
            "Blizzard","Blizzard II","Blizzard III",
            "Thunder","Thunder II","Thunder III"],
    "COR":["Earth Shot", "Water Shot", "Wind Shot", "Fire Shot", "Ice Shot", "Thunder Shot","Ranged Attack"],
    "RNG":["Ranged Attack"],
    "SAM":["Ranged Attack"],
    "THF":["Ranged Attack"],

}


main_jobs = sorted(["NIN", "DRK", "SCH", "RDM", "BLM", "SAM", "DRG", "WHM", "WAR", "COR", "BRD", "THF","MNK","DNC","BST","RUN","RNG","PUP","BLU","GEO","PLD"]) # If you add jobs here, make sure to add them in the tab_inputs.py file too.

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

while True:

    event, values = window.read()
    # print(event)

    # Exit the program if given exit or null command.
    if event in (None, "Exit"):
        break


# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

    # # Allow the user to define their font size. Currently broken for some UI elements.
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

# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

    # Inside this try: block are all of the possible events the user can cause by interacting with the GUI.
    # If something fails, then it runs the "except:" block at the end of the code.
    try:

# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

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
                window["enemy_mnd"].update(f"{preset_enemies[enemy]['MND']}")
                window["enemy_location"].update(f"({preset_enemies[enemy]['Location']})")

# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------


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

# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

        # Update the drop down menus for COR rolls when the user selects a roll that is already selected in the other slot.
        if event in ["roll1","roll2"]:
            rolls = {"roll1":values["roll1"], "roll2":values["roll2"]}
            roll1 = values["roll1"]
            roll2 = values["roll2"]
            i = int(event[-1])
            for j in [k+1 for k in range(2) if (k+1)!=i]:
                if rolls[f"roll{i}"] == rolls[f"roll{j}"]:
                    window[f"roll{j}"].update(value="None")

# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

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

# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

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

# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

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

# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

        # Automatically turn off and disable Blaze of Glory if Bolster is turned on.
        if event == "bolster":
            if values["bolster"]:
                if values["geo_bog"]:
                    window["geo_bog"].update(False)
                window["geo_bog"].update(disabled=True)
            else:
                window["geo_bog"].update(disabled=False)

# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

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

# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

        # Automatically turn off Marcato if Soul Voice is turned on.
        if event == "soulvoice":
            if values["soulvoice"]:
                if values["marcato"]:
                    window["marcato"].update(False)
                window["marcato"].update(disabled=True)
            else:
                window["marcato"].update(disabled=False)

# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

        # Setup the buttons which display/hide gear lists on the gear tab.
        # This is triggered when clicking on a gear slot grid point in the "Select Gear" tab.
        # The event format is "display head" for example.
        if event.split()[0] == "display":
            selected_slot = event.split()[1]
            for slot in gear_dict:
                window[f"{slot} display"].update(visible=True if selected_slot==slot else False)

# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

        jse_ear_names = {"nin":"Hattori","drk":"Heathen","blm":"Wicce","rdm":"Lethargy","drg":"Peltast","whm":"Ebers","sam":"Kasuga","sch":"Arbatel","war":"Boii","cor":"Chasseur","brd":"Fili","thf":"Skulker","mnk":"Bhikku","dnc":"Maculele","bst":"Nukumi","geo":"Azimuth","pld":"Chevalier","rng":"Amini","blu":"Hashishin","run":"Erilaz","pup":"Karagoz"}


        # Setup buttons to automatically select everything in the displayed list.
        if event in ["select all gear", "unselect all gear"]:
            main_job = values["mainjob"]
            odyrank = values["odyssey rank"]

            # First figure out which list is currently displayed.
            for slot in gear_dict:
                if window[f"{slot} display"].visible:
                    selected_slot = slot
                    break

            # Loop over all gear in the selected slot and select everything that the main job can equip. This SHOULD be identical to everything visible in that list.
            if event == "select all gear":
                for equipment in gear_dict[selected_slot]:
                    if main_job.lower() in equipment["Jobs"]:
                        if "Nyame" in equipment["Name2"] and equipment["Name2"][-1]=="A": # Uncheck Nyame Path A
                            window[f"checkbox_{selected_slot}:{equipment['Name2']}"].update(False)
                            continue

                        if "Kraken" in equipment["Name2"]: # Uncheck Kraken Club
                            window[f"checkbox_{selected_slot}:{equipment['Name2']}"].update(False)
                            continue

                        if selected_slot=="neck" and "R20" in equipment["Name2"]: # Unselect JSE+1 necks
                            window[f"checkbox_{selected_slot}:{equipment['Name2']}"].update(False)
                            continue

                        if selected_slot in ["ear1", "ear2"]: # Unselect JSE+2 earrings
                            if jse_ear_names[main_job.lower()] in equipment["Name2"] and "+2" in equipment["Name2"]:
                                window[f"checkbox_{selected_slot}:{equipment['Name2']}"].update(False)
                                continue

                        window[f"checkbox_{selected_slot}:{equipment['Name2']}"].update(True if str(equipment.get("Rank",odyrank))==odyrank else False)

                    else:
                        window[f"checkbox_{selected_slot}:{equipment['Name2']}"].update(False)


            # Unselect everything in the selected slot.
            elif event == "unselect all gear":
                for equipment in gear_dict[selected_slot]: # No need for a job check here. We're unselecting everything in this slot anyway.
                    window[f"checkbox_{selected_slot}:{equipment['Name2']}"].update(False)

# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

        # select every piece of equipment in all slots that your main job can equip.
        if event == "select ALL main":
            main_job = values["mainjob"]
            odyrank = values["odyssey rank"]
            ws_name = values["select weaponskill"]

            for slot in gear_dict:
                for equipment in gear_dict[slot]:
                    if main_job.lower() in equipment["Jobs"]:
                        # First turn off Nyame Path A,
                        if "Nyame" in equipment["Name2"] and equipment["Name2"][-1]=="A":
                            window[f"checkbox_{slot}:{equipment['Name2']}"].update(False)
                            continue

                        if "Kraken" in equipment["Name2"]: # Uncheck Kraken Club
                            window[f"checkbox_{slot}:{equipment['Name2']}"].update(False)
                            continue

                        if slot=="neck" and "R20" in equipment["Name2"]: # Do not select JSE+1 necks
                            window[f"checkbox_{slot}:{equipment['Name2']}"].update(False)
                            continue

                        if slot in ["ear1", "ear2"]: # Unselect JSE+1 earrings
                            if jse_ear_names[main_job.lower()] in equipment["Name2"] and "+2" in equipment["Name2"]:
                                window[f"checkbox_{slot}:{equipment['Name2']}"].update(False)
                                continue

                        # If using a melee WS, then unselect weapons that can't use it (this is annoying when testing magic since it unselects stuff)
                        if ws_name not in ws_dict["Marksmanship"]+ws_dict["Archery"]:
                            if slot == "main" and ws_name not in ws_dict[equipment["Skill Type"]]:
                                window[f"checkbox_{slot}:{equipment['Name2']}"].update(False)
                            else:
                                window[f"checkbox_{slot}:{equipment['Name2']}"].update(True if str(equipment.get("Rank",odyrank))==odyrank else False) # This line selects everything that passed all the previous checks as long as Odyssey rank requirement is met

                        # If using a ranged WS, then unselect guns for bow WSs and bows for gun WSs. Also unselect equipment ammo since you can't shoot equipment (like seething bomblet)
                        elif ws_name in ws_dict["Marksmanship"]+ws_dict["Archery"]:
                            if slot == "ranged" and ws_name not in ws_dict.get(equipment.get("Skill Type","None"),[]):
                                window[f"checkbox_{slot}:{equipment['Name2']}"].update(False)
                            if slot == "ammo" and equipment.get("Type","None") not in ["Bullet", "Arrow", "Bolt"]:
                                window[f"checkbox_{slot}:{equipment['Name2']}"].update(False)

                            # Select all items except Odyssey gear with rank different than "odyrank"
                            window[f"checkbox_{slot}:{equipment['Name2']}"].update(True if str(equipment.get("Rank",odyrank))==odyrank else False) # This line selects everything that passed all the previous checks as long as Odyssey rank requirement is met
                    else:
                        window[f"checkbox_{slot}:{equipment['Name2']}"].update(False)

                        # Keeping the following line commented because it has a link to something useful.
                        # if X in window.AllKeysDict: # https://github.com/PySimpleGUI/PySimpleGUI/issues/1597

# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

        # Update which radio gear slot is displayed on the inputs tab based on the equipment slot clicked from the 4x4 grid.
        # This event is triggers when clicking on an equipment slot in the inputs tab.
        # The event format is "showradio legs", which would hide all radio-button frames except the legs slot.
        if event.split()[0] == "showradio":
            selected_slot = event.split()[-1]
            for slot in gear_dict:
                window[f"radiobox_{slot}"].update(visible=True if selected_slot==slot else False)

# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

        # The user selected a new sub job.
        if event == "subjob":
            main_job = values["mainjob"]
            sub_job = values["subjob"]
            if sub_job == main_job:
                window["subjob"].update("None") # Prioritize main job if main and sub are set to the same thing.

# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

        # The user selected a new main job.
        # Gear lists and job abilities need to be updated when the main job changes.
        if event == "mainjob":

            main_job = values["mainjob"]
            sub_job = values["subjob"]

            if sub_job == main_job:
                window["subjob"].update("None") # Prioritize main job if main and sub are set to the same thing.


            # Update the main-hand weapon to be something your newly selected main job can equip.
            # if main_job.lower() not in eq
            # new_main = [k["Name"] for k in mains if main_job.lower() in k["Jobs"]][0]
            # window[f"showradio main"].update(image_data=item2image(new_main))


            # Update the radio and checkbox buttons to only show items that the main job can use.
            for slot in gear_dict:

                # First loop once to hide everything.
                for equipment in gear_dict[slot]:
                    if main_job.lower() not in equipment["Jobs"]:
                        window[f"checkbox_{slot}:{equipment['Name2']}"].update(False) # Unselect all items in the Select Gear tab that your new main job cant use.

                    window[f"checkbox_{slot}:{equipment['Name2']}"].hide_row()
                    window[f"start{slot}:{equipment['Name2']}"].hide_row()
                # Now loop once again and unhide things in alphabetical order. Without the first hide all loop, things get thrown in at the bottom and would be out of order.
                for equipment in gear_dict[slot]:
                    if main_job.lower() in equipment["Jobs"]:
                        window[f"checkbox_{slot}:{equipment['Name2']}"].unhide_row()
                        window[f"start{slot}:{equipment['Name2']}"].unhide_row()

            # Show/hide job abilities based on the main job selected
            window["futae toggle"].update(visible=True if main_job.lower()=="nin" else False)
            window["magic burst toggle"].update(visible=True if main_job.lower() in ["whm","blm","rdm","sch","geo","drk","nin"] else False)
            window["ebullience toggle"].update(visible=True if main_job.lower()=="sch" else False)
            window["sa toggle"].update(visible=True if main_job.lower()=="thf" else False)
            window["ta toggle"].update(visible=True if main_job.lower()=="thf" else False)
            window["building toggle"].update(visible=True if main_job.lower()=="dnc" else False)
            window["select flourish"].update(visible=True if main_job.lower()=="dnc" else False)
            window["footwork toggle"].update(visible=True if main_job.lower()=="mnk" else False)
            window["impetus toggle"].update(visible=True if main_job.lower()=="mnk" else False)
            window["trueshot toggle"].update(visible=True if main_job.lower() in ["rng","cor"] else False)
            window["velocityshot toggle"].update(visible=True if main_job.lower() in ["rng"] else False)
            window["hovershot toggle"].update(visible=True if main_job.lower() in ["rng"] else False)
            window["doubleshot toggle"].update(visible=True if main_job.lower() in ["rng"] else False)
            window["tripleshot toggle"].update(visible=True if main_job.lower() in ["cor"] else False)
            window["bloodrage toggle"].update(visible=True if main_job.lower() in ["war"] else False)
            window["mightystrikes toggle"].update(visible=True if main_job.lower() in ["war"] else False)
            window["lastresort toggle"].update(visible=True if main_job.lower() in ["drk"] else False)

            # Deselect Job abilities when changing jobs so they arent enabled while hidden.
            window["magic burst toggle"].update(False)
            window["futae toggle"].update(False)
            window["ebullience toggle"].update(False)
            window["building toggle"].update(False)
            window["select flourish"].update("No Flourish")
            window["sa toggle"].update(False)
            window["ta toggle"].update(False)
            window["impetus toggle"].update(False)
            window["footwork toggle"].update(False)
            window["trueshot toggle"].update(False)
            window["velocityshot toggle"].update(False)
            window["hovershot toggle"].update(False)
            window["doubleshot toggle"].update(False)
            window["tripleshot toggle"].update(False)
            window["bloodrage toggle"].update(False)
            window["mightystrikes toggle"].update(False)
            window["lastresort toggle"].update(False)

            # Enable magic sets for casting jobs.
            if main_job in spell_dict:
                window["select spell"].update(disabled=False)
                window["select spell"].update(values=spell_dict[main_job])
                window["select spell"].update(spell_dict[main_job][0])
                window["quicklook magic"].update(disabled=False)
                window["Run Magic"].update(disabled=False)
            else:
                window["quicklook magic"].update(disabled=True)
                window["Run Magic"].update(disabled=True)
                window["select spell"].update(disabled=True)
                window["select spell"].update(values=[])

            # Update the gear lists so that scroll bar doesn't get stuck without showing everything
            # https://stackoverflow.com/questions/75383587/how-to-manage-scrollbar-with-not-visible-items-in-pysimplegui
            window.refresh()
            for slot in gear_dict:
                window[f"{slot} display col"].contents_changed()
                window[f"radiobox_{slot}_col"].contents_changed()



# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

        # Setup fancy pictures on the buttons when you select a radio button on starting set tab.
        # The pictures and the WS list will update based on your selection.
        if event[:5] == "start":
            # First update the gear picture:
            slot = event.split(":")[0][5:]
            item = event.split(":")[1]
            item_name = all_names_map[item]
            window[f"showradio {slot}"].update(image_data=item2image(item_name))
            # window[f"showradio {slot}"].set_tooltip(item)

            item_dictionary = name2dictionary(item, all_gear)

            # Update the tooltip to show the gear's stats when changing gear with the radio buttons.
            tooltip_stats = f"{item}\n"
            ignore_stats = ["Jobs","Name","Name2","Type","Skill Type","Rank"]
            base_stats = ["STR", "DEX", "VIT", "AGI", "INT", "MND", "CHR"]
            wpn_stats = ["DMG","Delay"]
            main_stats = ["Accuracy","Attack","Ranged Accuracy","Ranged Attack","Magic Accuracy","Magic Damage","Magic Attack"]
            bonus_stats = ["Blood Pact Damage", "Kick Attacks", "Kick Attacks Attack", "Martial Arts", "Sneak Attack", "Trick Attack", "Double Shot", "True Shot","Zanshin", "Hasso", "Quick Draw", "Quick Draw II", "Triple Shot","Magic Crit Rate II","Magic Burst Accuracy","Fencer","JA Haste","Accuracy", "AGI", "Attack", "Axe Skill", "CHR", "Club Skill", "Crit Damage", "Crit Rate", "DA", "DA DMG", "Dagger Skill", "Daken", "Dark Affinity", "Dark Elemental Bonus", "Delay", "DEX", "DMG", "Dual Wield", "Earth Affinity", "Earth Elemental Bonus", "Elemental Bonus", "Elemental Magic Skill", "Fire Affinity", "Fire Elemental Bonus", "ftp", "Gear Haste", "Great Axe Skill", "Great Katana Skill", "Great Sword Skill", "Hand-to-Hand Skill", "Ice Affinity", "Ice Elemental Bonus", "INT", "Katana Skill", "Light Affinity", "Light Elemental Bonus", "Magic Accuracy Skill", "Magic Accuracy", "Magic Attack", "Magic Burst Damage II", "Magic Burst Damage", "Magic Damage", "MND", "Name", "Name2", "Ninjutsu Damage", "Ninjutsu Magic Attack", "Ninjutsu Skill", "OA2", "OA3", "OA4", "OA5", "OA6", "OA7", "OA8", "PDL", "Polearm Skill", "QA", "Ranged Accuracy", "Ranged Attack", "Scythe Skill", "Skillchain Bonus", "Staff Skill", "Store TP", "STR", "Sword Skill", "TA", "TA DMG", "Throwing Skill", "Thunder Affinity", "Thunder Elemental Bonus", "TP Bonus", "VIT", "Water Affinity", "Water Elemental Bonus", "Weaponskill Accuracy", "Weaponskill Damage", "Weather", "Wind Affinity", "Wind Elemental Bonus","Polearm Skill","Marksmanship Skill","Archery Skill"]
            def_stats = ["Evasion","Magic Evasion", "Magic Def","DT","MDT","PDT"]

            nl = False # nl = "NewLine". Used to add new lines in specific places in the tooltip text
            for k in wpn_stats:
                if item_dictionary.get(k,False):
                    tooltip_stats += f"{k}:{item_dictionary[k]},"
                    nl = True
                if k=="Delay" and nl:
                    tooltip_stats += "\n"

            nl = False
            for k in base_stats:
                if item_dictionary.get(k,False):
                    tooltip_stats += f"{k}:{item_dictionary[k]},"
                    nl = True
                if nl and k=="CHR":
                    tooltip_stats += "\n"

            nl = False
            for k in main_stats:
                if item_dictionary.get(k,False):
                    tooltip_stats += f"{k}:{item_dictionary[k]},"
                    nl = True
                if "Attack" in k and nl:
                    tooltip_stats += "\n"
                    nl = False

            for k in item_dictionary:
                if k in base_stats or k in ignore_stats or k in main_stats or k in wpn_stats or k in def_stats:
                    continue
                tooltip_stats += f"{k}:{item_dictionary[k]}\n"

            nl = False
            for k in def_stats:
                if item_dictionary.get(k,False):
                    tooltip_stats += f"{k}:{item_dictionary[k]}," # item_dictionary = starting_gearset[slot]  when comparing this file to tab_inputs.py
                    nl = True
                if "Def" in k and nl:
                    tooltip_stats += "\n" # tooltip_stats = default_tooltips[slot]
                    nl = False

            window[f"showradio {slot}"].set_tooltip(tooltip_stats)



            # Now update the WS list:
            if slot in ["main","ranged"]:
                skill_type_main0 = starting_gearset["main"].get("Skill Type","None")
                skill_type_ranged0 = starting_gearset["ranged"].get("Skill Type","None")

                item_dictionary = name2dictionary(item, all_gear)
                starting_gearset[slot] = item_dictionary

                skill_type_main = starting_gearset["main"].get("Skill Type","None") # None is possible in a weird edge case the user has to be trying to make happen.
                main_ws_list = ws_dict.get(skill_type_main,[])
                # print(skill_type_main, starting_gearset)

                skill_type_ranged = starting_gearset["ranged"].get("Skill Type","None") # Ranged skill type might be "Instrument"
                ranged_ws_list = ws_dict.get(skill_type_ranged,[])

                if (slot=="ranged" and (skill_type_ranged0 != skill_type_ranged)) or (slot=="main" and (skill_type_main0 != skill_type_main)):

                    updated_ws_list = sorted(main_ws_list + ranged_ws_list)
                    # print(skill_type_main,skill_type_ranged)

                    window["select weaponskill"].update(values=updated_ws_list)
                    window["select weaponskill"].update(updated_ws_list[0])

# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

        # Begin collecting variables to pass into the main code. There will be a lot of variables.
        if event in ["Run WS", "Run Magic", "Run TP", "quicklook", "quicklook magic", "quicklook TP", "get stats"]:

            main_job = values["mainjob"]
            sub_job = values["subjob"]

            # Define weapon skill and TP range.
            ws_name = values["select weaponskill"]
            min_tp = int(values["mintp"]) if int(values["mintp"]) > 1000 else 1000
            max_tp = int(values["maxtp"]) if int(values["maxtp"]) < 3000 else 3000
            starting_tp = int(values["startingtp"]) if int(values["startingtp"]) <= 999 else 999
            starting_tp = min_tp-1 if starting_tp >= min_tp else starting_tp
            starting_tp = 0 if starting_tp < 0 else starting_tp


            fitn = 2 # Fit two slots simultaneously. Hard-coded because 3 isn't worth the time and 1 occasionally results in incorrect sets

            # How many simulations in the final plot?
            n_sims = int(values["n_sims"]) if int(values["n_sims"]) > 2000 else 2000


            conditions = {
                         "PDT":int(values["dt_req"]),
                         "MDT":int(values["dt_req"]),
                        #  "Subtle Blow":int(values["sb_req"]) if int(values["sb_req"]) < 50 else 50,
                        #  "Subtle Blow II":int(values["sb2_req"]) if int(values["sb2_req"]) < 50 else 50,
                        #  "Magic Evasion":int(values["meva_req"]),
                        #  "Magic Defense":int(values["mdef_req"]),
                   }
            conditions["PDT"] = conditions["PDT"] * -1 if conditions["PDT"] > 0 else conditions["PDT"] # Allow the user to input positive ot negative values to avoid confusion.
            conditions["MDT"] = conditions["MDT"] * -1 if conditions["MDT"] > 0 else conditions["MDT"]

            conditions["PDT"] = -50 if conditions["PDT"] < -50 else conditions["PDT"] # Limit PDT and MDT to -50 so the code doesn't try to find 70% DT that doesnt do anything.
            conditions["MDT"] = -50 if conditions["MDT"] < -50 else conditions["MDT"]

            # How many maximum iterations before assuming converged? Currently hard-coded to 10 and 0. 0 means "do not find best set."
            # Usually it should finish with 3~5 iterations, but more doesn't hurt since the code will end earlier if it finds the best set earlier.
            n_iter = 10 if values["find set"] else 0

            # Update the starting gearset with the selections the user supplied using the radio buttons.
            useful_values = [k for k in values if "start"==k[:5] and ":" in k]
            for k in useful_values:
                if values[k]: # if the start item is set to true. This is only true for items with radio buttons selected on the input tab.
                    slot = k.split(":")[0][5:] # The slot is recorded in the key
                    item_name2 = k.split(":")[1] # The item name is also recorded in the key, separated by a ":" without a space
                    starting_gearset[slot] = name2dictionary(item_name2,all_gear)

            # Import the buff potencies.
            from buffs import *

            # Define BRD buffs
            brd_on = values["brd_on"]
            active_songs = [values[k] for k in values if "song"==k[:4]]
            marcato = values["marcato"]
            soulvoice = values["soulvoice"]
            nsong = int(values["nsong"].split()[-1])

            # Minuets cap at Songs+8
            brd_min5_attack  = ((brd["Minuet V"]["Attack"][0] + min(8,nsong)*brd["Minuet V"]["Attack"][1])*(1.0+0.5*marcato if values["song1"]=="Minuet V" else 1.0) if "Minuet V" in active_songs else 0)*(1.0+1.0*soulvoice)
            brd_min4_attack  = ((brd["Minuet IV"]["Attack"][0] + min(8,nsong)*brd["Minuet IV"]["Attack"][1])*(1.0+0.5*marcato if values["song1"]=="Minuet IV" else 1.0) if "Minuet IV" in active_songs else 0)*(1.0+1.0*soulvoice)
            brd_min3_attack  = ((brd["Minuet III"]["Attack"][0] + min(8,nsong)*brd["Minuet III"]["Attack"][1])*(1.0+0.5*marcato if values["song1"]=="Minuet III" else 1.0) if "Minuet III" in active_songs else 0)*(1.0+1.0*soulvoice)

            # Honor March caps at Songs+4
            brd_hm_accuracy        = ((brd["Honor March"]["Accuracy"][0] + min(4,nsong)*brd["Honor March"]["Accuracy"][1])*(1.0+0.5*marcato if values["song1"]=="Honor March" else 1.0) if "Honor March" in active_songs else 0)*(1.0+1.0*soulvoice)
            brd_hm_rangedaccuracy  = ((brd["Honor March"]["Ranged Accuracy"][0] + min(4,nsong)*brd["Honor March"]["Ranged Accuracy"][1])*(1.0+0.5*marcato if values["song1"]=="Honor March" else 1.0) if "Honor March" in active_songs else 0)*(1.0+1.0*soulvoice)
            brd_hm_attack          = ((brd["Honor March"]["Attack"][0] + min(4,nsong)*brd["Honor March"]["Attack"][1])*(1.0+0.5*marcato if values["song1"]=="Honor March" else 1.0) if "Honor March" in active_songs else 0)*(1.0+1.0*soulvoice)
            brd_hm_rangedattack    = ((brd["Honor March"]["Ranged Attack"][0] + min(4,nsong)*brd["Honor March"]["Ranged Attack"][1])*(1.0+0.5*marcato if values["song1"]=="Honor March" else 1.0) if "Honor March" in active_songs else 0)*(1.0+1.0*soulvoice)
            brd_hm_haste           = ((brd["Honor March"]["Haste"][0] + min(4,nsong)*brd["Honor March"]["Haste"][1])*(1.0+0.5*marcato if values["song1"]=="Honor March" else 1.0) if "Honor March" in active_songs else 0)*(1.0+1.0*soulvoice)

            # Madrigals cap at Songs+9
            brd_swordmad_accuracy  = ((brd["Sword Madrigal"]["Accuracy"][0] + min(9,nsong)*brd["Sword Madrigal"]["Accuracy"][1])*(1.0+0.5*marcato if values["song1"]=="Sword Madrigal" else 1.0) if "Sword Madrigal" in active_songs else 0)*(1.0+1.0*soulvoice)
            brd_blademad_accuracy  = ((brd["Blade Madrigal"]["Accuracy"][0] + min(9,nsong)*brd["Blade Madrigal"]["Accuracy"][1])*(1.0+0.5*marcato if values["song1"]=="Blade Madrigal" else 1.0) if "Blade Madrigal" in active_songs else 0)*(1.0+1.0*soulvoice)

            # Madrigals cap at Songs+8
            brd_hunter_rangedaccuracy  = ((brd["Hunter's Prelude"]["Ranged Accuracy"][0] + min(8,nsong)*brd["Hunter's Prelude"]["Ranged Accuracy"][1])*(1.0+0.5*marcato if values["song1"]=="Hunter's Prelude" else 1.0) if "Hunter's Prelude" in active_songs else 0)*(1.0+1.0*soulvoice)
            brd_archer_rangedaccuracy  = ((brd["Archer's Prelude"]["Ranged Accuracy"][0] + min(8,nsong)*brd["Archer's Prelude"]["Ranged Accuracy"][1])*(1.0+0.5*marcato if values["song1"]=="Archer's Prelude" else 1.0) if "Archer's Prelude" in active_songs else 0)*(1.0+1.0*soulvoice)

            # Marches cap at Songs+8
            brd_vmarch_haste  = ((brd["Victory March"]["Haste"][0] + min(8,nsong)*brd["Victory March"]["Haste"][1])*(1.0+0.5*marcato if values["song1"]=="Victory March" else 1.0) if "Victory March" in active_songs else 0)*(1.0+1.0*soulvoice)
            brd_amarch_haste  = ((brd["Advancing March"]["Haste"][0] + min(8,nsong)*brd["Advancing March"]["Haste"][1])*(1.0+0.5*marcato if values["song1"]=="Advancing March" else 1.0) if "Advancing March" in active_songs else 0)*(1.0+1.0*soulvoice)


            brd_attack = brd_on*int(brd_min5_attack + brd_min4_attack + brd_min3_attack + brd_hm_attack)
            brd_accuracy = brd_on*int(brd_hm_accuracy + brd_swordmad_accuracy + brd_blademad_accuracy)
            brd_rangedaccuracy = brd_on*int(brd_hm_rangedaccuracy + brd_hunter_rangedaccuracy + brd_archer_rangedaccuracy)
            brd_haste = brd_on*(brd_vmarch_haste + brd_amarch_haste + brd_hm_haste)

            # Etudes cap at Songs+9
            brd_str = ((brd["Sinewy Etude"]["STR"][0] + min(9,nsong)*brd["Sinewy Etude"]["STR"][1])*(1.0+0.5*marcato if values["song1"]=="Sinewy Etude" else 1.0) if "Sinewy Etude" in active_songs else 0)*(1.0+1.0*soulvoice) + ((brd["Herculean Etude"]["STR"][0] + min(9,nsong)*brd["Herculean Etude"]["STR"][1])*(1.0+0.5*marcato if values["song1"]=="Herculean Etude" else 1.0) if "Herculean Etude" in active_songs else 0)*(1.0+1.0*soulvoice)
            brd_dex = ((brd["Dextrous Etude"]["DEX"][0] + min(9,nsong)*brd["Dextrous Etude"]["DEX"][1])*(1.0+0.5*marcato if values["song1"]=="Dextrous Etude" else 1.0) if "Dextrous Etude" in active_songs else 0)*(1.0+1.0*soulvoice) + ((brd["Uncanny Etude"]["DEX"][0] + min(9,nsong)*brd["Uncanny Etude"]["DEX"][1])*(1.0+0.5*marcato if values["song1"]=="Uncanny Etude" else 1.0) if "Uncanny Etude" in active_songs else 0)*(1.0+1.0*soulvoice)
            brd_vit = ((brd["Vivavious Etude"]["VIT"][0] + min(9,nsong)*brd["Vivavious Etude"]["VIT"][1])*(1.0+0.5*marcato if values["song1"]=="Vivavious Etude" else 1.0) if "Vivavious Etude" in active_songs else 0)*(1.0+1.0*soulvoice) + ((brd["Vital Etude"]["VIT"][0] + min(9,nsong)*brd["Vital Etude"]["VIT"][1])*(1.0+0.5*marcato if values["song1"]=="Vital Etude" else 1.0) if "Vital Etude" in active_songs else 0)*(1.0+1.0*soulvoice)
            brd_agi = ((brd["Quick Etude"]["AGI"][0] + min(9,nsong)*brd["Quick Etude"]["AGI"][1])*(1.0+0.5*marcato if values["song1"]=="Quick Etude" else 1.0) if "Quick Etude" in active_songs else 0)*(1.0+1.0*soulvoice) + ((brd["Swift Etude"]["AGI"][0] + min(9,nsong)*brd["Swift Etude"]["AGI"][1])*(1.0+0.5*marcato if values["song1"]=="Swift Etude" else 1.0) if "Swift Etude" in active_songs else 0)*(1.0+1.0*soulvoice)
            brd_int = ((brd["Learned Etude"]["INT"][0] + min(9,nsong)*brd["Learned Etude"]["INT"][1])*(1.0+0.5*marcato if values["song1"]=="Learned Etude" else 1.0) if "Learned Etude" in active_songs else 0)*(1.0+1.0*soulvoice) + ((brd["Sage Etude"]["INT"][0] + min(9,nsong)*brd["Sage Etude"]["INT"][1])*(1.0+0.5*marcato if values["song1"]=="Sage Etude" else 1.0) if "Sage Etude" in active_songs else 0)*(1.0+1.0*soulvoice)
            brd_mnd = ((brd["Spirited Etude"]["MND"][0] + min(9,nsong)*brd["Spirited Etude"]["MND"][1])*(1.0+0.5*marcato if values["song1"]=="Spirited Etude" else 1.0) if "Spirited Etude" in active_songs else 0)*(1.0+1.0*soulvoice) + ((brd["Logical Etude"]["MND"][0] + min(9,nsong)*brd["Logical Etude"]["MND"][1])*(1.0+0.5*marcato if values["song1"]=="Logical Etude" else 1.0) if "Logical Etude" in active_songs else 0)*(1.0+1.0*soulvoice)
            brd_chr = ((brd["Enchanting Etude"]["CHR"][0] + min(9,nsong)*brd["Enchanting Etude"]["CHR"][1])*(1.0+0.5*marcato if values["song1"]=="Enchanting Etude" else 1.0) if "Enchanting Etude" in active_songs else 0)*(1.0+1.0*soulvoice) + ((brd["Bewitching Etude"]["CHR"][0] + min(9,nsong)*brd["Bewitching Etude"]["CHR"][1])*(1.0+0.5*marcato if values["song1"]=="Bewitching Etude" else 1.0) if "Bewitching Etude" in active_songs else 0)*(1.0+1.0*soulvoice)


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
            languor_potency = (geomancy_potency)*(geo_on*((geo["Languor"]["Magic Evasion"][0] + nbubble*geo["Languor"]["Magic Evasion"][1] if "Languor" in active_bubbles else 0)*(1.0+0.5*blazeofglory*(geobubble=="Geo-Languor"))*(1.0+1.0*bolster) + (geo["Languor"]["Magic Evasion"][0] if entrust == "Entrust-Languor" else 0)))

            # Define buffs from white magic:
            whm_on = values["whm_on"]
            whm_haste = whm_on*(whm["Haste"]["Haste"]*(values["nhaste"] == "Haste") + whm["Haste II"]["Haste"]*(values["nhaste"] == "Haste II"))
            whm_str   = whm_on*(whm["Boost-STR"]["STR"]*(values["whm_boost"]=="Boost-STR"))
            whm_dex   = whm_on*(whm["Boost-DEX"]["DEX"]*(values["whm_boost"]=="Boost-DEX"))
            whm_vit   = whm_on*(whm["Boost-VIT"]["VIT"]*(values["whm_boost"]=="Boost-VIT"))
            whm_agi   = whm_on*(whm["Boost-AGI"]["AGI"]*(values["whm_boost"]=="Boost-AGI"))
            whm_int   = whm_on*(whm["Boost-INT"]["INT"]*(values["whm_boost"]=="Boost-INT"))
            whm_mnd   = whm_on*(whm["Boost-MND"]["MND"]*(values["whm_boost"]=="Boost-MND"))
            whm_chr   = whm_on*(whm["Boost-CHR"]["CHR"]*(values["whm_boost"]=="Boost-CHR"))

            # Define Dia
            dia_dictionary = {"None":0,
                              "Dia": 104./1024+(28./1024*values["LIGHTSHOT"]),
                              "Dia II": 156./1024+(28./1024*values["LIGHTSHOT"]),
                              "Dia III": 208./1024+(28./1024*values["LIGHTSHOT"]),
            }
            dia_potency = dia_dictionary[values["ndia"]] if whm_on else 0.0

            use_food = False if values["food"] == "None" else True
            if use_food:
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
            else:
                food_attack,food_rangedattack,food_accuracy,food_rangedaccuracy,food_magicaccuracy,food_magicattack,food_str,food_dex,food_vit,food_agi,food_int,food_mnd,food_chr = [0 for k in range(13)]



            # Collect all of the buffs into a single dictionary which gets looped over in the main code to add towards your final stats.
            buffs = {"food": {"Attack": food_attack, "Ranged Attack": food_attack, "Accuracy": food_accuracy, "Ranged Accuracy":food_accuracy, "Magic Attack":food_magicattack, "Magic Accuracy":food_magicaccuracy, "STR":food_str,"DEX":food_dex, "VIT":food_vit, "AGI":food_agi, "INT":food_int, "MND":food_mnd, "CHR":food_chr,},
                     "brd": {"Attack": brd_attack, "Accuracy": brd_accuracy, "Ranged Accuracy": brd_rangedaccuracy, "Ranged Attack": brd_attack,"Haste":brd_haste, "STR":brd_str,"DEX":brd_dex, "VIT":brd_vit, "AGI":brd_agi, "INT":brd_int, "MND":brd_mnd, "CHR":brd_chr,},
                     "cor": {"Attack": cor_attack, "Ranged Attack": cor_attack, "Store TP": cor_stp, "Accuracy": cor_accuracy, "Magic Attack": cor_magicattack, "DA":cor_da, "Crit Rate": cor_critrate},
                     "geo": {"Attack": geo_attack, "Ranged Attack": geo_attack, "Accuracy": geo_accuracy, "Ranged Accuracy":geo_accuracy, "Magic Accuracy":geo_magicaccuracy, "Magic Attack":geo_magicattack, "STR":geo_str,"DEX":geo_dex, "VIT":geo_vit, "AGI":geo_agi, "INT":geo_int, "MND":geo_mnd, "CHR":geo_chr,"Haste":geo_haste},
                     "whm": {"Haste": whm_haste, "STR":whm_str,"DEX":whm_dex, "VIT":whm_vit, "AGI":whm_agi, "INT":whm_int, "MND":whm_mnd, "CHR":whm_chr}, # WHM buffs like boost-STR. Not tested
                     }

            # Define your enemy stats based on the enemy tab.
            enemy = {"Defense":int(values["enemy_defense"]),
                     "Evasion":int(values["enemy_evasion"]),
                     "Magic Defense":int(values["enemy_mdefense"]),
                     "Magic Evasion":int(values["enemy_mevasion"]),
                     "VIT":int(values["enemy_vit"]),
                     "INT":int(values["enemy_int"]),
                     "AGI":int(values["enemy_agi"]),
                     "MND":int(values["enemy_mnd"]),
                    }

            # Decrease enemy stats based on debuffs selected. TODO: "Ignores Enemy DEF" WSs need to be added here somehow... Might be easier to pass the FULL enemy defense and apply debuffs in the main code.
            enemy["Defense"] *= (1-(dia_potency + frailty_potency)) if (1-(dia_potency + frailty_potency)) > 0.01 else 0.01
            enemy["Magic Defense"] = (enemy["Magic Defense"] - malaise_potency) if (enemy["Magic Defense"]- malaise_potency) > -50 else -50
            enemy["Evasion"] -= torpor_potency
            enemy["Magic Evasion"] -= languor_potency


            # We need to transfer the list of gear to check into a list of lists now. This will be used by the main code to check each piece, slot by slot.
            check_gear = [] # List of lists, containing dictionaries for items to be checked. This gets appended to later using the items in the GUI with checkboxes marked.
            check_slots = ["main","sub","ranged","ammo","head","neck","ear1","ear2","body","hands","ring1","ring2","back","waist","legs","feet"] # Slot names to check. This gets filtered later with .remove()
            remove_slots = []
            for slot in check_slots:
                gear_to_check = []
                for val in [k for k in values if "checkbox_" in k and ":" in k]: # value = checkbox_<slot>:<itemname>
                    # print(slot,"|", val,"|", val.split(":")[0],"|",values[val])
                    if val.split(":")[0] == f"checkbox_{slot}" and values[val]:
                        item_name = val.split(":")[-1]
                        gear_to_check.append(name2dictionary(item_name,all_gear))
                        # print(slot,"|",item_name) # Print gear to be checked
                if len(gear_to_check) > 0:
                    check_gear.append(gear_to_check)
                else:
                    remove_slots.append(slot)
            for slot in remove_slots:
                check_slots.remove(slot)

            spell = values["select spell"]
            burst = values["magic burst toggle"]
            futae = values["futae toggle"]
            ebullience = values["ebullience toggle"]
            sneak_attack = values["sa toggle"]
            trick_attack = values["ta toggle"]
            footwork = values["footwork toggle"]
            impetus = values["impetus toggle"]
            building_flourish = values["building toggle"]
            climactic_flourish = True if values["select flourish"] == "Climactic Flourish" else False
            striking_flourish = True if values["select flourish"] == "Striking Flourish" else False
            ternary_flourish = True if values["select flourish"] == "Ternary Flourish" else False
            true_shot_toggle = values["trueshot toggle"]
            velocity_shot_toggle = values["velocityshot toggle"]
            bloodrage_toggle = values["bloodrage toggle"]
            mightystrikes_toggle = values["mightystrikes toggle"]
            lastresort_toggle = values["lastresort toggle"]
            hovershot_toggle = values["hovershot toggle"]
            doubleshot_toggle = values["doubleshot toggle"]
            tripleshot_toggle = values["tripleshot toggle"]

            # Define a dictionary so we can just pass this one thing in instead of passing 10 things to the WS function later
            job_abilities = {"Ebullience":ebullience,
                             "Futae":futae,
                             "Sneak Attack":sneak_attack,
                             "Trick Attack":trick_attack,
                             "Footwork":footwork,
                             "Impetus":impetus,
                             "Building Flourish":building_flourish,
                             "Climactic Flourish":climactic_flourish,
                             "Striking Flourish":striking_flourish,
                             "Ternary Flourish":ternary_flourish,
                             "True Shot":true_shot_toggle,
                             "Velocity Shot":velocity_shot_toggle,
                             "Blood Rage":bloodrage_toggle,
                             "Mighty Strikes":mightystrikes_toggle,
                             "Last Resort":lastresort_toggle,
                             "Hover Shot":hovershot_toggle,
                             "Double Shot":doubleshot_toggle,
                             "Triple Shot":tripleshot_toggle,
                             "metric":values["tp priority"],
                             "shell v":values["whm_on"]
                             }

            kick_ws_footwork = True if "Kick" in ws_name and footwork else False # TODO: maybe use this later or delete it from here. we already define it in the other files anyway


            # --------------------------------------------------------------------------------------------
            # --------------------------------------------------------------------------------------------
            # --------------------------------------------------------------------------------------------

            # Perform an average damage weapon skill. Print the result below the gear set.
            if event == "quicklook":
                from wsdist import weaponskill
                from set_stats import *
                gearset = set_gear(buffs, starting_gearset, main_job ,sub_job, job_abilities=job_abilities)
                quicklook_damage, tp = weaponskill(main_job, sub_job, ws_name, enemy, gearset, min_tp, max_tp, starting_tp, buffs, starting_gearset, False, spell, job_abilities, burst, False)
                window["quickaverage"].update(f"{'Average =':>10s} {int(quicklook_damage):>6d} damage")

            # --------------------------------------------------------------------------------------------
            # --------------------------------------------------------------------------------------------
            # --------------------------------------------------------------------------------------------

            # Return the TP set statistic (either DPS, or time to weapon skill, or some combination of the two) for the given set.
            if event == "quicklook TP":
                from wsdist import weaponskill
                from set_stats import *
                gearset = set_gear(buffs, starting_gearset, main_job ,sub_job, job_abilities=job_abilities)
                quicklook_time, tp = weaponskill(main_job, sub_job, ws_name, enemy, gearset, min_tp, max_tp, starting_tp, buffs, starting_gearset, False, spell, job_abilities, burst, False, True)
                window["quickaverage"].update(f"{'Average =':>10s} {quicklook_time:>6.3f} s / WS\n{'=':>10s} {tp:6.1f} TP / round")

            # --------------------------------------------------------------------------------------------
            # --------------------------------------------------------------------------------------------
            # --------------------------------------------------------------------------------------------

            # Perform an average damage spell. Print the result below the gear set.
            elif event == "quicklook magic":
                from wsdist import weaponskill
                from set_stats import *
                gearset = set_gear(buffs, starting_gearset, main_job ,sub_job, job_abilities=job_abilities)
                quicklook_damage, tp = weaponskill(main_job, sub_job, ws_name, enemy, gearset, min_tp, max_tp, starting_tp, buffs, starting_gearset, True, spell, job_abilities, burst, False)
                if spell == "Ranged Attack":
                    priority = values["tp priority"]
                    if priority=="Damage":
                        window["quickaverage"].update(f"{'Average =':>10s} {quicklook_damage:>6.0f} (dmg^2)(tp)\n{'=':>10s} {tp:6.1f} TP / round")
                    else:
                        window["quickaverage"].update(f"{'Average =':>10s} {quicklook_damage:>6.0f} (dmg)(tp^2)\n{'=':>10s} {tp:6.1f} TP / round")
                else:
                    window["quickaverage"].update(f"{'Average =':>10s} {int(quicklook_damage):>6d} damage")

            # --------------------------------------------------------------------------------------------
            # --------------------------------------------------------------------------------------------
            # --------------------------------------------------------------------------------------------

            # Perform proper weapon skill simulations. Find the best set if the user requested it through the checkbox.
            elif event == "Run WS":
                from wsdist import run_weaponskill

                starting_gearset2 = starting_gearset.copy() # Create a copy of the starting gearset so any unequips do not affect the inputs tab
                if values["find set"]:
                    for slot in gear_dict:
                        # print(slot)
                        # count how many checkboxes are selected for that slot. break out if >0
                        check_unequip = False
                        for k in values:
                            if f"checkbox_{slot}:" in k: # Check each of the checkbox values
                                if values[k]: # if any of them are True for this slot, then check if you have something equipped there that shouldnt be
                                    check_unequip = True
                                    break
                        if check_unequip:
                            # print("checking unequip condition")
                            # print(starting_gearset2[slot]["Name2"],values[f"checkbox_{slot}:{starting_gearset2[slot]['Name2']}"])
                            if not values[f"checkbox_{slot}:{starting_gearset2[slot]['Name2']}"]:
                                # If, in <slot>, you have <item> equipped, and the checkbox for that item is not selected, then:
                                # print("Unequipping ",starting_gearset2[slot]['Name2'])
                                starting_gearset2[slot] = Empty

                show_final_plot = values["show final plot"] # TODO: Show final plot = false for magical WSs too
                best_set = run_weaponskill(main_job, sub_job, ws_name, min_tp, max_tp, starting_tp, n_iter, n_sims, check_gear, check_slots, buffs, enemy, starting_gearset2, show_final_plot, False, spell, job_abilities, conditions, burst, False) # Last False for check_tp_set
                window["copy best set"].update(disabled=False)

            # --------------------------------------------------------------------------------------------
            # --------------------------------------------------------------------------------------------
            # --------------------------------------------------------------------------------------------

            # Find the best TP set using average attacks per round, average TP gain per round, and time per WS.
            elif event == "Run TP":
                from wsdist import run_weaponskill

                starting_gearset2 = starting_gearset.copy() # Create a copy of the starting gearset so any unequips do not affect the inputs tab
                if values["find set"]:
                    for slot in gear_dict:
                        # print(slot)
                        # count how many checkboxes are selected for that slot. break out if >0
                        check_unequip = False
                        for k in values:
                            if f"checkbox_{slot}:" in k: # Check each of the checkbox values
                                if values[k]: # if any of them are True for this slot, then check if you have something equipped there that shouldnt be
                                    check_unequip = True
                                    break
                        if check_unequip:
                            # print("checking unequip condition")
                            # print(starting_gearset2[slot]["Name2"],values[f"checkbox_{slot}:{starting_gearset2[slot]['Name2']}"])
                            if not values[f"checkbox_{slot}:{starting_gearset2[slot]['Name2']}"]:
                                # If, in <slot>, you have <item> equipped, and the checkbox for that item is not selected, then:
                                # print("Unequipping ",starting_gearset2[slot]['Name2'])
                                starting_gearset2[slot] = Empty

                show_final_plot = False # TODO: Show final plot = false for magical WSs too
                best_set = run_weaponskill(main_job, sub_job, ws_name, min_tp, max_tp, starting_tp, n_iter, n_sims, check_gear, check_slots, buffs, enemy, starting_gearset2, show_final_plot, False, spell, job_abilities, conditions, burst, True)
                window["copy best set"].update(disabled=False)

            # --------------------------------------------------------------------------------------------
            # --------------------------------------------------------------------------------------------
            # --------------------------------------------------------------------------------------------

            # Perform proper magic damage simulations. Find the best set if the user requested it through the checkbox.
            elif event == "Run Magic":
                from wsdist import run_weaponskill

                starting_gearset2 = starting_gearset.copy() # Create a copy of the starting gearset so any unequips do not affect the inputs tab
                if values["find set"]:
                    for slot in gear_dict:
                        # print(slot)
                        # count how many checkboxes are selected for that slot. break out if >0
                        check_unequip = False
                        for k in values:
                            if f"checkbox_{slot}:" in k: # Check each of the checkbox values
                                if values[k]: # if any of them are True for this slot, then check if you have something equipped there that shouldnt be
                                    check_unequip = True
                                    break
                        if check_unequip:
                            # print("checking unequip condition")
                            # print(starting_gearset2[slot]["Name2"],values[f"checkbox_{slot}:{starting_gearset2[slot]['Name2']}"])
                            if not values[f"checkbox_{slot}:{starting_gearset2[slot]['Name2']}"]:
                                # If, in <slot>, you have <item> equipped, and the checkbox for that item is not selected, then:
                                # print("Unequipping ",starting_gearset2[slot]['Name2'])
                                starting_gearset2[slot] = Empty


                show_final_plot = False
                best_set = run_weaponskill(main_job, sub_job, ws_name, min_tp, max_tp, starting_tp, n_iter, n_sims, check_gear, check_slots, buffs, enemy, starting_gearset2, show_final_plot, True, spell, job_abilities, conditions, burst, False)
                window["copy best set"].update(disabled=False)

            # --------------------------------------------------------------------------------------------
            # --------------------------------------------------------------------------------------------
            # --------------------------------------------------------------------------------------------

            # Simply print player stats for the supplied gearset to the Outputs tab.
            elif event == "get stats":
                from set_stats import *

                # Defining the empty set lets us see the contribution to stats from gear vs base.
                # It also means it'll call the set_gear() class twice, so expect two print statements if testing/debugging with the "Calc sets" button.
                empty_set = {'main':Hitaki,'sub':Empty,'ranged':Empty,'ammo':Empty,'head':Empty,'body':Empty,'hands':Empty,'legs':Empty,'feet':Empty,'neck':Empty,'waist':Empty,'ear1':Empty,'ear2':Empty,'ring1':Empty,'ring2':Empty,'back':Empty,}
                empty_gearset = set_gear({"food":{},"brd":{},"cor":{},"geo":{},"whm":{}},empty_set, main_job, sub_job)

                gearset = set_gear(buffs, starting_gearset, main_job, sub_job, job_abilities=job_abilities) # put impetus here, otherwise it's effect won't show up
                dual_wield = gearset.gear['sub'].get('Type', 'None') == "Weapon"

                window["tab group"].Widget.select(2) # https://github.com/PySimpleGUI/PySimpleGUI/issues/415

                base_stats = ["STR","DEX","VIT","AGI","INT","MND","CHR"]
                for k in base_stats:
                    player_value = f"{k}: {int(empty_gearset.playerstats[k]):3d}{'+' + str(int(gearset.playerstats[k])-int(empty_gearset.playerstats[k])):>5s}"
                    window[f"{k.lower()} stat"].update(f"{k}: {int(gearset.playerstats[k])}")
                    window[f"{k.lower()} stat"].set_tooltip(player_value)


                player_accuracy1 = int(gearset.playerstats['Accuracy1'])
                window["acc1 stat"].update(f"{'Accuracy1:':<16s} {player_accuracy1:>4d}")
                player_accuracy2 = int(gearset.playerstats['Accuracy2']) if dual_wield else 0
                window["acc2 stat"].update(f"{'Accuracy2:':<16s} {player_accuracy2:>4d}")
                player_attack1 = int(gearset.playerstats['Attack1'])
                window["atk1 stat"].update(f"{'Attack1:':<16s} {player_attack1:>4d}")
                player_attack2 = int(gearset.playerstats['Attack2']) if dual_wield else 0
                window["atk2 stat"].update(f"{'Attack2:':<16s} {player_attack2:>4d}")
                player_rangedaccuracy = int(gearset.playerstats['Ranged Accuracy'])
                window["racc stat"].update(f"{'Ranged Accuracy:':<16s} {player_rangedaccuracy:>4d}")
                player_rangedattack = int(gearset.playerstats['Ranged Attack'])
                window["ratk stat"].update(f"{'Ranged Attack:':<16s} {player_rangedattack:>4d}")

                player_magic_accuracy = int(gearset.playerstats['Magic Accuracy'])
                window["macc stat"].update(f"{'Magic Accuracy:':<20s} {player_magic_accuracy:>4d}")
                player_matk = int(gearset.playerstats['Magic Attack'])
                window["matk stat"].update(f"{'Magic Attack:':<20s} {player_matk:>4d}")
                player_magic_damage = int(gearset.playerstats['Magic Damage'])
                window["mdmg stat"].update(f"{'Magic Damage:':<20s} {player_magic_damage:>4d}")
                magic_burst_bonus = int(gearset.playerstats['Magic Burst Damage'])
                window["mbb stat"].update(f"{'Magic Burst Bonus:':<21s} {magic_burst_bonus:>3d}")
                magic_burst_bonus2 = int(gearset.playerstats['Magic Burst Damage II'])
                window["mbb2 stat"].update(f"{'Magic Burst Bonus II:':<21s} {magic_burst_bonus2:>3d}")
                magic_burst_bonus3 = int(gearset.playerstats['Magic Burst Damage Trait'])
                window["mbb3 stat"].update(f"{'Magic Burst Trait:':<21s} {magic_burst_bonus3:>3d}")

                wsd = int(gearset.playerstats['Weaponskill Damage'])
                window["wsd stat"].update(f"{'Weapon skill damage:':<21s} {wsd:>3d}")
                ws_bonus = int(gearset.playerstats['Weaponskill Bonus'])
                window["ws bonus stat"].update(f"{'Weapon skill trait:':<21s} {ws_bonus:>3d}")
                tp_bonus = int(gearset.playerstats['TP Bonus'])
                window["tp bonus stat"].update(f"{'TP Bonus:':<20s} {tp_bonus:>4d}")


                pdl = int(gearset.playerstats['PDL'])/100
                window["pdl gear stat"].update(f"{'PDL (gear):':<20s} {pdl:>4.2f}")
                pdl_trait = int(gearset.playerstats['PDL Trait'])/100
                window["pdl trait stat"].update(f"{'PDL (trait):':<20s} {pdl_trait:>4.2f}")

                qa = int(gearset.playerstats['Zanshin'])
                window["zanshin stat"].update(f"{'Zanshin:':<21s} {qa:>3d}")

                qa = int(gearset.playerstats['QA'])
                window["qa stat"].update(f"{'Quad. Attack:':<21s} {qa:>3d}")
                ta = int(gearset.playerstats['TA'])
                window["ta stat"].update(f"{'Triple Attack:':<21s} {ta:>3d}")
                da = int(gearset.playerstats['DA'])
                window["da stat"].update(f"{'Double Attack:':<21s} {da:>3d}")
                crit_rate = int(gearset.playerstats['Crit Rate']) + 20*values["bloodrage toggle"] + 100*values["mightystrikes toggle"]
                crit_rate = 100 if crit_rate > 100 else crit_rate
                window["crit rate stat"].update(f"{'Crit. Rate:':<21s} {crit_rate:>3d}")
                crit_damage = int(gearset.playerstats['Crit Damage'])
                window["crit damage stat"].update(f"{'Crit. Damage:':<21s} {crit_damage:>3d}")

                stp = int(gearset.playerstats['Store TP'])
                window["stp stat"].update(f"{'Store TP:':<16s} {stp:>4d}")

                dw = int(gearset.playerstats['Dual Wield']) if dual_wield else 0
                window["dw stat"].update(f"{'Dual Wield:':<16s} {dw:>4d}")

                marts = int(gearset.playerstats['Martial Arts']) if gearset.gear["main"]["Skill Type"] == "Hand-to-Hand" else 0
                window["marts stat"].update(f"{'Martial Arts:':<16s} {marts:>4d}")

                gear_haste = gearset.playerstats['Gear Haste']/102.4*100
                window["gear haste stat"].update(f"{'Gear Haste:':<15s} {gear_haste:>5.1f}")
                magic_haste = gearset.playerstats['Magic Haste']*100 # Magic Haste is already using base-1024
                window["magic haste stat"].update(f"{'Magic Haste:':<15s} {magic_haste:>5.1f}")
                ja_haste = gearset.playerstats['JA Haste']/102.4*100
                window["ja haste stat"].update(f"{'JA Haste:':<15s} {ja_haste:>5.1f}")

                two_handed = ["Great Sword", "Great Katana", "Great Axe", "Polearm", "Scythe", "Staff"]
                one_handed = ["Axe", "Club", "Dagger", "Sword", "Katana","Hand-to-Hand"]
                magic = ["Elemental Magic", "Ninjutsu"]
                ranged_skills = ["Throwing", "Marksmanship", "Archery"]
                for k in sorted(one_handed+two_handed):
                    window[f"{k} skill display"].update(f"{k+':':<16s} {gearset.playerstats[f'{k} Skill']:>4d}")
                    window[f"{k} skill display"].set_tooltip(f"Total {k} skill from gear, excluding main/off-hand weapons.\nMain-hand: +{gearset.gear['main'].get(f'{k} Skill',0)}\nOff-hand: +{gearset.gear['sub'].get(f'{k} Skill',0)}")
                for k in sorted(ranged_skills+magic):
                    window[f"{k} skill display"].update(f"{k+':':<16s} {gearset.playerstats[f'{k} Skill']:>4d}")

                window["macc skill stat"].update(f"{'Magic Accuracy Skill:':<21s} {gearset.playerstats[f'Magic Accuracy Skill']-gearset.gear['sub'].get('Magic Accuracy Skill',0):>3d}")

                base_delay = 480
                delay1 = gearset.playerstats['Delay1'] + 480*(gearset.gear["main"]["Skill Type"]=="Hand-to-Hand")
                delay2 = gearset.playerstats['Delay2'] if dual_wield else delay1

                gear_haste  = 256./1024. if  gear_haste/100 > 256./1024. else  gear_haste/100
                magic_haste = 448./1024. if magic_haste/100 > 448./1024. else magic_haste/100
                ja_haste    = 256./1024. if    ja_haste/100 > 256./1024. else    ja_haste/100
                total_haste = gear_haste + magic_haste + ja_haste

                delay = (delay1+delay2)/2. # Effective weapon delay. The delay minimum is 20% of this value. delay2=delay1 if not dual wielding, the this just becomes delay1

                rdelay = (delay-marts)*(1-dw/100)*(1-total_haste) # Reduced weapon delay, including martial arts, dual wield, and all forms of haste
                rdelay = 0.2*delay if rdelay < 0.2*delay else rdelay # -80% delay cap, including Dual Wield, Martial Arts, and Haste

                delay_reduction = 1 - rdelay/delay # Should be between 0 and 0.8

                window["delay reduction stat"].update(f"{'Delay Reduction:':<16s} {(delay_reduction)*100:>4.1f}")

                daken = int(gearset.playerstats["Daken"]) if main_job=="NIN" and gearset.gear["ammo"].get("Skill Type","None") == "Throwing" else 0
                window["daken stat"].update(f"{'Daken:':<16s} {daken:>4d}")
                kickattack = int(gearset.playerstats["Kick Attacks"]) if (main_job=="MNK" or sub_job=="MNK") and gearset.gear["main"]["Skill Type"] == "Hand-to-Hand" else 0
                window["kickattack stat"].update(f"{'Kick Attacks:':<16s} {kickattack:>4d}")

                pdt = int(gearset.playerstats["PDT"]) + int(gearset.playerstats["DT"])
                pdt2 = int(gearset.playerstats["PDT2"])
                window["pdt stat"].update(f"{'Physical DT:':<16s} {pdt+pdt2:>4d}")

                mdt = int(gearset.playerstats["MDT"]) + int(gearset.playerstats["DT"]) - 29*values["whm_on"]
                window["mdt stat"].update(f"{'Magical DT:':<16s} {mdt:>4d}")

                meva = int(gearset.playerstats["Magic Evasion"])
                window["meva stat"].update(f"{'Magic Evasion:':<16s} {meva:>4d}")

                mdef = int(gearset.playerstats["Magic Def"])
                window["mdef stat"].update(f"{'Magic Def:':<16s} {mdef:>4d}")

                eva = int(gearset.playerstats["Evasion"])
                window["eva stat"].update(f"{'Evasion:':<16s} {eva:>4d}")



# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

        # Copy the best set to the initial set tab for convenience:
        if event == "copy best set":
            window["tab group"].Widget.select(0) # https://github.com/PySimpleGUI/PySimpleGUI/issues/415
            for val in values:
                if type(val) == str:
                    if "start" == val[:5]:
                        window[val].update(False)
            for slot in best_set:
                window[f"showradio {slot}"].update(image_data=item2image(best_set[slot]["Name"]))
                if f"start{slot}:{best_set[slot]['Name2']}" in window.AllKeysDict: # https://github.com/PySimpleGUI/PySimpleGUI/issues/1597
                    window[f"start{slot}:{best_set[slot]['Name2']}"].update(True)
                # window[f"showradio {slot}"].set_tooltip(best_set[slot]["Name2"])

                tooltip_stats = f"{best_set[slot]['Name2']}\n"
                ignore_stats = ["Jobs","Name","Name2","Type","Skill Type","Rank"]
                base_stats = ["STR", "DEX", "VIT", "AGI", "INT", "MND", "CHR"]
                wpn_stats = ["DMG","Delay"]
                main_stats = ["Accuracy","Attack","Ranged Accuracy","Ranged Attack","Magic Accuracy","Magic Damage","Magic Attack"]
                bonus_stats = ["Blood Pact Damage", "Kick Attacks", "Kick Attacks Attack", "Martial Arts", "Sneak Attack", "Trick Attack", "Double Shot", "True Shot","Zanshin", "Hasso", "Quick Draw", "Quick Draw II", "Triple Shot","Magic Crit Rate II","Magic Burst Accuracy","Fencer","JA Haste","Accuracy", "AGI", "Attack", "Axe Skill", "CHR", "Club Skill", "Crit Damage", "Crit Rate", "DA", "DA DMG", "Dagger Skill", "Daken", "Dark Affinity", "Dark Elemental Bonus", "Delay", "DEX", "DMG", "Dual Wield", "Earth Affinity", "Earth Elemental Bonus", "Elemental Bonus", "Elemental Magic Skill", "Fire Affinity", "Fire Elemental Bonus", "ftp", "Gear Haste", "Great Axe Skill", "Great Katana Skill", "Great Sword Skill", "Hand-to-Hand Skill", "Ice Affinity", "Ice Elemental Bonus", "INT", "Katana Skill", "Light Affinity", "Light Elemental Bonus", "Magic Accuracy Skill", "Magic Accuracy", "Magic Attack", "Magic Burst Damage II", "Magic Burst Damage", "Magic Damage", "MND", "Name", "Name2", "Ninjutsu Damage", "Ninjutsu Magic Attack", "Ninjutsu Skill", "OA2", "OA3", "OA4", "OA5", "OA6", "OA7", "OA8", "PDL", "Polearm Skill", "QA", "Ranged Accuracy", "Ranged Attack", "Scythe Skill", "Skillchain Bonus", "Staff Skill", "Store TP", "STR", "Sword Skill", "TA", "TA DMG", "Throwing Skill", "Thunder Affinity", "Thunder Elemental Bonus", "TP Bonus", "VIT", "Water Affinity", "Water Elemental Bonus", "Weaponskill Accuracy", "Weaponskill Damage", "Weather", "Wind Affinity", "Wind Elemental Bonus","Polearm Skill","Marksmanship Skill","Archery Skill"]
                def_stats = ["Evasion","Magic Evasion", "Magic Def","DT","MDT","PDT"]

                nl = False
                for k in wpn_stats:
                    if best_set[slot].get(k,False):
                        tooltip_stats += f"{k}:{best_set[slot][k]},"
                        nl = True
                    if k=="Delay" and nl:
                        tooltip_stats += "\n"

                nl = False
                for k in base_stats:
                    if best_set[slot].get(k,False):
                        tooltip_stats += f"{k}:{best_set[slot][k]},"
                        nl = True
                    if nl and k=="CHR":
                        tooltip_stats += "\n"

                nl = False
                for k in main_stats:
                    if best_set[slot].get(k,False):
                        tooltip_stats += f"{k}:{best_set[slot][k]},"
                        nl = True
                    if "Attack" in k and nl:
                        tooltip_stats += "\n"
                        nl = False
                for k in best_set[slot]:
                    if k in base_stats or k in ignore_stats or k in main_stats or k in wpn_stats or k in def_stats:
                        continue
                    tooltip_stats += f"{k}:{best_set[slot][k]}\n"

                nl = False
                for k in def_stats:
                    if best_set[slot].get(k,False):
                        tooltip_stats += f"{k}:{best_set[slot][k]}," # best_set[slot] = starting_gearset[slot]  when comparing this file to tab_inputs.py
                        nl = True
                    if "Def" in k and nl:
                        tooltip_stats += "\n" # tooltip_stats = default_tooltips[slot]
                        nl = False

                window[f"showradio {slot}"].set_tooltip(tooltip_stats)


            # Update the WS list if the weapons changed.
            skill_type_main = best_set["main"].get("Skill Type","None")
            skill_type_ranged = best_set["ranged"].get("Skill Type","None")

            main_ws_list = ws_dict.get(skill_type_main,[])
            ranged_ws_list = ws_dict.get(skill_type_ranged,[])
            updated_ws_list = sorted(main_ws_list + ranged_ws_list)
            original_ws_selection = values["select weaponskill"]

            window["select weaponskill"].update(values=updated_ws_list)
            window["select weaponskill"].update(original_ws_selection)

# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------


    # This is the except block that runs if any of the above events throws an error.
    except Exception as err:

        traceback.print_exc() # print the most recent error to the output tab.
                              # this is only the most recent. if you have a chain of errors, then you'll have to work your way up one at a time.


# window.set_min_size(window.size)
window.close()
