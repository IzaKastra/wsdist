#
# Created by Kastra on Asura.
# Feel free to /tell in game or send a PM on FFXIAH you have questions, comments, or suggestions.
#
# Version date: 2022 November 12
#
# Enemy information taken from https://w.atwiki.jp/bartlett3/pages/327.html
#
# Dho Gates triple-bats
apex_bats = {'Name': 'Apex Bats',
             'Level': 129,
             'Defense': 1142,
             'Evasion': 1043,
             'VIT': 254,
             'AGI': 356, # AGI unknown. Using value from apex_toad
             'MND': 233,
             'INT': 233,
             'CHR': 277, # CHR unknown. Using value from apex_toad
             'Magic Defense': 0,
             'Location':"Dho Gates"}

# Woh Gates toads
apex_toad = {'Name': "Apex Toad",
             'Level': 132,
             'Defense': 1239,
             'Evasion': 1133,
             'VIT': 270,
             'AGI': 356, # AGI roughly measured using Scoreboard on two different toads.
             'MND': 224,
             'INT': 293,
             'CHR': 277,
             'Magic Defense': 0,
             'Location':"Woh Gates"}

# Outer Ra'Kaznar single bats
apex_bat  = {'Name': "Apex Bat",
             'Level': 135,
             'Defense': 1338,
             'Evasion': 1224,
             'VIT': 289,
             'AGI': 356, # AGI unknown. Using value from apex_toad
             'MND': 267,
             'INT': 267,
             'CHR': 277, # CHR unknown. Using value from apex_toad
             'Magic Defense': 0,
             'Location':"Outer Ra'Kaznar"}

ozma = {"Name": "Ozma",
             'Level': 999,
             'Defense': 9999,
             'Evasion': 9999,
             'VIT': 999,
             'AGI': 999, # AGI unknown. Using value from apex_toad
             'MND': 999,
             'INT': 999,
             'CHR': 999, # CHR unknown. Using value from apex_toad
             'Magic Defense': 100,
             'Location':"Chocobo's Air Garden"}

octorok = {"Name": "Octorok",
             'Level': 1,
             'Defense': 1,
             'Evasion': 1,
             'VIT': 1,
             'AGI': 1,
             'MND': 1,
             'INT': 1,
             'CHR': 1,
             'Magic Defense': 0,
             'Location':"Hyrule"}

preset_enemies = {"Apex Bat":apex_bat, "Apex Bats":apex_bats, "Apex Toad":apex_toad, "Octorok":octorok, "Ozma":ozma, }
