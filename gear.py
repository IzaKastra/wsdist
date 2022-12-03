#
# Created by Kastra on Asura.
# Feel free to /tell in game or send a PM on FFXIAH you have questions, comments, or suggestions.
#
# Version date: 2022 December 03
#
# This file contains a list of all gear to be considered.
# "Name" is the item name as seen in-game. "Name" is used to pull the correct item ID from the equipviewer icons to create the fancy plot in the end.
# "Name2" is the same as "Name", but it includes augment paths. "Name2" is only used to distinguish between augment paths. Not all items need a "Name2". This is the reason the main code uses so many try/except blocks...
# "Skill Type" for weapons is the weapon type (katana, club, sword, etc) that gains some amount of skill.
# "Type" is used exclusively for melee, ranged, and ammo slots. "Type" is used for the code to distinguish between a grip and an off-hand weapon such that a grip in the off-hand does not trigger an off-hand attack. The options are "weapon", "grip", "ranged", "ammo", "shuriken", "throwing".
# Augmented gear shows its augmented stats as additions to the base stats. For example: Heishi has "159+7" DMG and "0+30" Accuracy when fully augmented. This isn"t necessary, but it makes the book-keeping much easier.
# "jobs" is the list of jobs that can use the item. Still in-progress, but with no immediate plans for it.

# The last dictionary key for each gear piece is the jobs that can wear it. This is used to quickly gather all pieces of gear that a job can wear to be tested. (if "nin" in jobs). Future work.
all_jobs = ["war","mnk","whm","blm","rdm","thf","pld","drk","bst","brd","rng","smn","sam","nin","drg","blu","cor","pup","dnc","sch","geo","run"]


# Convert items.lua file into a reduced weapons and armor only .txt file:
# sed "s/",ja\=.*category=/;/g" items.lua | sed "s/\,flags=.*//g" | sed "s/^.*id=//g" | sed "s/,en=\"/;/" | sed "s/\"//g" | sed "s/Weapon\,da.*/Weapon/g" | awk -F";" "{if($3=="Armor" || $3=="Weapon") print $1";"$2}" > item_list.txt


# BLM Stuff:
Amalric_Coif = {"Name":"Amalric Coif +1", "Name2":"Amalric Coif +1A",   "STR":10,"DEX":10,"VIT":10,"AGI":1,"INT":24,"MND":20,"CHR":19,"Magic Accuracy":36+20,"Magic Attack":0+20,"Magic Burst Damage":0,"Magic Burst Damage II":0,"Magic Damage":0,"Jobs":["blm","sch","rdm","geo"]}
Amalric_Doublet = {"Name":"Amalric Doublet +1", "Name2":"Amalric Doublet +1A","STR":16,"DEX":19,"VIT":16,"AGI":16,"INT":38,"MND":30,"CHR":28,"Magic Accuracy":33+20,"Magic Attack":33+20,"Magic Burst Damage":0,"Magic Burst Damage II":0,"Magic Damage":0,"Jobs":["blm","sch","rdm","geo"]}
Amalric_Gages = {"Name":"Amalric Gages +1", "Name2":"Amalric Gages +1A",  "STR":3,"DEX":23,"VIT":20,"AGI":2,"INT":24,"MND":34,"CHR":19,"Magic Accuracy":0+20,"Magic Attack":33+20,"Magic Burst Damage":0,"Magic Burst Damage II":6,"Magic Damage":0,"Jobs":["blm","sch","rdm","geo"]}
Amalric_Slops = {"Name":"Amalric Slops +1", "Name2":"Amalric Slops +1A",  "STR":19,"DEX":0,"VIT":6,"AGI":14,"INT":40,"MND":25,"CHR":19,"Magic Accuracy":0+20,"Magic Attack":40+20,"Magic Burst Damage":0,"Magic Burst Damage II":0,"Magic Damage":0,"Jobs":["blm","sch","rdm","geo"]}
Amalric_Nails = {"Name":"Amalric Nails +1", "Name2":"Amalric Nails +1A",  "STR":6,"DEX":6,"VIT":6,"AGI":26,"INT":21,"MND":20,"CHR":33,"Magic Accuracy":0+20,"Magic Attack":32,"Magic Burst Damage":0,"Magic Burst Damage II":0,"Magic Damage":20,"Jobs":["blm","sch","rdm","geo"]}

Ea_Hat = {"Name":"Ea Hat +1",                 "STR":20,"DEX":21,"VIT":24,"AGI":25,"INT":43,"MND":29,"CHR":29,"Magic Accuracy":50,"Magic Attack":38,"Magic Burst Damage":7, "Magic Burst Damage II":7,"Jobs":["blm", "rdm", "geo"]}
Ea_Houppelande = {"Name":"Ea Houppelande +1", "STR":23,"DEX":24,"VIT":26,"AGI":26,"INT":48,"MND":37,"CHR":34,"Magic Accuracy":52,"Magic Attack":44,"Magic Burst Damage":9, "Magic Burst Damage II":9,"Jobs":["blm", "rdm", "geo"]}
Ea_Cuffs = {"Name":"Ea Cuffs +1",             "STR":7,"DEX":29,"VIT":30,"AGI":0,"INT":40,"MND":40,"CHR":23,"Magic Accuracy":49,"Magic Attack":35,"Magic Burst Damage":6, "Magic Burst Damage II":6,"Jobs":["blm", "rdm", "geo"]}
Ea_Slops = {"Name":"Ea Slops +1",             "STR":26,"DEX":0,"VIT":17,"AGI":24,"INT":48,"MND":31,"CHR":23,"Magic Accuracy":51,"Magic Attack":41,"Magic Burst Damage":8, "Magic Burst Damage II":8,"Jobs":["blm", "rdm", "geo"]}
Ea_Pigaches = {"Name":"Ea Pigaches +1",       "STR":11,"DEX":14,"VIT":15,"AGI":38,"INT":5,"MND":26,"CHR":39,"Magic Accuracy":48,"Magic Attack":32,"Magic Burst Damage":5, "Magic Burst Damage II":5,"Jobs":["blm", "rdm", "geo"]}

Agwu_Cap = {"Name":"Agwu's Cap", "Name2": "Agwu's Cap R25", "STR":26,"DEX":24,"VIT":11,"AGI":5,"INT":33,"MND":26,"CHR":25, "Accuracy":40+10, "Magic Accuracy":40+10,"Magic Attack":35+23,"Magic Burst Damage":7,"Magic Burst Damage II":0,"Magic Damage":20+13,"Jobs":["blm", "sch", "geo"]}
Agwu_Robe = {"Name":"Agwu's Robe", "Name2": "Agwu's Robe R25", "STR":33,"DEX":30,"VIT":19,"AGI":20,"INT":47,"MND":37,"CHR":35, "Accuracy":40+10, "Magic Accuracy":40+10,"Magic Attack":35+23,"Magic Burst Damage":10,"Magic Burst Damage II":0,"Magic Damage":20,"Jobs":["blm", "sch", "geo"]}
Agwu_Gages = {"Name":"Agwu's Gages", "Name2": "Agwu's Gages R25", "STR":14,"DEX":38,"VIT":23,"AGI":6,"INT":33,"MND":40,"CHR":25, "Accuracy":40+10, "Magic Accuracy":40+10,"Magic Attack":35+23,"Magic Burst Damage":8,"Magic Burst Damage II":0+5,"Magic Damage":20,"Jobs":["blm", "sch", "geo"]}
Agwu_Slops = {"Name":"Agwu's Slops", "Name2": "Agwu's Slops R25", "STR":43,"DEX":0,"VIT":8,"AGI":17,"INT":49,"MND":32,"CHR":25, "Accuracy":40+10, "Magic Accuracy":40+10,"Magic Attack":35+23,"Magic Burst Damage":9,"Magic Burst Damage II":0,"Magic Damage":20,"Jobs":["blm", "sch", "geo"]}
Agwu_Pigaches = {"Name":"Agwu's Pigaches", "Name2": "Agwu's Pigaches R25", "STR":21,"DEX":25,"VIT":8,"AGI":30,"INT":30,"MND":26,"CHR":39, "Accuracy":40+10, "Magic Accuracy":40+10,"Magic Attack":35+23,"Magic Burst Damage":6,"Magic Burst Damage II":0,"Magic Damage":20,"Jobs":["blm", "sch", "geo"]}

Wicce_Petasos = {"Name":"Wicce Petasos +3", "STR":22,"DEX":25,"VIT":27,"AGI":16,"INT":39,"MND":32,"CHR":32, "Accuracy":61,"Magic Accuracy":61,"Magic Attack":51,"Magic Burst Damage":0,"Magic Burst Damage II":0,"Magic Damage":31,"Elemental Magic Skill":35,"Jobs":["blm"]}
Wicce_Coat = {"Name":"Wicce Coat +3", "STR":29,"DEX":34,"VIT":34,"AGI":34,"INT":50,"MND":43,"CHR":43, "Accuracy":64,"Magic Accuracy":64,"Magic Attack":59,"Magic Burst Damage":0,"Magic Burst Damage II":5,"Magic Damage":34,"Jobs":["blm"]}
Wicce_Gloves = {"Name":"Wicce Gloves +3", "STR":16,"DEX":40,"VIT":38,"AGI":20,"INT":38,"MND":47,"CHR":32, "Accuracy":62,"Magic Accuracy":62,"Magic Attack":57,"Magic Burst Damage":0,"Magic Burst Damage II":0,"Magic Damage":32,"Jobs":["blm"]}
Wicce_Chausses = {"Name":"Wicce Chausses +3", "STR":31,"DEX":0,"VIT":31,"AGI":31,"INT":53,"MND":38,"CHR":32, "Accuracy":63,"Magic Accuracy":63,"Magic Attack":58,"Magic Burst Damage":15,"Magic Burst Damage II":0,"Magic Damage":33,"Jobs":["blm"]}
Wicce_Sabots = {"Name":"Wicce Sabots +3", "STR":18,"DEX":21,"VIT":23,"AGI":44,"INT":36,"MND":32,"CHR":47, "Accuracy":60,"Magic Accuracy":60,"Magic Attack":50,"Magic Burst Damage":0,"Magic Burst Damage II":0,"Magic Damage":30,"Jobs":["blm"]}
Wicce_Earring = {"Name":"Wicce Earring +2", "Magic Attack":9,"Magic Damage":9,"INT":15,"MND":15,"Magic Accuracy":20,"Jobs":["blm"]}
Malignance_Earring = {"Name":"Malignance Earring","INT":8,"MND":8,"Magic Accuracy":10,"Magic Attack":8,"Jobs":["blm","rdm","sch","geo","drk"]}
Enki_Strap = {"Name":"Enki Strap", "INT":10,"MND":10,"Magic Accuracy":10, "Type":"Grip","Jobs":["blm","rdm","sch","geo"]}
Marin_Staff = {"Name":"Marin Staff +1","Name2":"Marin Staff +1 R15","INT":36,"MND":22,"Magic Accuracy":15+40,"Magic Attack":28+40,"Magic Damage":217,"Staff Skill":242, 'Skill Type': 'Staff', 'Type':'Weapon', 'DMG': 199, 'Delay': 356,"Magic Accuracy Skill":228,"Jobs":["blm","rdm","sch","geo"]}

Archmage_Petasos = {"Name":"Archmage's Petasos +3", "STR":24,"DEX":24,"VIT":24,"AGI":24,"INT":34,"MND":29,"CHR":29, "Magic Accuracy":43,"Magic Attack":55, "Elemental Magic Skill":21, "Accuracy":37,"Jobs":["blm"]}
Archmage_Coat = {"Name":"Archmage's Coat +3", "STR":31,"DEX":31,"VIT":31,"AGI":31,"INT":46,"MND":39,"CHR":39, "Magic Accuracy":40,"Magic Attack":52, "Elemental Magic Skill":24, "Accuracy":40,"Jobs":["blm"]}
Archmage_Gloves = {"Name":"Archmage's Gloves +3", "STR":16,"DEX":38,"VIT":35,"AGI":15,"INT":36,"MND":43,"CHR":29, "Magic Accuracy":38,"Magic Attack":50, "Elemental Magic Skill":23, "Accuracy":38,"Jobs":["blm"]}
Archmage_Tonbon = {"Name":"Archmage's Tonbon +3", "STR":35,"DEX":0,"VIT":22,"AGI":27,"INT":40,"MND":34,"CHR":29, "Magic Accuracy":46,"Magic Attack":58, "Magic Burst Damage II":3, "Accuracy":39,"Jobs":["blm"]}
Archmage_Sabots = {"Name":"Archmage's Sabots +3", "STR":20,"DEX":21,"VIT":20,"AGI":43,"INT":30,"MND":29,"CHR":44, "Magic Accuracy":42,"Magic Attack":54, "Elemental Magic Skill":17, "Accuracy":36,"Jobs":["blm"]}
Sorcerers_Stole = {"Name":"Sorcerer's Stole +2", "Name2":"Sorcerer's Stole +2 R25", "INT":0+15, "MND":0+15, "Magic Burst Damage":10, "Magic Accuracy":30+25, "Magic Attack":7}
Quanpur_Necklace = {"Name":"Quanpur Necklace", "Magic Attack":7, "Earth Elemental Bonus":5,"Jobs":["blm","rdm","sch","geo"]}

Taranus_Cape = {"Name":"Taranus's Cape", "Magic Burst Damage":5, "INT":30, "Magic Accuracy":30, "Magic Damage":20, "Magic Attack":10,"Jobs":["blm"]}
Freke_Ring = {"Name":"Freke Ring", "INT":10, "Magic Attack":8,"Jobs":["blm","rdm","sch","geo"]}
Regal_Earring = {"Name":"   ", "INT":10, "MND":10, "CHR":10, "Magic Attack":7,"Jobs":["blm","rdm","sch","geo"]}
Mizukage_no_Kubikazari = {"Name":"Mizukage-no-Kubikazari","INT":4, "MND":4, "Magic Attack":8, "Magic Burst Damage":10,"Jobs":["blm","rdm","sch","geo"]}
Barkarole_Earring = {"Name":"Barkarole Earring", "INT":3, "Magic Accuracy":8, "Magic Attack":8,"Jobs":["blm","sch","geo"]}
Bunzi_Rod = {"Name":"Bunzi's Rod", "Name2":"Bunzi's Rod R25", "INT":15, "MND":15, "DMG":144+10,"Delay":216,"Magic Accuracy":40+10,"Magic Attack":35+25,"Magic Damage":248,"Club Skill":242, 'Skill Type': 'Club', 'Type':'Weapon',"Magic Accuracy Skill":255,"Magic Burst Damage":10, "Accuracy":40+10,"Jobs":["blm","rdm","sch","geo"]}

Spaekona_Petasos = {"Name":"Spaekona Petasos +3", "STR":29,"DEX":29,"VIT":29,"AGI":29,"INT":37,"MND":34,"CHR":34,"Magic Accuracy":47,"Magic Damage":42,"Magic Attack":23,"Jobs":["blm"]}
Spaekona_Coat = {"Name":"Spaekona Coat +3", "STR":31,"DEX":31,"VIT":31,"AGI":31,"INT":39,"MND":39,"CHR":39,"Magic Accuracy":55,"Magic Damage":48,"Magic Attack":0,"Jobs":["blm"]}
Spaekona_Gloves = {"Name":"Spaekona Gloves +3", "STR":16,"DEX":38,"VIT":35,"AGI":15,"INT":37,"MND":43,"CHR":29,"Magic Accuracy":52,"Magic Damage":44,"Magic Attack":0,"Elemental Magic Skill":21,"Magic Burst Damage II":8,"Jobs":["blm"]}
Spaekona_Tonbon = {"Name":"Spaekona Tonbon +3", "STR":35,"DEX":0,"VIT":22,"AGI":27,"INT":44,"MND":34,"CHR":29,"Magic Accuracy":49,"Magic Damage":46,"Magic Attack":30,"Jobs":["blm"]}
Spaekona_Sabots = {"Name":"Spaekona Sabots +3", "STR":20,"DEX":21,"VIT":20,"AGI":43,"INT":32,"MND":29,"CHR":44,"Magic Accuracy":54,"Magic Damage":40,"Magic Attack":26,"Jobs":["blm"]}




Empty = {"Name": "Empty"}

Grape_Daifuku = {"Name": "Grape Daifuku", "Type":"Food","STR":2, "VIT":3, "Attack":50, "Ranged Attack":50, "Accuracy":80, "Ranged Accuracy":80, "Magic Attack":3}
Sublime_Sushi = {"Name": "Sublime Sushi", "Type":"Food","STR":6, "DEX":7, "MND":-3, "CHR":6, "Accuracy":100, "Ranged Accuracy":100}
Marine_Stewpot = {"Name": "Marine Stewpot", "Type":"Food", "Accuracy":90, "Ranged Accuracy":90, "Magic Accuracy":90}
Tropical_Crepe = {"Name": "Tropical Crepe", "Type":"Food", "Magic Accuracy":90, "INT":2, "MND":2}
all_food = [Grape_Daifuku, Sublime_Sushi,Marine_Stewpot,Tropical_Crepe]

# If adding new weapons, you must include a dictionary key for "Skill Type", "Type", "DMG", and "Delay". Use the entries already present as examples
Amanomurakumo = {"Name": "Amanomurakumo", "Name2": "Amanomurakumo R15", "Skill Type": "Great Katana", "Type":"Weapon", "DMG": 308+18, "Delay": 437, "Accuracy": 60, "Great Katana Skill": 269, "Magic Accuracy Skill": 228, "Store TP":10, "Skillchain Bonus":5, "Jobs":["sam"]}
Anguta = {"Name": "Anguta", "Name2": "Anguta R15", "Skill Type": "Scythe", "Type":"Weapon", "DMG":370+17, "Delay":528, "Magic Damage":186, "Scythe Skill":269, "TP Bonus": 500, "Magic Accuracy Skill":242, "Accuracy":0+30, "Magic Accuracy":0+30, "Store TP":10,"Jobs":["drk"]}
Apocalypse = {"Name": "Apocalypse", "Name2": "Apocalypse R15", "Skill Type": "Scythe", "Type":"Weapon", "DMG":362+21, "Delay":513, "Magic Damage":217, "Scythe Skill":269, "Magic Accuracy Skill":242, "Accuracy":60+15, "JA Haste":10,"Jobs":["drk"]}
Caladbolg = {"Name": "Caladbolg", "Name2": "Caladbolg R15", "Skill Type": "Great Sword", "Type":"Weapon", "DMG":303+11, "Delay":430, "Magic Damage":155, "Great Sword Skill":269, "Magic Accuracy Skill":242,"VIT":50+20,"STR":0+20,"Jobs":["drk"]}
Crepuscular_Knife = {"Name": "Twilight Knife", "Name2": "Crepuscular Knife", "Skill Type": "Dagger", "Type":"Weapon", "DMG":133, "Delay":190, "DEX":15, "AGI":15, "CHR":15, "Accuracy":40, "Magic Accuracy":40, "Dagger Skill":248, "Magic Accuracy Skill":248, "QA":5, "Jobs":["nin"]}
Dojikiri = {"Name": "Dojikiri Yasutsuna","Name2": "Dojikiri Yasutsuna R15", "Skill Type": "Great Katana", "Type":"Weapon", "DMG": 315+15, "Delay": 450, "Store TP": 10, "Accuracy": 0+30, "Magic Accuracy":0+30, "TP Bonus": 500, "Great Katana Skill": 269, "Magic Accuracy Skill": 228, "Magic Damage": 155, "Jobs":["sam"]}
Gleti_Knife = {"Name": "Gleti's Knife", "Name2": "Gleti's Knife R25", "Skill Type": "Dagger", "Type":"Weapon", "DMG":133+10, "Delay":200, "DEX":15, "AGI":15, "Accuracy":40+10, "Attack":30+40, "Magic Accuracy":40+10, "Dagger Skill":255, "Magic Accuracy Skill":242,"Crit Rate":5,"TA":6, "Jobs":["nin","thf","dnc"]}
Gokotai = {"Name": "Gokotai", "Name2": "Gokotai", "Skill Type": "Katana", "Type":"Weapon", "DMG": 157, "Delay": 227, "Katana Skill": 250, "Magic Accuracy Skill": 250, "Magic Damage": 217, "DEX": 15, "AGI":15, "INT":15, "Accuracy": 40, "Attack": 30, "Ranged Accuracy": 40, "Magic Accuracy": 40, "Magic Attack": 16, "Jobs":["nin"]}
Hachimonji = {"Name": "Hachimonji", "Name2": "Hachimonji", "Skill Type": "Great Katana", "Type":"Weapon", "DMG": 318, "Delay":450, "STR":20, "DEX":20, "VIT":20, "Accuracy":40, "Attack":30, "Magic Accuracy":40, "Great Katana Skill":250, "Magic Accuracy Skill":250, "Jobs":["nin","sam"]}
Heishi = {"Name": "Heishi Shorinken", "Name2": "Heishi Shorinken R15", "Skill Type": "Katana", "Type":"Weapon", "DMG": 159+7, "Delay": 227, "Store TP": 10, "Accuracy": 0+30, "Magic Accuracy":0+30, "TP Bonus": 500, "Katana Skill": 269, "Magic Accuracy Skill": 242, "Magic Damage": 186, "Jobs":["nin"]}
Hitaki = {"Name": "Hitaki", "Name2": "Hitaki", "Skill Type": "Katana", "Type":"Weapon", "DMG":  49, "Delay": 216, "TP Bonus": 1000, "Katana Skill": 0, "Jobs":["nin"]}
Kannagi = {"Name": "Kannagi", "Name2": "Kannagi R15", "Skill Type": "Katana", "Type":"Weapon", "DMG": 148+5, "Delay": 210, "Katana Skill": 269, "Magic Accuracy Skill": 242, "Magic Damage": 186, "DEX": 0+20, "AGI":50+20, "Jobs":["nin"]}
Kikoku = {"Name": "Kikoku", "Name2": "Kikoku R15", "Skill Type": "Katana", "Type":"Weapon", "DMG": 148+8, "Delay": 210, "Attack": 60, "Katana Skill": 269, "Magic Accuracy Skill": 242, "Magic Damage": 186, "Jobs":["nin"]}
Kogarasumaru = {"Name": "Kogarasumaru", "Name2": "Kogarasumaru R15", "Skill Type": "Great Katana", "Type":"Weapon", "DMG": 281+29, "Delay": 450, "Accuracy": 0+30, "Magic Accuracy":0+30, "Great Katana Skill": 269, "Magic Accuracy Skill": 228, "Jobs":["sam"]}
Kraken_Club = {"Name": "Kraken Club", "Name2": "Kraken Club", "Skill Type": "Club", "Type":"Weapon", "DMG":11, "Delay":264, "OA2":15, "OA3":25, "OA4":25, "OA5":15, "OA6":10, "OA7":3, "OA8":2, "Jobs":["nin","drk","sam"]}
Kujaku = {"Name": "Kujaku", "Name2": "Kujaku", "Skill Type": "Katana", "Type":"Weapon", "DMG":118, "Delay":227, "Accuracy":15,"Katana Skill":242,"Magic Accuracy Skill":242, "Jobs":["nin"]}
Kunimitsu = {"Name": "Kunimitsu", "Name2": "Kunimitsu R25", "Skill Type": "Katana", "Type":"Weapon", "DMG":151+11, "Delay":227, "DEX":15, "AGI":15, "Accuracy":40+10, "Attack":30+40, "Ranged Accuracy":40, "Magic Accuracy":40+10,"Magic Attack":20, "Magic Damage":217, "Magic Burst Damage":10,"Store TP":5, "Magic Accuracy Skill":248, "Katana Skill": 248, "Weaponskill Damage":5, "Jobs":["nin"]}
Liberator = {"Name": "Liberator", "Name2": "Liberator R15", "Skill Type": "Scythe", "Type":"Weapon", "DMG":330+34, "Delay":528, "Magic Accuracy":50+30, "Magic Damage":217, "Scythe Skill":269, "Magic Accuracy Skill":242, "Accuracy":0+30,"Jobs":["drk"]}
Masamune = {"Name": "Masamune", "Name2": "Masamune R15", "Skill Type": "Great Katana", "Type":"Weapon", "DMG": 308+11, "Delay": 437, "Great Katana Skill": 269, "Magic Accuracy Skill": 228, "AGI": 0+20, "STR":50+20, "Jobs":["sam"]}
Naegling = {"Name": "Naegling", "Name2": "Naegling", "Skill Type": "Sword", "Type":"Weapon", "DMG": 166, "Delay": 240, "Sword Skill": 250, "Magic Accuracy Skill": 250, "Magic Damage": 217, "DEX": 15, "MND":15, "INT":15, "Accuracy": 40, "Attack": 30, "Magic Accuracy": 40, "Magic Attack": 16, "Jobs":["nin","drk"]}
Nagi = {"Name": "Nagi", "Name2": "Nagi R15", "Skill Type": "Katana", "Type":"Weapon", "DMG": 142+14, "Delay": 227, "Accuracy": 0+30, "Magic Accuracy":40+30, "Katana Skill": 269, "Magic Accuracy Skill": 242, "Magic Damage": 186, "Jobs":["nin"]}
Ragnarok = {"Name": "Ragnarok", "Name2": "Ragnarok R15", "Skill Type": "Great Sword", "Type":"Weapon", "DMG":304+17, "Delay":431, "Magic Damage":155, "Great Sword Skill":269, "Magic Accuracy Skill":242,"DEX":0+15,"STR":35+15,"MND":35+15,"INT":0+15,"Jobs":["drk"]}
Redemption = {"Name": "Redemption", "Name2": "Redemption R15", "Skill Type": "Scythe", "Type":"Weapon", "DMG":354+13, "Delay":502, "Magic Damage":217, "Scythe Skill":269, "Magic Accuracy Skill":242,"DEX":0+15,"STR":35+15,"MND":35+15,"INT":0+15,"Jobs":["drk"]}
Shining_One = {"Name": "Shining One", "Name2": "Shining One", "Skill Type": "Polearm", "Type": "Weapon", "DMG":333, "Delay":480, "STR":20, "INT":20, "MND":20, "Accuracy":40, "Attack":30, "Magic Accuracy":40, "Magic Attack":21, "Magic Damage":226, "Polearm Skill":250, "Magic Accuracy Skill":250 , "Jobs":["sam","drg"]}
Tauret = {"Name": "Tauret", "Name2": "Tauret", "Skill Type": "Dagger", "Type":"Weapon", "DMG": 125, "Delay": 180, "Dagger Skill": 250, "Magic Accuracy Skill": 250, "Magic Damage": 217, "DEX": 15, "MND":15, "INT":15, "Accuracy": 40, "Attack": 30, "Magic Accuracy": 40, "Magic Attack": 16, "Jobs":["nin","thf","dnc","rdm"]}
Ternion = {"Name": "Ternion Dagger +1","Name2": "Ternion Dagger +1 R15", "Skill Type": "Dagger", "Type":"Weapon", "DMG": 100+17, "Delay": 175, "Accuracy":27+40, "Magic Accuracy":0+40, "Dagger Skill":228, "Magic Accuracy Skill":188, "TA":4, "AGI":14, "Weaponskill Damage":5, "Jobs":["nin","thf","dnc","rdm"]}
Tsuru = {"Name": "Tsuru", "Name2": "Tsuru R25", "Skill Type": "Katana", "Type":"Weapon", "DMG":131, "Delay":190,"VIT":15,"AGI":15,"Accuracy":40,"Ranged Accuracy":40, "Katana Skill":242, "Magic Accuracy Skill":242,"Daken":8, "Jobs":["nin"]}
MalevolenceA = {"Name": "Malevolence","Name2": "MalevolenceA", "Skill Type":"Dagger","Type":"Weapon","DMG":94,"Delay":201,"INT":0+10,"Magic Accuracy":25+10, "Magic Attack":34+10, "Magic Damage":118, "Magic Accuracy Skill":201, "Dagger Skill":242,"Jobs":["nin","thf","dnc","rdm","drk"]}
MalevolenceB = {"Name": "Malevolence","Name2": "MalevolenceB", "Skill Type":"Dagger","Type":"Weapon","DMG":94,"Delay":201,"INT":0+10,"Magic Accuracy":25+10, "Magic Attack":34+10, "Magic Damage":118, "Magic Accuracy Skill":201, "Dagger Skill":242,"Jobs":["nin","thf","dnc","rdm","drk"]}
#Karambit = {"Name": "Karambit" "Skill Type":"Hand-to-Hand", "Type":"Weapon", "DMG":"Base+180","Delay":"base+96", "STR":20, "DEX":20,"VIT":20,"Accuracy":40,"Attack":30,"Magic Accuracy":40,"Hand-to-Hand Skill":250, "Magic Accuracy Skill":250}

Alber_Strap = {"Name": "Alber Strap", "Type": "Grip", "Magic Attack":7, "DA":2,"Jobs":all_jobs}
Rigorous_Grip = {"Name": "Rigorous Grip +1", "Name2": "Rigorous Grip +1 R15", "Type":"Grip", "STR":4+15, "Attack":13+30, "Accuracy":3,"Jobs":all_jobs}
Utu_Grip = {"Name": "Utu Grip", "Type": "Grip", "Accuracy":30, "Attack":30,"Jobs":["drk","sam"]}

mains = [Heishi, Kannagi, Kikoku, Nagi, Gokotai, MalevolenceA, Tauret, Naegling, Anguta, Liberator, Apocalypse, Redemption]
subs = [Ternion, Kunimitsu, Gleti_Knife, Tauret, Gokotai, Crepuscular_Knife, MalevolenceB, Hitaki]
grips = [Rigorous_Grip, Utu_Grip]

mains = [Anguta,Apocalypse,Crepuscular_Knife,Gleti_Knife,Gokotai,Hachimonji,Heishi,Kannagi,Kikoku,Kunimitsu,Liberator,Naegling,Nagi,Redemption,Tauret,Ternion,Tsuru,MalevolenceA,MalevolenceB,Ragnarok,Caladbolg]
subs = [Crepuscular_Knife,Gleti_Knife,Gokotai,Hitaki,Kunimitsu,Tauret,Ternion,Tsuru,MalevolenceA,MalevolenceB,]



Date = {"Name": "Date Shuriken", "Skill Type": "Throwing", "DMG": 125, "Delay": 192, "Accuracy": 5, "Ranged Accuracy": 5, "Throwing Skill": 242, "DEX": 5, "AGI": 5, "Jobs":["nin"]}
Happo = {"Name": "Happo Shuriken", "Skill Type": "Throwing", "DMG":  99, "Delay": 188, "Accuracy": 6, "Attack": 6, "Ranged Accuracy": 11, "Throwing Skill": 228, "Crit Rate": 2, "Jobs":["nin"]}
Seki = {"Name": "Seki Shuriken", "Skill Type": "Throwing", "DMG": 101, "Delay": 192, "Attack": 13, "Store TP": 2, "Throwing Skill": 242, "Jobs":["nin"]}
Donar_Gun = {"Name": "Donar Gun", "DEX":5, "AGI":5, "Thunder Elemental Bonus": 15, "Jobs":["nin"]} 

Aurgelmir_Orb = {"Name": "Aurgelmir Orb +1", "STR":7, "DEX":7, "VIT":7, "Attack":10, "Store TP":5, "Jobs":["nin","drk","sam","rdm","drg"]}
Cath_Palug_Stone = {"Name": "Cath Palug Stone", "DEX":10, "AGI":10, "Accuracy":15, "Jobs":["nin","thf","dnc","run"]}
Coiste_Bodhar = {"Name": "Coiste Bodhar", "Name2": "Coiste Bodhar R25", "Attack":15,"STR":8,"DA":3,"Store TP":3,"Jobs":["nin","drk","sam","drg","rdm"]}
Crepuscular_Pebble = {"Name": "Ghastly Tathlum", "Name2": "Crepuscular Pebble", "STR":3, "VIT":3, "PDL":3, "Jobs":all_jobs}
Ghastly_Tathlum = {"Name": "Ghastly Tathlum +1", "Name2": "Ghastly Tathlum +1 R15", "Magic Damage":11+10, "INT":6+5, "Jobs":all_jobs}
Knobkierrie = {"Name": "Knobkierrie", "Attack":23, "Weaponskill Damage":6, "Jobs":["drk","sam"]}
Oshashas_Treatise = {"Name":"Oshasha's Treatise","Accuracy":5,"Attack":5,"Weaponskill Damage":3,"Jobs":all_jobs}
Pemphredo_Tathlum = {"Name": "Pemphredo Tathlum", "INT":4, "Magic Accuracy":8, "Magic Attack":4, "Jobs":all_jobs}
Seething_Bomblet = {"Name": "Seething Bomblet +1", "Name2": "Seeth. Bomblet +1 R15", "Accuracy":13, "Attack":13, "Magic Attack":7, "STR":4+10, "Gear Haste":0+4, "Jobs":["nin","drk","sam"]}
Yetshila = {"Name": "Yetshila +1", "Crit Rate":2, "Crit Damage":6, "Jobs":["nin","drk"]}
ammos = [Yetshila, Seething_Bomblet, Cath_Palug_Stone, Aurgelmir_Orb, Pemphredo_Tathlum, Ghastly_Tathlum, Crepuscular_Pebble, Coiste_Bodhar, Oshashas_Treatise]
ammos = [Seki, Happo, Date, Aurgelmir_Orb,Cath_Palug_Stone,Coiste_Bodhar,Crepuscular_Pebble,Ghastly_Tathlum,Knobkierrie,Oshashas_Treatise,Pemphredo_Tathlum,Seething_Bomblet,Yetshila,]

Adhemar_Bonnet_A = {"Name": "Adhemar Bonnet +1", "Name2": "Adhemar Bonnet +1 A", "STR":19, "DEX":21+12, "VIT":15, "AGI":19+12, "INT":14, "MND":14, "CHR":14, "Accuracy":0+20, "Attack":36, "Ranged Attack":36, "Gear Haste":8, "TA":4, "Crit Damage":6,"Jobs":["nin"]}
Adhemar_Bonnet_B = {"Name": "Adhemar Bonnet +1", "Name2": "Adhemar Bonnet +1 B", "STR":19+12, "DEX":21+12, "VIT":15, "AGI":19, "INT":14, "MND":14, "CHR":14, "Attack":36+20, "Ranged Attack":36, "Gear Haste":8, "TA":4, "Crit Rate": 6,"Jobs":["nin"]}
Blistering_Sallet = {"Name": "Blistering Sallet +1", "Name2": "Blistering Sallet +1 R15", "STR":16+25, "DEX":16+25, "VIT":16, "AGI":16, "INT":16, "MND":16, "CHR":16, "Accuracy":6+45, "Magic Accuracy":0+45, "Gear Haste":8, "DA":3, "Crit Rate":10,"Jobs":all_jobs}
Dampening_Tam = {"Name": "Dampening Tam", "STR":18, "DEX":24+10, "VIT":18, "AGI":20, "INT":18, "MND":22, "CHR":18, "Accuracy":20+15,"Ranged Accuracy":20,"Magic Accuracy":20+15,"Gear Haste":7,"QA":3,"Jobs":["nin"]}
Flamma_Zucchetto = {"Name": "Flamma Zucchetto +2", "STR":36,"DEX":32,"VIT":24,"AGI":16,"INT":12,"MND":12,"CHR":12,"Accuracy":44,"Magic Accuracy":44,"Gear Haste":4,"Store TP":6,"TA":5,"Jobs":["drk","sam"]}
Hachiya_Hatsuburi = {"Name": "Hachiya Hatsuburi +3", "STR": 33, "DEX": 33, "VIT":32, "AGI":32, "INT":31, "MND":31, "CHR": 31, "Magic Accuracy": 54, "Ninjutsu Skill": 17, "Gear Haste": 8, "Weaponskill Damage":10,"Jobs":["nin"]}
Hizamaru_Somen = {"Name": "Hizamaru Somen +2", "STR":33, "DEX":29, "VIT":27, "AGI":24, "INT":12, "MND":10, "CHR":20, "Accuracy":20, "Attack":26, "Gear Haste":6,"Jobs":["nin","sam"]}
Kendatsuba_Jinpachi = {"Name": "Kendatsuba Jinpachi +1", "STR":23,"DEX":47,"VIT":32,"AGI":34,"INT":19,"MND":17,"CHR":19,"Accuracy":50,"Ranged Accuracy":45,"Gear Haste":6,"TA":4,"Crit Rate":5,"Jobs":["nin","sam"]}
Malignance_Chapeau = {"Name": "Malignance Chapeau", "STR":11,"DEX":40,"VIT":19,"AGI":33,"INT":25,"MND":16,"CHR":17,"Accuracy":50,"Ranged Accuracy":50,"Magic Accuracy":50,"Gear Haste":6,"Store TP":8,"PDL":3,"Jobs":["nin"]}
Mochizuki_Hatsuburi = {"Name": "Mochizuki Hatsuburi +3", "STR":31, "DEX":31, "VIT":33, "AGI":33, "INT":32, "MND":32, "CHR":32, "Accuracy":44,"Attack":62,"Magic Accuracy": 37, "Magic Attack": 61, "Gear Haste": 8, "Ninjutsu Magic Attack": 21,"Jobs":["nin"]}
Mpaca_Cap = {"Name": "Mpaca's Cap", "Name2": "Mpaca's Cap R25", "STR":33, "DEX":30, "VIT":26, "AGI":24, "INT":20, "MND":17, "CHR":20,"Accuracy":40+10,"Attack":40+25,"Magic Accuracy":40+10,"Gear Haste":6,"TA":3,"Crit Rate":4,"TP Bonus":200,"Jobs":["nin","sam"]}
Mummu_Bonnet = {"Name": "Mummu Bonnet +2", "STR":20,"DEX":39,"VIT":16,"AGI":34,"INT":15,"MND":14,"CHR":17,"Accuracy":44,"Ranged Accuracy":44,"Magic Accuracy":44,"Gear Haste":8,"Crit Rate":5,"Jobs":["nin"]}
Nyame_Helm = {"Name": "Nyame Helm", "Name2": "Nyame Helm R25 B", "STR":26, "DEX":25, "VIT":24, "AGI":23, "INT":28, "MND":26, "CHR":24,"Accuracy":40,"Attack":30+30, "Gear Haste":6,"Weaponskill Damage":0+10,"DA":0+4,"Magic Accuracy":40,"Magic Attack":30,"Ranged Accuracy":40,"Ranged Attack":30+30,"Magic Burst Damage":5,"Jobs":all_jobs}
Pixie_Hairpin = {"Name": "Pixie Hairpin +1", "INT":27, "Dark Elemental Bonus":28,"Jobs":all_jobs}
Ratri_Sallet = {"Name": "Ratri Sallet +1", "STR":40, "DEX":33, "VIT":26, "AGI":21, "INT":26, "MND":23, "CHR":22, "Magic Accuracy":45, "Scythe Skill":54, "Gear Haste":7, "Weaponskill Damage":8,"Jobs":["drk"]}
Ryuo_Somen_A = {"Name": "Ryuo Somen +1", "Name2": "Ryuo Somen +1 A", "STR":21+12, "DEX":17+12, "VIT":14, "AGI":20, "INT":11, "MND":11, "CHR":11, "Accuracy":35+20,"Ranged Accuracy":35,"Gear Haste":7,"Store TP":7,"Dual Wield":9,"Jobs":all_jobs}
Sakpata_Helm = {"Name": "Sakpata's Helm", "Name2": "Sakpata's Helm R25", "STR":33,"DEX":20,"VIT":40,"AGI":21,"INT":19,"MND":23,"CHR":21,"Accuracy":40+10,"Magic Accuracy":40+10,"Attack":40+25,"Gear Haste":4,"DA":5,"PDL":5,"DA DMG":0+13,"Jobs":["drk"]}
Sulevia_Mask = {"Name": "Sulevia's Mask +2", "STR":33,"DEX":19,"VIT":40,"AGI":12,"INT":11,"MND":22,"CHR":22,"Accuracy":44,"Attack":48,"Gear Haste":3,"Store TP":10,"Jobs":["drk"]}
Hattori_Zukin = {"Name": "Hattori Zukin +3", "STR":31,"DEX":41,"VIT":28,"AGI":34,"INT":27,"MND":27,"CHR":27,"Accuracy":61,"Attack":61,"Ranged Accuracy":61,"Magic Accuracy":61,"Gear Haste":10,"Dual Wield":7,"Jobs":["nin"]}
Heathen_Burgeonet = {"Name": "Heathen's Burgeonet +3", "STR":42,"DEX":26,"VIT":33,"AGI":28,"INT":31,"MND":27,"CHR":29,"Accuracy":61,"Attack":61,"Magic Accuracy":61,"Gear Haste":7,"Scythe Skill":38,"DA":6,"PDL":10,"Jobs":["drk"]}
heads = [Adhemar_Bonnet_A,Adhemar_Bonnet_B, Hachiya_Hatsuburi, Mochizuki_Hatsuburi, Malignance_Chapeau, Kendatsuba_Jinpachi, Mummu_Bonnet, Nyame_Helm, Mpaca_Cap, Blistering_Sallet,Hattori_Zukin]
heads = [Adhemar_Bonnet_A,Adhemar_Bonnet_B,Blistering_Sallet,Flamma_Zucchetto,Hachiya_Hatsuburi,Kendatsuba_Jinpachi,Malignance_Chapeau,Mpaca_Cap,Mummu_Bonnet,Nyame_Helm,Ratri_Sallet,Ryuo_Somen_A,Sakpata_Helm,Sulevia_Mask,Hattori_Zukin,Heathen_Burgeonet,Mochizuki_Hatsuburi]
heads = [Adhemar_Bonnet_A,Adhemar_Bonnet_B,Blistering_Sallet,Dampening_Tam,Flamma_Zucchetto,Hachiya_Hatsuburi,Hizamaru_Somen,Kendatsuba_Jinpachi,Malignance_Chapeau,Mochizuki_Hatsuburi,Mpaca_Cap,Mummu_Bonnet,Nyame_Helm,Pixie_Hairpin,Ratri_Sallet,Ryuo_Somen_A,Sakpata_Helm,Sulevia_Mask,Hattori_Zukin,Heathen_Burgeonet,]


Abyssal_Beads = {"Name": "Abyssal Bead Necklace +2", "Name2":"Abyssal Bead Necklace +2 R25","Accuracy":15,"Magic Accuracy":15,"Attack":40,"Store TP":0+7,"STR":0+25,"Crit Rate":4,"PDL":0+10,"Jobs":["drk"]}
Baetyl_Pendant = {"Name": "Baetyl Pendant", "Magic Attack":13, "Jobs":all_jobs}
Caro_Necklace = {"Name": "Caro Necklace", "STR":6,"DEX":6,"Attack":10, "Jobs":all_jobs}
Fotia_Gorget = {"Name": "Fotia Gorget", "Weaponskill Accuracy": 10, "ftp": 25./256., "Jobs":all_jobs}
Ninja_Nodowa = {"Name": "Ninja Nodowa +2", "Name2": "Ninja Nodowa +2 R25", "Accuracy": 25, "Ranged Accuracy": 25, "Store TP": 7, "DEX":15, "AGI":15, "Daken":25, "PDL":10, "Jobs":["nin"]}
Rep_Plat_Medal = {"Name": "Republican Platinum Medal", "STR":10, "Attack":30, "Ranged Attack":30,"Jobs":all_jobs}
Samurai_Nodowa = {"Name": "Samurai's Nodowa +2", "Name2":"Samurai's Nodowa +2 R25", "Accuracy":30, "Store TP":7+7, "STR":0+25, "PDL":0+10, "Jobs":["sam"]}
Sanctity_Necklace = {"Name": "Sanctity Necklace", "Attack":10,"Ranged Attack":10,"Ranged Accuracy":10,"Magic Accuracy":10,"Magic Attack":10, "Jobs":all_jobs}
Sibyl_Scarf = {"Name": "Sibyl Scarf", "INT":10, "Magic Attack":10,"Jobs":all_jobs}
Warders_Charm = {"Name": "Warder's Charm +1", "Name2": "Warder's Charm +1 R15","Magic Burst Damage":10,"Jobs":all_jobs}
necks = [Ninja_Nodowa, Fotia_Gorget, Caro_Necklace, Baetyl_Pendant, Rep_Plat_Medal,Sibyl_Scarf,Warders_Charm]
necks = [Abyssal_Beads,Baetyl_Pendant,Caro_Necklace,Fotia_Gorget,Ninja_Nodowa,Rep_Plat_Medal,Samurai_Nodowa, Sanctity_Necklace,Sibyl_Scarf,]
necks = [Abyssal_Beads,Baetyl_Pendant,Caro_Necklace,Fotia_Gorget,Ninja_Nodowa,Rep_Plat_Medal,Sanctity_Necklace,Sibyl_Scarf,Warders_Charm]

Balder_Earring = {"Name": "Balder Earring +1", "Attack":10, "Store TP":3, "QA":1, "Jobs":all_jobs}
Brutal_Earring = {"Name": "Brutal Earring", "DA":5,"Store TP":1, "Jobs":all_jobs}
Cessance_Earring = {"Name": "Cessance Earring", "Accuracy":6, "DA":3, "Store TP":3, "Jobs":all_jobs}
Crematio_Earring = {"Name": "Crematio Earring", "Magic Attack":6,"Magic Damage":6, "Jobs":all_jobs}
Crepuscular_Earring = {"Name": "Crepuscular Earring", "Accuracy":10, "Ranged Accuracy":10, "Magic Accuracy":10, "Store TP":5,"Jobs":all_jobs}
Dedition_Earring = {"Name": "Dedition Earring", "Accuracy":-10, "Ranged Accuracy":-10, "Attack":-10, "Ranged Attack":-10, "Store TP":8, "Jobs":all_jobs}
Dignitary_Earring = {"Name": "Dignitary's Earring", "Accuracy":10,"Magic Accuracy":10,"Store TP":3, "Jobs":all_jobs}
Eabani_Earring = {"Name": "Eabani Earring", "Dual Wield":4, "Jobs":all_jobs}
Friomisi_Earring = {"Name": "Friomisi Earring", "Magic Attack":10, "Jobs":all_jobs}
Ishvara_Earring = {"Name": "Ishvara Earring", "Weaponskill Damage":2, "Jobs":all_jobs}
Lugra_Earring_Aug = {"Name": "Lugra Earring +1", "Name2": "Lugra Earring +1 R15 (day)", "STR":0+8,"DEX":0+8,"VIT":0+8,"INT":0+8,"DA":3, "Jobs":["war","pld","drk","bst","sam","nin"]}
Mache_Earring1 = {"Name": "Mache Earring +1", "Name2": "Mache Earring +1A", "DEX":8,"Accuracy":10,"DA":2, "Jobs":all_jobs}
Mache_Earring2 = {"Name": "Mache Earring +1", "Name2": "Mache Earring +1B", "DEX":8,"Accuracy":10,"DA":2, "Jobs":all_jobs}
Moonshade_Earring = {"Name": "Moonshade Earring", "Accuracy":4, "TP Bonus":250, "Jobs":all_jobs}
Odr_Earring = {"Name": "Odr Earring", "DEX":10,"Accuracy":10,"Crit Rate":5, "Jobs":["mnk","thf","rng","nin","blu","cor","dnc","run"]}
Schere_Earring = {"Name": "Schere Earring", "Name2":"Schere Earring R25", "STR":5, "DA":6, "Accuracy":15, "Attack":10, "Jobs":["war","mnk","drk","sam","pup"]}
Static_Earring = {"Name": "Static Earring", "MND":2, "Magic Burst Damage":5, "Jobs":all_jobs}
Suppanomimi = {"Name": "Suppanomimi", "AGI":2,"Dual Wield":5,"Sword Skill":5, "Jobs":all_jobs}
Telos_Earring = {"Name": "Telos Earring", "Accuracy":10, "Attack":10, "Ranged Accuracy":10, "Ranged Attack":10, "DA":1, "Store TP":5, "Jobs":all_jobs}
Thrud_Earring = {"Name": "Thrud Earring", "STR":10, "VIT":10, "Weaponskill Damage":3, "Jobs":["war","pld","drk","bst","sam","drg"]}
Hattori_Earring = {"Name": "Hattori Earring +2", "PDL":9, "Throwing Skill":12, "Katana Skill":12, "Accuracy":18, "Magic Accuracy":18, "Store TP":7, "DEX":11, "AGI":11, "Jobs":["nin"]}
Heathen_Earring = {"Name": "Heathen's Earring +2", "Attack":20, "PDL":9, "Accuracy":18, "Weaponskill Damage":6, "STR":11, "INT":11, "Jobs":["drk"]}
ears = [Static_Earring,Ishvara_Earring, Lugra_Earring_Aug, Moonshade_Earring, Brutal_Earring, Friomisi_Earring, Crematio_Earring, Balder_Earring, Mache_Earring1, Mache_Earring2, Odr_Earring, Crepuscular_Earring,Telos_Earring]
ears2 = [Static_Earring, Ishvara_Earring, Lugra_Earring_Aug, Moonshade_Earring, Brutal_Earring, Friomisi_Earring, Crematio_Earring, Balder_Earring, Mache_Earring1, Mache_Earring2, Odr_Earring, Crepuscular_Earring,Hattori_Earring,Telos_Earring,Heathen_Earring]

ears = [Brutal_Earring,Cessance_Earring,Crematio_Earring,Friomisi_Earring,Ishvara_Earring,Lugra_Earring_Aug,Mache_Earring1,Mache_Earring2,Moonshade_Earring,Odr_Earring,Schere_Earring,Thrud_Earring]
ears2 = [Balder_Earring,Brutal_Earring,Cessance_Earring,Crematio_Earring,Friomisi_Earring,Ishvara_Earring,Lugra_Earring_Aug,Mache_Earring1,Mache_Earring2,Moonshade_Earring,Odr_Earring,Schere_Earring,Thrud_Earring,Hattori_Earring,Heathen_Earring]

ears = [Suppanomimi,Dedition_Earring,Telos_Earring,Eabani_Earring,Cessance_Earring, Balder_Earring,Brutal_Earring,Crematio_Earring,Friomisi_Earring,Ishvara_Earring,Lugra_Earring_Aug,Mache_Earring1,Mache_Earring2,Moonshade_Earring,Odr_Earring,Schere_Earring,Static_Earring,Thrud_Earring]
ears2 = [Suppanomimi,Dedition_Earring,Telos_Earring,Eabani_Earring,Cessance_Earring, Balder_Earring,Brutal_Earring,Crematio_Earring,Friomisi_Earring,Ishvara_Earring,Lugra_Earring_Aug,Mache_Earring1,Mache_Earring2,Moonshade_Earring,Odr_Earring,Schere_Earring,Static_Earring,Thrud_Earring,Hattori_Earring,Heathen_Earring,]

Abnoba_Kaftan = {"Name": "Abnoba Kaftan", "STR":25, "DEX":38, "VIT":24, "AGI":28, "INT":21, "MND":21, "CHR":21, "Accuracy":22, "Attack":22, "Gear Haste":4, "Crit Rate":5, "Crit Damage":5,"Jobs":["nin"]}
Adhemar_Jacket_A = {"Name": "Adhemar Jacket +1", "Name2": "Adhemar Jacket +1 A", "STR":26, "DEX":33+12, "VIT":23, "AGI":29+12, "INT":20, "MND":20, "CHR":20, "Accuracy":35+20, "Attack":35, "Ranged Accuracy":35, "Ranged Attack":35, "Gear Haste":4, "TA":4, "Dual Wield":6,"Jobs":["nin"]}
Adhemar_Jacket_B = {"Name": "Adhemar Jacket +1", "Name2": "Adhemar Jacket +1 B", "STR":26+12, "DEX":33+12, "VIT":23, "AGI":29, "INT":20, "MND":20, "CHR":20, "Accuracy":35, "Attack":35+20, "Ranged Accuracy":35, "Ranged Attack":35, "Gear Haste":4, "TA":4, "Dual Wield":6,"Jobs":["nin"]}
Agony_Jerkin = {"Name": "Agony Jerkin +1", "Name2": "Agony Jerkin +1 R15", "STR":24+10, "DEX":35+10, "VIT":24+10, "AGI":28+10, "INT":23+10, "MND":23+10, "CHR":23+10, "Attack":23+60, "Gear Haste":4, "Accuracy":14, "Store TP":0+10,"Jobs":["nin"]}
Ashera_Harness = {"Name": "Ashera Harness", "STR":30, "DEX":40, "VIT":30, "AGI":30, "INT":30, "MND":30, "CHR":40, "Accuracy":45, "Attack":45, "Gear Haste":4, "Store TP":10,"Jobs":["nin"]}
Dagon_Breastplate = {"Name": "Dagon Breastplate", "STR":40,"DEX":30,"VIT":40,"AGI":30,"INT":30,"MND":30,"CHR":30,"Accuracy":45,"Attack":45,"Gear Haste":1,"Crit Rate":4, "TA":5,"Jobs":["drk","sam"]}
Flamma_Korazin = {"Name": "Flamma Korazin +2", "STR":43,"DEX":39,"VIT":32,"AGI":20,"INT":20,"MND":20,"CHR":20,"Accuracy":46,"Magic Accuracy":46,"Gear Haste":2,"Store TP":9,"Jobs":["drk","sam"]}
Gyve_Doublet = {"Name": "Gyve Doublet", "STR":19, "DEX":19, "VIT":19, "AGI":19, "INT":39, "MND":33, "CHR":33, "Magic Attack":42, "Gear Haste":3,"Jobs":["nin","drk"]}
Hachiya_Chainmail = {"Name": "Hachiya Chainmail +3", "STR":39, "DEX":35, "VIT":36, "AGI":35, "INT":34, "MND":34, "CHR":34, "Accuracy":50, "Gear Haste":4,"Dual Wield":10,"Crit Rate":8,"Jobs":["nin"]}
Herculean_Vest = {"Name": "Herculean Vest", "STR":28, "DEX":34, "VIT":24, "AGI":30, "INT":21, "MND":20, "CHR":21, "Accuracy":15, "Ranged Accuracy":15, "Gear Haste":4, "Store TP":3, "Crit Rate":3,"Jobs":["nin"]}
Hizamaru_Haramaki = {"Name": "Hizamaru Haramaki +2", "STR":40, "DEX":36, "VIT":34, "AGI":28, "INT":20, "MND":17, "CHR":28, "Accuracy":46, "Attack":28, "Gear Haste":4,"Jobs":["nin","sam"]}
Ignominy_Cuirass = {"Name": "Ignominy Cuirass +3", "STR":46,"DEX":29,"VIT":39,"AGI":29,"INT":29,"MND":29,"CHR":29,"Accuracy":50,"Attack":48,"Gear Haste":3,"Weaponskill Damage":10,"Jobs":["drk"]}
Kendatsuba_Samue = {"Name": "Kendatsuba Samue +1", "STR":33, "DEX":39, "VIT":21, "AGI":37, "INT":24, "MND":23, "CHR":21, "Accuracy": 52, "Ranged Accuracy": 47, "Gear Haste": 4, "TA": 6, "Crit Rate": 9,"Jobs":["nin","sam"]}
Malignance_Tabard = {"Name": "Malignance Tabard", "STR":19, "DEX":49, "VIT":25, "AGI":42, "INT":19, "MND":24, "CHR":24, "Accuracy":50, "Ranged Accuracy":50, "Magic Accuracy":50, "Gear Haste":4, "Store TP":11, "PDL":6,"Jobs":["nin"]}
Mochizuki_Chainmail = {"Name": "Mochizuki Chainmail +3", "STR":34, "DEX":35, "VIT":31, "AGI":35, "INT":34, "MND":34, "CHR":34, "Accuracy":51, "Attack":87, "Ranged Accuracy":47, "Ranged Attack":79, "Magic Accuracy":40,"Gear Haste":4,"Dual Wield":9,"Daken":10,"Jobs":["nin"]}
Mpaca_Doublet = {"Name": "Mpaca's Doublet", "Name2": "Mpaca's Doublet R25", "STR":39, "DEX":37, "VIT":34, "AGI":28, "INT":28, "MND":25, "CHR":28,"Accuracy":40+10,"Attack":40+25,"Magic Accuracy":40+10,"Gear Haste":4,"TA":4,"Crit Rate":7, "Store TP":0+7,"Jobs":["nin","sam"]}
Mummu_Jacket = {"Name": "Mummu Jacket +2", "STR":25, "DEX":48, "VIT":24, "AGI":44, "INT":21, "MND":20, "CHR":24, "Accuracy":46, "Ranged Accuracy":46, "Magic Accuracy":46, "Gear Haste":4, "Store TP":6, "Crit Rate": 6,"Jobs":["nin"]}
Nyame_Mail = {"Name": "Nyame Mail", "Name2": "Nyame Mail R25 B", "STR":35, "DEX":24, "VIT":35, "AGI":33, "INT":42, "MND":37, "CHR":35, "Accuracy":40, "Attack":30+30, "Gear Haste":3, "Weaponskill Damage":0+12, "Magic Accuracy":40, "Magic Attack":30, "Ranged Accuracy":40, "Ranged Attack":30+30,"DA":0+5,"Magic Burst Damage":7,"Jobs":all_jobs}
Ratri_Breastplate = {"Name": "Ratri Breastplate +1", "STR":48, "DEX":34, "VIT":30, "AGI":21, "INT":25, "MND":25, "CHR":24, "Magic Accuracy":47, "Scythe Skill":56, "Gear Haste":3, "Weaponskill Damage":10,"Jobs":["drk"]}
Ryuo_Domaru_A = {"Name": "Ryuo Domaru +1", "Name2": "Ryuo Domaru +1 A", "STR":28+12, "DEX":24+12, "VIT":23, "AGI":29, "INT":19, "MND":19, "CHR":19,"Accuracy":37+20,"Attack":37,"Gear Haste":3,"Crit Rate":5,"Jobs":["nin","sam"]}
Sakonji_Domaru = {"Name":"Sakonji Domaru +3", "STR":42, "DEX":37, "VIT":36, "AGI":31, "INT":31, "MND":31, "CHR":31, "Accuracy":47, "Attack":80, "Magic Accuracy":40, "Gear Haste":3, "Store TP":10, "Weaponskill Damage":10,"Jobs":["sam"]}
Sakpata_Breastplate = {"Name": "Sakpata's Breastplate", "Name2": "Sakpata's Breastplate R25", "STR":42,"DEX":25,"VIT":42,"AGI":25,"INT":24,"MND":28,"CHR":26,"Accuracy":40+10,"Magic Accuracy":40+10,"Attack":40+25,"Gear Haste":2,"DA":8,"PDL":8,"Jobs":["drk"]}
Samnuha_Coat = {"Name": "Samnuha Coat", "STR":26, "DEX":33, "VIT":23, "AGI":29, "INT":20, "MND":20, "CHR":20, "Accuracy":23, "Magic Accuracy":23+15, "Magic Attack":20+15, "Gear Haste":4, "Dual Wield":5, "Magic Burst Damage II": 8,"Jobs":["nin"]}
Sulevia_Platemail = {"Name": "Sulevia's Platemail +2", "STR":41,"DEX":24,"VIT":41,"AGI":16,"INT":16,"MND":27,"CHR":27,"Accuracy":46,"Attack":50,"Gear Haste":1,"Jobs":["drk"]}
Tatenashi_Haramaki = {"Name": "Tatenashi Haramaki +1", "Name2": "Tatenashi Haramaki +1 R15", "STR":28+10, "DEX":24+10, "VIT":28+10, "AGI":19+10, "INT":19+10, "MND":19+10, "CHR":19+10,"Accuracy":35+30,"Attack":35,"Gear Haste":3,"Crit Rate":6,"Store TP":8,"TA":0+5,"Jobs":["nin","sam"]}
Hattori_Ningi = {"Name": "Hattori Ningi +3", "STR":40,"DEX":47,"VIT":35,"AGI":43,"INT":36,"MND":31,"CHR":31,"Accuracy":64,"Attack":74,"Ranged Accuracy":64,"Magic Accuracy":64,"Gear Haste":4,"Crit Rate":8,"Jobs":["nin"]}
Heathen_Cuirass = {"Name": "Heathen's Cuirass +3", "STR":47,"DEX":31,"VIT":43,"AGI":33,"INT":35,"MND":35,"CHR":35,"Accuracy":64,"Attack":74,"Magic Accuracy":64,"Gear Haste":4,"Crit Rate":7,"Jobs":["drk"]}
bodies = [Kendatsuba_Samue, Adhemar_Jacket_A, Adhemar_Jacket_B, Malignance_Tabard, Nyame_Mail, Samnuha_Coat, Gyve_Doublet, Abnoba_Kaftan, Mpaca_Doublet, Tatenashi_Haramaki, Ryuo_Domaru_A, Agony_Jerkin, Hattori_Ningi]
bodies = [Abnoba_Kaftan,Adhemar_Jacket_A,Adhemar_Jacket_B,Agony_Jerkin,Dagon_Breastplate,Flamma_Korazin,Hizamaru_Haramaki,Ignominy_Cuirass,Kendatsuba_Samue,Malignance_Tabard,Mpaca_Doublet,Nyame_Mail,Ratri_Breastplate,Sakonji_Domaru,Sakpata_Breastplate,Sulevia_Platemail,Tatenashi_Haramaki,Hattori_Ningi,Heathen_Cuirass]
bodies = [Abnoba_Kaftan,Adhemar_Jacket_A,Adhemar_Jacket_B,Agony_Jerkin,Ashera_Harness,Dagon_Breastplate,Flamma_Korazin,Gyve_Doublet,Hachiya_Chainmail,Herculean_Vest,Hizamaru_Haramaki,Ignominy_Cuirass,Kendatsuba_Samue,Malignance_Tabard,Mochizuki_Chainmail,Mpaca_Doublet,Mummu_Jacket,Nyame_Mail,Ratri_Breastplate,Ryuo_Domaru_A,Sakpata_Breastplate,Samnuha_Coat,Sulevia_Platemail,Tatenashi_Haramaki,Hattori_Ningi,Heathen_Cuirass,]

Adhemar_Wristbands_A = {"Name": "Adhemar Wristbands +1", "Name2": "Adhemar Wristbands +1 A", "STR":15, "DEX":44+12, "VIT":29, "AGI":7+12, "INT":12, "MND":30, "CHR":17, "Accuracy":32+20, "Ranged Accuracy":32, "TA":4, "Store TP":7, "Gear Haste":5, "Jobs":["nin"]}
Adhemar_Wristbands_B = {"Name": "Adhemar Wristbands +1", "Name2": "Adhemar Wristbands +1 B", "STR":15+12, "DEX":44+12, "VIT":29, "AGI":7, "INT":12, "MND":30, "CHR":17, "Accuracy":32, "Ranged Accuracy":32, "TA":4, "Store TP":7, "Attack":0+20, "Gear Haste":5, "Jobs":["nin"]}
Flamma_Manopolas = {"Name": "Flamma Manopolas +2", "STR":23,"DEX":46,"VIT":35,"AGI":8,"INT":7,"MND":24,"CHR":17,"Accuracy":43,"Magic Accuracy":43,"Gear Haste":4,"Store TP":6,"Crit Rate":8,"Jobs":["drk","sam"]}
Floral_Gauntlets = {"Name": "Floral Gauntlets", "STR":16, "DEX":35,"VIT":29,"AGI":12,"INT":12,"MND":30,"CHR":17,"Accuracy":21+15,"Ranged Accuracy":21+15,"Gear Haste":5,"Dual Wield":5,"TA":3, "Jobs":["nin"]}
Hachiya_Tekko = {"Name": "Hachiya Tekko +3", "STR":20, "DEX":44, "VIT":38, "AGI":26, "INT":20, "MND":38, "CHR":26, "Accuracy":48, "Ranged Accuracy":48, "Ranged Attack":48, "Throwing Skill":14, "Gear Haste":5,"Daken":10, "Jobs":["nin"]}
Herculean_Gloves = {"Name": "Herculean Gloves", "STR":16, "DEX":39, "VIT":30, "AGI":8, "INT":14, "MND":26, "CHR":19, "Accuracy":12, "Ranged Accuracy":12, "Gear Haste":5,"TA":2, "Jobs":["nin"]}
Hizamaru_Kote = {"Name": "Hizamaru Kote +2", "STR":20, "DEX":43, "VIT":38, "AGI":16, "INT":7, "MND":21, "CHR":25, "Accuracy":43, "Attack":23, "Gear Haste":4, "Jobs":["nin","sam"]}
Kendatsuba_Tekko = {"Name": "Kendatsuba Tekko +1", "STR":14, "DEX":62, "VIT":37, "AGI":5, "INT":14, "MND":28, "CHR":21, "Accuracy":49, "Ranged Accuracy":44, "Gear Haste":4,"TA":4, "Crit Rate":5, "Jobs":["nin","sam"]}
Leyline_Gloves = {"Name": "Leyline Gloves", "STR":11, "DEX":35,"VIT":32,"AGI":5,"INT":12,"MND":30,"CHR":17,"Accuracy":18+15,"Magic Accuracy":18+15,"Magic Attack":15+15,"Gear Haste":5, "Jobs":["nin"]}
Malignance_Gloves = {"Name": "Malignance Gloves", "STR":25, "DEX":56, "VIT":32, "AGI":24, "INT":11, "MND":42, "CHR":21, "Accuracy":50, "Ranged Accuracy":50, "Magic Accuracy":50, "Gear Haste":4,"Store TP":12,"PDL":4, "Jobs":["nin"]}
Mochizuki_Tekko = {"Name": "Mochizuki Tekko +3", "STR":30, "DEX":44,"VIT":37,"AGI":16,"INT":20,"MND":38,"CHR":26,"Accuracy":38,"Attack":79,"Magic Accuracy":38,"Gear Haste":5, "Jobs":["nin"]}
Mpaca_Gloves = {"Name": "Mpaca's Gloves", "Name2": "Mpaca's Gloves R25", "STR":20, "DEX":44,"VIT":38,"AGI":16,"INT":15,"MND":29,"CHR":25,"Accuracy":40+10,"Attack":40+25,"Magic Accuracy":40+10,"Gear Haste":4,"TA":3,"Crit Rate":5, "TA DMG":0+9, "Jobs":["nin","sam"]}
Mummu_Wrists = {"Name": "Mummu Wrists +2", "STR":16, "DEX":53,"VIT":30,"AGI":22,"INT":14,"MND":26,"CHR":21,"Accuracy":43,"Ranged Accuracy":43,"Magic Accuracy":43,"Gear Haste":5,"DA":6,"Crit Rate":6, "Jobs":["nin"]}
Nyame_Gauntlets = {"Name": "Nyame Gauntlets", "Name2": "Nyame Gauntlets R25 B", "STR":17, "DEX":42, "VIT":39, "AGI":12, "INT":28, "MND":40, "CHR":24, "Accuracy":40, "Attack":30+30, "Gear Haste":3, "Weaponskill Damage":0+10, "Magic Accuracy":40, "Magic Attack":30, "Ranged Accuracy":40, "Ranged Attack":30+30,"DA":0+4,"Magic Burst Damage":5, "Jobs":all_jobs}
Ratri_Gadlings = {"Name": "Ratri Gadlings +1", "STR":28, "DEX":48, "VIT":34, "AGI":0, "INT":14, "MND":32, "CHR":24, "Magic Accuracy":44, "Scythe Skill":53, "Gear Haste":4, "Weaponskill Damage":8,"Jobs":["drk"]}
Ryuo_Tekko_A = {"Name": "Ryuo Tekko +1", "Name2": "Ryuo Tekko +1 A", "STR":12+12, "DEX":38+12, "VIT":30, "AGI":13, "INT":12, "MND":30, "CHR":17,"Accuracy":33+20,"Ranged Accuracy":33,"Gear Haste":4,"Crit Rate":5,"Crit Damage":5, "Jobs":["nin","sam"]}
Ryuo_Tekko_D = {"Name": "Ryuo Tekko +1", "Name2": "Ryuo Tekko +1 D", "STR":12, "DEX":38+12, "VIT":30, "AGI":13, "INT":12, "MND":30, "CHR":17,"Accuracy":33+25,"Ranged Accuracy":33,"Gear Haste":4,"Crit Rate":5,"Crit Damage":5, "DA":0+4, "Jobs":["nin","sam"]}
Sakpata_Gauntlets = {"Name": "Sakpata's Gauntlets", "Name2": "Sakpata's Gauntlets R25", "STR":24,"DEX":35,"VIT":46,"AGI":0,"INT":14,"MND":33,"CHR":26,"Accuracy":40+10,"Magic Accuracy":40+10,"Attack":40+25,"Gear Haste":4,"DA":6,"PDL":6,"Store TP":0+7,"Jobs":["drk"]}
Sulevia_Gauntlets = {"Name": "Sulevia's Gauntlets +2", "STR":23,"DEX":34,"VIT":45,"AGI":0,"INT":6,"MND":32,"CHR":27,"Accuracy":43,"Attack":47,"Gear Haste":3,"DA":6,"Jobs":["drk"]}
Tatenashi_Gote = {"Name": "Tatenashi Gote +1", "Name2": "Tatenashi Gote +1 R15", "STR":8+10, "DEX":40+10, "VIT":32+10, "AGI":7+10, "INT":6+10, "MND":23+10, "CHR":16+10,"Accuracy":21+40,"Gear Haste":4,"Store TP":7,"TA":0+4, "Jobs":["nin","sam"]}
Hattori_Tekko = {"Name": "Hattori Tekko +3", "STR":27,"DEX":55,"VIT":40,"AGI":24,"INT":27,"MND":40,"CHR":27,"Gear Haste":5,"Accuracy":62,"Attack":62,"Ranged Accuracy":62,"Magic Accuracy":62,"Ninjutsu Magic Attack":18,"Magic Burst Damage":15,"Jobs":["nin"]}
Heathen_Gauntlets = {"Name": "Heathen's Gauntlets +3", "STR":27,"DEX":43,"VIT":47,"AGI":0,"INT":25,"MND":40,"CHR":35,"Gear Haste":6,"Accuracy":62,"Attack":72,"Magic Accuracy":62,"Great Sword Skill":38, "Jobs":["drk"]}
hands = [Adhemar_Wristbands_A, Adhemar_Wristbands_B, Mochizuki_Tekko, Mummu_Wrists, Malignance_Gloves, Kendatsuba_Tekko, Nyame_Gauntlets, Mpaca_Gloves, Tatenashi_Gote, Ryuo_Tekko_A, Ryuo_Tekko_D, Hattori_Tekko]
hands = [Adhemar_Wristbands_A,Adhemar_Wristbands_B,Flamma_Manopolas,Kendatsuba_Tekko,Malignance_Gloves,Mpaca_Gloves,Mummu_Wrists,Nyame_Gauntlets,Ratri_Gadlings,Ryuo_Tekko_A,Ryuo_Tekko_D,Sakpata_Gauntlets,Sulevia_Gauntlets,Hattori_Tekko,Heathen_Gauntlets]
hands = [Adhemar_Wristbands_A,Adhemar_Wristbands_B,Flamma_Manopolas,Floral_Gauntlets,Hachiya_Tekko,Herculean_Gloves,Hizamaru_Kote,Kendatsuba_Tekko,Leyline_Gloves,Malignance_Gloves,Mochizuki_Tekko,Mpaca_Gloves,Mummu_Wrists,Nyame_Gauntlets,Ratri_Gadlings,Ryuo_Tekko_A,Ryuo_Tekko_D,Sakpata_Gauntlets,Sulevia_Gauntlets,Tatenashi_Gote,Hattori_Tekko,Heathen_Gauntlets,]

Apate_Ring = {"Name": "Apate Ring", "STR":6, "DEX":6, "AGI":6, "Store TP":3,"Jobs":all_jobs}
Archon_Ring = {"Name": "Archon Ring", "Dark Elemental Bonus":5,"Jobs":all_jobs}
Begrudging_Ring = {"Name": "Begrudging Ring", "Accuracy":7, "Attack": 7, "Crit Rate":5,"Jobs":all_jobs}
Beithir_Ring = {"Name": "Beithir Ring", "Name2": "Beithir Ring R25", "STR":3, "DEX":3, "VIT":3, "AGI":3, "Weaponskill Accuracy":0+15, "Attack":0+10, "Weaponskill Damage":2,"Jobs":["nin","sam","drk"]}
Chirich_Ring = {"Name": "Chirich Ring +1", "Accuracy":10, "Store TP":6,"Jobs":all_jobs}
Crepuscular_Ring = {"Name": "Crepuscular Ring", "Ranged Accuracy":10, "Magic Accuracy":10, "Store TP":6,"Jobs":all_jobs}
Dingir_Ring = {"Name": "Dingir Ring", "AGI":10, "Ranged Attack":25, "Magic Attack":10,"Jobs":["nin"]}
Epaminondas_Ring = {"Name": "Epaminondas's Ring", "Weaponskill Damage":5, "Store TP":-10,"Jobs":all_jobs}
Epona_Ring = {"Name": "Epona's Ring", "DA":3,"TA":3,"Jobs":["nin"]}
Flamma_Ring = {"Name": "Flamma Ring", "Accuracy":6, "Magic Accuracy":6, "Store TP":5,"Jobs":["drk","sam"]}
Gere_Ring = {"Name": "Gere Ring", "STR":10, "Attack":16, "TA":5,"Jobs":["nin"]}
Hetairoi_Ring = {"Name": "Hetairoi Ring", "Crit Rate":1, "TA":2, "TA DMG":5,"Jobs":all_jobs}
Ilabrat_Ring = {"Name": "Ilabrat Ring", "DEX":10, "AGI":10, "Attack":25, "Store TP":5,"Jobs":["nin","sam"]}
Karieyh_Ring = {"Name": "Karieyh Ring", "Weaponskill Accuracy":10, "Weaponskill Damage":4,"Jobs":all_jobs}
Locus_Ring = {"Name": "Locus Ring", "Magic Burst Damage":5,"Jobs":all_jobs}  # Ignoring the Magic Crit Rate +5 stat since we do not know how it behaves.
Metamorph_Ring = {"Name": "Metamorph Ring +1", "Name2": "Metamorph Ring +1 R15", "INT":6+10, "MND":6+10, "CHR":6+10, "Magic Accuracy":4+10,"Jobs":all_jobs}
Mujin_Band = {"Name": "Mujin Band", "Skillchain Bonus": 5, "Magic Burst Damage II":5,"Jobs":all_jobs}
Mummu_Ring = {"Name": "Mummu Ring", "Accuracy":6, "Ranged Accuracy":6, "Magic Accuracy":6, "Crit Rate":3,"Jobs":["nin"]}
Niqmaddu_Ring = {"Name": "Niqmaddu Ring", "STR":10, "DEX":10, "VIT":10, "QA":3,"Jobs":["drk","sam"]}
Petrov_Ring = {"Name": "Petrov Ring", "STR":3, "DEX":3, "VIT":3, "AGI":3, "DA":1,"Store TP":5,"Jobs":all_jobs}
Regal_Ring = {"Name": "Regal Ring", "STR":10, "DEX":10, "VIT":10, "AGI":10, "Attack":20, "Ranged Attack":20,"Jobs":["nin","drk","sam"]}
Rufescent_Ring = {"Name": "Rufescent Ring", "STR":6, "MND":6, "Weaponskill Accuracy": 7,"Jobs":all_jobs}
Shiva_Ring1 = {"Name": "Shiva Ring +1", "Name2": "Shiva Ring +1A", "INT":9, "Magic Attack":3,"Jobs":all_jobs}
Shiva_Ring2 = {"Name": "Shiva Ring +1", "Name2": "Shiva Ring +1B", "INT":9, "Magic Attack":3,"Jobs":all_jobs}
Shukuyu_Ring = {"Name": "Shukuyu Ring", "STR":7, "Attack":15,"Jobs":all_jobs}
Sroda_Ring = {"Name": "Sroda Ring", "STR":15, "DEX":-20, "PDL":3,"Jobs":all_jobs}
Weatherspoon_Ring = {"Name": "Weatherspoon Ring +1", "Light Elemental Bonus":11, "Magic Accuracy":13,"Jobs":all_jobs}
rings = [Mujin_Band, Sroda_Ring, Gere_Ring, Hetairoi_Ring, Shukuyu_Ring, Apate_Ring, Ilabrat_Ring, Regal_Ring, Epona_Ring, Petrov_Ring, Rufescent_Ring, Begrudging_Ring, Epaminondas_Ring, Mummu_Ring, Beithir_Ring, Dingir_Ring, Metamorph_Ring, Shiva_Ring1, Shiva_Ring2, Weatherspoon_Ring]
rings2 = [Mujin_Band, Sroda_Ring, Gere_Ring, Hetairoi_Ring, Shukuyu_Ring, Apate_Ring, Ilabrat_Ring, Regal_Ring, Epona_Ring, Petrov_Ring, Rufescent_Ring, Begrudging_Ring, Epaminondas_Ring, Mummu_Ring, Beithir_Ring, Dingir_Ring, Metamorph_Ring, Shiva_Ring1, Shiva_Ring2, Weatherspoon_Ring]

rings = [Apate_Ring,Begrudging_Ring,Beithir_Ring,Chirich_Ring,Dingir_Ring,Epaminondas_Ring,Epona_Ring,Flamma_Ring,Gere_Ring,Hetairoi_Ring,Ilabrat_Ring,Metamorph_Ring,Mummu_Ring,Niqmaddu_Ring,Petrov_Ring,Regal_Ring,Rufescent_Ring,Shukuyu_Ring,Sroda_Ring,Weatherspoon_Ring,]
rings2 = [Apate_Ring,Begrudging_Ring,Beithir_Ring,Chirich_Ring,Dingir_Ring,Epaminondas_Ring,Epona_Ring,Flamma_Ring,Gere_Ring,Hetairoi_Ring,Ilabrat_Ring,Metamorph_Ring,Mummu_Ring,Niqmaddu_Ring,Petrov_Ring,Regal_Ring,Rufescent_Ring,Shukuyu_Ring,Sroda_Ring,Weatherspoon_Ring,]

rings = [Apate_Ring,Archon_Ring,Begrudging_Ring,Beithir_Ring,Chirich_Ring,Crepuscular_Ring,Dingir_Ring,Epaminondas_Ring,Epona_Ring,Flamma_Ring,Gere_Ring,Hetairoi_Ring,Ilabrat_Ring,Karieyh_Ring,Locus_Ring,Metamorph_Ring,Mujin_Band,Mummu_Ring,Niqmaddu_Ring,Petrov_Ring,Regal_Ring,Rufescent_Ring,Shiva_Ring1,Shiva_Ring2,Shukuyu_Ring,Sroda_Ring,Weatherspoon_Ring,]
rings2 = [Apate_Ring,Archon_Ring,Begrudging_Ring,Beithir_Ring,Chirich_Ring,Crepuscular_Ring,Dingir_Ring,Epaminondas_Ring,Epona_Ring,Flamma_Ring,Gere_Ring,Hetairoi_Ring,Ilabrat_Ring,Karieyh_Ring,Locus_Ring,Metamorph_Ring,Mujin_Band,Mummu_Ring,Niqmaddu_Ring,Petrov_Ring,Regal_Ring,Rufescent_Ring,Shiva_Ring1,Shiva_Ring2,Shukuyu_Ring,Sroda_Ring,Weatherspoon_Ring,]

Andartia_Critagi = {"Name": "Andartia's Mantle", "Name2": "Andartia's Mantle AGI Crit Rate", "AGI":30, "Accuracy":20, "Attack":20, "Crit Rate":10, "Jobs":["nin"]}
Andartia_Critdex = {"Name": "Andartia's Mantle", "Name2": "Andartia's Mantle DEX Crit Rate", "DEX":30, "Accuracy":20, "Attack":20, "Crit Rate":10, "Jobs":["nin"]}
Andartia_DAagi = {"Name": "Andartia's Mantle", "Name2": "Andartia's Mantle AGI DA", "AGI":30, "Accuracy":20, "Attack":20, "DA":10, "Jobs":["nin"]}
Andartia_DAdex = {"Name": "Andartia's Mantle", "Name2": "Andartia's Mantle DEX DA", "DEX":30, "Accuracy":20, "Attack":20, "DA":10, "Jobs":["nin"]}
Andartia_DAstr = {"Name": "Andartia's Mantle", "Name2": "Andartia's Mantle STR DA", "STR":30, "Accuracy":20, "Attack":20, "DA":10, "Jobs":["nin"]}
Andartia_Nuke = {"Name": "Andartia's Mantle", "Name2": "Andartia's Mantle INT Magic Attack", "INT":30, "Magic Attack":10, "Magic Accuracy":20, "Magic Damage":20, "Jobs":["nin"]}
Andartia_WSDstr_mdmg = {"Name": "Andartia's Mantle", "Name2": "Andartia's Mantle STR WSD MDMG", "INT":30, "Weaponskill Damage":10, "Magic Accuracy":20, "Magic Damage":20, "Jobs":["nin"]}
Andartia_STP = {"Name": "Andartia's Mantle", "Name2": "Andartia's Mantle DEX Store TP", "DEX":30, "Accuracy":20, "Attack":20, "Store TP":10, "Jobs":["nin"]}
Andartia_DW = {"Name": "Andartia's Mantle", "Name2": "Andartia's Mantle DEX Dual Wield", "DEX":30, "Accuracy":20, "Attack":20, "Dual Wield":10, "Jobs":["nin"]}
Andartia_WSDagi = {"Name": "Andartia's Mantle", "Name2": "Andartia's Mantle AGI WSD", "AGI":30, "Accuracy":20, "Attack":20, "Weaponskill Damage":10, "Jobs":["nin"]}
Andartia_WSDdex = {"Name": "Andartia's Mantle", "Name2": "Andartia's Mantle DEX WSD", "DEX":30, "Accuracy":20, "Attack":20, "Weaponskill Damage":10, "Jobs":["nin"]}
Andartia_WSDstr = {"Name": "Andartia's Mantle", "Name2": "Andartia's Mantle STR WSD", "STR":30, "Accuracy":20, "Attack":20, "Weaponskill Damage":10, "Jobs":["nin"]}
Ankou_Mantle_WSDstr = {"Name": "Ankou's Mantle", "Name2": "Ankou's Mantle STR WSD", "STR":30, "Accuracy":20, "Attack":20, "Weaponskill Damage":10, "Jobs":["drk"]}
Ankou_Mantle_DAstr = {"Name": "Ankou's Mantle", "Name2": "Ankou's Mantle STR DA", "STR":30, "Accuracy":20, "Attack":20, "DA":10, "Jobs":["drk"]}
Ankou_Mantle_STPdex = {"Name": "Ankou's Mantle", "Name2": "Ankou's Mantle DEX Store TP", "DEX":30, "Accuracy":20, "Attack":20, "Store TP":10, "Jobs":["drk"]}
Smertrios_DAstr = {"Name": "Smertrios's Mantle", "Name2": "Smertrios's Mantle STR DA", "STR":30, "Attack":20, "Accuracy":20, "DA":10, "Skillchain Bonus":3,"Jobs":["sam"]}
Smertrios_WSDstr = {"Name": "Smertrios's Mantle", "Name2": "Smertrios's Mantle STR WSD", "STR":30, "Attack":20, "Accuracy":20, "Weaponskill Damage":10, "Skillchain Bonus":3,"Jobs":["sam"]}
capes = [Andartia_DAdex, Andartia_DAstr, Andartia_DAagi, Andartia_Critagi, Andartia_Critdex, Andartia_WSDstr, Andartia_WSDdex, Andartia_WSDagi, Andartia_Nuke, Andartia_WSDstr_mdmg]
capes = [Andartia_DW,Andartia_Critagi,Andartia_Critdex,Andartia_DAdex,Andartia_DAstr,Andartia_Nuke,Andartia_WSDstr_mdmg,Andartia_STP,Andartia_WSDagi,Andartia_WSDdex,Andartia_WSDstr,Ankou_Mantle_WSDstr,Ankou_Mantle_DAstr,Ankou_Mantle_STPdex,Smertrios_DAstr,Smertrios_WSDstr,]

Eschan_Stone = {"Name": "Eschan Stone", "Accuracy":15, "Ranged Accuracy":15, "Attack":15, "Ranged Attack":15, "Magic Accuracy":7, "Magic Attack":7,"Jobs":all_jobs}
Fotia_Belt = {"Name": "Fotia Belt", "Weaponskill Accuracy": 10, "ftp": 25./256.,"Jobs":all_jobs}
Grunfeld_Rope = {"Name": "Grunfeld Rope", "STR":5, "DEX":5, "Accuracy":10, "Attack":20, "DA":2,"Jobs":all_jobs}
Hachirin_no_Obi = {"Name": "Hachirin-no-Obi", "Weather":2,"Jobs":all_jobs}
Ioskeha_Belt = {"Name": "Ioskeha Belt +1", "Accuracy":17, "DA":9, "Gear Haste":8,"Jobs":["drk","sam"]}
Kentarch_Belt = {"Name": "Kentarch Belt +1", "Name2": "Kentarch Belt +1 R15", "STR":0+10, "DEX":0+10, "Accuracy":14, "DA":3, "Store TP":5,"Jobs":["nin","drk","sam"]}
Orpheus_Sash = {"Name": "Orpheus's Sash", "Elemental Bonus": 15,"Jobs":all_jobs}
Reiki_Yotai = {"Name": "Reiki Yotai", "Accuracy":10, "Ranged Accuracy":10, "Store TP":4, "Dual Wield":7,"Jobs":["nin","drk","sam"]}
Sailfi_Belt = {"Name": "Sailfi Belt +1", "Name2": "Sailfi Belt +1 R15", "Gear Haste":9, "TA":2, "Attack":14, "STR":0+15, "DA":0+5,"Jobs":["nin","drk","sam"]}
Windbuffet_Belt = {"Name": "Windbuffet Belt +1", "Accuracy":2, "TA":2, "QA":2,"Jobs":all_jobs}
Skrymir_Cord = {"Name":"Skrymir Cord +1", "Magic Accuracy":7, "Magic Attack":7, "Magic Damage":35,"Jobs":all_jobs}
waists = [Windbuffet_Belt, Fotia_Belt, Grunfeld_Rope, Kentarch_Belt, Sailfi_Belt, Orpheus_Sash,Skrymir_Cord]
waists = [Eschan_Stone,Fotia_Belt,Grunfeld_Rope,Ioskeha_Belt,Kentarch_Belt,Orpheus_Sash,Reiki_Yotai,Sailfi_Belt,Windbuffet_Belt,Skrymir_Cord,]
waists = [Eschan_Stone,Fotia_Belt,Grunfeld_Rope,Ioskeha_Belt,Kentarch_Belt,Orpheus_Sash,Reiki_Yotai,Sailfi_Belt,Windbuffet_Belt,Skrymir_Cord,]

Adhemar_Kecks_A = {"Name": "Adhemar Kecks +1", "Name2": "Adhemar Kecks +1 A", "STR":32, "DEX":0+12, "VIT":15, "AGI":30+12, "INT":28, "MND":16, "CHR":8, "Accuracy":34+20, "Ranged Accuracy":34, "Gear Haste":6, "Store TP":8,"Jobs":["nin"]}
Adhemar_Kecks_B = {"Name": "Adhemar Kecks +1", "Name2": "Adhemar Kecks +1 B", "STR":32+12, "DEX":0+12, "VIT":15, "AGI":30, "INT":28, "MND":16, "CHR":8, "Accuracy":34, "Ranged Accuracy":34, "Attack":20, "Gear Haste":6, "Store TP":8,"Jobs":["nin"]}
Fallen_Flanchard = {"Name": "Fallen's Flanchard +3", "STR":45,"DEX":0,"VIT":31,"AGI":26,"INT":40,"MND":27,"CHR":20,"Accuracy":39,"Attack":64,"Gear Haste":5,"Weaponskill Damage":10,"Jobs":["drk"]}
Flamma_Dirs = {"Name": "Flamma Dirs +2", "STR":53,"DEX":11,"VIT":29,"AGI":16,"INT":24,"MND":14,"CHR":11,"Accuracy":45,"Magic Accuracy":45,"Gear Haste":4,"Store TP":8,"Jobs":["drk","sam"]}
Gyve_Trousers = {"Name": "Gyve Trousers", "STR":19, "DEX":12, "VIT":19, "AGI":5, "INT":35, "MND":25, "CHR":23, "Magic Attack":40, "Gear Haste":5,"Jobs":["nin"]}
Hachiya_Hakama = {"Name": "Hachiya Hakama +3", "STR":42, "DEX":0, "VIT":24, "AGI":31, "INT":42, "MND":27, "CHR":20, "Accuracy":56, "Ranged Accuracy":35, "Gear Haste":6, "Store TP":6, "Dual Wield":5,"Jobs":["nin"]}
Herculean_Trousers = {"Name": "Herculean Trousers", "STR":33, "DEX":0, "VIT":16, "AGI":32, "INT":29, "MND":15, "CHR":10, "Attack":15, "Ranged Attack":15,"Gear Haste":6, "Store TP":4,"Jobs":["nin"]}
Hizamaru_Hizayoroi = {"Name": "Hizamaru Hizayoroi +2", "STR":50, "DEX":0, "VIT":32, "AGI":24, "INT":24, "MND":11, "CHR":19, "Accuracy":45, "Attack":27, "Gear Haste":9, "Weaponskill Damage":7,"Jobs":["nin","sam"]}
Ignominy_Flanchard = {"Name": "Ignominy Flanchard +3", "STR":50,"DEX":15,"VIT":31,"AGI":26,"INT":40,"MND":22,"CHR":20,"Accuracy":49,"Attack":45,"Gear Haste":5,"DA":10,"Jobs":["drk"]}
Jokushu_Haidate = {"Name": "Jokushu Haidate", "STR":29, "DEX":35, "VIT":15, "AGI":21, "INT":30, "MND":17, "CHR":11, "Gear Haste":20, "Crit Rate":4,"Jobs":["nin","sam"]}
Kendatsuba_Hakama = {"Name": "Kendatsuba Hakama +1", "STR":37, "DEX":5, "VIT":25, "AGI":33, "INT":32, "MND":16,"CHR":12,"Accuracy":51,"Ranged Accuracy":46,"Gear Haste":9,"TA":5,"Crit Rate":7,"Jobs":["nin","sam"]}
Malignance_Tights = {"Name": "Malignance Tights", "STR":28, "DEX":0, "VIT":17, "AGI":42, "INT":26, "MND":19, "CHR":12, "Accuracy":50, "Ranged Accuracy":50, "Magic Accuracy":50, "Gear Haste":9, "Store TP":10, "PDL":5,"Jobs":["nin"]}
Mochizuki_Hakama = {"Name": "Mochizuki Hakama +3", "STR":42, "DEX":0, "VIT":24, "AGI":36, "INT":42, "MND":27, "CHR":20, "Accuracy":39, "Attack":64, "Magic Accuracy":39, "Gear Haste":6, "Dual Wield":10, "Weaponskill Damage":10,"Jobs":["nin"]}
Mpaca_Hose = {"Name": "Mpaca's Hose", "Name2": "Mpaca's Hose R25", "STR":49, "DEX":0, "VIT":32, "AGI":25, "INT":32,"MND":19,"CHR":19,"Accuracy":40+10,"Attack":40+25,"Magic Accuracy":40+10,"Gear Haste":9,"TA":4,"Crit Rate":6,"PDL":0+7,"Jobs":["nin","sam"]}
Mummu_Kecks = {"Name": "Mummu Kecks +2", "STR":33, "DEX":11, "VIT":16, "AGI":45, "INT":29, "MND":15, "CHR":12, "Accuracy":45, "Ranged Accuracy":45, "Magic Accuracy": 45, "Gear Haste":6, "Crit Rate": 7,"Jobs":["nin"]}
Nyame_Flanchard = {"Name": "Nyame Flanchard", "Name2": "Nyame Flanchard R25 B", "STR":43, "DEX":0, "VIT":30, "AGI":34, "INT":44, "MND":32, "CHR":24, "Accuracy":40, "Attack":30+30, "Gear Haste":3, "Weaponskill Damage":0+11, "Magic Accuracy":40, "Magic Attack":30, "Ranged Accuracy":40, "Ranged Attack":30+30,"DA":0+5,"Magic Burst Damage":6,"Jobs":all_jobs}
Rao_Haidate_B = {"Name": "Rao Haidate +1", "Name2": "Rao Haidate +1 B", "STR":46+12, "DEX":0+12, "VIT":15, "AGI":21, "INT":30, "MND":31, "CHR":8, "Attack":43+20, "Gear Haste":6, "Store TP":8,"Jobs":["nin","sam"]}
Ratri_Cuisses = {"Name": "Ratri Cuisses +1", "STR":52, "DEX":0, "VIT":21, "AGI":19, "INT":37, "MND":19, "CHR":15, "Magic Accuracy":46, "Scythe Skill":55, "Gear Haste":5, "Weaponskill Damage":9, "Store TP":10,"Jobs":["drk"]}
Ryuo_Hakama_A = {"Name": "Ryuo Hakama +1", "Name2": "Ryuo Hakama +1 A", "STR":29+12, "DEX":0+12, "VIT":15, "AGI":21, "INT":30, "MND":17, "CHR":11,"Accuracy":0+20,"Attack":33,"Ranged Attack":33, "Gear Haste":5,"Store TP":8,"DA":4,"Jobs":["nin","sam"]}
Sakpata_Cuisses = {"Name": "Sakpata's Cuisses", "Name2": "Sakpata's Cuisses R25", "STR":48,"DEX":0,"VIT":34,"AGI":23,"INT":32,"MND":21,"CHR":17,"Accuracy":40+10,"Magic Accuracy":40+10,"Attack":40+25,"Gear Haste":4,"DA":7,"PDL":7,"Jobs":["drk"]}
Samnuha_Tights = {"Name": "Samnuha Tights", "STR":38+10, "DEX":6+10, "VIT":15, "AGI":30, "INT":28, "MND":16, "CHR":8, "Accuracy":15, "Ranged Accuracy":15, "Gear Haste":6, "Store TP":7, "DA":3, "TA":3,"Jobs":["nin"]}
Sulevia_Flanchard = {"Name": "Sulevia's Flanchard +2", "STR":47,"DEX":0,"VIT":33,"AGI":14,"INT":24,"MND":20,"CHR":18,"Accuracy":45,"Attack":49,"Gear Haste":2,"TA":4,"Jobs":["drk"]}
Tatenashi_Haidate = {"Name": "Tatenashi Haidate +1", "Name2": "Tatenashi Haidate +1 R15", "STR":45+10, "DEX":0+10, "VIT":25+10, "AGI":15+10, "INT":23+10, "MND":12+10, "CHR":10+10,"Accuracy":0+60,"Attack":31,"Gear Haste":5,"Store TP":7,"TA":0+3,"Jobs":["nin","sam"]}
Wakido_Haidate = {"Name": "Wakido Haidate +3", "STR":44, "DEX":0, "VIT":29, "AGI":25, "INT":37, "MND":26, "CHR":20, "Accuracy":49, "Attack":40, "Ranged Attack":40, "Gear Haste":5, "Store TP":9, "Weaponskill Damage":10,"Jobs":["sam"]}
Hattori_Hakama = {"Name": "Hattori Hakama +3", "STR":44,"DEX":0,"VIT":27,"AGI":35,"INT":45,"MND":27,"CHR":21,"Gear Haste":8,"Katana Skill":33,"Accuracy":63,"Ranged Accuracy":63,"Magic Accuracy":63,"Attack":63,"Jobs":["nin"]}
Heathen_Flanchard = {"Name": "Heathen's Flanchard +3", "STR":53,"DEX":0,"VIT":35,"AGI":30,"INT":41,"MND":29,"CHR":26,"Gear Haste":5,"Accuracy":63,"Magic Accuracy":63,"Attack":73,"Jobs":["drk"]}
legs = [Kendatsuba_Hakama, Adhemar_Kecks_A, Adhemar_Kecks_B, Mochizuki_Hakama, Samnuha_Tights, Jokushu_Haidate, Malignance_Tights, Mummu_Kecks, Gyve_Trousers, Hizamaru_Hizayoroi, Nyame_Flanchard, Mpaca_Hose, Tatenashi_Haidate, Ryuo_Hakama_A, Rao_Haidate_B, Hattori_Hakama]
legs = [Adhemar_Kecks_A,Adhemar_Kecks_B,Fallen_Flanchard,Flamma_Dirs,Hizamaru_Hizayoroi,Ignominy_Flanchard,Jokushu_Haidate,Kendatsuba_Hakama,Malignance_Tights,Mochizuki_Hakama,Mpaca_Hose,Mummu_Kecks,Nyame_Flanchard,Rao_Haidate_B,Ratri_Cuisses,Ryuo_Hakama_A,Sakpata_Cuisses,Samnuha_Tights,Sulevia_Flanchard,Tatenashi_Haidate,Wakido_Haidate,Hattori_Hakama,Heathen_Flanchard]
legs = [Adhemar_Kecks_A,Adhemar_Kecks_B,Fallen_Flanchard,Flamma_Dirs,Gyve_Trousers,Hachiya_Hakama,Herculean_Trousers,Hizamaru_Hizayoroi,Ignominy_Flanchard,Jokushu_Haidate,Kendatsuba_Hakama,Malignance_Tights,Mochizuki_Hakama,Mpaca_Hose,Mummu_Kecks,Nyame_Flanchard,Rao_Haidate_B,Ratri_Cuisses,Ryuo_Hakama_A,Sakpata_Cuisses,Samnuha_Tights,Sulevia_Flanchard,Tatenashi_Haidate,Hattori_Hakama,Heathen_Flanchard,]

Adhemar_Gamashes_A = {"Name": "Adhemar Gamashes +1", "Name2": "Adhemar Gamashes +1 A", "STR":15, "DEX":23+12, "VIT":8, "AGI":42+12, "INT":0, "MND":11, "CHR":25, "Accuracy":20, "Attack":34, "Ranged Attack":34, "Magic Attack":35, "Gear Haste":4, "Crit Rate":4, "Jobs":["nin"]}
Adhemar_Gamashes_B = {"Name": "Adhemar Gamashes +1", "Name2": "Adhemar Gamashes +1 B", "STR":15+12, "DEX":23+12, "VIT":8, "AGI":42, "INT":0, "MND":11, "CHR":25, "Attack":34+20, "Ranged Attack":34, "Magic Attack":35, "Gear Haste":4, "Crit Rate":4, "Jobs":["nin"]}
Flamma_Gambieras = {"Name": "Flamma Gambieras +2", "STR":31,"DEX":34,"VIT":20,"AGI":26,"INT":0,"MND":6,"CHR":20,"Accuracy":42,"Magic Accuracy":42,"Gear Haste":2,"Store TP":6,"DA":6,"Jobs":["drk","sam"]}
Hachiya_Kyahan = {"Name": "Hachiya Kyahan +3", "STR":24, "DEX":25, "VIT":21, "AGI":44, "INT":20, "MND":22, "CHR":39, "Magic Accuracy":52, "Magic Attack":23, "Gear Haste":4, "Magic Burst Damage": 10, "Jobs":["nin"]}
Herculean_Boots = {"Name": "Herculean Boots", "STR":16, "DEX":24, "VIT":10, "AGI":43, "INT":0, "MND":11, "CHR":26, "Accuracy":10, "Attack":10,"Ranged Accuracy":10,"Ranged Attack":10,"Magic Accuracy":10,"Magic Attack":10,"Gear Haste":4,"TA":2, "Jobs":["nin"]}
Herculean_Boots_QA = {"Name": "Herculean Boots", "STR":16, "DEX":24, "VIT":10, "AGI":43, "INT":0, "MND":11, "CHR":26, "Accuracy":10+35, "Attack":10+18,"Ranged Accuracy":10,"Ranged Attack":10,"Magic Accuracy":10+3,"Magic Attack":10+3,"Gear Haste":4,"TA":2,"QA":3, "Jobs":["nin"]}
Hizamaru_Sune_Ate = {"Name": "Hizamaru Sune-ate +2", "STR":28, "DEX":31, "VIT":23, "AGI":34, "INT":0, "MND":3, "CHR":28, "Accuracy":42, "Attack":24, "Gear Haste":3, "Dual Wield":8, "Jobs":["nin","sam"]}
Kendatsuba_Sune_Ate = {"Name": "Kendatsuba Sune-ate +1", "STR":20, "DEX":44, "VIT":21, "AGI":44, "INT":0, "MND":14, "CHR":26, "Accuracy":48, "Ranged Accuracy":43, "Gear Haste":3, "TA":4, "Crit Rate":5, "Jobs":["nin","sam"]}
Malignance_Boots = {"Name": "Malignance Boots", "STR":6, "DEX":40, "VIT":12, "AGI":49, "INT":0, "MND":15, "CHR":40, "Accuracy":50, "Ranged Accuracy":50, "Magic Accuracy":50, "Gear Haste":3, "Store TP":9, "PDL":2, "Jobs":["nin"]}
Mochizuki_Kyahan = {"Name": "Mochizuki Kyahan +3", "STR":28, "DEX":29, "VIT":25, "AGI":48, "INT":0, "MND":22, "CHR":39, "Accuracy":43, "Attack":76, "Magic Accuracy":36, "Ninjutsu Skill":23, "Gear Haste":4, "Ninjutsu Damage":25, "Jobs":["nin"]}
Mpaca_Boots = {"Name": "Mpaca's Boots", "Name2": "Mpaca's Boots R25","STR":28,"DEX":32,"VIT":23,"AGI":34,"INT":0,"MND":11,"CHR":28,"Accuracy":40+10,"Attack":40+25,"Magic Accuracy":40+10,"Gear Haste":3,"TA":3,"Crit Rate":3,"Magic Attack":0+40, "Jobs":["nin","sam"]}
Mummu_Gamashes = {"Name": "Mummu Gamashes +2", "STR":16, "DEX":37, "VIT":10, "AGI":57, "INT":0, "MND":11, "CHR":29, "Accuracy":42, "Ranged Accuracy": 42, "Magic Accuracy": 42, "Gear Haste":4, "Crit Rate":5, "Jobs":["nin"]}
Nyame_Sollerets = {"Name": "Nyame Sollerets", "Name2": "Nyame Sollerets R25 B", "STR":23, "DEX":26, "VIT":24, "AGI":46, "INT":25, "MND":26, "CHR":38, "Accuracy":40, "Attack":30+30, "Gear Haste":3, "Weaponskill Damage":0+0, "Magic Accuracy":40, "Magic Attack":30, "Ranged Accuracy":40, "Ranged Attack":30+30,"DA":0+4,"Magic Burst Damage":5, "Jobs":all_jobs}
Rao_SuneAte_D = {"Name": "Rao Sune-ate +1", "Name2": "Rao Sune-ate +1 D", "STR":17, "DEX":26, "VIT":12, "AGI":34, "INT":0, "MND":16, "CHR":28,"Accuracy":41,"Crit Rate":0+4,"Gear Haste":4,"DA":0+4, "Jobs":["nin","sam"]}
Ratri_Sollerets = {"Name": "Ratri Sollerets +1", "STR":29, "DEX":26, "VIT":17, "AGI":32, "INT":0, "MND":16, "CHR":31, "Magic Accuracy":43, "Scythe Skill":52, "Gear Haste":3, "Weaponskill Damage":8,"Jobs":["drk"]}
Ryuo_SuneAte_D = {"Name": "Ryuo Sune-Ate +1", "Name2": "Ryuo Sune-ate +1 D", "STR":27+12, "DEX":19, "VIT":11, "AGI":38, "INT":0, "MND":5, "CHR":19,"Attack":32+25,"Ranged Attack":32,"Crit Rate":0+4,"Gear Haste":3, "Jobs":["nin","sam"]}
Sakpata_Leggings = {"Name": "Sakpata's Leggings", "Name2": "Sakpata's Leggings R25", "STR":29,"DEX":20,"VIT":30,"AGI":35,"INT":0,"MND":19,"CHR":32,"Accuracy":40+10,"Magic Accuracy":40+10,"Attack":40+25,"Gear Haste":2,"DA":4,"PDL":4,"Jobs":["drk"]}
Sulevia_Leggings = {"Name": "Sulevia's Leggings +2", "STR":29,"DEX":19,"VIT":29,"AGI":26,"INT":0,"MND":18,"CHR":32,"Accuracy":42,"Attack":46,"Gear Haste":1,"Weaponskill Damage":7,"Jobs":["drk"]}
Tatenashi_SuneAte = {"Name": "Tatenashi Sune-ate +1", "Name2": "Tatenashi Sune-ate +1 R15", "STR":16+10, "DEX":19+10, "VIT":16+10, "AGI":32+10, "INT":0+10, "MND":5+10, "CHR":19+10,"Accuracy":0+60,"Gear Haste":3,"Store TP":7,"TA":0+3, "Jobs":["nin","sam"]}
Hattori_Kyahan = {"Name": "Hattori Kyahan +3", "STR":27,"DEX":39,"VIT":23,"AGI":54,"INT":0,"MND":22,"CHR":40,"Gear Haste":5,"Accuracy":60,"Attack":60,"Ranged Accuracy":60,"Magic Accuracy":60,"Weaponskill Damage":12,"Jobs":["nin"]}
Heathen_Sollerets = {"Name": "Heathen's Sollerets +3", "STR":33,"DEX":25,"VIT":30,"AGI":42,"INT":22,"MND":26,"CHR":38,"Gear Haste":3,"Accuracy":60,"Attack":60,"Ranged Accuracy":60,"Magic Accuracy":60,"Weaponskill Damage":12,"Jobs":["drk"]}
feet = [Mochizuki_Kyahan, Adhemar_Gamashes_A, Adhemar_Gamashes_B, Malignance_Boots, Mummu_Gamashes, Kendatsuba_Sune_Ate, Nyame_Sollerets, Mpaca_Boots, Tatenashi_SuneAte, Ryuo_SuneAte_D, Rao_SuneAte_D,Hattori_Kyahan]
feet = [Adhemar_Gamashes_A,Adhemar_Gamashes_B,Flamma_Gambieras,Kendatsuba_Sune_Ate,Malignance_Boots,Mpaca_Boots,Mummu_Gamashes,Nyame_Sollerets,Rao_SuneAte_D,Ratri_Sollerets,Ryuo_SuneAte_D,Sakpata_Leggings,Sulevia_Leggings,Tatenashi_SuneAte,Hattori_Kyahan,Heathen_Sollerets]
feet = [Adhemar_Gamashes_A,Adhemar_Gamashes_B,Flamma_Gambieras,Hachiya_Kyahan,Herculean_Boots,Herculean_Boots_QA,Hizamaru_Sune_Ate,Kendatsuba_Sune_Ate,Malignance_Boots,Mochizuki_Kyahan,Mpaca_Boots,Mummu_Gamashes,Nyame_Sollerets,Rao_SuneAte_D,Ratri_Sollerets,Ryuo_SuneAte_D,Sakpata_Leggings,Sulevia_Leggings,Tatenashi_SuneAte,Hattori_Kyahan,Heathen_Sollerets,]

# Confirm that the stats for each piece of gear being checked are spelled correctly.
# Compare each stat against a pre-made list of accepted stats.
available_stats = ["JA Haste","Accuracy", "AGI", "Attack", "Axe Skill", "CHR", "Club Skill", "Crit Damage", "Crit Rate", "DA", "DA DMG", "Dagger Skill", "Daken", "Dark Affinity", "Dark Elemental Bonus", "Delay", "DEX", "DMG", "Dual Wield", "Earth Affinity", "Earth Elemental Bonus", "Elemental Bonus", "Elemental Magic Skill", "Fire Affinity", "Fire Elemental Bonus", "ftp", "Gear Haste", "Great Axe Skill", "Great Katana Skill", "Great Sword Skill", "Hand-to-Hand Skill", "Ice Affinity", "Ice Elemental Bonus", "INT", "Jobs", "Katana Skill", "Light Affinity", "Light Elemental Bonus", "Magic Accuracy Skill", "Magic Accuracy", "Magic Attack", "Magic Burst Damage II", "Magic Burst Damage", "Magic Damage", "MND", "Name", "Name2", "Ninjutsu Damage", "Ninjutsu Magic Attack", "Ninjutsu Skill", "OA2", "OA3", "OA4", "OA5", "OA6", "OA7", "OA8", "PDL", "Polearm Skill", "QA", "Ranged Accuracy", "Ranged Attack", "Scythe Skill", "Skill Type", "Skillchain Bonus", "Staff Skill", "Store TP", "STR", "Sword Skill", "TA", "TA DMG", "Throwing Skill", "Thunder Affinity", "Thunder Elemental Bonus", "TP Bonus", "Type", "Utu CHR", "VIT", "Water Affinity", "Water Elemental Bonus", "Weaponskill Accuracy", "Weaponskill Damage", "Weather", "Wind Affinity", "Wind Elemental Bonus"]

typo = False
slots = [mains, subs, grips, ammos, heads, necks, ears, ears2, bodies, hands, rings, rings2, capes, waists, legs, feet]
for slot in slots:
  for gear in slot:
    keys = gear.keys()
    for key in keys:
      if key not in available_stats:
        print(f"Incorrect stat name found on \"{gear.get('Name2',gear['Name'])}\":  \"{key}\"")
        typo = True

    # May as well add the "Name2" value to all items that do not have it. This is huge for cleaning up the main code
    # While they do not have a typed-out "Name2", as long as another code uses this code, then each piece of gear will have "Name2" available now.
    # I'll clean up the main code later.
    name2 = gear.get('Name2','None')
    if name2 == 'None':
        gear.update({'Name2': gear['Name']})

if typo:
  print("Check the \"available_stats\" list at the end of the gear.py file for a list of accepted stat names.")
  import sys ; sys.exit()
