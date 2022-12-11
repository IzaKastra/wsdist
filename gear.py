#
# Created by Kastra on Asura.
# Feel free to /tell in game or send a PM on FFXIAH you have questions, comments, or suggestions.
#
# Version date: 2022 December 11
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

Empty = {"Name":"Empty", "Jobs":all_jobs, "DMG":0, "Delay":999, "Skill Type":"None", "Type":"None"}

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
Crepuscular_Knife = {"Name": "Crepuscular Knife", "Name2": "Crepuscular Knife", "Skill Type": "Dagger", "Type":"Weapon", "DMG":133, "Delay":190, "DEX":15, "AGI":15, "CHR":15, "Accuracy":40, "Magic Accuracy":40, "Dagger Skill":248, "Magic Accuracy Skill":248, "QA":5, "Jobs":["nin","rdm","war","thf","dnc","cor"]}
Dojikiri = {"Name": "Dojikiri Yasutsuna","Name2": "Dojikiri Yasutsuna R15", "Skill Type": "Great Katana", "Type":"Weapon", "DMG": 315+15, "Delay": 450, "Store TP": 10, "Accuracy": 0+30, "Magic Accuracy":0+30, "TP Bonus": 500, "Great Katana Skill": 269, "Magic Accuracy Skill": 228, "Magic Damage": 155, "Jobs":["sam"]}
Gleti_Knife = {"Name": "Gleti's Knife", "Name2": "Gleti's Knife R25", "Skill Type": "Dagger", "Type":"Weapon", "DMG":133+10, "Delay":200, "DEX":15, "AGI":15, "Accuracy":40+10, "Attack":30+40, "Magic Accuracy":40+10, "Dagger Skill":255, "Magic Accuracy Skill":242,"Crit Rate":5,"TA":6, "Jobs":["nin","thf","dnc","rdm","brd","cor"]}
Gokotai = {"Name": "Gokotai", "Name2": "Gokotai", "Skill Type": "Katana", "Type":"Weapon", "DMG": 157, "Delay": 227, "Katana Skill": 250, "Magic Accuracy Skill": 250, "Magic Damage": 217, "DEX": 15, "AGI":15, "INT":15, "Accuracy": 40, "Attack": 30, "Ranged Accuracy": 40, "Magic Accuracy": 40, "Magic Attack": 16, "Jobs":["nin"]}
Hachimonji = {"Name": "Hachimonji", "Name2": "Hachimonji", "Skill Type": "Great Katana", "Type":"Weapon", "DMG": 318, "Delay":450, "STR":20, "DEX":20, "VIT":20, "Accuracy":40, "Attack":30, "Magic Accuracy":40, "Great Katana Skill":250, "Magic Accuracy Skill":250, "Jobs":["nin","sam"]}
Heishi = {"Name": "Heishi Shorinken", "Name2": "Heishi Shorinken R15", "Skill Type": "Katana", "Type":"Weapon", "DMG": 159+7, "Delay": 227, "Store TP": 10, "Accuracy": 0+30, "Magic Accuracy":0+30, "TP Bonus": 500, "Katana Skill": 269, "Magic Accuracy Skill": 242, "Magic Damage": 186, "Jobs":["nin"]}
Hitaki = {"Name": "Hitaki", "Name2": "Hitaki", "Skill Type": "Katana", "Type":"Weapon", "DMG":  49, "Delay": 216, "TP Bonus": 1000, "Katana Skill": 0, "Jobs":["nin"]}
Kannagi = {"Name": "Kannagi", "Name2": "Kannagi R15", "Skill Type": "Katana", "Type":"Weapon", "DMG": 148+5, "Delay": 210, "Katana Skill": 269, "Magic Accuracy Skill": 242, "Magic Damage": 186, "DEX": 0+20, "AGI":50+20, "Jobs":["nin"]}
Kikoku = {"Name": "Kikoku", "Name2": "Kikoku R15", "Skill Type": "Katana", "Type":"Weapon", "DMG": 148+8, "Delay": 210, "Attack": 60, "Katana Skill": 269, "Magic Accuracy Skill": 242, "Magic Damage": 186, "Jobs":["nin"]}
Kogarasumaru = {"Name": "Kogarasumaru", "Name2": "Kogarasumaru R15", "Skill Type": "Great Katana", "Type":"Weapon", "DMG": 281+29, "Delay": 450, "Accuracy": 0+30, "Magic Accuracy":0+30, "Great Katana Skill": 269, "Magic Accuracy Skill": 228, "Jobs":["sam"]}
Kraken_Club = {"Name": "Kraken Club", "Name2": "Kraken Club", "Skill Type": "Club", "Type":"Weapon", "DMG":11, "Delay":264, "OA2":15, "OA3":25, "OA4":25, "OA5":15, "OA6":10, "OA7":3, "OA8":2, "Jobs":["nin","drk","sam"]}
Kunimitsu = {"Name": "Kunimitsu", "Name2": "Kunimitsu R25", "Skill Type": "Katana", "Type":"Weapon", "DMG":151+11, "Delay":227, "DEX":15, "AGI":15, "Accuracy":40+10, "Attack":30+40, "Ranged Accuracy":40, "Magic Accuracy":40+10,"Magic Attack":20, "Magic Damage":217, "Magic Burst Damage":10,"Store TP":5, "Magic Accuracy Skill":248, "Katana Skill": 248, "Weaponskill Damage":5, "Jobs":["nin"]}
Liberator = {"Name": "Liberator", "Name2": "Liberator R15", "Skill Type": "Scythe", "Type":"Weapon", "DMG":330+34, "Delay":528, "Magic Accuracy":50+30, "Magic Damage":217, "Scythe Skill":269, "Magic Accuracy Skill":242, "Accuracy":0+30,"Jobs":["drk"]}
Masamune = {"Name": "Masamune", "Name2": "Masamune R15", "Skill Type": "Great Katana", "Type":"Weapon", "DMG": 308+11, "Delay": 437, "Great Katana Skill": 269, "Magic Accuracy Skill": 228, "AGI": 0+20, "STR":50+20, "Jobs":["sam"]}
Naegling = {"Name": "Naegling", "Name2": "Naegling", "Skill Type": "Sword", "Type":"Weapon", "DMG": 166, "Delay": 240, "Sword Skill": 250, "Magic Accuracy Skill": 250, "Magic Damage": 217, "DEX": 15, "MND":15, "INT":15, "Accuracy": 40, "Attack": 30, "Magic Accuracy": 40, "Magic Attack": 16, "Jobs":["nin","drk","rdm","war","drg","brd","blu","cor"]}
Nagi = {"Name": "Nagi", "Name2": "Nagi R15", "Skill Type": "Katana", "Type":"Weapon", "DMG": 142+14, "Delay": 227, "Accuracy": 0+30, "Magic Accuracy":40+30, "Katana Skill": 269, "Magic Accuracy Skill": 242, "Magic Damage": 186, "Jobs":["nin"]}
Ragnarok = {"Name": "Ragnarok", "Name2": "Ragnarok R15", "Skill Type": "Great Sword", "Type":"Weapon", "DMG":304+17, "Delay":431, "Magic Damage":155, "Great Sword Skill":269, "Magic Accuracy Skill":242,"DEX":0+15,"STR":35+15,"MND":35+15,"INT":0+15,"Jobs":["drk"]}
Redemption = {"Name": "Redemption", "Name2": "Redemption R15", "Skill Type": "Scythe", "Type":"Weapon", "DMG":354+13, "Delay":502, "Magic Damage":217, "Scythe Skill":269, "Magic Accuracy Skill":242,"DEX":0+15,"STR":35+15,"MND":35+15,"INT":0+15,"Jobs":["drk"]}
Shining_One = {"Name": "Shining One", "Name2": "Shining One", "Skill Type": "Polearm", "Type":"Weapon", "DMG":333, "Delay":480, "STR":20, "INT":20, "MND":20, "Accuracy":40, "Attack":30, "Magic Accuracy":40, "Magic Attack":21, "Magic Damage":226, "Polearm Skill":250, "Magic Accuracy Skill":250 , "Jobs":["sam","drg","war","pld"]}
Tauret = {"Name": "Tauret", "Name2": "Tauret", "Skill Type": "Dagger", "Type":"Weapon", "DMG": 125, "Delay": 180, "Dagger Skill": 250, "Magic Accuracy Skill": 250, "Magic Damage": 217, "DEX": 15, "MND":15, "INT":15, "Accuracy": 40, "Attack": 30, "Magic Accuracy": 40, "Magic Attack": 16, "Jobs":["nin","thf","dnc","rdm","cor","brd"]}
Ternion = {"Name": "Ternion Dagger +1","Name2": "Ternion Dagger +1 R15", "Skill Type": "Dagger", "Type":"Weapon", "DMG": 100+17, "Delay": 175, "Accuracy":27+40, "Magic Accuracy":0+40, "Dagger Skill":228, "Magic Accuracy Skill":188, "TA":4, "AGI":14, "Weaponskill Damage":5, "Jobs":["war","blm","rdm","thf","pld","drk","bst","brd","rng","sam","nin","drg","smn","dnc","sch","geo"]}
Tsuru = {"Name": "Tsuru", "Name2": "Tsuru R25", "Skill Type": "Katana", "Type":"Weapon", "DMG":131, "Delay":190,"VIT":15,"AGI":15,"Accuracy":40,"Ranged Accuracy":40, "Katana Skill":242, "Magic Accuracy Skill":242,"Daken":8, "Jobs":["nin"]}
MalevolenceA = {"Name": "Malevolence","Name2": "MalevolenceA", "Skill Type":"Dagger","Type":"Weapon","DMG":94,"Delay":201,"INT":0+10,"Magic Accuracy":25+10, "Magic Attack":34+10, "Magic Damage":118, "Magic Accuracy Skill":201, "Dagger Skill":242,"Jobs":["nin","thf","dnc","rdm","drk","cor"]}
MalevolenceB = {"Name": "Malevolence","Name2": "MalevolenceB", "Skill Type":"Dagger","Type":"Weapon","DMG":94,"Delay":201,"INT":0+10,"Magic Accuracy":25+10, "Magic Attack":34+10, "Magic Damage":118, "Magic Accuracy Skill":201, "Dagger Skill":242,"Jobs":["nin","thf","dnc","rdm","drk","cor"]}
Marin_Staff = {"Name":"Marin Staff +1","Name2":"Marin Staff +1 R15","INT":36,"MND":22,"Magic Accuracy":15+40,"Magic Attack":28+40,"Magic Damage":217,"Staff Skill":242, "Skill Type": "Staff", "Type":"Weapon", "DMG": 199, "Delay": 356,"Magic Accuracy Skill":228,"Jobs":["blm","rdm","sch","geo"]}
Maxentius = {"Name":"Maxentius","INT":15,"MND":15,"CHR":15,"Accuracy":40,"Magic Accuracy":40,"Magic Attack":21,"Magic Damage":232,"Club Skill":250,"Type":"Weapon","Skill Type":"Club","Magic Accuracy Skill":250,"DMG":200,"Delay":288,"Magic Burst Damage":4,"Jobs":["whm","blm","rdm","blu","sch","geo"]}
Bunzi_Rod = {"Name":"Bunzi's Rod", "Name2":"Bunzi's Rod R25", "INT":15, "MND":15, "DMG":144+10,"Delay":216,"Magic Accuracy":40+10,"Magic Attack":35+25,"Magic Damage":248,"Club Skill":242, "Skill Type": "Club", "Type":"Weapon","Magic Accuracy Skill":255,"Magic Burst Damage":10, "Accuracy":40+10,"Jobs":["blm","rdm","sch","geo","whm","smn","blu"]}
Almace = {"Name":"Almace","Name2":"Almace R15","Type":"Weapon","Skill Type":"Sword","DMG":158+5,"Delay":224,"DEX":50+20,"MND":20,"Magic Damage":186,"Sword Skill":269,"Magic Accuracy Skill":255,"Jobs":["rdm","blu","pld"]}
Excalibur = {"Name":"Excalibur","Name2":"Excalibur R15","Type":"Weapon","Skill Type":"Sword","DMG":164+9,"Delay":233,"Attack":60,"Magic Damage":186,"Sword Skill":269,"Magic Accuracy Skill":255,"Jobs":["rdm","pld"]}
Sequence = {"Name":"Sequence", "Name2":"Sequence R15","Type":"Weapon","Skill Type":"Sword","DMG":168+8,"Delay":240,"Accuracy":0+30,"Magic Accuracy":0+30,"TP Bonus":500,"Magic Damage":186,"Magic Accuracy Skill":242,"Sword Skill":269,"Store TP":10,"Jobs":["rdm","blu","pld"]}
Murgleis = {"Name":"Murgleis", "Name2":"Murgleis R15","Type":"Weapon","Skill Type":"Sword","DMG":140+17,"Delay":224,"Accuracy":0+30,"Magic Accuracy":40+30,"Magic Damage":217,"Magic Accuracy Skill":255,"Sword Skill":269,"Jobs":["rdm"]}
Thibron = {"Name": "Thibron", "Skill Type": "Sword", "Type":"Weapon", "DMG":  55, "Delay": 238, "TP Bonus": 1000, "Sword Skill": 0, "Jobs":["rdm","pld","blu"]}
Gungnir = {"Name":"Gungnir","Name2":"Gungnir R15","Type":"Weapon","Skill Type":"Polearm","DMG":347+20,"Delay":492,"Accuracy":60,"Magic Damage":155,"Magic Accuracy Skill":228,"Polearm Skill":269,"DA":5,"Jobs":["drg"]}
Trishula = {"Name":"Trishula","Name2":"Trishula R15","Type":"Weapon","Skill Type":"Polearm","DMG":345+15,"Delay":492,"Accuracy":0+30,"Magic Accuracy":0+30,"Magic Damage":155,"Magic Accuracy Skill":228,"Polearm Skill":269,"Store TP":10,"TP Bonus":500,"Jobs":["drg"]}
Ryunohige = {"Name":"Ryunohige","Name2":"Ryunohige R15","Type":"Weapon","Skill Type":"Polearm","DMG":307+32,"Delay":492,"Accuracy":0+30,"Magic Accuracy":0+30,"Magic Damage":155,"Magic Accuracy Skill":228,"Polearm Skill":269,"Jobs":["drg"]}
Rhongomiant = {"Name":"Rhongomiant","Name2":"Rhongomiant R15","Type":"Weapon","Skill Type":"Polearm","DMG":347+12,"Delay":492,"VIT":50+20,"STR":20,"Magic Damage":155,"Magic Accuracy Skill":228,"Polearm Skill":269,"Jobs":["drg"]}
Loxotic_Mace = {"Name":"Loxotic Mace +1", "Name2":"Loxotic Mace +1 R15", "DMG":190+33,"Delay":334,"Type":"Weapon","Skill Type":"Club","Club Skill":242,"Accuracy":21+40,"Magic Accuracy":0+40,"Attack":21,"Magic Accuracy Skill":188,"DEX":9,"Weaponskill Damage":10,"Jobs":["war","drk","run"]}
Mandau = {"Name":"Mandau","Name2":"Mandau R15","Type":"Weapon","Skill Type":"Dagger","DMG":124+7,"Delay":176,"TA DMG":10,"Attack":60,"Dagger Skill":269,"Magic Accuracy Skill":228,"Crit Rate":5,"Crit Damage":5,"Jobs":["rdm","thf","brd"]}
Nandaka = {"Name":"Nandaka","Type":"Weapon","Skill Type":"Great Sword","DMG":333,"Delay":480,"DEX":20,"INT":20,"MND":20,"Accuracy":40,"Magic Accuracy":40,"Attack":30,"Magic Attack":21,"Magic Damage":226,"Great Sword Skill":250,"Magic Accuracy Skill":250,"Jobs":["war","pld","drk","run"]}
Montante = {"Name":"Montante +1","Name2":"Montante +1 R15","Type":"Weapon","Skill Type":"Great Sword","DMG":299+20,"Delay":475,"Great Sword Skill":242,"Magic Accuracy Skill":188,"Accuracy":0+40,"Magic Accuracy":0+40,"Attack":34,"TA":5,"Jobs":["war","pld","drk","run"]}
Akademos = {"Name":"Akademos","Name2":"Akademos R15C","Type":"Weapon","Skill Type":"Staff","DMG":198,"Delay":366,"INT":12+15,"MND":12,"Magic Accuracy":10+15,"Magic Attack":38+15,"Magic Damage":217,"Staff Skill":242,"Magic Accuracy Skill":228,"Magic Burst Damage":10,"Jobs":["sch"]}
Crocea_Mors = {"Name":"Crocea Mors", "Name2":"Crocea Mors R25C", "Type":"Weapon","Skill Type":"Sword","DMG":180+7,"Delay":260,"Accuracy":50,"Magic Accuracy":50,"Magic Damage":217,"Sword Skill":269,"Magic Accuracy Skill":255,"Jobs":["rdm"]} # Elemental WS damage is applied in the WS python files.
Daybreak = {"Name":"Daybreak","Type":"Weapon","Skill Type":"Club","DMG":150,"Delay":216,"Magic Accuracy":40,"Magic Attack":40,"Magic Accuracy Skill":242,"Magic Damage":241,"Club Skill":228,"MND":30,"Light Elemental Bonus":50,"Jobs":["whm","blm","rdm","brd","smn","sch","geo"]}
Mjollnir = {"Name":"Mjollnir","Name2":"Mjollnir R15","Type":"Weapon","Skill Type":"Club","DMG":217+12,"Delay":308,"Attack":60,"Accuracy":20,"Magic Accuracy":20,"Magic Damage":217,"Club Skill":269,"Magic Accuracy Skill":255,"Jobs":["whm"]}
Yagrush = {"Name":"Yagrush","Name2":"Yagrush R15","Type":"Weapon","Skill Type":"Club","DMG":167+17,"Delay":267,"Magic Accuracy":40+30,"Magic Damage":217,"Club Skill":269,"Magic Accuracy Skill":255,"Accuracy":0+30,"Jobs":["whm"]}
Gambanteinn = {"Name":"Gambanteinn","Name2":"Gambanteinn R15","Type":"Weapon","Skill Type":"Club","DMG":212+7,"Delay":300,"MND":20,"Magic Damage":217,"Club Skill":269,"Magic Accuracy Skill":255,"Jobs":["whm"]}
Tishtrya = {"Name":"Tishtrya", "Name2":"Tishtrya R15","Type":"Weapon","Skill Type":"Club","DMG":185+8,"Delay":264,"Accuracy":0+30,"Magic Accuracy":0+30,"TP Bonus":500,"Magic Damage":217,"Magic Accuracy Skill":255,"Club Skill":269,"Store TP":10,"Jobs":["whm","geo"]}
Sindri = {"Name":"Sindri", "Name2":"Sindri R15","Type":"Weapon","Skill Type":"Club","DMG":175,"Delay":324,"Accuracy":27+50,"Attack":15+30,"DA":4+5,"INT":6,"MND":6,"Magic Damage":90,"Magic Accuracy Skill":188,"Club Skill":228,"Jobs":["whm"]}
Chango = {"Name":"Chango", "Name2":"Chango R15","Type":"Weapon", "Skill Type":"Great Axe", "DMG":336+16, "Delay":480, "Magic Damage":155, "Great Axe Skill":269, "Magic Accuracy Skill":228, "Store TP":10, "TP Bonus":500, "Accuracy":30,"Magic Accuracy":30,"Jobs":["war"]}#Karambit = {"Name": "Karambit" "Skill Type":"Hand-to-Hand", "Type":"Weapon", "DMG":"Base+180","Delay":"base+96", "STR":20, "DEX":20,"VIT":20,"Accuracy":40,"Attack":30,"Magic Accuracy":40,"Hand-to-Hand Skill":250, "Magic Accuracy Skill":250}
Ukonvasara = {"Name":"Ukonvasara","Name2":"Ukonvasara R15","STR":50+20, "DEX":0+20, "DMG":340+12, "Delay":482, "Great Axe Skill":269, "Type":"Weapon", "Skill Type":"Great Axe","Jobs":["war"]}
Conqueror = {"Name":"Conqueror","Name2":"Conqueror R15", "DMG":315+32, "Delay":504, "Accuracy":30, "Magic Accuracy":30, "Great Axe Skill":269, "Magic Accuracy Skill":228, "Type":"Weapon", "Skill Type":"Great Axe","Jobs":["war"]}
Bravura = {"Name":"Bravura","Name2":"Bravura R15", "DMG":344+20, "Delay":488, "Accuracy":60, "DA DMG":20, "Great Axe Skill":269, "Magic Accuracy Skill":228, "Type":"Weapon", "Skill Type":"Great Axe","Jobs":["war"]}
Dolichenus = {"Name":"Dolichenus","DEX":15,"INT":15, "MND":15, "DMG":200, "Delay":288, "Accuracy":40, "Attack":30, "Magic Accuracy":40, "Magic Attack":16, "Magic Damage":217, "Axe Skill":250, "Magic Accuracy Skill":250, "Type":"Weapon", "Skill Type":"Axe","Jobs":["war","drk","bst","rng","run"]}
Laevateinn = {"Name":"Laevateinn","Name2":"Laevateinn R15", "DMG":251+26, "Delay":402, "Accuracy":30+30, "Magic Accuracy":30+30, "Magic Attack":70+49, "Magic Damage":279, "Magic Accuracy Skill":269, "Type":"Weapon", "Skill Type":"Staff","Jobs":["blm"]}
Khatvanga = {"Name":"Khatvanga","Name2":"Khatvanga R15","DMG":268+8, "Delay":402, "Magic Damage":279, "Magic Accuracy Skill":269,"Accuracy":0+30, "Magic Accuracy":0+30, "TP Bonus":500, "Type":"Weapon", "Skill Type":"Staff","Jobs":["blm","smn","sch"]}
Hvergelmir = {"Name":"Hvergelmir","Name2":"Hvergelmir R15","DMG":275+10, "Delay":390, "Magic Damage":279, "Magic Accuracy Skill":269, "Type":"Weapon", "Skill Type":"Staff","Jobs":["blm","smn","sch"]}
Claustrum = {"Name":"Claustrum","Name2":"Claustrum R15", "DMG":275+16, "Delay":390, "Accuracy":60, "Magic Damage":279, "Magic Accuracy Skill":269, "Type":"Weapon", "Skill Type":"Staff","Jobs":["blm","smn"]}
Tizona = {"Name":"Tizona","Name2":"Tizona R15","DMG":147+18, "Delay":236, "Accuracy":0+30, "Magic Accuracy":40+30, "Magic Damage":186, "Magic Accuracy Skill":255, "Type":"Weapon", "Skill Type":"Sword", "Sword Skill":269,"Jobs":["blu"]}
Terpsichore = {"Name":"Terpsichore","Name2":"Terpsichore R15","DMG":128+16, "Delay":205, "Magic Damage":155, "Dagger Skill":269, "Magic Accuracy Skill":228, "Type":"Weapon", "Skill Type":"Dagger","Jobs":["dnc"]}
Tupsimati = {"Name":"Tupsimati","Name2":"Tupsimati R15","DMG":251, "Delay":402, "Accuracy":40+30, "Magic Accuracy":40+30, "Magic Attack":50+49, "Magic Damage":279, "Magic Accuracy Skill":269, "Type":"Weapon", "Skill Type":"Staff","Jobs":["sch"]}
Carnwenhan = {"Name":"Carnwenhan","Name2":"Carnwenhan R15","DMG":116+14, "Delay":186, "Magic Accuracy":40+30,"Accuracy":0+30, "Magic Damage":155, "Dagger Skill":269, "Magic Accuracy Skill":255, "Type":"Weapon", "Skill Type":"Dagger","Jobs":["brd"]}
Aeneas = {"Name":"Aeneas","Name2":"Aeneas R15","DMG":140+6, "Delay":200, "Accuracy":0+30,"Magic Accuracy":0+30, "Magic Damage":155, "Dagger Skill":269, "Magic Accuracy Skill":228, "Store TP":10, "TP Bonus":500, "Type":"Weapon", "Skill Type":"Staff","Jobs":["thf","brd","dnc"]}
Kustawi = {"Name":"Kustawi +1","Name2":"Kustawi +1 R25","Type":"Weapon","Skill Type":"Dagger","DMG":114, "Delay":189, "Ranged Accuracy":25+40, "Ranged Attack":16+20, "Dagger Skill":242, "Magic Accuracy Skill":188, "Magic Accuracy":0+40, "Jobs":["war","thf","pld","drk","brd","rng","sam","nin","drg","cor","pup","dnc"]}
Twashtar = {"Name":"Twashtar","Name2":"Twashtar R25","Type":"Weapon", "Skill Type":"Dagger","DEX":50+20, "AGI":0+20, "DMG":124+4, "Delay":176, "Magic Damage":155, "Dagger Skill":269, "Magic Accuracy Skill":228, "Jobs":["thf","brd","dnc"]}
Centovente = {"Name": "Centovente", "Skill Type": "Dagger", "Type":"Weapon", "DMG":42, "Delay":186, "TP Bonus":1000, "Dagger Skill":0, "Jobs":["thf","brd","dnc"]}
Malignance_Pole = {"Name":"Malignance Pole","VIT":40,"DMG":286, "Delay":412, "Type":"Weapon", "Skill Type":"Staff","Staff Skill":255,"Accuracy":40, "Magic Accuracy Skill":215, "Weaponskill Damage":15, "Jobs":["mnk","whm","blm","pld","drg","smn","sch","geo"]}
Mafic_Cudgel = {"Name":"Mafic Cudgel","VIT":15,"INT":6, "MND":6, "DMG":142, "Delay":278, "Type":"Weapon", "Skill Type":"Club", "Accuracy":27, "Club Skill":228, "Magic Accuracy Skill":188, "Jobs":all_jobs}
Drepanum = {"Name":"Drepanum", "Type":"Weapon", "Skill Type":"Scythe", "DEX":20, "INT":20, "MND":20,  "DMG":366, "Delay":528, "Accuracy":40, "Attack":30, "Magic Accuracy":40, "Magic Attack":21, "Magic Damage":226, "Magic Accuracy Skill":250,"Scythe Skill":250, "Jobs":["war","blm","drk","bst"]}
Xoanon = {"Name":"Xoanon", "Type":"Weapon", "Skill Type":"Staff", "INT":20, "MND":20, "CHR":20, "DMG":254, "Delay":366, "Accuracy":40, "Magic Accuracy":40, "Magic Attack":26, "Magic Damage":241, "Magic Accuracy Skill":250, "Staff Skill":250,"Jobs":["war","mnk","whm","blm","rdm","bst","brd","smn","sch","geo"]}

Alber_Strap = {"Name": "Alber Strap", "Skill Type":"None", "Type": "Grip", "Magic Attack":7, "DA":2,"Jobs":all_jobs}
Rigorous_Grip = {"Name": "Rigorous Grip +1", "Name2": "Rigorous Grip +1 R15", "Skill Type":"None", "Type":"Grip", "STR":4+15, "Attack":13+30, "Accuracy":3,"Jobs":all_jobs}
Utu_Grip = {"Name": "Utu Grip", "Skill Type":"None", "Type": "Grip", "Accuracy":30, "Attack":30,"Jobs":["drk","sam","war","drg","run"]}
Niobid_Strap = {"Name":"Niobid Strap","Skill Type":"None", "Type":"Grip", "Accuracy":5, "Magic Accuracy":5, "Magic Attack":5,"Jobs":all_jobs}
Enki_Strap = {"Name":"Enki Strap", "INT":10,"MND":10,"Magic Accuracy":10, "Skill Type":"None", "Type":"Grip","Jobs":["blm","rdm","sch","geo"]}

Ammurapi_Shield = {"Name":"Ammurapi Shield", "Type":"Shield", "Skill Type": "Shield", "INT":13, "MND":13, "Magic Accuracy":38, "Magic Attack":38,"Jobs":["blm","sch","rdm","geo"]}
Blurred_Shield = {"Name":"Blurred Shield +1","Type":"Shield","Skill Type":"Shield","Accuracy":20,"Attack":20,"Fencer":1,"Weaponskill Damage":7,"Jobs":["war","pld","drk"]}
Nusku_Shield = {"Name":"Nusku Shield +1","Type":"Shield","Skill Type":"Shield","Ranged Accuracy":20,"Ranged Attack":20,"Store TP":3,"Jobs":["rng","cor"]}

mains = [Xoanon,Drepanum,Mafic_Cudgel,Malignance_Pole,Twashtar,Kustawi,Aeneas,Carnwenhan,Tupsimati,Terpsichore,Tizona,Claustrum,Hvergelmir,Khatvanga,Laevateinn,Dolichenus,Bravura,Conqueror,Ukonvasara,Chango,Mjollnir,Tishtrya,Gambanteinn,Yagrush,Daybreak,Crocea_Mors,Akademos,Montante,Nandaka,Mandau,Loxotic_Mace,Rhongomiant,Ryunohige,Trishula,Gungnir,Murgleis,Sequence,Excalibur,Almace,Maxentius,Amanomurakumo,Anguta,Apocalypse,Caladbolg,Crepuscular_Knife,Dojikiri,Gleti_Knife,Gokotai,Hachimonji,Heishi,Kannagi,Kikoku,Kogarasumaru,Kunimitsu,Liberator,Masamune,Naegling,Nagi,Ragnarok,Redemption,Shining_One,Tauret,Ternion,Tsuru,MalevolenceA,MalevolenceB,Marin_Staff,Bunzi_Rod]
subs = [Centovente,Nusku_Shield,Daybreak,Sindri,Thibron,Maxentius, Crepuscular_Knife,Gleti_Knife,Gokotai,Hitaki,Kunimitsu,Naegling,Tauret,Ternion,Tsuru,MalevolenceA,MalevolenceB,Bunzi_Rod,Ammurapi_Shield,Blurred_Shield,Empty]
grips = [Rigorous_Grip, Utu_Grip, Enki_Strap, Alber_Strap, Niobid_Strap]



Date = {"Name": "Date Shuriken", "Skill Type": "Throwing", "Type":"Shuriken", "DMG": 125, "Delay": 192, "Accuracy": 5, "Ranged Accuracy": 5, "Throwing Skill": 242, "DEX": 5, "AGI": 5, "Jobs":["nin"]}
Happo = {"Name": "Happo Shuriken", "Skill Type": "Throwing", "Type":"Shuriken", "DMG":  99, "Delay": 188, "Accuracy": 6, "Attack": 6, "Ranged Accuracy": 11, "Throwing Skill": 228, "Crit Rate": 2, "Jobs":["nin"]}
Seki = {"Name": "Seki Shuriken", "Skill Type": "Throwing", "Type":"Shuriken", "DMG": 101, "Delay": 192, "Attack": 13, "Store TP": 2, "Throwing Skill": 242, "Jobs":["nin"]}
Donar_Gun = {"Name": "Donar Gun", "Type":"Gun","DMG":103,"Delay":548,"Skill Type":"Marksmanship","Marksmanship Skill":228, "DEX":5, "AGI":5, "Thunder Elemental Bonus": 15, "Jobs":["nin","rng","thf","cor"]} 
Ullr = {"Name":"Ullr","Type":"Bow","Skill Type":"Archery","Archery Skill":250,"DMG":178,"Delay":360,"STR":15,"DEX":15,"AGI":15,"Ranged Accuracy":40,"Ranged Attack":30,"Magic Accuracy":40,"Jobs":["war","rdm","thf","pld","drk","bst","rng","sam","nin"]}
Yoichinoyumi = {"Name":"Yoichinoyumi","Name2":"Yoichinoyumi R15", "DMG":303+7, "Delay":524, "Ranged Accuracy":90, "Ranged Attack":45, "Archery Skill":269, "Type":"Bow", "Skill Type":"Archery","Crit Rate":5,"Jobs":["rng","sam"]}
Armageddon = {"Name":"Armageddon","Name2":"Armageddon R15","STR":0+20,"AGI":50+20,"DMG":143+8, "Delay":582, "Magic Damage":217, "Marksmanship Skill":269, "Type":"Gun", "Skill Type":"Marksmanship","Jobs":["rng","cor"]}
Fomalhaut = {"Name":"Fomalhaut","Name2":"Fomalhaut R15","DMG":167+9, "Delay":600, "Accuracy":0+30, "Magic Accuracy":40+30, "Magic Damage":155, "Marksmanship Skill":269, "Store TP":10, "TP Bonus":500, "Type":"Gun", "Skill Type":"Marksmanship","Jobs":["rng","cor"]}
Death_Penalty = {"Name":"Death Penalty","Name2":"Death Penalty R15","Ranged Accuracy":30, "Magic Accuracy":30,"DMG":101+6, "Delay":480, "Magic Damage":217, "Marksmanship Skill":269, "Quick Draw II":60,"Type":"Gun", "Skill Type":"Marksmanship","Jobs":["cor"]}
Ataktos = {"Name":"Ataktos","DMG":53, "Delay":600, "Type":"Gun", "Skill Type":"Marksmanship","TP Bonus":1000,"Jobs":["cor","rng"]}
Molybdosis = {"Name":"Molybdosis","AGI":25,"DMG":103, "Delay":480, "Ranged Attack":45, "Magic Attack":30, "Type":"Gun","Skill Type":"Marksmanship", "Marksmanship Skill":242, "Crit Damage":10, "Jobs":["cor"]}
ranged = [Molybdosis,Ataktos,Death_Penalty,Fomalhaut,Yoichinoyumi,Armageddon,Empty,Donar_Gun,Ullr]

# Linos is pretty annoying. Define a loop to create them all here. Ignore snow_stats since you'll want Acc/Atk+15 anyway
dusk_stats = ["STR","DEX","VIT","AGI","INT","MND","CHR"]
leaf_stats = ["Weaponskill Damage", "DA", "Crit Rate"]
for base_stat in dusk_stats:
    for main_stat in leaf_stats:
        ranged.append({"Name":"Linos","Name2":f"Linos {base_stat} {main_stat}", "Type":"Instrument", "Skill Type":"Instrument","Accuracy":15, "Attack":15,f"{base_stat}":8, f"{main_stat}":3, "Jobs":["brd"]})


Aurgelmir_Orb = {"Name": "Aurgelmir Orb +1","Type":"Equipment", "STR":7, "DEX":7, "VIT":7, "Attack":10, "Store TP":5, "Jobs":["nin","drk","sam","rdm","drg","war","mnk","rdm","thf","pld","bst","brd","rng","blu","cor","dnc","run"]}
Cath_Palug_Stone = {"Name": "Cath Palug Stone","Type":"Equipment", "DEX":10, "AGI":10, "Accuracy":15, "Jobs":["nin","thf","dnc","run"]}
Coiste_Bodhar = {"Name": "Coiste Bodhar", "Name2": "Coiste Bodhar R25","Type":"Equipment", "Attack":15,"STR":8,"DA":3,"Store TP":3,"Jobs":["nin","drk","sam","drg","rdm","war","mnk","thf","pld","bst","rng","blu","cor","dnc","run"]}
Crepuscular_Pebble = {"Name": "Ghastly Tathlum", "Name2": "Crepuscular Pebble","Type":"Equipment", "STR":3, "VIT":3, "PDL":3, "Jobs":all_jobs}
Ghastly_Tathlum = {"Name": "Ghastly Tathlum +1", "Name2": "Ghastly Tathlum +1 R15","Type":"Equipment", "Magic Damage":11+10, "INT":6+5, "Jobs":all_jobs}
Knobkierrie = {"Name": "Knobkierrie","Type":"Equipment", "Attack":23, "Weaponskill Damage":6, "Jobs":["drk","sam","war","mnk","drg","run"]}
Oshashas_Treatise = {"Name":"Oshasha's Treatise","Type":"Equipment","Accuracy":5,"Attack":5,"Weaponskill Damage":3,"Jobs":all_jobs}
Pemphredo_Tathlum = {"Name": "Pemphredo Tathlum","Type":"Equipment", "INT":4, "Magic Accuracy":8, "Magic Attack":4, "Jobs":all_jobs}
Seething_Bomblet = {"Name": "Seething Bomblet +1", "Name2": "Seeth. Bomblet +1 R15","Type":"Equipment", "Accuracy":13, "Attack":13, "Magic Attack":7, "STR":4+10, "Gear Haste":0+4, "Jobs":["nin","drk","war","run"]}
Yetshila = {"Name": "Yetshila +1","Type":"Equipment", "Crit Rate":2, "Crit Damage":6, "Jobs":["nin","drk","thf","rdm","war","cor","run"]}
Voluspa_Tathlum = {"Name":"Voluspa Tathlum","Type":"Equipment","STR":5,"DEX":5,"CHR":5,"Accuracy":10,"Attack":10,"Jobs":["mnk","rdm","thf","bst","rng","nin","drg","cor","pup","dnc","run"]}
Amar_Cluster = {"Name":"Amar Cluster","Type":"Equipment","STR":2,"Accuracy":10,"Jobs":["war","mnk","whm","blm","rdm","thf","pld","drk","bst","brd","rng","sam","nin","drg","smn","blu","cor","pup","dnc","sch","geo","run"]}
Floestone = {"Name":"Floestone","Type":"Equipment","STR":3,"INT":5,"Attack":10,"Jobs":["war","mnk","whm","blm","rdm","thf","pld","drk","bst","brd","rng","sam","nin","drg","smn","blu","cor","pup","dnc","sch","geo","run"]}
Sroda_Tathlum = {"Name":"Sroda Tathlum","Type":"Equipment","Magic Accuracy":-10,"Magic Crit Rate II":10,"Jobs":["blm","rdm","sch","geo"]} 


Living_Bullet = {"Name":"Living Bullet", "Type":"Bullet", "DMG":245,"Delay":240,"Magic Accuracy":25,"Magic Attack":35,"Jobs":["cor"]}
Test_Bullet = {"Name":"Bullet","Name2":"Test Bullet", "Type":"Bullet", "DMG":999,"Delay":999,"DEX":150,"STR":150,"Attack":150,"Ranged Attack":150,"Jobs":all_jobs}
Test_Arrow = {"Name":"Stone Arrow","Name2":"Test Arrow", "Type":"Arrow", "DMG":999,"Delay":999,"MND":150,"INT":150,"Magic Attack":150,"Jobs":all_jobs}
Beryllium_Arrow = {"Name":"Beryllium Arrow","Type":"Arrow","DMG":77,"Delay":90,"Ranged Accuracy":12,"Jobs":["war","rdm","thf","pld","drk","bst","rng","sam","nin"]}
Raetic_Arrow = {"Name":"Raetic Arrow","Type":"Arrow","DMG":80,"Delay":90,"Ranged Accuracy":10,"Jobs":["war","blm","rdm","thf","pld","drk","bst","brd","rng","sam","nin","smn","blu","sch"]}
Yoichi_Arrow = {"Name":"Yoichi's Arrow", "DMG":89, "Delay":90, "Ranged Accuracy":35, "Ranged Attack":25, "Type":"Arrow","Jobs":["rng","sam"]}
Devastating_Bullet = {"Name":"Devastating Bullet","DMG":277,"Delay":240,"Ranged Accuracy":35,"Magic Accuracy":35,"Type":"Bullet","Jobs":["cor","rng"]}
Chrono_Bullet = {"Name":"Chrono Bullet","DMG":300,"Delay":240,"Ranged Accuracy":20,"Ranged Attack":20,"Type":"Bullet","Jobs":["cor","rng"]}
Hauksbok_Bullet = {"Name":"Hauksbok Bullet","DMG":300,"Delay":240,"AGI":10,"Magic Attack":40,"Type":"Bullet","Jobs":["cor","rng"]}
Hauksbok_Arrow = {"Name":"Hauksbok Arrow","DMG":110,"Delay":90,"STR":10,"Weaponskill Damage":20,"Ranged Accuracy":20,"Type":"Arrow","Jobs":["rng"]}
ammos = [Hauksbok_Bullet,Devastating_Bullet,Chrono_Bullet,Yoichi_Arrow,Sroda_Tathlum,Beryllium_Arrow,Living_Bullet,Floestone, Amar_Cluster,Voluspa_Tathlum,Date,Happo,Seki,Aurgelmir_Orb,Cath_Palug_Stone,Coiste_Bodhar,Crepuscular_Pebble,Ghastly_Tathlum,Knobkierrie,Oshashas_Treatise,Pemphredo_Tathlum,Seething_Bomblet,Yetshila,Empty]
# Raetic Arrow does not proc for weapon skills.


Adhemar_Bonnet_A = {"Name": "Adhemar Bonnet +1", "Name2": "Adhemar Bonnet +1 A", "STR":19, "DEX":21+12, "VIT":15, "AGI":19+12, "INT":14, "MND":14, "CHR":14, "Accuracy":0+20, "Attack":36, "Ranged Attack":36, "Gear Haste":8, "TA":4, "Crit Damage":6,"Jobs":["mnk","thf","rng","nin","blu","cor","dnc","run"]}
Adhemar_Bonnet_B = {"Name": "Adhemar Bonnet +1", "Name2": "Adhemar Bonnet +1 B", "STR":19+12, "DEX":21+12, "VIT":15, "AGI":19, "INT":14, "MND":14, "CHR":14, "Attack":36+20, "Ranged Attack":36, "Gear Haste":8, "TA":4, "Crit Rate": 6,"Jobs":["mnk","thf","rng","nin","blu","cor","dnc","run"]}
Blistering_Sallet = {"Name": "Blistering Sallet +1", "Name2": "Blistering Sallet +1 R15", "STR":16+25, "DEX":16+25, "VIT":16, "AGI":16, "INT":16, "MND":16, "CHR":16, "Accuracy":6+45, "Magic Accuracy":0+45, "Gear Haste":8, "DA":3, "Crit Rate":10,"Jobs":all_jobs}
Dampening_Tam = {"Name": "Dampening Tam", "STR":18, "DEX":24+10, "VIT":18, "AGI":20, "INT":18, "MND":22, "CHR":18, "Accuracy":20+15,"Ranged Accuracy":20,"Magic Accuracy":20+15,"Gear Haste":7,"QA":3,"Jobs":["nin","thf","dnc","run","mnk","rng","cor","blu"]}
Flamma_Zucchetto = {"Name": "Flamma Zucchetto +2", "STR":36,"DEX":32,"VIT":24,"AGI":16,"INT":12,"MND":12,"CHR":12,"Accuracy":44,"Magic Accuracy":44,"Gear Haste":4,"Store TP":6,"TA":5,"Jobs":["drk","sam","war","pld","drg"]}
Hachiya_Hatsuburi = {"Name": "Hachiya Hatsuburi +3", "STR": 33, "DEX": 33, "VIT":32, "AGI":32, "INT":31, "MND":31, "CHR": 31, "Magic Accuracy": 54, "Ninjutsu Skill": 17, "Gear Haste": 8, "Weaponskill Damage":10,"Jobs":["nin"]}
Hizamaru_Somen = {"Name": "Hizamaru Somen +2", "STR":33, "DEX":29, "VIT":27, "AGI":24, "INT":12, "MND":10, "CHR":20, "Accuracy":20, "Attack":26, "Gear Haste":6,"Jobs":["nin","sam","mnk","pup"]}
Kendatsuba_Jinpachi = {"Name": "Kendatsuba Jinpachi +1", "STR":23,"DEX":47,"VIT":32,"AGI":34,"INT":19,"MND":17,"CHR":19,"Accuracy":50,"Ranged Accuracy":45,"Gear Haste":6,"TA":4,"Crit Rate":5,"Jobs":["nin","sam","mnk"]}
Malignance_Chapeau = {"Name": "Malignance Chapeau", "STR":11,"DEX":40,"VIT":19,"AGI":33,"INT":25,"MND":16,"CHR":17,"Accuracy":50,"Ranged Accuracy":50,"Magic Accuracy":50,"Gear Haste":6,"Store TP":8,"PDL":3,"Jobs":["mnk", "rdm", "thf", "bst", "rng", "nin", "blu", "cor", "pup", "dnc"]}
Mochizuki_Hatsuburi = {"Name": "Mochizuki Hatsuburi +3", "STR":31, "DEX":31, "VIT":33, "AGI":33, "INT":32, "MND":32, "CHR":32, "Accuracy":44,"Attack":62,"Magic Accuracy": 37, "Magic Attack": 61, "Gear Haste": 8, "Ninjutsu Magic Attack": 21,"Jobs":["nin"]}
Mpaca_Cap = {"Name": "Mpaca's Cap", "Name2": "Mpaca's Cap R25", "STR":33, "DEX":30, "VIT":26, "AGI":24, "INT":20, "MND":17, "CHR":20,"Accuracy":40+10,"Attack":40+25,"Magic Accuracy":40+10,"Gear Haste":6,"TA":3,"Crit Rate":4,"TP Bonus":200,"Jobs":["nin","sam","mnk","pup"]}
Mummu_Bonnet = {"Name": "Mummu Bonnet +2", "STR":20,"DEX":39,"VIT":16,"AGI":34,"INT":15,"MND":14,"CHR":17,"Accuracy":44,"Ranged Accuracy":44,"Magic Accuracy":44,"Gear Haste":8,"Crit Rate":5,"Jobs":["nin","mnk","thf","rng","cor","dnc"]} 
Nyame_Helm = {"Name": "Nyame Helm", "Name2": "Nyame Helm R25 B", "STR":26, "DEX":25, "VIT":24, "AGI":23, "INT":28, "MND":26, "CHR":24,"Accuracy":40,"Attack":30+30, "Gear Haste":6,"Weaponskill Damage":0+10,"DA":0+4,"Magic Accuracy":40,"Magic Attack":30,"Ranged Accuracy":40,"Ranged Attack":30+30,"Magic Burst Damage":5,"Jobs":all_jobs}
Pixie_Hairpin = {"Name": "Pixie Hairpin +1", "INT":27, "Dark Elemental Bonus":28,"Jobs":all_jobs}
Ratri_Sallet = {"Name": "Ratri Sallet +1", "STR":40, "DEX":33, "VIT":26, "AGI":21, "INT":26, "MND":23, "CHR":22, "Magic Accuracy":45, "Scythe Skill":54, "Gear Haste":7, "Weaponskill Damage":8,"Jobs":["drk"]}
Ryuo_Somen_A = {"Name": "Ryuo Somen +1", "Name2": "Ryuo Somen +1 A", "STR":21+12, "DEX":17+12, "VIT":14, "AGI":20, "INT":11, "MND":11, "CHR":11, "Accuracy":35+20,"Ranged Accuracy":35,"Gear Haste":7,"Store TP":7,"Dual Wield":9,"Jobs":["nin","sam","mnk","pup"]}
Sakpata_Helm = {"Name": "Sakpata's Helm", "Name2": "Sakpata's Helm R25", "STR":33,"DEX":20,"VIT":40,"AGI":21,"INT":19,"MND":23,"CHR":21,"Accuracy":40+10,"Magic Accuracy":40+10,"Attack":40+25,"Gear Haste":4,"DA":5,"PDL":5,"DA DMG":0+13,"Jobs":["drk","war","pld"]}
Sulevia_Mask = {"Name": "Sulevia's Mask +2", "STR":33,"DEX":19,"VIT":40,"AGI":12,"INT":11,"MND":22,"CHR":22,"Accuracy":44,"Attack":48,"Gear Haste":3,"Store TP":10,"Jobs":["drk","war","pld","drg"]}
Hattori_Zukin = {"Name": "Hattori Zukin +3", "STR":31,"DEX":41,"VIT":28,"AGI":34,"INT":27,"MND":27,"CHR":27,"Accuracy":61,"Attack":61,"Ranged Accuracy":61,"Magic Accuracy":61,"Gear Haste":10,"Dual Wield":7,"Jobs":["nin"]}
Heathen_Burgeonet = {"Name": "Heathen's Burgeonet +3", "STR":42,"DEX":26,"VIT":33,"AGI":28,"INT":31,"MND":27,"CHR":29,"Accuracy":61,"Attack":61,"Magic Accuracy":61,"Gear Haste":7,"Scythe Skill":38,"DA":6,"PDL":10,"Jobs":["drk"]}
Amalric_Coif = {"Name":"Amalric Coif +1", "Name2":"Amalric Coif +1A",   "STR":10,"DEX":10,"VIT":10,"AGI":1,"INT":24,"MND":20,"CHR":19,"Magic Accuracy":36+20,"Magic Attack":0+20,"Magic Burst Damage":0,"Magic Burst Damage II":0,"Magic Damage":0,"Gear Haste":6,"Jobs":["blm","sch","rdm","geo","blu"]}
Ea_Hat = {"Name":"Ea Hat +1","STR":20,"DEX":21,"VIT":24,"AGI":25,"INT":43,"MND":29,"CHR":29,"Magic Accuracy":50,"Magic Attack":38,"Magic Burst Damage":7, "Magic Burst Damage II":7,"Gear Haste":6,"Jobs":["blm", "rdm", "geo"]}
Agwu_Cap = {"Name":"Agwu's Cap", "Name2": "Agwu's Cap R25", "STR":26,"DEX":24,"VIT":11,"AGI":5,"INT":33,"MND":26,"CHR":25, "Accuracy":40+10, "Magic Accuracy":40+10,"Magic Attack":35+23,"Magic Burst Damage":7,"Magic Burst Damage II":0,"Magic Damage":20+13,"Gear Haste":6,"Jobs":["blm", "sch", "geo", "run"]}
Wicce_Petasos = {"Name":"Wicce Petasos +3", "STR":22,"DEX":25,"VIT":27,"AGI":16,"INT":39,"MND":32,"CHR":32, "Accuracy":61,"Magic Accuracy":61,"Magic Attack":51,"Magic Burst Damage":0,"Magic Burst Damage II":0,"Magic Damage":31,"Elemental Magic Skill":35,"Gear Haste":6,"Jobs":["blm"]}
Archmage_Petasos = {"Name":"Archmage's Petasos +3", "STR":24,"DEX":24,"VIT":24,"AGI":24,"INT":34,"MND":29,"CHR":29, "Magic Accuracy":43,"Magic Attack":55, "Elemental Magic Skill":21, "Accuracy":37,"Gear Haste":6,"Jobs":["blm"]}
Spaekona_Petasos = {"Name":"Spaekona Petasos +3", "STR":29,"DEX":29,"VIT":29,"AGI":29,"INT":37,"MND":34,"CHR":34,"Magic Accuracy":47,"Magic Damage":42,"Magic Attack":23,"Gear Haste":6,"Jobs":["blm"]}
Gleti_Mask = {"Name":"Gleti's Mask", "Name2":"Gleti's Mask R25", "STR":33,"DEX":28,"VIT":30,"AGI":23,"INT":19,"MND":19,"Accuracy":40+10,"Magic Accuracy":40+10,"Attack":40+25,"Gear Haste":6,"PDL":6,"Crit Rate":5,"Jobs":["thf","bst","drg","blu","dnc"]}
Jhakri_Coronal = {"Name":"Jhakri Coronal +2","STR":31,"DEX":27,"VIT":7,"AGI":1,"INT":36,"MND":21,"CHR":20,"Accuracy":44,"Attack":44,"Magic Accuracy":44,"Magic Attack":41,"Gear Haste":3,"Skillchain Bonus":7,"Jobs":["blm","rdm","blu","sch","geo"]}
Vitiation_Chapeau = {"Name":"Vitiation Chapeau +3","STR":24,"DEX":24,"VIT":24,"AGI":24,"INT":29,"MND":42,"CHR":29,"Accuracy":37,"Attack":62,"Magic Accuracy":37,"Gear Haste":6,"Weaponskill Damage":6, "Jobs":["rdm"]}
Lethargy_Chappel = {"Name":"Lethargy Chappel +3","STR":25,"DEX":29,"VIT":25,"AGI":25,"INT":38,"MND":38,"CHR":30,"Accuracy":61,"Attack":61,"Magic Accuracy":61,"Magic Attack":56,"Magic Damage":31,"Gear Haste":6,"Jobs":["rdm"]}
Vishap_Armet = {"Name":"Vishap Armet +3","STR":37,"DEX":30,"VIT":35,"AGI":30,"INT":29,"MND":32,"CHR":29,"Accuracy":47,"Attack":42,"Gear Haste":7, "Jobs":["drg"]}
Pteroslaver_Armet = {"Name":"Pteroslaver Armet +3","STR":37,"DEX":25,"VIT":35,"AGI":25,"INT":24,"MND":24,"CHR":24,"Accuracy":44,"Attack":77,"Magic Accuracy":37, "Gear Haste":7,"TA":4,"Jobs":["drg"]}
Peltast_Mezail = {"Name":"Peltast's Mezail +3","STR":36,"DEX":32,"VIT":35,"AGI":30,"INT":26,"MND":26,"CHR":26,"Accuracy":61,"Attack":71,"Magic Accuracy":61, "Polearm Skill":27, "Gear Haste":7,"Weaponskill Damage":12,"Jobs":["drg"]}
Ayanmo_Zucchetto = {"Name":"Ayanmo Zucchetto +2","STR":20,"DEX":39,"VIT":16,"AGI":23,"INT":15,"MND":25,"CHR":15,"Accuracy":44,"Magic Accuracy":44,"Gear Haste":6,"Store TP":6,"Jobs":["whm","rdm","brd","blu","run"]}
Bunzi_Hat = {"Name":"Bunzi's Hat", "Name2":"Bunzi's Hat R25","STR":16, "DEX":16, "VIT":16, "AGI":0, "INT":34, "MND":33, "CHR":30, "Accuracy":40+10, "Attack":40+25, "Magic Accuracy":40+10, "Magic Attack":30, "Magic Damage":30+25, "Gear Haste":6, "Magic Burst Damage":7, "Store TP":0+7, "Jobs":["whm","rdm", "brd", "smn"]}
Piety_Cap = {"Name":"Piety Cap +3", "Name2":"Piety Cap +3 R25","STR":26, "DEX":26, "VIT":31, "AGI":26, "INT":31, "MND":36, "CHR":31, "Accuracy":37, "Attack":62, "Gear Haste":6, "Jobs":["whm"]}
Arbatel_Bonnet = {"Name":"Arbatel Bonnet +3","STR":24, "DEX":25, "VIT":27, "AGI":16, "INT":38, "MND":34, "CHR":32, "Accuracy":61, "Magic Accuracy":61, "Magic Attack":51, "Magic Damage":31, "Gear Haste":6, "Jobs":["sch"]}
Pedagogy_Mortarboard = {"Name":"Pedagogy Mortarboard +3","STR":24, "DEX":24, "VIT":24, "AGI":24, "INT":39, "MND":39, "CHR":29, "Accuracy":15, "Magic Accuracy":37, "Magic Attack":49, "Gear Haste":6, "Elemental Magic Skill":19, "Magic Burst Damage II":4, "Magic Burst Accuracy":15, "Jobs":["sch"]}
Agoge_Mask = {"Name":"Agoge Mask +3","STR":35, "DEX":28, "VIT":35, "AGI":28, "INT":28, "MND":28, "CHR":28, "Accuracy":37, "Attack":83, "Magic Accuracy":37, "Gear Haste":8, "Weaponskill Damage":10, "Jobs":["war"]}
Boii_Mask = {"Name":"Boii Mask +3","STR":43, "DEX":32, "VIT":42, "AGI":30, "INT":26, "MND":26, "CHR":26, "Accuracy":61, "Attack":71, "Magic Accuracy":61, "Gear Haste":7, "DA":7, "Crit Rate":6, "Jobs":["war"]}
Sakonji_Kabuto = {"Name":"Sakonji Kabuto +3","STR":34, "DEX":30, "VIT":32, "AGI":30, "INT":29, "MND":29, "CHR":29, "Accuracy":45, "Attack":79, "Ranged Accuracy":45, "Ranged Attack":79, "Magic Accuracy":37, "Gear Haste":7, "Store TP":8, "Jobs":["sam"]}
Wakido_Kabuto = {"Name":"Wakido Kabuto +3","STR":37, "DEX":33, "VIT":32, "AGI":30, "INT":29, "MND":29, "CHR":29, "Accuracy":47, "Attack":41, "Gear Haste":7, "Jobs":["sam"]}
Kasuga_Kabuto = {"Name":"Kasuga Kabuto +3","STR":36, "DEX":34, "VIT":35, "AGI":30, "INT":26, "MND":26, "CHR":26, "Accuracy":61, "Attack":61, "Magic Accuracy":61, "Gear Haste":7, "Store TP":12, "Jobs":["sam"]}
Laksamana_Tricorne = {"Name":"Laksamana's Tricorne +3","STR":33, "DEX":34, "VIT":27, "AGI":39, "INT":30, "MND":30, "CHR":31, "Ranged Accuracy":38, "Magic Accuracy":56, "Quick Draw":20, "Gear Haste":8, "Jobs":["cor"]}
Lanun_Tricorne = {"Name":"Lanun Tricorne +3","STR":35, "DEX":29, "VIT":22, "AGI":41, "INT":25, "MND":25, "CHR":26, "Ranged Accuracy":37, "Ranged Attack":87, "Magic Accuracy":37, "Gear Haste":8, "Jobs":["cor"]}
Chasseur_Tricorne = {"Name":"Chasseur's Tricorne +3","STR":31, "DEX":33, "VIT":23, "AGI":40, "INT":27, "MND":27, "CHR":22, "Accuracy":61, "Ranged Accuracy":61, "Ranged Attack":61, "Magic Accuracy":61, "Gear Haste":8, "Jobs":["cor"]}
Brioso_Roundlet = {"Name":"Brioso Roundlet +3","STR":26, "DEX":29, "VIT":26, "AGI":29, "INT":34, "MND":35, "CHR":41, "Magic Accuracy":61, "Gear Haste":6, "Jobs":["brd"]}
Bihu_Roundlet = {"Name":"Bihu Roundlet +3","STR":21, "DEX":24, "VIT":28, "AGI":24, "INT":29, "MND":27, "CHR":40, "Accuracy":37, "Attack":62, "Magic Accuracy":51, "Gear Haste":6, "Jobs":["brd"]}
Fili_Calot = {"Name":"Fili Calot +3","STR":23, "DEX":31, "VIT":22, "AGI":26, "INT":30, "MND":32, "CHR":42, "Accuracy":61, "Magic Accuracy":61, "Gear Haste":6, "Jobs":["brd"]}
Ikenga_Hat = {"Name":"Ikenga's Hat","STR":25, "DEX":32, "VIT":20, "AGI":29, "INT":17, "MND":19, "CHR":20, "Ranged Accuracy":40+10, "Ranged Attack":40+25, "Magic Accuracy":40+10, "Store TP":8, "PDL":4, "Magic Attack":0+40, "Jobs":["rng","cor"]}
Meghanada_Visor = {"Name":"Meghanada Visor +2","STR":27, "DEX":33, "VIT":15, "AGI":31, "INT":12, "MND":22, "CHR":23, "Accuracy":48, "Attack":44, "Ranged Accuracy":48, "Ranged Attack":44, "Gear Haste":4, "Jobs":["thf","rng","bst","cor","dnc","run"]}
Oshosi_Mask = {"Name":"Oshosi Mask +1","STR":37, "DEX":24, "VIT":23, "AGI":44, "INT":19, "MND":19, "CHR":25, "Ranged Accuracy":45, "Magic Accuracy":50, "Double Shot":6, "Triple Shot":5, "Jobs":["cor","rng"]}
heads = [Oshosi_Mask,Meghanada_Visor,Ikenga_Hat,Fili_Calot,Bihu_Roundlet,Brioso_Roundlet,Chasseur_Tricorne,Lanun_Tricorne,Laksamana_Tricorne,Kasuga_Kabuto,Wakido_Kabuto,Sakonji_Kabuto,Boii_Mask,Agoge_Mask,Pedagogy_Mortarboard,Arbatel_Bonnet,Piety_Cap,Bunzi_Hat,Ayanmo_Zucchetto,Vishap_Armet,Pteroslaver_Armet,Peltast_Mezail,Vitiation_Chapeau,Lethargy_Chappel,Jhakri_Coronal,Gleti_Mask,Adhemar_Bonnet_A,Adhemar_Bonnet_B,Blistering_Sallet,Dampening_Tam,Flamma_Zucchetto,Hachiya_Hatsuburi,Hizamaru_Somen,Kendatsuba_Jinpachi,Malignance_Chapeau,Mochizuki_Hatsuburi,Mpaca_Cap,Mummu_Bonnet,Nyame_Helm,Pixie_Hairpin,Ratri_Sallet,Ryuo_Somen_A,Sakpata_Helm,Sulevia_Mask,Hattori_Zukin,Heathen_Burgeonet,Amalric_Coif,Ea_Hat,Agwu_Cap,Wicce_Petasos,Archmage_Petasos,Spaekona_Petasos]

two_handed = ["Great Sword", "Great Katana", "Great Axe", "Polearm", "Scythe", "Staff"]
one_handed = ["Axe", "Club", "Dagger", "Sword", "Katana", "Hand-to-Hand"]
ranged_skills = ["Throwing", "Marksmanship", "Archery"]

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
Sorcerers_Stole = {"Name":"Sorcerer's Stole +2", "Name2":"Sorcerer's Stole +2 R25", "INT":0+15, "MND":0+15, "Magic Burst Damage":10, "Magic Accuracy":30+25, "Magic Attack":7,"Jobs":["blm"]}
Quanpur_Necklace = {"Name":"Quanpur Necklace", "Magic Attack":7, "Earth Elemental Bonus":5,"Jobs":["blm","rdm","sch","geo"]}
Mizukage_no_Kubikazari = {"Name":"Mizukage-no-Kubikazari","INT":4, "MND":4, "Magic Attack":8, "Magic Burst Damage":10,"Jobs":["blm","rdm","sch","geo","whm","brd"]}
Duelist_Torque = {"Name":"Duelist's Torque +2", "Name2":"Duelist's Torque +2 R25", "Magic Accuracy":30, "INT":15, "MND":15,"Jobs":["rdm"]}
Dragoon_Collar = {"Name":"Dragoon's collar +2","Name2":"Dragoon's collar +2 R25","STR":0+15,"VIT":0+15,"PDL":0+10,"Crit Rate":4,"Jobs":["drg"]}
Clerics_Torque = {"Name":"Cleric's Torque +2", "Name2":"Cleric's Torque +2 R25", "INT":15, "MND":15, "Jobs":["whm"]}
Lissome_Necklace = {"Name":"Lissome Necklace", "Accuracy":8, "Store TP":4, "DA":1,"Jobs":["war","mnk","whm","blm","rdm","thf","pld","drk","bst","brd","rng","sam","nin","drg","smn","blu","cor","pup","dnc","sch","geo","run"]}
Marked_Gorget = {"Name":"Marked Gorget","AGI":3,"Ranged Accuracy":15,"Ranged Attack":15,"Store TP":2,"Jobs":["war","mnk","whm","blm","rdm","thf","pld","drk","bst","brd","rng","sam","nin","drg","smn","blu","cor","pup","dnc","sch","geo","run"]}
Argute_Stole = {"Name":"Argute Stole +2","Name2":"Argute Stole +2 R25","Magic Accuracy":30,"Magic Burst Damage":10,"INT":15,"MND":15,"Magic Damage":25,"Jobs":["sch"]}
Warrior_Beads = {"Name": "Warrior's Bead Necklace +2", "Name2":"Warrior's Bead Necklace +2 R25","Accuracy":25,"Attack":25,"Fencer":1,"DA":0+7,"STR":0+15,"DEX":0+15,"Jobs":["war"]}
Iskur_Gorget = {"Name":"Iskur Gorget","Ranged Accuracy":30,"Ranged Attack":30,"Store TP":8,"Jobs":["thf","rng","nin","cor"]}
Commodore_Charm = {"Name":"Commodore Charm +2", "Name2":"Commodore Charm +2 R25", "Ranged Accuracy":25, "Magic Accuracy":4, "STR":15, "AGI":15, "Magic Attack":7,"Magic Damage":25,"Jobs":["cor"]}
Bards_Charm = {"Name":"Bard's Charm +2", "Name2":"Bard's Charm +2 R25", "Accuracy":30, "QA":3, "DEX":25, "CHR":25, "PDL":10,"Store TP":7,"Jobs":["brd"]}
necks = [Bards_Charm,Commodore_Charm,Iskur_Gorget,Marked_Gorget,Warrior_Beads,Argute_Stole,Dragoon_Collar,Duelist_Torque,Abyssal_Beads,Baetyl_Pendant,Caro_Necklace,Fotia_Gorget,Ninja_Nodowa,Rep_Plat_Medal,Samurai_Nodowa,Sanctity_Necklace,Sibyl_Scarf,Warders_Charm,Sorcerers_Stole,Quanpur_Necklace,Mizukage_no_Kubikazari]

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
Regal_Earring = {"Name":"Regal Earring", "INT":10, "MND":10, "CHR":10, "Magic Attack":7,"Jobs":["blm","rdm","sch","geo","whm","brd"]}
Malignance_Earring = {"Name":"Malignance Earring","INT":8,"MND":8,"Magic Accuracy":10,"Magic Attack":8,"Jobs":["blm","rdm","sch","geo","drk","whm"]}
Barkarole_Earring = {"Name":"Barkarole Earring", "INT":3, "Magic Accuracy":8, "Magic Attack":8,"Jobs":["blm","sch","geo"]}
Wicce_Earring = {"Name":"Wicce Earring +2", "Magic Attack":9,"Magic Damage":9,"INT":15,"MND":15,"Magic Accuracy":20,"Jobs":["blm"]}
Sherida_Earring = {"Name":"Sherida Earring", "STR":5, "DEX":5, "DA":5, "Store TP":5, "Jobs":["mnk","rdm","thf","bst","rng","drg","dnc","run"]}
Lethargy_Earring = {"Name":"Lethargy Earring +2", "Accuracy":0+18,"Magic Accuracy":0+18, "DA":0+7, "STR":0+11, "DEX":0+11, "Jobs":["rdm"]}
Peltast_Earring = {"Name":"Peltast's Earring +2", "PDL":9, "Accuracy":18,"Magic Accuracy":18,"Crit Rate":7,"STR":11,"VIT":11,"Jobs":["drg"]}
Ebers_Earring = {"Name":"Ebers Earring +2", "Accuracy":18,"Magic Accuracy":18,"STR":11,"MND":11,"Jobs":["whm"]}
Kasuga_Earring = {"Name":"Kasuga Earring +2","Store TP":9,"Skillchain Bonus":7,"Accuracy":18,"Weaponskill Damage":5,"STR":11,"DEX":11,"Jobs":["sam"]}
Arbatel_Earring = {"Name":"Arbatel Earring +2","Magic Attack":9,"Magic Damage":9,"Magic Accuracy":18,"INT":11,"MND":11,"Jobs":["sch"]}
Enervating_Earring = {"Name":"Enervating Earring","Ranged Accuracy":7,"Ranged Attack":7,"Store TP":4,"Jobs":["war","mnk","whm","blm","rdm","thf","pld","drk","bst","brd","rng","sam","nin","drg","smn","blu","cor","pup","dnc","sch","geo","run"]}
Boii_Earring = {"Name":"Boii Earring +2","DA":9,"Accuracy":18,"Magic Accuracy":18,"STR":11,"VIT":11,"Crit Rate":7,"Jobs":["war"]}
Chasseurs_Earring = {"Name":"Chasseur's Earring +2","Accuracy":18,"Magic Accuracy":18,"STR":11,"AGI":11,"Crit Rate":7,"Jobs":["cor"]}
Fili_Earring = {"Name":"Fili Earring +2","Accuracy":18,"MND":11,"CHR":11,"Jobs":["brd"]}
ears = [Fili_Earring,Chasseurs_Earring,Enervating_Earring,Boii_Earring,Arbatel_Earring,Kasuga_Earring,Ebers_Earring,Peltast_Earring,Lethargy_Earring,Sherida_Earring,Balder_Earring,Brutal_Earring,Cessance_Earring,Crematio_Earring,Crepuscular_Earring,Dedition_Earring,Dignitary_Earring,Eabani_Earring,Friomisi_Earring,Ishvara_Earring,Lugra_Earring_Aug,Mache_Earring1,Mache_Earring2,Moonshade_Earring,Odr_Earring,Schere_Earring,Static_Earring,Suppanomimi,Telos_Earring,Thrud_Earring,Hattori_Earring,Heathen_Earring,Regal_Earring,Malignance_Earring,Barkarole_Earring,Wicce_Earring]
ears2 = [Fili_Earring,Chasseurs_Earring,Enervating_Earring,Boii_Earring,Arbatel_Earring,Kasuga_Earring,Ebers_Earring,Peltast_Earring,Lethargy_Earring,Sherida_Earring,Balder_Earring,Brutal_Earring,Cessance_Earring,Crematio_Earring,Crepuscular_Earring,Dedition_Earring,Dignitary_Earring,Eabani_Earring,Friomisi_Earring,Ishvara_Earring,Lugra_Earring_Aug,Mache_Earring1,Mache_Earring2,Moonshade_Earring,Odr_Earring,Schere_Earring,Static_Earring,Suppanomimi,Telos_Earring,Thrud_Earring,Hattori_Earring,Heathen_Earring,Regal_Earring,Malignance_Earring,Barkarole_Earring,Wicce_Earring]
# Note that JSE+2 earrings are available in both slots.
# This is because if the 2nd best earring is coincidentally placed in the right_ear, the JSE+2 earring might not be enough to replace it, even if it is significantly better than the third best option.
# This results in a set that SHOULD have JSE+2 earring in it, but does not. Just remember that the output should place JSE+2 in the right ear. I'll find a way to force it later. TODO

Abnoba_Kaftan = {"Name": "Abnoba Kaftan", "STR":25, "DEX":38, "VIT":24, "AGI":28, "INT":21, "MND":21, "CHR":21, "Accuracy":22, "Attack":22, "Gear Haste":4, "Crit Rate":5, "Crit Damage":5,"Jobs":["nin","mnk","thf","rng","blu","cor","pup","dnc","run"]}
Adhemar_Jacket_A = {"Name": "Adhemar Jacket +1", "Name2": "Adhemar Jacket +1 A", "STR":26, "DEX":33+12, "VIT":23, "AGI":29+12, "INT":20, "MND":20, "CHR":20, "Accuracy":35+20, "Attack":35, "Ranged Accuracy":35, "Ranged Attack":35, "Gear Haste":4, "TA":4, "Dual Wield":6,"Jobs":["mnk","thf","rng","nin","blu","cor","dnc","run"]}
Adhemar_Jacket_B = {"Name": "Adhemar Jacket +1", "Name2": "Adhemar Jacket +1 B", "STR":26+12, "DEX":33+12, "VIT":23, "AGI":29, "INT":20, "MND":20, "CHR":20, "Accuracy":35, "Attack":35+20, "Ranged Accuracy":35, "Ranged Attack":35, "Gear Haste":4, "TA":4, "Dual Wield":6,"Jobs":["mnk","thf","rng","nin","blu","cor","dnc","run"]}
Agony_Jerkin = {"Name": "Agony Jerkin +1", "Name2": "Agony Jerkin +1 R15", "STR":24+10, "DEX":35+10, "VIT":24+10, "AGI":28+10, "INT":23+10, "MND":23+10, "CHR":23+10, "Attack":23+60, "Gear Haste":4, "Accuracy":14, "Store TP":0+10,"Jobs":["nin","war","rdm","thf","pld","drk","bst","brd","rng","sam","drg","blu","cor","dnc","run"]}
Ashera_Harness = {"Name": "Ashera Harness", "STR":30, "DEX":40, "VIT":30, "AGI":30, "INT":30, "MND":30, "CHR":40, "Accuracy":45, "Attack":45, "Gear Haste":4, "Store TP":10,"Jobs":["nin","mnk","thf","brd","dnc","run"]}
Dagon_Breastplate = {"Name": "Dagon Breastplate", "STR":40,"DEX":30,"VIT":40,"AGI":30,"INT":30,"MND":30,"CHR":30,"Accuracy":45,"Attack":45,"Gear Haste":1,"Crit Rate":4, "TA":5,"Jobs":["drk","sam","pld","war","drg"]}
Flamma_Korazin = {"Name": "Flamma Korazin +2", "STR":43,"DEX":39,"VIT":32,"AGI":20,"INT":20,"MND":20,"CHR":20,"Accuracy":46,"Magic Accuracy":46,"Gear Haste":2,"Store TP":9,"Jobs":["drk","sam","war","pld","drg"]}
Gyve_Doublet = {"Name": "Gyve Doublet", "STR":19, "DEX":19, "VIT":19, "AGI":19, "INT":39, "MND":33, "CHR":33, "Magic Attack":42, "Gear Haste":3,"Jobs":["whm","brd","smn","blu","pup","nin","drk","blm","rdm","sch","geo","rng"]}
Hachiya_Chainmail = {"Name": "Hachiya Chainmail +3", "STR":39, "DEX":35, "VIT":36, "AGI":35, "INT":34, "MND":34, "CHR":34, "Accuracy":50, "Gear Haste":4,"Dual Wield":10,"Crit Rate":8,"Jobs":["nin"]}
Herculean_Vest = {"Name": "Herculean Vest", "STR":28, "DEX":34, "VIT":24, "AGI":30, "INT":21, "MND":20, "CHR":21, "Accuracy":15, "Ranged Accuracy":15, "Gear Haste":4, "Store TP":3, "Crit Rate":3,"Jobs":["nin","mnk","thf","rng","blu","cor","pup","dnc","run"]}
Hizamaru_Haramaki = {"Name": "Hizamaru Haramaki +2", "STR":40, "DEX":36, "VIT":34, "AGI":28, "INT":20, "MND":17, "CHR":28, "Accuracy":46, "Attack":28, "Gear Haste":4,"Jobs":["nin","sam","mnk","pup"]}
Ignominy_Cuirass = {"Name": "Ignominy Cuirass +3", "STR":46,"DEX":29,"VIT":39,"AGI":29,"INT":29,"MND":29,"CHR":29,"Accuracy":50,"Attack":48,"Gear Haste":3,"Weaponskill Damage":10,"Jobs":["drk"]}
Kendatsuba_Samue = {"Name": "Kendatsuba Samue +1", "STR":33, "DEX":39, "VIT":21, "AGI":37, "INT":24, "MND":23, "CHR":21, "Accuracy": 52, "Ranged Accuracy": 47, "Gear Haste": 4, "TA": 6, "Crit Rate": 9,"Jobs":["nin","sam","mnk"]}
Malignance_Tabard = {"Name": "Malignance Tabard", "STR":19, "DEX":49, "VIT":25, "AGI":42, "INT":19, "MND":24, "CHR":24, "Accuracy":50, "Ranged Accuracy":50, "Magic Accuracy":50, "Gear Haste":4, "Store TP":11, "PDL":6,"Jobs":["mnk", "rdm", "thf", "bst", "rng", "nin", "blu", "cor", "pup", "dnc"]}
Mochizuki_Chainmail = {"Name": "Mochizuki Chainmail +3", "STR":34, "DEX":35, "VIT":31, "AGI":35, "INT":34, "MND":34, "CHR":34, "Accuracy":51, "Attack":87, "Ranged Accuracy":47, "Ranged Attack":79, "Magic Accuracy":40,"Gear Haste":4,"Dual Wield":9,"Daken":10,"Jobs":["nin"]}
Mpaca_Doublet = {"Name": "Mpaca's Doublet", "Name2": "Mpaca's Doublet R25", "STR":39, "DEX":37, "VIT":34, "AGI":28, "INT":28, "MND":25, "CHR":28,"Accuracy":40+10,"Attack":40+25,"Magic Accuracy":40+10,"Gear Haste":4,"TA":4,"Crit Rate":7, "Store TP":0+7,"Jobs":["nin","sam","mnk","pup"]}
Mummu_Jacket = {"Name": "Mummu Jacket +2", "STR":25, "DEX":48, "VIT":24, "AGI":44, "INT":21, "MND":20, "CHR":24, "Accuracy":46, "Ranged Accuracy":46, "Magic Accuracy":46, "Gear Haste":4, "Store TP":6, "Crit Rate": 6,"Jobs":["nin","mnk","thf","rng","cor","dnc"]}
Nyame_Mail = {"Name": "Nyame Mail", "Name2": "Nyame Mail R25 B", "STR":35, "DEX":24, "VIT":35, "AGI":33, "INT":42, "MND":37, "CHR":35, "Accuracy":40, "Attack":30+30, "Gear Haste":3, "Weaponskill Damage":0+12, "Magic Accuracy":40, "Magic Attack":30, "Ranged Accuracy":40, "Ranged Attack":30+30,"DA":0+5,"Magic Burst Damage":7,"Jobs":all_jobs}
Ratri_Breastplate = {"Name": "Ratri Breastplate +1", "STR":48, "DEX":34, "VIT":30, "AGI":21, "INT":25, "MND":25, "CHR":24, "Magic Accuracy":47, "Scythe Skill":56, "Gear Haste":3, "Weaponskill Damage":10,"Jobs":["drk"]}
Ryuo_Domaru_A = {"Name": "Ryuo Domaru +1", "Name2": "Ryuo Domaru +1 A", "STR":28+12, "DEX":24+12, "VIT":23, "AGI":29, "INT":19, "MND":19, "CHR":19,"Accuracy":37+20,"Attack":37,"Gear Haste":3,"Crit Rate":5,"Jobs":["nin","sam","mnk","pup"]}
Sakonji_Domaru = {"Name":"Sakonji Domaru +3", "STR":42, "DEX":37, "VIT":36, "AGI":31, "INT":31, "MND":31, "CHR":31, "Accuracy":47, "Attack":80, "Magic Accuracy":40, "Gear Haste":3, "Store TP":10, "Weaponskill Damage":10,"Jobs":["sam"]}
Sakpata_Breastplate = {"Name": "Sakpata's Breastplate", "Name2": "Sakpata's Breastplate R25", "STR":42,"DEX":25,"VIT":42,"AGI":25,"INT":24,"MND":28,"CHR":26,"Accuracy":40+10,"Magic Accuracy":40+10,"Attack":40+25,"Gear Haste":2,"DA":8,"PDL":8,"Jobs":["drk","war","pld"]}
Samnuha_Coat = {"Name": "Samnuha Coat", "STR":26, "DEX":33, "VIT":23, "AGI":29, "INT":20, "MND":20, "CHR":20, "Accuracy":23, "Magic Accuracy":23+15, "Magic Attack":20+15, "Gear Haste":4, "Dual Wield":5, "Magic Burst Damage II": 8,"Jobs":["nin","mnk","thf","rng","blu","cor","pup","dnc","run"]}
Sulevia_Platemail = {"Name": "Sulevia's Platemail +2", "STR":41,"DEX":24,"VIT":41,"AGI":16,"INT":16,"MND":27,"CHR":27,"Accuracy":46,"Attack":50,"Gear Haste":1,"Jobs":["drk","war","pld","drg"]}
Tatenashi_Haramaki = {"Name": "Tatenashi Haramaki +1", "Name2": "Tatenashi Haramaki +1 R15", "STR":28+10, "DEX":24+10, "VIT":28+10, "AGI":19+10, "INT":19+10, "MND":19+10, "CHR":19+10,"Accuracy":35+30,"Attack":35,"Gear Haste":3,"Crit Rate":6,"Store TP":8,"TA":0+5,"Jobs":["nin","sam","mnk","war","rng"]}
Hattori_Ningi = {"Name": "Hattori Ningi +3", "STR":40,"DEX":47,"VIT":35,"AGI":43,"INT":36,"MND":31,"CHR":31,"Accuracy":64,"Attack":74,"Ranged Accuracy":64,"Magic Accuracy":64,"Gear Haste":4,"Crit Rate":8,"Jobs":["nin"]}
Heathen_Cuirass = {"Name": "Heathen's Cuirass +3", "STR":47,"DEX":31,"VIT":43,"AGI":33,"INT":35,"MND":35,"CHR":35,"Accuracy":64,"Attack":74,"Magic Accuracy":64,"Gear Haste":4,"Crit Rate":7,"Jobs":["drk"]}
Amalric_Doublet = {"Name":"Amalric Doublet +1", "Name2":"Amalric Doublet +1A","STR":16,"DEX":19,"VIT":16,"AGI":16,"INT":38,"MND":30,"CHR":28,"Magic Accuracy":33+20,"Magic Attack":33+20,"Magic Burst Damage":0,"Magic Burst Damage II":0,"Magic Damage":0,"Gear Haste":3,"Jobs":["blm","sch","rdm","geo","blu"]}
Ea_Houppelande = {"Name":"Ea Houppelande +1", "STR":23,"DEX":24,"VIT":26,"AGI":26,"INT":48,"MND":37,"CHR":34,"Magic Accuracy":52,"Magic Attack":44,"Magic Burst Damage":9, "Magic Burst Damage II":9,"Gear Haste":3,"Jobs":["blm", "rdm", "geo"]}
Agwu_Robe = {"Name":"Agwu's Robe", "Name2": "Agwu's Robe R25", "STR":33,"DEX":30,"VIT":19,"AGI":20,"INT":47,"MND":37,"CHR":35, "Accuracy":40+10, "Magic Accuracy":40+10,"Magic Attack":35+23,"Magic Burst Damage":10,"Magic Burst Damage II":0,"Magic Damage":20,"Gear Haste":3,"Jobs":["blm", "sch", "geo", "run"]}
Wicce_Coat = {"Name":"Wicce Coat +3", "STR":29,"DEX":34,"VIT":34,"AGI":34,"INT":50,"MND":43,"CHR":43, "Accuracy":64,"Magic Accuracy":64,"Magic Attack":59,"Magic Burst Damage":0,"Magic Burst Damage II":5,"Magic Damage":34,"Gear Haste":3,"Jobs":["blm"]}
Archmage_Coat = {"Name":"Archmage's Coat +3", "STR":31,"DEX":31,"VIT":31,"AGI":31,"INT":46,"MND":39,"CHR":39, "Magic Accuracy":40,"Magic Attack":52, "Elemental Magic Skill":24, "Accuracy":40,"Gear Haste":3,"Jobs":["blm"]}
Spaekona_Coat = {"Name":"Spaekona Coat +3", "STR":31,"DEX":31,"VIT":31,"AGI":31,"INT":39,"MND":39,"CHR":39,"Magic Accuracy":55,"Magic Damage":48,"Magic Attack":0,"Gear Haste":3,"Jobs":["blm"]}
Gleti_Cuirass = {"Name":"Gleti's Cuirass", "Name2":"Gleti's Cuirass R25","STR":39,"DEX":34,"VIT":39,"AGI":26,"INT":26,"MND":26,"CHR":26,"Accuracy":40+10,"Attack":40+25,"Magic Accuracy":40+10,"Gear Haste":3,"PDL":9,"Crit Rate":8,"DA":9,"Jobs":["thf","bst","drg","blu","dnc"]}
Jhakri_Robe = {"Name":"Jhakri Robe +2","STR":37,"DEX":33,"VIT":14,"AGI":16,"INT":50,"MND":32,"CHR":30,"Accuracy":46,"Attack":46,"Magic Accuracy":46,"Magic Attack":43,"Gear Haste":4,"Jobs":["blm","rdm","blu","sch","geo"]}
Vitiation_Tabard = {"Name":"Vitiation Tabard +3","STR":31,"DEX":31,"VIT":31,"AGI":31,"INT":39,"MND":45,"CHR":39,"Accuracy":40,"Attack":65,"Magic Accuracy":40,"Gear Haste":3,"Jobs":["rdm"]}
Lethargy_Sayon = {"Name":"Lethargy Sayon +3","STR":34,"DEX":34,"VIT":30,"AGI":30,"INT":47,"MND":45,"CHR":35,"Accuracy":64,"Attack":64,"Magic Accuracy":64,"Magic Attack":54,"Magic Damage":34,"Gear Haste":3,"Jobs":["rdm"]}
Vishap_Mail = {"Name":"Vishap Mail +3","STR":41,"DEX":31,"VIT":41,"AGI":31,"INT":31,"MND":31,"CHR":31,"Accuracy":57,"Attack":35,"Gear Haste":3,"Store TP":8,"Jobs":["drg"]}
Pteroslaver_Mail = {"Name":"Pteroslaver Mail +3","STR":44,"DEX":39,"VIT":36,"AGI":31,"INT":31,"MND":31,"CHR":31,"Accuracy":40,"Attack":80,"Magic Accuracy":40,"Gear Haste":3,"Jobs":["drg"]}
Peltast_Plackart = {"Name":"Peltast's Plackart +3","STR":43,"DEX":39,"VIT":43,"AGI":34,"INT":34,"MND":34,"CHR":34,"Accuracy":64,"Attack":74,"Magic Accuracy":64,"Gear Haste":3,"Store TP":14,"PDL":10,"Jobs":["drg"]}
Ayanmo_Corazza = {"Name":"Ayanmo Corazza +2","STR":28,"DEX":48,"VIT":24,"AGI":33,"INT":21,"MND":31,"CHR":21,"Accuracy":46,"Magic Accuracy":46,"Gear Haste":4, "DA":7,"Jobs":["whm","rdm","brd","blu","run"]}
Bunzi_Robe = {"Name":"Bunzi's Robe", "Name2":"Bunzi's Robe R25","STR":23, "DEX":25, "VIT":23, "AGI":21, "INT":48, "MND":43, "CHR":42, "Accuracy":40+10, "Attack":40+25, "Magic Accuracy":40+10, "Magic Attack":30, "Magic Damage":30+25, "Gear Haste":3, "Magic Burst Damage":10, "PDL":0+7, "Jobs":["whm","rdm", "brd", "smn"]}
Piety_Bliaut = {"Name":"Piety Bliaut +3", "Name2":"Piety Bliaut +3 R25","STR":31, "DEX":31, "VIT":31, "AGI":31, "INT":39, "MND":39, "CHR":39, "Accuracy":40, "Attack":65, "Gear Haste":3, "Jobs":["whm"]}
Arbatel_Gown = {"Name":"Arbatel Gown +3","STR":29, "DEX":34, "VIT":34, "AGI":34, "INT":50, "MND":43, "CHR":43, "Accuracy":64, "Magic Accuracy":64, "Magic Attack":59, "Magic Damage":34, "Gear Haste":3, "Jobs":["sch"]}
Pummeler_Lorica = {"Name":"Pummeler's Lorica +3","STR":40, "DEX":34, "VIT":40, "AGI":33, "INT":33, "MND":33, "CHR":33, "Accuracy":50, "Attack":32, "Gear Haste":4, "Weaponskill Damage":10,"Jobs":["war"]}
Agoge_Lorica = {"Name":"Agoge Lorica +3","STR":36, "DEX":35, "VIT":36, "AGI":30, "INT":30, "MND":30, "CHR":30, "Accuracy":50, "Attack":85, "Magic Accuracy":40, "Gear Haste":4, "DA":7, "Jobs":["war"]}
Boii_Lorica = {"Name":"Boii Lorica +3","STR":43, "DEX":39, "VIT":43, "AGI":34, "INT":34, "MND":34, "CHR":34, "Accuracy":64, "Attack":74, "Magic Accuracy":64, "Great Axe Skill":21, "Gear Haste":3, "Store TP":11, "Jobs":["war"]}
Wakido_Domaru = {"Name":"Wakido Domaru +3","STR":41, "DEX":31, "VIT":41, "AGI":31, "INT":31, "MND":31, "CHR":31, "Accuracy":57, "Gear Haste":3, "Jobs":["sam"]}
Kasuga_Domaru = {"Name":"Kasuga Domaru +3","STR":43, "DEX":39, "VIT":43, "AGI":34, "INT":34, "MND":34, "CHR":34, "Accuracy":64, "Attack":74, "Magic Accuracy":64, "Great Katana Skill":21, "Gear Haste":3, "Store TP":14, "Zanshin":16, "Jobs":["sam"]}
Lanun_Frac = {"Name":"Lanun Frac +3","STR":37, "DEX":39, "VIT":31, "AGI":43, "INT":36, "MND":33, "CHR":33, "Accuracy":49, "Ranged Attack":83, "Magic Accuracy":40, "Magic Attack":61,"Gear Haste":4, "Jobs":["cor"]}
Laksamana_Frac = {"Name":"Laksamana's Frac +3","STR":39, "DEX":39, "VIT":31, "AGI":45, "INT":33, "MND":33, "CHR":33, "Ranged Accuracy":57, "Ranged Attack":35, "Gear Haste":4, "Weaponskill Damage":10, "Jobs":["cor"]}
Chasseur_Frac = {"Name":"Chasseur's Frac +3","STR":40, "DEX":43, "VIT":33, "AGI":49, "INT":34, "MND":34, "CHR":29, "Accuracy":64, "Ranged Accuracy":64, "Ranged Attack":74, "Magic Accuracy":64, "Gear Haste":4, "Triple Shot":14, "Jobs":["cor"]}
Brioso_Justaucorps = {"Name":"Brioso Justaucorps +3","STR":29, "DEX":31, "VIT":29, "AGI":31, "INT":39, "MND":38, "CHR":43, "Magic Accuracy":64, "Gear Haste":3, "Jobs":["brd"]}
Bihu_Justaucorps = {"Name":"Bihu Justaucorps +3","STR":39, "DEX":41, "VIT":39, "AGI":41, "INT":39, "MND":38, "CHR":43, "Accuracy":53, "Attack":92, "Magic Accuracy":54, "Gear Haste":3, "Weaponskill Damage":10, "Jobs":["brd"]}
Fili_Hongreline = {"Name":"Fili Hongreline +3","STR":29, "DEX":38, "VIT":31, "AGI":33, "INT":39, "MND":43, "CHR":48, "Accuracy":64, "Magic Accuracy":64, "Gear Haste":3, "Jobs":["brd"]}
Meghanada_Cuirie = {"Name":"Meghanada Cuirie +2","STR":34, "DEX":45, "VIT":23, "AGI":41, "INT":19, "MND":28, "CHR":29, "Accuracy":50, "Attack":46, "Ranged Accuracy":50, "Ranged Attack":46, "Gear Haste":2, "Crit Damage":6, "Jobs":["thf","rng","bst","cor","dnc","run"]}
Oshosi_Vest = {"Name":"Oshosi Vest +1","STR":38, "DEX":30, "VIT":26, "AGI":49, "INT":21, "MND":21, "CHR":26, "Ranged Accuracy":47, "Magic Accuracy":52, "Store TP":10, "Double Shot":8, "Triple Shot":7, "Jobs":["cor","rng"]}
Ikenga_Vest = {"Name":"Ikenga's Vest","Name2":"Ikenga's Vest R25","STR":33, "DEX":43, "VIT":28, "AGI":39, "INT":24, "MND":25, "CHR":26, "Ranged Accuracy":40+10, "Ranged Attack":40+25, "Magic Accuracy":40+10, "Store TP":11, "PDL":7, "TP Bonus":0+190, "Jobs":["cor","rng"]}
bodies = [Oshosi_Vest,Meghanada_Cuirie,Ikenga_Vest,Fili_Hongreline,Bihu_Justaucorps,Brioso_Justaucorps,Chasseur_Frac,Laksamana_Frac,Lanun_Frac,Kasuga_Domaru,Wakido_Domaru,Boii_Lorica,Agoge_Lorica, Pummeler_Lorica, Arbatel_Gown,Piety_Bliaut,Bunzi_Robe,Ayanmo_Corazza,Peltast_Plackart,Pteroslaver_Mail,Vishap_Mail,Lethargy_Sayon,Vitiation_Tabard,Jhakri_Robe,Gleti_Cuirass,Abnoba_Kaftan,Adhemar_Jacket_A,Adhemar_Jacket_B,Agony_Jerkin,Ashera_Harness,Dagon_Breastplate,Flamma_Korazin,Gyve_Doublet,Hachiya_Chainmail,Herculean_Vest,Hizamaru_Haramaki,Ignominy_Cuirass,Kendatsuba_Samue,Malignance_Tabard,Mochizuki_Chainmail,Mpaca_Doublet,Mummu_Jacket,Nyame_Mail,Ratri_Breastplate,Ryuo_Domaru_A,Sakonji_Domaru,Sakpata_Breastplate,Samnuha_Coat,Sulevia_Platemail,Tatenashi_Haramaki,Hattori_Ningi,Heathen_Cuirass,Amalric_Doublet,Ea_Houppelande,Agwu_Robe,Wicce_Coat,Archmage_Coat,Spaekona_Coat,]

Adhemar_Wristbands_A = {"Name": "Adhemar Wristbands +1", "Name2": "Adhemar Wristbands +1 A", "STR":15, "DEX":44+12, "VIT":29, "AGI":7+12, "INT":12, "MND":30, "CHR":17, "Accuracy":32+20, "Ranged Accuracy":32, "TA":4, "Store TP":7, "Gear Haste":5, "Jobs":["mnk","thf","rng","nin","blu","cor","dnc","run"]}
Adhemar_Wristbands_B = {"Name": "Adhemar Wristbands +1", "Name2": "Adhemar Wristbands +1 B", "STR":15+12, "DEX":44+12, "VIT":29, "AGI":7, "INT":12, "MND":30, "CHR":17, "Accuracy":32, "Ranged Accuracy":32, "TA":4, "Store TP":7, "Attack":0+20, "Gear Haste":5, "Jobs":["mnk","thf","rng","nin","blu","cor","dnc","run"]}
Flamma_Manopolas = {"Name": "Flamma Manopolas +2", "STR":23,"DEX":46,"VIT":35,"AGI":8,"INT":7,"MND":24,"CHR":17,"Accuracy":43,"Magic Accuracy":43,"Gear Haste":4,"Store TP":6,"Crit Rate":8,"Jobs":["drk","sam","war","pld","drg"]}
Floral_Gauntlets = {"Name": "Floral Gauntlets", "STR":16, "DEX":35,"VIT":29,"AGI":12,"INT":12,"MND":30,"CHR":17,"Accuracy":21+15,"Ranged Accuracy":21+15,"Gear Haste":5,"Dual Wield":5,"TA":3, "Jobs":["nin","thf","rng","cor"]}
Hachiya_Tekko = {"Name": "Hachiya Tekko +3", "STR":20, "DEX":44, "VIT":38, "AGI":26, "INT":20, "MND":38, "CHR":26, "Accuracy":48, "Ranged Accuracy":48, "Ranged Attack":48, "Throwing Skill":14, "Gear Haste":5,"Daken":10, "Jobs":["nin"]}
Herculean_Gloves = {"Name": "Herculean Gloves", "STR":16, "DEX":39, "VIT":30, "AGI":8, "INT":14, "MND":26, "CHR":19, "Accuracy":12, "Ranged Accuracy":12, "Gear Haste":5,"TA":2, "Jobs":["nin","mnk","thf","rng","blu","cor","pup","dnc","run"]}
Hizamaru_Kote = {"Name": "Hizamaru Kote +2", "STR":20, "DEX":43, "VIT":38, "AGI":16, "INT":7, "MND":21, "CHR":25, "Accuracy":43, "Attack":23, "Gear Haste":4, "Jobs":["nin","sam","mnk","pup"]}
Kendatsuba_Tekko = {"Name": "Kendatsuba Tekko +1", "STR":14, "DEX":62, "VIT":37, "AGI":5, "INT":14, "MND":28, "CHR":21, "Accuracy":49, "Ranged Accuracy":44, "Gear Haste":4,"TA":4, "Crit Rate":5, "Jobs":["nin","sam","mnk"]}
Malignance_Gloves = {"Name": "Malignance Gloves", "STR":25, "DEX":56, "VIT":32, "AGI":24, "INT":11, "MND":42, "CHR":21, "Accuracy":50, "Ranged Accuracy":50, "Magic Accuracy":50, "Gear Haste":4,"Store TP":12,"PDL":4, "Jobs":["mnk", "rdm", "thf", "bst", "rng", "nin", "blu", "cor", "pup", "dnc"]}
Mochizuki_Tekko = {"Name": "Mochizuki Tekko +3", "STR":30, "DEX":44,"VIT":37,"AGI":16,"INT":20,"MND":38,"CHR":26,"Accuracy":38,"Attack":79,"Magic Accuracy":38,"Gear Haste":5, "Jobs":["nin"]}
Mpaca_Gloves = {"Name": "Mpaca's Gloves", "Name2": "Mpaca's Gloves R25", "STR":20, "DEX":44,"VIT":38,"AGI":16,"INT":15,"MND":29,"CHR":25,"Accuracy":40+10,"Attack":40+25,"Magic Accuracy":40+10,"Gear Haste":4,"TA":3,"Crit Rate":5, "TA DMG":0+9, "Jobs":["nin","sam","mnk","pup"]}
Mummu_Wrists = {"Name": "Mummu Wrists +2", "STR":16, "DEX":53,"VIT":30,"AGI":22,"INT":14,"MND":26,"CHR":21,"Accuracy":43,"Ranged Accuracy":43,"Magic Accuracy":43,"Gear Haste":5,"DA":6,"Crit Rate":6, "Jobs":["nin","mnk","thf","rng","cor","dnc"]}
Nyame_Gauntlets = {"Name": "Nyame Gauntlets", "Name2": "Nyame Gauntlets R25 B", "STR":17, "DEX":42, "VIT":39, "AGI":12, "INT":28, "MND":40, "CHR":24, "Accuracy":40, "Attack":30+30, "Gear Haste":3, "Weaponskill Damage":0+10, "Magic Accuracy":40, "Magic Attack":30, "Ranged Accuracy":40, "Ranged Attack":30+30,"DA":0+4,"Magic Burst Damage":5, "Jobs":all_jobs}
Ratri_Gadlings = {"Name": "Ratri Gadlings +1", "STR":28, "DEX":48, "VIT":34, "AGI":0, "INT":14, "MND":32, "CHR":24, "Magic Accuracy":44, "Scythe Skill":53, "Gear Haste":4, "Weaponskill Damage":8,"Jobs":["drk"]}
Ryuo_Tekko_A = {"Name": "Ryuo Tekko +1", "Name2": "Ryuo Tekko +1 A", "STR":12+12, "DEX":38+12, "VIT":30, "AGI":13, "INT":12, "MND":30, "CHR":17,"Accuracy":33+20,"Ranged Accuracy":33,"Gear Haste":4,"Crit Rate":5,"Crit Damage":5, "Jobs":["nin","sam","mnk","pup"]}
Ryuo_Tekko_D = {"Name": "Ryuo Tekko +1", "Name2": "Ryuo Tekko +1 D", "STR":12, "DEX":38+12, "VIT":30, "AGI":13, "INT":12, "MND":30, "CHR":17,"Accuracy":33+25,"Ranged Accuracy":33,"Gear Haste":4,"Crit Rate":5,"Crit Damage":5, "DA":0+4, "Jobs":["nin","sam","mnk","pup"]}
Sakpata_Gauntlets = {"Name": "Sakpata's Gauntlets", "Name2": "Sakpata's Gauntlets R25", "STR":24,"DEX":35,"VIT":46,"AGI":0,"INT":14,"MND":33,"CHR":26,"Accuracy":40+10,"Magic Accuracy":40+10,"Attack":40+25,"Gear Haste":4,"DA":6,"PDL":6,"Store TP":0+7,"Jobs":["drk","war","pld"]}
Sulevia_Gauntlets = {"Name": "Sulevia's Gauntlets +2", "STR":23,"DEX":34,"VIT":45,"AGI":0,"INT":6,"MND":32,"CHR":27,"Accuracy":43,"Attack":47,"Gear Haste":3,"DA":6,"Jobs":["drk","war","pld","drg"]}
Tatenashi_Gote = {"Name": "Tatenashi Gote +1", "Name2": "Tatenashi Gote +1 R15", "STR":8+10, "DEX":40+10, "VIT":32+10, "AGI":7+10, "INT":6+10, "MND":23+10, "CHR":16+10,"Accuracy":21+40,"Gear Haste":4,"Store TP":7,"TA":0+4, "Jobs":["nin","sam","mnk","war","rng"]}
Hattori_Tekko = {"Name": "Hattori Tekko +3", "STR":27,"DEX":55,"VIT":40,"AGI":24,"INT":27,"MND":40,"CHR":27,"Gear Haste":5,"Accuracy":62,"Attack":62,"Ranged Accuracy":62,"Magic Accuracy":62,"Ninjutsu Magic Attack":18,"Magic Burst Damage":15,"Jobs":["nin"]}
Heathen_Gauntlets = {"Name": "Heathen's Gauntlets +3", "STR":27,"DEX":43,"VIT":47,"AGI":0,"INT":25,"MND":40,"CHR":35,"Gear Haste":6,"Accuracy":62,"Attack":72,"Magic Accuracy":62,"Great Sword Skill":28, "Jobs":["drk"]}
Amalric_Gages = {"Name":"Amalric Gages +1", "Name2":"Amalric Gages +1A",  "STR":3,"DEX":23,"VIT":20,"AGI":2,"INT":24,"MND":34,"CHR":19,"Magic Accuracy":0+20,"Magic Attack":33+20,"Magic Burst Damage":0,"Magic Burst Damage II":6,"Magic Damage":0,"Gear Haste":3,"Jobs":["blm","sch","rdm","geo","blu"]}
Ea_Cuffs = {"Name":"Ea Cuffs +1","STR":7,"DEX":29,"VIT":30,"AGI":0,"INT":40,"MND":40,"CHR":23,"Magic Accuracy":49,"Magic Attack":35,"Magic Burst Damage":6, "Magic Burst Damage II":6,"Gear Haste":3,"Jobs":["blm", "rdm", "geo"]}
Agwu_Gages = {"Name":"Agwu's Gages", "Name2": "Agwu's Gages R25", "STR":14,"DEX":38,"VIT":23,"AGI":6,"INT":33,"MND":40,"CHR":25, "Accuracy":40+10, "Magic Accuracy":40+10,"Magic Attack":35+23,"Magic Burst Damage":8,"Magic Burst Damage II":0+5,"Magic Damage":20,"Gear Haste":3,"Jobs":["blm", "sch", "geo", "run"]}
Wicce_Gloves = {"Name":"Wicce Gloves +3", "STR":16,"DEX":40,"VIT":38,"AGI":20,"INT":38,"MND":47,"CHR":32, "Accuracy":62,"Magic Accuracy":62,"Magic Attack":57,"Magic Burst Damage":0,"Magic Burst Damage II":0,"Magic Damage":32,"Gear Haste":3,"Jobs":["blm"]}
Archmage_Gloves = {"Name":"Archmage's Gloves +3", "STR":16,"DEX":38,"VIT":35,"AGI":15,"INT":36,"MND":43,"CHR":29, "Magic Accuracy":38,"Magic Attack":50, "Elemental Magic Skill":23, "Accuracy":38,"Jobs":["blm"]}
Spaekona_Gloves = {"Name":"Spaekona Gloves +3", "STR":16,"DEX":38,"VIT":35,"AGI":15,"INT":37,"MND":43,"CHR":29,"Magic Accuracy":52,"Magic Damage":44,"Magic Attack":0,"Gear Haste":3,"Elemental Magic Skill":21,"Magic Burst Damage II":8,"Gear Haste":3,"Jobs":["blm"]}
Gleti_Gauntlets = {"Name":"Gleti's Gauntlets", "Name2":"Gleti's Gauntlets R25","STR":20,"DEX":42,"VIT":43,"AGI":15,"INT":14,"MND":30,"CHR":24,"Accuracy":40+10,"Attack":40+25,"Magic Accuracy":40+10,"Gear Haste":3,"PDL":7,"Crit Rate":6,"Store TP":7,"Jobs":["thf","bst","drg","blu","dnc"]}
Jhakri_Cuffs = {"Name":"Jhakri Cuffs +2", "STR":18,"DEX":41,"VIT":17,"AGI":2,"INT":36,"MND":35,"CHR":20,"Accuracy":43,"Attack":43,"Magic Accuracy":43,"Magic Attack":40,"Gear Haste":0,"Weaponskill Damage":7,"Jobs":["blm","rdm","blu","sch","geo"]}
Atrophy_Gloves = {"Name":"Atrophy Gloves +3","STR":21,"DEX":43,"VIT":35,"AGI":15,"INT":29,"MND":43,"CHR":29,"Accuracy":53,"Attack":30,"Gear Haste":3,"Weaponskill Damage":6,"Jobs":["rdm"]}
Vitiation_Gloves = {"Name":"Vitiation Gloves +3","STR":16,"DEX":38,"VIT":35,"AGI":15,"INT":32,"MND":46,"CHR":29,"Accuracy":38,"Attack":63,"Magic Accuracy":38,"Gear Haste":3, "Jobs":["rdm"]}
Lethargy_Gantherots = {"Name":"Lethargy Gantherots +3","STR":16,"DEX":43,"VIT":39,"AGI":15,"INT":33,"MND":50,"CHR":29,"Accuracy":62,"Attack":62,"Magic Accuracy":62,"Magic Attack":52,"Magic Damage":32,"Gear Haste":3,"Jobs":["rdm"]}
Vishap_Finger_Gauntlets = {"Name":"Vishap Finger Gauntlets +3","STR":16,"DEX":40,"VIT":40,"AGI":17,"INT":20,"MND":37,"CHR":30,"Accuracy":48,"Attack":35,"Gear Haste":4,"Jobs":["drg"]}
Pteroslaver_Finger_Gauntlets = {"Name":"Pteroslaver Finger Gauntlets +3","STR":16,"DEX":43,"VIT":40,"AGI":20,"INT":20,"MND":36,"CHR":30,"Accuracy":46,"Attack":63,"Magic Accuracy":38,"Gear Haste":4,"Weaponskill Damage":10,"Jobs":["drg"]}
Peltast_Vambraces = {"Name":"Peltast's Vambraces +3","STR":24,"DEX":47,"VIT":47,"AGI":22,"INT":21,"MND":39,"CHR":30,"Accuracy":62,"Attack":62,"Magic Accuracy":62,"Gear Haste":4,"DA":7,"Jobs":["drg"]}
Ayanmo_Manopolas = {"Name":"Ayanmo Manopolas +2","STR":16,"DEX":53,"VIT":30,"AGI":11,"INT":14,"MND":37,"CHR":19,"Accuracy":43,"Magic Accuracy":43,"Gear Haste":4,"Jobs":["whm","rdm","brd","blu","run"]}
Bunzi_Gloves = {"Name":"Bunzi's Gloves", "Name2":"Bunzi's Gloves R25","STR":10, "DEX":29, "VIT":26, "AGI":7, "INT":34, "MND":47, "CHR":30, "Accuracy":40+10, "Attack":40+25, "Magic Accuracy":40+10, "Magic Attack":30, "Magic Damage":30+25, "Gear Haste":3, "DA":8, "Magic Burst Damage":8, "Magic Burst Damage II":0+7, "Jobs":["whm","rdm","brd","smn"]}
Piety_Mitts = {"Name":"Piety Mitts +3", "Name2":"Piety Mitts +3 R25","STR":16, "DEX":38, "VIT":35, "AGI":15, "INT":29, "MND":43, "CHR":29, "Accuracy":38, "Attack":63, "Gear Haste":3, "Jobs":["whm"]}
Gazu_bracelet = {"Name":"Gazu Bracelet +1", "Name2":"Gazu Bracelet +1 R15","STR":10+10, "DEX":32+10, "VIT":32+10, "AGI":6+10, "INT":14+10, "MND":29+10, "CHR":19+10, "Accuracy":44+50, "Attack":-17, "Gear Haste":5+10, "Jobs":["mnk","whm","blm","rdm","thf","drk","brd","rng","smn","blu","cor","pup","dnc","sch","geo","run"]}
Arbatel_Bracers = {"Name":"Arbatel Bracers +3","STR":16, "DEX":40, "VIT":38, "AGI":20, "INT":36, "MND":47, "CHR":32, "Accuracy":62, "Magic Accuracy":62, "Magic Attack":52, "Magic Damage":32, "Gear Haste":3, "Magic Burst Damage":15, "Jobs":["sch"]}
Agoge_Mufflers = {"Name":"Agoge Mufflers +3","STR":25, "DEX":39, "VIT":47, "AGI":13, "INT":21, "MND":36, "CHR":26, "Accuracy":38, "Attack":86, "Magic Accuracy":38, "Gear Haste":5, "Fencer":1,"Jobs":["war"]}
Boii_Mufflers = {"Name":"Boii Mufflers +3","STR":24, "DEX":47, "VIT":47, "AGI":22, "INT":130, "MND":38, "CHR":31, "Accuracy":62, "Attack":62, "Magic Accuracy":62, "Axe Skill":31, "Gear Haste":4, "Weaponskill Damage":12, "Jobs":["war"]}
Wakido_Kote = {"Name":"Wakido Kote +3","STR":24, "DEX":40, "VIT":40, "AGI":17, "INT":20, "MND":36, "CHR":30, "Accuracy":48, "Gear Haste":4, "Jobs":["sam"]}
Sakonji_Kote = {"Name":"Sakonji Kote +3","STR":16, "DEX":40, "VIT":40, "AGI":17, "INT":20, "MND":36, "CHR":30, "Accuracy":47, "Attack":81, "Magic Accuracy":38, "Gear Haste":4, "Jobs":["sam"]}
Kasuga_Kote = {"Name":"Kasuga Kote +3","STR":24, "DEX":47, "VIT":47, "AGI":23, "INT":21, "MND":39, "CHR":31, "Accuracy":62, "Attack":62, "Ranged Accuracy":62, "Ranged Attack":62, "Magic Accuracy":62, "Gear Haste":4, "Jobs":["sam"]}
Laksamana_Gants = {"Name":"Laksamana's Gants +3","STR":21, "DEX":45, "VIT":39, "AGI":17, "INT":22, "MND":40, "CHR":27, "Accuracy":30, "Magic Accuracy":53, "Gear Haste":5, "Jobs":["cor"]}
Lanun_Gants = {"Name":"Lanun Gants +3","STR":26, "DEX":45, "VIT":39, "AGI":22, "INT":22, "MND":40, "CHR":27, "Ranged Accuracy":44, "Ranged Attack":76, "Magic Accuracy":38, "Gear Haste":5, "Jobs":["cor"]}
Chasseur_Gants = {"Name":"Chasseur's Gants +3","STR":28, "DEX":49, "VIT":38, "AGI":26, "INT":23, "MND":44, "CHR":26, "Accuracy":62, "Ranged Accuracy":62, "Ranged Attack":62, "Magic Accuracy":62, "Gear Haste":5, "Crit Rate":8, "Weaponskill Damage":12,"Jobs":["cor"]}
Fili_Manchettes = {"Name":"Fili Manchettes +3","STR":16, "DEX":43, "VIT":36, "AGI":20, "INT":29, "MND":47, "CHR":39, "Accuracy":62, "Magic Accuracy":62, "Gear Haste":3, "Jobs":["brd"]}
Bihu_Cuffs = {"Name":"Bihu Cuffs +3","STR":16, "DEX":38, "VIT":35, "AGI":15, "INT":29, "MND":42, "CHR":33, "Accuracy":38, "Attack":63, "Magic Accuracy":44, "Gear Haste":3, "Jobs":["brd"]}
Brioso_Cuffs = {"Name":"Brioso Cuffs +3","STR":16, "DEX":38, "VIT":35, "AGI":15, "INT":29, "MND":42, "CHR":39, "Magic Accuracy":48, "Gear Haste":3, "Jobs":["brd"]}
Ikenga_Gloves = {"Name":"Ikenga's Gloves","STR":21, "DEX":48, "VIT":34, "AGI":19, "INT":16, "MND":32, "CHR":24, "Ranged Accuracy":40+10, "Ranged Attack":40+25, "Magic Accuracy":40+10, "Store TP":9, "PDL":5, "Jobs":["rng","cor"]}
Carmine_Finger_Gauntlets_D = {"Name":"Carmine Finger Gauntlets +1","Name2":"Carmine Finger Gauntlets +1 D","STR":10, "DEX":33, "VIT":32, "AGI":12, "INT":14, "MND":32, "CHR":23, "Ranged Attack":38+20, "Magic Attack":30+12, "Gear Haste":5, "Store TP":0+6, "Jobs":["rdm","pld","drk","drg","blu","run","rng","cor"]}
Meghanada_Gloves = {"Name":"Meghanada Gloves +2","STR":23, "DEX":50, "VIT":29, "AGI":19, "INT":11, "MND":34, "CHR":27, "Accuracy":47, "Attack":43, "Ranged Accuracy":47, "Ranged Attack":43, "Gear Haste":4, "Weaponskill Damage":7, "Jobs":["thf","rng","bst","cor","dnc","run"]}
Oshosi_Gloves = {"Name":"Oshosi Gloves +1","STR":25, "DEX":35, "VIT":34, "AGI":56, "INT":11, "MND":29, "CHR":20, "Ranged Accuracy":44, "Magic Accuracy":49, "Double Shot":5, "Triple Shot":4, "Jobs":["cor","rng"]}
hands = [Oshosi_Gloves,Meghanada_Gloves,Carmine_Finger_Gauntlets_D, Ikenga_Gloves,Fili_Manchettes,Bihu_Cuffs,Brioso_Cuffs,Chasseur_Gants,Lanun_Gants,Laksamana_Gants,Kasuga_Kote,Sakonji_Kote,Wakido_Kote,Boii_Mufflers,Agoge_Mufflers,Arbatel_Bracers,Piety_Mitts,Bunzi_Gloves,Ayanmo_Manopolas,Peltast_Vambraces,Pteroslaver_Finger_Gauntlets,Vishap_Finger_Gauntlets,Atrophy_Gloves,Vitiation_Gloves,Lethargy_Gantherots,Jhakri_Cuffs,Gleti_Gauntlets,Adhemar_Wristbands_A,Adhemar_Wristbands_B,Flamma_Manopolas,Floral_Gauntlets,Hachiya_Tekko,Herculean_Gloves,Hizamaru_Kote,Kendatsuba_Tekko,Malignance_Gloves,Mochizuki_Tekko,Mpaca_Gloves,Mummu_Wrists,Nyame_Gauntlets,Ratri_Gadlings,Ryuo_Tekko_A,Ryuo_Tekko_D,Sakpata_Gauntlets,Sulevia_Gauntlets,Tatenashi_Gote,Hattori_Tekko,Heathen_Gauntlets,Amalric_Gages,Ea_Cuffs,Agwu_Gages,Wicce_Gloves,Archmage_Gloves,Spaekona_Gloves,]

Apate_Ring = {"Name": "Apate Ring", "STR":6, "DEX":6, "AGI":6, "Store TP":3,"Jobs":all_jobs}
Archon_Ring = {"Name": "Archon Ring", "Dark Elemental Bonus":5,"Jobs":all_jobs}
Begrudging_Ring = {"Name": "Begrudging Ring", "Accuracy":7, "Attack": 7, "Crit Rate":5,"Jobs":all_jobs}
Beithir_Ring = {"Name": "Beithir Ring", "Name2": "Beithir Ring R25", "STR":3, "DEX":3, "VIT":3, "AGI":3, "Weaponskill Accuracy":0+15, "Attack":0+10, "Weaponskill Damage":2,"Jobs":["nin","sam","drk","war","mnk","thf","pld","bst","rng","drg","blu","pup","dnc"]}
Chirich_Ring = {"Name": "Chirich Ring +1", "Accuracy":10, "Store TP":6,"Jobs":all_jobs}
Crepuscular_Ring = {"Name": "Crepuscular Ring", "Ranged Accuracy":10, "Magic Accuracy":10, "Store TP":6,"Jobs":all_jobs}
Dingir_Ring = {"Name": "Dingir Ring", "AGI":10, "Ranged Attack":25, "Magic Attack":10,"Jobs":["nin","rng","thf","cor"]}
Epaminondas_Ring = {"Name": "Epaminondas's Ring", "Weaponskill Damage":5, "Store TP":-10,"Jobs":all_jobs}
Epona_Ring = {"Name": "Epona's Ring", "DA":3,"TA":3,"Jobs":["nin","mnk","thf","bst","rng","blu","cor","pup","dnc","run"]}
Flamma_Ring = {"Name": "Flamma Ring", "Accuracy":6, "Magic Accuracy":6, "Store TP":5,"Jobs":["drk","sam","war","pld","drg"]}
Gere_Ring = {"Name": "Gere Ring", "STR":10, "Attack":16, "TA":5,"Jobs":["nin","mnk","thf","bst","pup","dnc"]}
Hetairoi_Ring = {"Name": "Hetairoi Ring", "Crit Rate":1, "TA":2, "TA DMG":5,"Jobs":all_jobs}
Ilabrat_Ring = {"Name": "Ilabrat Ring", "DEX":10, "AGI":10, "Attack":25, "Store TP":5,"Jobs":["nin","sam","rdm","mnk","whm","thf","bst","brd","rng","blu","cor","dnc","run"]}
Karieyh_Ring = {"Name": "Karieyh Ring", "Weaponskill Accuracy":10, "Weaponskill Damage":4,"Jobs":all_jobs}
Locus_Ring = {"Name": "Locus Ring", "Magic Burst Damage":5,"Jobs":all_jobs}  # Ignoring the Magic Crit Rate +5 stat since we do not know how it behaves.
Metamorph_Ring = {"Name": "Metamorph Ring +1", "Name2": "Metamorph Ring +1 R15", "INT":6+10, "MND":6+10, "CHR":6+10, "Magic Accuracy":4+10,"Jobs":all_jobs}
Mujin_Band = {"Name": "Mujin Band", "Skillchain Bonus": 5, "Magic Burst Damage II":5,"Jobs":all_jobs}
Mummu_Ring = {"Name": "Mummu Ring", "Accuracy":6, "Ranged Accuracy":6, "Magic Accuracy":6, "Crit Rate":3,"Jobs":["nin","thf","dnc","rng","mnk","cor"]}
Niqmaddu_Ring = {"Name": "Niqmaddu Ring", "STR":10, "DEX":10, "VIT":10, "QA":3,"Jobs":["drk","sam","war","mnk","drg","pup","run"]}
Petrov_Ring = {"Name": "Petrov Ring", "STR":3, "DEX":3, "VIT":3, "AGI":3, "DA":1,"Store TP":5,"Jobs":all_jobs}
Regal_Ring = {"Name": "Regal Ring", "STR":10, "DEX":10, "VIT":10, "AGI":10, "Attack":20, "Ranged Attack":20,"Jobs":["nin","drk","sam","war","mnk","thf","pld","bst","rng","drg","cor","pup","dnc","run"]}
Rufescent_Ring = {"Name": "Rufescent Ring", "STR":6, "MND":6, "Weaponskill Accuracy": 7,"Jobs":all_jobs}
Shiva_Ring1 = {"Name": "Shiva Ring +1", "Name2": "Shiva Ring +1A", "INT":9, "Magic Attack":3,"Jobs":all_jobs}
Shiva_Ring2 = {"Name": "Shiva Ring +1", "Name2": "Shiva Ring +1B", "INT":9, "Magic Attack":3,"Jobs":all_jobs}
Fenrir_Ring1 = {"Name": "Fenrir Ring +1", "Name2": "Fenrir Ring +1A", "Magic Accuracy":3, "Magic Attack":3, "Magic Damage":3,"Jobs":all_jobs}
Fenrir_Ring2 = {"Name": "Fenrir Ring +1", "Name2": "Fenrir Ring +1B", "Magic Accuracy":3, "Magic Attack":3, "Magic Damage":3,"Jobs":all_jobs}
Shukuyu_Ring = {"Name": "Shukuyu Ring", "STR":7, "Attack":15,"Jobs":all_jobs}
Sroda_Ring = {"Name": "Sroda Ring", "STR":15, "DEX":-20, "PDL":3,"Jobs":all_jobs}
Weatherspoon_Ring = {"Name": "Weatherspoon Ring +1", "Light Elemental Bonus":11, "Magic Accuracy":13,"Jobs":all_jobs}
Freke_Ring = {"Name":"Freke Ring", "INT":10, "Magic Attack":8,"Jobs":["whm","blm","rdm","sch","geo"]}
Stikini_Ring1 = {"Name":"Stikini Ring +1", "MND":8, "Magic Accuracy":8, "Elemental Magic Skill":8, "Ninjutsu Skill":8, "Dark Magic Skill":8, "Jobs":["war","whm","blm","rdm","thf","pld","drk","bst","brd","rng","sam","nin","drg","blu","pup","dnc","sch","run","geo"]}
Stikini_Ring2 = {"Name":"Stikini Ring +1", "MND":8, "Magic Accuracy":8, "Elemental Magic Skill":8, "Ninjutsu Skill":8, "Dark Magic Skill":8, "Jobs":["war","whm","blm","rdm","thf","pld","drk","bst","brd","rng","sam","nin","drg","blu","pup","dnc","sch","run","geo"]}
Ayanmo_Ring = {"Name":"Ayanmo Ring", "Accuracy":6, "Magic Accuracy":6, "Jobs":["whm","rdm","brd","blu","run"]}
Cacoethic_Ring = {"Name":"Cacoethic Ring +1","Name2":"Cacoethic Ring +1 R15","Accuracy":11,"Ranged Accuracy":16,"DEX":0+10,"AGI":0+10,"Jobs":["war","mnk","whm","blm","rdm","thf","pld","drk","bst","brd","rng","sam","nin","drg","smn","blu","cor","pup","dnc","sch","geo","run"]}
Ramuh_Ring1 = {"Name": "Ramuh Ring +1", "Name2": "Ramuh Ring +1A", "DEX":9, "Accuracy":5,"Jobs":all_jobs}
Ifrit_Ring1 = {"Name": "Ifrit Ring +1", "Name2": "Ifrit Ring +1A", "STR":9, "Attack":5,"Jobs":all_jobs}
Leviathan_Ring1 = {"Name": "Leviathan Ring +1", "Name2": "Leviathan Ring +1A", "MND":9, "Magic Accuracy":3,"Jobs":all_jobs}
Titan_Ring1 = {"Name": "Titan Ring +1", "Name2": "Titan Ring +1A", "VIT":9,"Jobs":all_jobs}
Carbuncle_Ring1 = {"Name": "Carbuncle Ring +1", "Name2": "Carbuncle Ring +1A", "CHR":9,"Magic Accuracy":4,"Jobs":all_jobs}
Garuda_Ring1 = {"Name": "Garuda Ring +1", "Name2": "Garuda Ring +1A", "AGI":9,"Ranged Accuracy":5,"Jobs":all_jobs}
rings = [Garuda_Ring1,Titan_Ring1,Carbuncle_Ring1,Ifrit_Ring1,Fenrir_Ring1,Cacoethic_Ring,Ramuh_Ring1,Ayanmo_Ring,Apate_Ring,Archon_Ring,Begrudging_Ring,Beithir_Ring,Chirich_Ring,Crepuscular_Ring,Dingir_Ring,Epaminondas_Ring,Epona_Ring,Flamma_Ring,Gere_Ring,Hetairoi_Ring,Ilabrat_Ring,Locus_Ring,Metamorph_Ring,Mujin_Band,Mummu_Ring,Niqmaddu_Ring,Petrov_Ring,Regal_Ring,Rufescent_Ring,Shiva_Ring1,Shukuyu_Ring,Sroda_Ring,Weatherspoon_Ring,Freke_Ring,]
rings2 = [Garuda_Ring1,Titan_Ring1,Carbuncle_Ring1,Ifrit_Ring1,Fenrir_Ring1,Cacoethic_Ring,Ramuh_Ring1,Ayanmo_Ring,Apate_Ring,Archon_Ring,Begrudging_Ring,Beithir_Ring,Chirich_Ring,Crepuscular_Ring,Dingir_Ring,Epaminondas_Ring,Epona_Ring,Flamma_Ring,Gere_Ring,Hetairoi_Ring,Ilabrat_Ring,Locus_Ring,Metamorph_Ring,Mujin_Band,Mummu_Ring,Niqmaddu_Ring,Petrov_Ring,Regal_Ring,Rufescent_Ring,Shiva_Ring1,Shukuyu_Ring,Sroda_Ring,Weatherspoon_Ring,Freke_Ring,]

Andartia_Critagi = {"Name": "Andartia's Mantle", "Name2": "Andartia's Mantle AGI Crit Rate", "AGI":30, "Accuracy":20, "Attack":20, "Crit Rate":10, "Jobs":["nin"]}
# Each job has identical Ambuscade cape augments. Here I define a simple code block to automatically build each possible type of ambu cape for each job.
# We define filters so that some cape variants aren't created, such as CHR capes on NIN which would never be used and would only waste computation time if included.
# This is a simple loop reading from pre-defined lists, but it will save us well over 100 lines of modifying nearly identical capes with different names and jobs.
cape_names = {"NIN":["Andartia's Mantle",{"Jobs":["nin"]},["STR","DEX","INT","AGI"]],
              "DRK":["Ankou's Mantle",{"Jobs":["drk"]},["STR","DEX","VIT","INT"]],
              "SAM":["Smertrios's Mantle",{"Jobs":["sam"]},["STR","DEX","VIT","INT"]],
              "RDM":["Sucellos's Cape",{"Jobs":["rdm"]},["STR","DEX","INT","MND"]],
              "DRG":["Brigantia's Mantle",{"Jobs":["drg"]},["STR","DEX","VIT","AGI","INT"]],
              "WAR":["Cichol's Mantle",{"DA DMG":20,"Jobs":["war"]},["STR","DEX","VIT","AGI","INT","MND","CHR"]],
              "COR":["Camulus's Mantle",{"Triple Shot":5,"Jobs":["cor"]},["STR","DEX","AGI","INT"]],
            #   "MNK":["Segomo's Mantle",{"Kick Attacks":10,"Kick Attacks Attack":25,"Jobs":["mnk"]},["STR","DEX","VIT","AGI","INT","MND","CHR"]] Commented out until I add "Kick Attacks" and Kick Attacks Attack" as stats to set_stats.py
              "WHM":["Alaunus's Cape",{"Jobs":["whm"]},["STR","DEX","MND"]],
              "GEO":["Nantosuelta's Cape",{"Jobs":["geo"]},["STR","DEX","MND","INT"]],
              "BRD":["Intarabus's Cape",{"Jobs":["brd"]},["STR","DEX","CHR"]],
              "BLM":["Taranus's Cape",{"Magic Burst Damage":5,"Jobs":["blm"]},["STR","DEX","INT","MND"]],
              "SCH":["Lugh's Cape",{"Skillchain Bonus":10,"Jobs":["sch"]},["STR","DEX","INT","MND"]],
            #   "THF":["Toutatis's Cape",{"Sneak Attack":10,"TA DMG":20,"Jobs":["thf"]},["STR","DEX","VIT","AGI","INT","MND","CHR"]], # Commented out until I add "Sneak Attack" as a stat to set_stats.py
            # etc etc.
            # Will add more capes as I add more jobs.
              }

# Now list each base stat and the main stats you want to be considered with the base stat.
ambu_stats = {"STR":["Weaponskill Damage","DA","Crit Rate"],
              "DEX":["Weaponskill Damage","DA","Store TP","Dual Wield","Crit Rate"],
              "VIT":["Weaponskill Damage","DA"],
              "AGI":["Weaponskill Damage","DA","Store TP","Crit Rate"],
              "INT":["Weaponskill Damage","DA"],
              "MND":["Weaponskill Damage","DA"],
              "CHR":["Weaponskill Damage","DA"]}

# I failed to write this in a single-line with list comprehension. I was close, but a multi-line for-loop is easier to read anyway...
capes = []
for job in cape_names:
    for base_stat in ambu_stats:
        if base_stat not in cape_names[job][2]:
            continue # Skip stats for jobs that don't use them. (For example: Don't consider ANY capes with CHR, MND, or VIT for NIN)
        for main_stat in ambu_stats[base_stat]:
            capes.append({**{"Name":f"{cape_names[job][0]}","Name2":f"{cape_names[job][0]} {base_stat} {main_stat}", "Accuracy":20, "Attack":20, f"{base_stat}":30, f"{main_stat}":10}, **{i:cape_names[job][1][i] for i in cape_names[job][1]}})
        if job in ["NIN", "RDM", "WHM", "BLM", "SCH", "GEO", "DRK", "WAR", "SAM"] and base_stat in ["INT","MND","STR","DEX"]: # List of jobs that use magic weapon skills
            if job=="SAM" and base_stat!="STR": # SAM only needs STR+WSD (probably)
                continue
            # Add capes with Macc+Mdmg + WSD + STAT
            capes.append({**{"Name":f"{cape_names[job][0]}","Name2":f"{cape_names[job][0]} {base_stat} Weaponskill Damage (Magic)", f"{base_stat}":30, "Weaponskill Damage":10, "Magic Accuracy":20, "Magic Damage":20}, **{i:cape_names[job][1][i] for i in cape_names[job][1]}})

        if job in ["NIN", "RDM", "COR", "RNG", "SAM"] and base_stat in ["AGI","STR"]: # The list of jobs that might build physical ranged WS sets.
            # add ranged WS sets with stat+30, WSD+10, Racc/Ratk+20 for a select few jobs. Only RNG gets a DEX cape, but it should use crit rate for jishnus  TODO
            capes.append({**{"Name":f"{cape_names[job][0]}","Name2":f"{cape_names[job][0]} {base_stat} Weaponskill Damage (Ranged)", f"{base_stat}":30, "Weaponskill Damage":10, "Ranged Accuracy":20, "Ranged Attack":20}, **{i:cape_names[job][1][i] for i in cape_names[job][1]}})

    if job in ["NIN", "BLM", "RDM", "SCH", "GEO", "DRK"]: # The list of jobs with access to nukes get nuke capes
        # add nuking capes with INT+30, Matk+10, Macc/Mdmg+20 for a select few jobs.
        capes.append({**{"Name":f"{cape_names[job][0]}","Name2":f"{cape_names[job][0]} INT Magic Attack", "INT":30, "Magic Attack":10, "Magic Accuracy":20, "Magic Damage":20}, **{i:cape_names[job][1][i] for i in cape_names[job][1]}})
    if job in ["COR"]: # COR needs an AGI+Matk cape for quick draw
        capes.append({**{"Name":f"{cape_names[job][0]}","Name2":f"{cape_names[job][0]} AGI Magic Attack (Magic)", "AGI":30, "Magic Attack":10, "Magic Accuracy":20, "Magic Damage":20}, **{i:cape_names[job][1][i] for i in cape_names[job][1]}})
    
# We now have a cape for all jobs with all combinations of stats that we care about.


Eschan_Stone = {"Name": "Eschan Stone", "Accuracy":15, "Ranged Accuracy":15, "Attack":15, "Ranged Attack":15, "Magic Accuracy":7, "Magic Attack":7,"Jobs":all_jobs}
Fotia_Belt = {"Name": "Fotia Belt", "Weaponskill Accuracy": 10, "ftp": 25./256.,"Jobs":all_jobs}
Grunfeld_Rope = {"Name": "Grunfeld Rope", "STR":5, "DEX":5, "Accuracy":10, "Attack":20, "DA":2,"Jobs":all_jobs}
Hachirin_no_Obi = {"Name": "Hachirin-no-Obi", "Weather":2,"Jobs":all_jobs}
Ioskeha_Belt = {"Name": "Ioskeha Belt +1", "Accuracy":17, "DA":9, "Gear Haste":8,"Jobs":["war","drk","sam","drg","run"]}
Kentarch_Belt = {"Name": "Kentarch Belt +1", "Name2": "Kentarch Belt +1 R15", "STR":0+10, "DEX":0+10, "Accuracy":14, "DA":3, "Store TP":5,"Jobs":["nin","drk","sam","war","rdm","thf","pld","bst","brd","rng","drg","blu","cor","dnc","run"]}
Orpheus_Sash = {"Name": "Orpheus's Sash", "Elemental Bonus": 15,"Jobs":all_jobs}
Reiki_Yotai = {"Name": "Reiki Yotai", "Accuracy":10, "Ranged Accuracy":10, "Store TP":4, "Dual Wield":7,"Jobs":["nin","drk","sam","war","mnk","rdm","thf","pld","bst","brd","drg","blu","cor","dnc","run"]}
Sailfi_Belt = {"Name": "Sailfi Belt +1", "Name2": "Sailfi Belt +1 R15", "Gear Haste":9, "TA":2, "Attack":14, "STR":0+15, "DA":0+5,"Jobs":["nin","drk","sam","war","rdm","thf","pld","bst","rng","brd","drg","blu","cor","dnc","run"]}
Windbuffet_Belt = {"Name": "Windbuffet Belt +1", "Accuracy":2, "TA":2, "QA":2,"Jobs":all_jobs}
Skrymir_Cord = {"Name":"Skrymir Cord +1", "Magic Accuracy":7, "Magic Attack":7, "Magic Damage":35,"Jobs":all_jobs}
Sacro_Cord = {"Name":"Sacro Cord", "INT":8, "MND":8, "Magic Accuracy":8, "Magic Attack":8, "Jobs":["whm","blm","rdm","blu","sch","geo"]}
Acuity_Belt = {"Name":"Acuity Belt +1","Name2":"Acuity Belt +1 R15", "INT":6+10, "Magic Accuracy":15,"Jobs":["mnk","whm","blm","rdm","pld","brd","rng","blu","pup","sch","geo","run"]}
Luminary_Sash = {"Name":"Luminary Sash", "MND":10, "Magic Accuracy":10, "Jobs":["mnk","whm","blm","rdm","pld","brd","rng","smn","blu","pup","sch","geo","run"]}
Yemaya_Belt = {"Name":"Yemaya Belt", "AGI":7, "Ranged Accuracy":10, "Ranged Attack":10, "Store TP":4, "Jobs":["mnk","whm","rdm","thf","bst","brd","rng","sam","nin","blu","cor","dnc","run"]}
Prosilio_Belt = {"Name":"Prosilio Belt +1","STR":10,"Attack":28,"DA":-5,"Weaponskill Accuracy":5,"Jobs":["war","mnk","whm","blm","rdm","thf","pld","drk","bst","brd","rng","sam","nin","drg","smn","blu","cor","pup","dnc","sch","geo","run"]}
Kwahu_Kachina_Belt = {"Name":"Kwahu kachina belt +1","AGI":8, "Ranged Accuracy":20, "Magic Accuracy":20, "Crit Rate":5, "Jobs":["rng","cor"]}
Tellen_Belt = {"Name":"Tellen Belt","Name2":"Tellen Belt R25","AGI":5, "Ranged Attack":0+10, "Ranged Accuracy":0+15, "True Shot":5, "Jobs":["rng","cor"]}
waists = [Tellen_Belt,Kwahu_Kachina_Belt,Prosilio_Belt,Yemaya_Belt,Luminary_Sash,Sacro_Cord,Acuity_Belt,Eschan_Stone,Fotia_Belt,Grunfeld_Rope,Ioskeha_Belt,Kentarch_Belt,Orpheus_Sash,Reiki_Yotai,Sailfi_Belt,Windbuffet_Belt,Skrymir_Cord,]

Adhemar_Kecks_A = {"Name": "Adhemar Kecks +1", "Name2": "Adhemar Kecks +1 A", "STR":32, "DEX":0+12, "VIT":15, "AGI":30+12, "INT":28, "MND":16, "CHR":8, "Accuracy":34+20, "Ranged Accuracy":34, "Gear Haste":6, "Store TP":8,"Jobs":["mnk","thf","rng","nin","blu","cor","dnc","run"]}
Adhemar_Kecks_B = {"Name": "Adhemar Kecks +1", "Name2": "Adhemar Kecks +1 B", "STR":32+12, "DEX":0+12, "VIT":15, "AGI":30, "INT":28, "MND":16, "CHR":8, "Accuracy":34, "Ranged Accuracy":34, "Attack":20, "Gear Haste":6, "Store TP":8,"Jobs":["mnk","thf","rng","nin","blu","cor","dnc","run"]}
Fallen_Flanchard = {"Name": "Fallen's Flanchard +3", "STR":45,"DEX":0,"VIT":31,"AGI":26,"INT":40,"MND":27,"CHR":20,"Accuracy":39,"Attack":64,"Gear Haste":5,"Weaponskill Damage":10,"Jobs":["drk"]}
Flamma_Dirs = {"Name": "Flamma Dirs +2", "STR":53,"DEX":11,"VIT":29,"AGI":16,"INT":24,"MND":14,"CHR":11,"Accuracy":45,"Magic Accuracy":45,"Gear Haste":4,"Store TP":8,"Jobs":["drk","sam","war","pld","drg"]}
Gyve_Trousers = {"Name": "Gyve Trousers", "STR":19, "DEX":12, "VIT":19, "AGI":5, "INT":35, "MND":25, "CHR":23, "Magic Attack":40, "Gear Haste":5,"Jobs":["whm","brd","smn","blu","pup","nin","drk","blm","rdm","sch","geo","rng"]}
Hachiya_Hakama = {"Name": "Hachiya Hakama +3", "STR":42, "DEX":0, "VIT":24, "AGI":31, "INT":42, "MND":27, "CHR":20, "Accuracy":56, "Ranged Accuracy":35, "Gear Haste":6, "Store TP":6, "Dual Wield":5,"Jobs":["nin"]}
Herculean_Trousers = {"Name": "Herculean Trousers", "STR":33, "DEX":0, "VIT":16, "AGI":32, "INT":29, "MND":15, "CHR":10, "Attack":15, "Ranged Attack":15,"Gear Haste":6, "Store TP":4,"Jobs":["nin","mnk","thf","rng","blu","cor","pup","dnc","run"]}
Hizamaru_Hizayoroi = {"Name": "Hizamaru Hizayoroi +2", "STR":50, "DEX":0, "VIT":32, "AGI":24, "INT":24, "MND":11, "CHR":19, "Accuracy":45, "Attack":27, "Gear Haste":9, "Weaponskill Damage":7,"Jobs":["nin","sam","mnk","pup"]}
Ignominy_Flanchard = {"Name": "Ignominy Flanchard +3", "STR":50,"DEX":15,"VIT":31,"AGI":26,"INT":40,"MND":22,"CHR":20,"Accuracy":49,"Attack":45,"Gear Haste":5,"DA":10,"Jobs":["drk"]}
Jokushu_Haidate = {"Name": "Jokushu Haidate", "STR":29, "DEX":35, "VIT":15, "AGI":21, "INT":30, "MND":17, "CHR":11, "Gear Haste":20, "Crit Rate":4,"Jobs":["nin","sam","war","mnk","bst","brd","rng"]}
Kendatsuba_Hakama = {"Name": "Kendatsuba Hakama +1", "STR":37, "DEX":5, "VIT":25, "AGI":33, "INT":32, "MND":16,"CHR":12,"Accuracy":51,"Ranged Accuracy":46,"Gear Haste":9,"TA":5,"Crit Rate":7,"Jobs":["nin","sam","mnk"]}
Malignance_Tights = {"Name": "Malignance Tights", "STR":28, "DEX":0, "VIT":17, "AGI":42, "INT":26, "MND":19, "CHR":12, "Accuracy":50, "Ranged Accuracy":50, "Magic Accuracy":50, "Gear Haste":9, "Store TP":10, "PDL":5,"Jobs":["mnk", "rdm", "thf", "bst", "rng", "nin", "blu", "cor", "pup", "dnc"]}
Mochizuki_Hakama = {"Name": "Mochizuki Hakama +3", "STR":42, "DEX":0, "VIT":24, "AGI":36, "INT":42, "MND":27, "CHR":20, "Accuracy":39, "Attack":64, "Magic Accuracy":39, "Gear Haste":6, "Dual Wield":10, "Weaponskill Damage":10,"Jobs":["nin"]}
Mpaca_Hose = {"Name": "Mpaca's Hose", "Name2": "Mpaca's Hose R25", "STR":49, "DEX":0, "VIT":32, "AGI":25, "INT":32,"MND":19,"CHR":19,"Accuracy":40+10,"Attack":40+25,"Magic Accuracy":40+10,"Gear Haste":9,"TA":4,"Crit Rate":6,"PDL":0+7,"Jobs":["nin","sam","mnk","pup"]}
Mummu_Kecks = {"Name": "Mummu Kecks +2", "STR":33, "DEX":11, "VIT":16, "AGI":45, "INT":29, "MND":15, "CHR":12, "Accuracy":45, "Ranged Accuracy":45, "Magic Accuracy": 45, "Gear Haste":6, "Crit Rate": 7,"Jobs":["nin","mnk","thf","rng","cor","dnc"]}
Nyame_Flanchard = {"Name": "Nyame Flanchard", "Name2": "Nyame Flanchard R25 B", "STR":43, "DEX":0, "VIT":30, "AGI":34, "INT":44, "MND":32, "CHR":24, "Accuracy":40, "Attack":30+30, "Gear Haste":3, "Weaponskill Damage":0+11, "Magic Accuracy":40, "Magic Attack":30, "Ranged Accuracy":40, "Ranged Attack":30+30,"DA":0+5,"Magic Burst Damage":6,"Jobs":all_jobs}
Rao_Haidate_B = {"Name": "Rao Haidate +1", "Name2": "Rao Haidate +1 B", "STR":46+12, "DEX":0+12, "VIT":15, "AGI":21, "INT":30, "MND":31, "CHR":8, "Attack":43+20, "Gear Haste":6, "Store TP":8,"Jobs":["nin","sam"]}
Ratri_Cuisses = {"Name": "Ratri Cuisses +1", "STR":52, "DEX":0, "VIT":21, "AGI":19, "INT":37, "MND":19, "CHR":15, "Magic Accuracy":46, "Scythe Skill":55, "Gear Haste":5, "Weaponskill Damage":9, "Store TP":10,"Jobs":["drk"]}
Ryuo_Hakama_A = {"Name": "Ryuo Hakama +1", "Name2": "Ryuo Hakama +1 A", "STR":29+12, "DEX":0+12, "VIT":15, "AGI":21, "INT":30, "MND":17, "CHR":11,"Accuracy":0+20,"Attack":33,"Ranged Attack":33, "Gear Haste":5,"Store TP":8,"DA":4,"Jobs":["nin","sam","mnk","pup"]}
Sakpata_Cuisses = {"Name": "Sakpata's Cuisses", "Name2": "Sakpata's Cuisses R25", "STR":48,"DEX":0,"VIT":34,"AGI":23,"INT":32,"MND":21,"CHR":17,"Accuracy":40+10,"Magic Accuracy":40+10,"Attack":40+25,"Gear Haste":4,"DA":7,"PDL":7,"Jobs":["drk","war","pld"]}
Samnuha_Tights = {"Name": "Samnuha Tights", "STR":38+10, "DEX":6+10, "VIT":15, "AGI":30, "INT":28, "MND":16, "CHR":8, "Accuracy":15, "Ranged Accuracy":15, "Gear Haste":6, "Store TP":7, "DA":3, "TA":3,"Jobs":["nin"]}
Sulevia_Flanchard = {"Name": "Sulevia's Flanchard +2", "STR":47,"DEX":0,"VIT":33,"AGI":14,"INT":24,"MND":20,"CHR":18,"Accuracy":45,"Attack":49,"Gear Haste":2,"TA":4,"Jobs":["drk","war","pld","drg"]}
Tatenashi_Haidate = {"Name": "Tatenashi Haidate +1", "Name2": "Tatenashi Haidate +1 R15", "STR":45+10, "DEX":0+10, "VIT":25+10, "AGI":15+10, "INT":23+10, "MND":12+10, "CHR":10+10,"Accuracy":0+60,"Attack":31,"Gear Haste":5,"Store TP":7,"TA":0+3,"Jobs":["nin","sam","mnk","war","rng"]}
Wakido_Haidate = {"Name": "Wakido Haidate +3", "STR":44, "DEX":0, "VIT":29, "AGI":25, "INT":37, "MND":26, "CHR":20, "Accuracy":49, "Attack":40, "Ranged Attack":40, "Gear Haste":5, "Store TP":9, "Weaponskill Damage":10,"Jobs":["sam"]}
Hattori_Hakama = {"Name": "Hattori Hakama +3", "STR":44,"DEX":0,"VIT":27,"AGI":35,"INT":45,"MND":27,"CHR":21,"Gear Haste":8,"Katana Skill":33,"Accuracy":63,"Ranged Accuracy":63,"Magic Accuracy":63,"Attack":63,"Jobs":["nin"]}
Heathen_Flanchard = {"Name": "Heathen's Flanchard +3", "STR":53,"DEX":0,"VIT":35,"AGI":30,"INT":41,"MND":29,"CHR":26,"Gear Haste":5,"Accuracy":63,"Magic Accuracy":63,"Attack":73,"Jobs":["drk"]}
Amalric_Slops = {"Name":"Amalric Slops +1", "Name2":"Amalric Slops +1A",  "STR":19,"DEX":0,"VIT":6,"AGI":14,"INT":40,"MND":25,"CHR":19,"Magic Accuracy":0+20,"Magic Attack":40+20,"Magic Burst Damage":0,"Magic Burst Damage II":0,"Magic Damage":0,"Gear Haste":5,"Jobs":["blm","sch","rdm","geo","blu"]}
Ea_Slops = {"Name":"Ea Slops +1","STR":26,"DEX":0,"VIT":17,"AGI":24,"INT":48,"MND":31,"CHR":23,"Magic Accuracy":51,"Magic Attack":41,"Magic Burst Damage":8, "Magic Burst Damage II":8,"Gear Haste":5,"Jobs":["blm", "rdm", "geo"]}
Agwu_Slops = {"Name":"Agwu's Slops", "Name2": "Agwu's Slops R25", "STR":43,"DEX":0,"VIT":8,"AGI":17,"INT":49,"MND":32,"CHR":25, "Accuracy":40+10, "Magic Accuracy":40+10,"Magic Attack":35+23,"Magic Burst Damage":9,"Magic Burst Damage II":0,"Magic Damage":20,"Gear Haste":5,"Jobs":["blm", "sch", "geo", "run"]}
Wicce_Chausses = {"Name":"Wicce Chausses +3", "STR":31,"DEX":0,"VIT":31,"AGI":31,"INT":53,"MND":38,"CHR":32, "Accuracy":63,"Magic Accuracy":63,"Magic Attack":58,"Magic Burst Damage":15,"Magic Burst Damage II":0,"Magic Damage":33,"Gear Haste":5,"Jobs":["blm"]}
Archmage_Tonban = {"Name":"Archmage's Tonban +3", "STR":35,"DEX":0,"VIT":22,"AGI":27,"INT":40,"MND":34,"CHR":29, "Magic Accuracy":46,"Magic Attack":58, "Magic Burst Damage II":3, "Accuracy":39,"Gear Haste":5,"Jobs":["blm"]}
Spaekona_Tonban = {"Name":"Spaekona Tonban +3", "STR":35,"DEX":0,"VIT":22,"AGI":27,"INT":44,"MND":34,"CHR":29,"Magic Accuracy":49,"Magic Damage":46,"Magic Attack":30,"Gear Haste":5,"Jobs":["blm"]}
Zoar_Subligar = {"Name":"Zoar Subligar +1", "Name2":"Zoar Subligar +1 R15", "STR":29+10, "DEX":0+10,"VIT":16+10,"AGI":20+10,"INT":30+10,"MND":17+10,"CHR":11+10, "Accuracy":0+30, "Gear Haste":6, "Store TP":-5, "DA":4, "TA":3, "Crit Rate":5, "Jobs":["war","rdm","thf","pld","drk","bst","brd","rng","sam","nin","drg","blu","cor","dnc","run"]}
Gleti_Breeches = {"Name":"Gleti's Breeches", "Name2":"Gleti's Breeches R25","STR":49,"VIT":37,"AGI":23,"INT":30,"MND":20,"CHR":17,"Accuracy":40+10,"Attack":40+25,"Magic Accuracy":40+10,"Gear Haste":5,"PDL":8,"Crit Rate":7,"Jobs":["thf","bst","drg","blu","dnc"]}
Jhakri_Slops = {"Name":"Jhakri Slops +2", "STR":47,"DEX":0,"VIT":3,"AGI":14,"INT":52,"MND":26,"CHR":20,"Accuracy":45,"Attack":45,"Magic Accuracy":45,"Magic Attack":42,"Gear Haste":2,"Store TP":9,"Jobs":["blm","rdm","blu","sch","geo"]}
Vitiation_Tights = {"Name":"Vitiation Tights +3","STR":35,"DEX":22,"VIT":22,"AGI":27,"INT":44,"MND":34,"CHR":29,"Accuracy":39,"Attack":64,"Magic Accuracy":39,"Gear Haste":5,"Elemental Magic Skill":23, "Jobs":["rdm"]}
Lethargy_Fuseau = {"Name":"Lethargy Fuseau +3","STR":38,"DEX":0,"VIT":20,"AGI":30,"INT":48,"MND":43,"CHR":30,"Accuracy":63,"Attack":63,"Magic Accuracy":63,"Magic Attack":58,"Magic Damage":33,"Gear Haste":5,"Magic Burst Damage":15,"Jobs":["rdm"]}
Vishap_Brais = {"Name":"Vishap Brais +3","STR":43,"DEX":20,"VIT":29,"AGI":25,"INT":36,"MND":26,"CHR":22,"Accuracy":49,"Gear Haste":5,"Weaponskill Damage":10,"Jobs":["drg"]}
Pteroslaver_Brais = {"Name":"Pteroslaver Brais +3","STR":43,"DEX":22,"VIT":41,"AGI":25,"INT":36,"MND":26,"CHR":22,"Accuracy":39,"Attack":64,"Gear Haste":5,"Store TP":10,"Jobs":["drg"]}
Peltast_Cuissots = {"Name":"Peltast's Cuissots +3","STR":53,"VIT":40,"AGI":30,"INT":38,"MND":27,"CHR":25,"Accuracy":63,"Attack":73,"Magic Accuracy":63,"Gear Haste":5,"Crit Damage":13,"Jobs":["drg"]}
Ayanmo_Cosciales = {"Name":"Ayanmo Cosciales +2","STR":33,"DEX":11,"VIT":16,"AGI":34,"INT":29,"MND":26,"CHR":10,"Accuracy":45,"Magic Accuracy":45,"Gear Haste":9,"Jobs":["whm","rdm","brd","blu","run"]}
Bunzi_Pants = {"Name":"Bunzi's Pants", "Name2":"Bunzi's Pants R25","STR":25, "DEX":0, "VIT":12, "AGI":19, "INT":51, "MND":38, "CHR":30, "Accuracy":40+10, "Attack":40+25, "Magic Accuracy":40+10, "Magic Attack":30, "Magic Damage":30+25, "Gear Haste":5, "Magic Burst Damage":9, "Jobs":["whm","rdm", "brd", "smn"]}
Piety_Pantaloons = {"Name":"Piety Pantaloons +3", "Name2":"Piety Pantaloons +3 R25","STR":35, "DEX":0, "VIT":22, "AGI":27, "INT":44, "MND":34, "CHR":29, "Accuracy":39, "Attack":64, "Gear Haste":5, "Jobs":["whm"]}
Arbatel_Pants = {"Name":"Arbatel Pants +3","STR":31, "DEX":0, "VIT":23, "AGI":31, "INT":53, "MND":38, "CHR":32, "Accuracy":63, "Magic Accuracy":63+36, "Magic Attack":53, "Magic Damage":33, "Gear Haste":5, "Jobs":["sch"]}
Pummeler_Cuisses = {"Name":"Pummeler's Cuisses +3","STR":40, "DEX":0, "VIT":27, "AGI":27, "INT":39, "MND":26, "CHR":26, "Accuracy":56, "Gear Haste":6, "DA":11,"Jobs":["war"]}
Agoge_Cuisses = {"Name":"Agoge Cuisses +3","STR":43, "DEX":0, "VIT":30, "AGI":24, "INT":36, "MND":23, "CHR":23, "Accuracy":39, "Attack":64, "Magic Accuracy":39, "Gear Haste":6, "DA":6, "DA DMG":11, "Jobs":["war"]}
Boii_Cuisses = {"Name":"Boii Cuisses +3","STR":53, "DEX":0, "VIT":40, "AGI":30, "INT":38, "MND":27, "CHR":25, "Accuracy":63, "Attack":73, "Magic Accuracy":63, "Gear Haste":8, "DA":8, "Fencer":4, "PDL":10, "TP Bonus":100, "Jobs":["war"]}
Sakonji_Haidate = {"Name":"Sakonji Haidate +3","STR":43, "DEX":0, "VIT":29, "AGI":25, "INT":36, "MND":26, "CHR":22, "Accuracy":39, "Attack":82, "Magic Accuracy":39, "Gear Haste":5, "Jobs":["sam"]}
Kasuga_Haidate = {"Name":"Kasuga Haidate +3","STR":53, "DEX":19, "VIT":40, "AGI":30, "INT":38, "MND":27, "CHR":25, "Accuracy":63, "Attack":63, "Magic Accuracy":63, "Gear Haste":5, "Store TP":11, "JA Haste":3,"Jobs":["sam"]}
Laksamana_Trews = {"Name":"Laksamana's Trews +3","STR":39, "DEX":0, "VIT":24, "AGI":33, "INT":40, "MND":27, "CHR":21, "Attack":35, "Ranged Accuracy":49, "Gear Haste":6, "Jobs":["cor"]}
Lanun_Trews = {"Name":"Lanun Trews +3","STR":42, "DEX":0, "VIT":24, "AGI":36, "INT":40, "MND":27, "CHR":21, "Attack":78, "Ranged Accuracy":46, "Ranged Attack":78, "Magic Accuracy":39, "Gear Haste":6, "Jobs":["cor"]}
Chasseur_Culottes = {"Name":"Chasseur's Culottes +3","STR":45, "DEX":20, "VIT":27, "AGI":43, "INT":43, "MND":31, "CHR":20, "Accuracy":63, "Ranged Accuracy":63, "Ranged Attack":63, "Magic Accuracy":63, "Gear Haste":6, "Store TP":12, "Jobs":["cor"]}
Brioso_Cannions = {"Name":"Brioso Cannions +3","STR":33, "DEX":0, "VIT":20, "AGI":27, "INT":44, "MND":33, "CHR":33, "Magic Accuracy":56, "Gear Haste":5, "Jobs":["brd"]}
Bihu_Cannions = {"Name":"Bihu Cannions +3","STR":33, "DEX":0, "VIT":20, "AGI":27, "INT":54, "MND":43, "CHR":43, "Accuracy":39, "Attack":64, "Magic Accuracy":52, "Gear Haste":5, "Jobs":["brd"]}
Fili_Rhingrave = {"Name":"Fili Rhingrave +3","STR":33, "DEX":0, "VIT":20, "AGI":30, "INT":44, "MND":38, "CHR":38, "Accuracy":63, "Magic Accuracy":63, "Gear Haste":5, "Jobs":["brd"]}
Ikenga_Trousers = {"Name":"Ikenga's Trousers","STR":38, "DEX":0, "VIT":20, "AGI":40, "INT":32, "MND":20, "CHR":15, "Ranged Accuracy":40+10, "Ranged Attack":40+25, "Magic Accuracy":40+10, "Store TP":10, "PDL":6, "Jobs":["rng","cor"]}
Darraigner_Brais = {"Name":"Darraigner's Brais","STR":29, "DEX":0, "VIT":16, "AGI":34, "INT":30, "MND":17, "CHR":11, "Ranged Attack":33, "Gear Haste":6, "Crit Damage":6, "Jobs":["thf","rng","cor"]}
Meghanada_Chausses = {"Name":"Meghanada Chausses +2","STR":40, "DEX":0, "VIT":15, "AGI":42, "INT":26, "MND":23, "CHR":18, "Accuracy":49, "Attack":45, "Ranged Accuracy":49, "Ranged Attack":45, "Gear Haste":4, "TA":5, "Jobs":["thf","rng","bst","cor","dnc","run"]}
Oshosi_Trousers = {"Name":"Oshosi Trousers +1","STR":43, "DEX":0, "VIT":19, "AGI":43, "INT":29, "MND":20, "CHR":15, "Ranged Accuracy":46, "Magic Accuracy":51, "True Shot":5, "Double Shot":7, "Triple Shot":6, "Jobs":["cor","rng"]}
Lustratio_Subligar = {"Name":"Lustratio Subligar +1","DEX":35+8, "Attack":38, "Accuracy":0+20, "Crit Rate":0+3, "Jobs":["war","thf","pld","drk","bst","brd","drg","dnc","run"]}
legs = [Lustratio_Subligar,Oshosi_Trousers,Meghanada_Chausses,Darraigner_Brais,Ikenga_Trousers,Brioso_Cannions,Bihu_Cannions,Fili_Rhingrave,Chasseur_Culottes,Lanun_Trews,Laksamana_Trews,Kasuga_Haidate,Sakonji_Haidate,Boii_Cuisses,Boii_Cuisses,Agoge_Cuisses,Pummeler_Cuisses,Arbatel_Pants,Piety_Pantaloons,Bunzi_Pants,Ayanmo_Cosciales,Peltast_Cuissots,Vishap_Brais,Pteroslaver_Brais,Vitiation_Tights,Lethargy_Fuseau,Jhakri_Slops,Gleti_Breeches,Zoar_Subligar,Adhemar_Kecks_A,Adhemar_Kecks_B,Fallen_Flanchard,Flamma_Dirs,Gyve_Trousers,Hachiya_Hakama,Herculean_Trousers,Hizamaru_Hizayoroi,Ignominy_Flanchard,Jokushu_Haidate,Kendatsuba_Hakama,Malignance_Tights,Mochizuki_Hakama,Mpaca_Hose,Mummu_Kecks,Nyame_Flanchard,Rao_Haidate_B,Ratri_Cuisses,Ryuo_Hakama_A,Sakpata_Cuisses,Samnuha_Tights,Sulevia_Flanchard,Tatenashi_Haidate,Wakido_Haidate,Hattori_Hakama,Heathen_Flanchard,Amalric_Slops,Ea_Slops,Agwu_Slops,Wicce_Chausses,Archmage_Tonban,Spaekona_Tonban,]

Adhemar_Gamashes_A = {"Name": "Adhemar Gamashes +1", "Name2": "Adhemar Gamashes +1 A", "STR":15, "DEX":23+12, "VIT":8, "AGI":42+12, "INT":0, "MND":11, "CHR":25, "Accuracy":20, "Attack":34, "Ranged Attack":34, "Magic Attack":35, "Gear Haste":4, "Crit Rate":4, "Jobs":["mnk","thf","rng","nin","blu","cor","dnc","run"]}
Adhemar_Gamashes_B = {"Name": "Adhemar Gamashes +1", "Name2": "Adhemar Gamashes +1 B", "STR":15+12, "DEX":23+12, "VIT":8, "AGI":42, "INT":0, "MND":11, "CHR":25, "Attack":34+20, "Ranged Attack":34, "Magic Attack":35, "Gear Haste":4, "Crit Rate":4, "Jobs":["mnk","thf","rng","nin","blu","cor","dnc","run"]}
Adhemar_Gamashes_C = {"Name": "Adhemar Gamashes +1", "Name2": "Adhemar Gamashes +1 C", "STR":15, "DEX":23, "VIT":8, "AGI":42+12, "INT":0, "MND":11, "CHR":25, "Attack":34, "Ranged Accuracy":0+20,"Ranged Attack":34+20, "Magic Attack":35, "Gear Haste":4, "Crit Rate":4, "Jobs":["mnk","thf","rng","nin","blu","cor","dnc","run"]}
Flamma_Gambieras = {"Name": "Flamma Gambieras +2", "STR":31,"DEX":34,"VIT":20,"AGI":26,"INT":0,"MND":6,"CHR":20,"Accuracy":42,"Magic Accuracy":42,"Gear Haste":2,"Store TP":6,"DA":6,"Jobs":["drk","sam","war","pld","drg"]}
Hachiya_Kyahan = {"Name": "Hachiya Kyahan +3", "STR":24, "DEX":25, "VIT":21, "AGI":44, "INT":20, "MND":22, "CHR":39, "Magic Accuracy":52, "Magic Attack":23, "Gear Haste":4, "Magic Burst Damage": 10, "Jobs":["nin"]}
Herculean_Boots = {"Name": "Herculean Boots", "STR":16, "DEX":24, "VIT":10, "AGI":43, "INT":0, "MND":11, "CHR":26, "Accuracy":10, "Attack":10,"Ranged Accuracy":10,"Ranged Attack":10,"Magic Accuracy":10,"Magic Attack":10,"Gear Haste":4,"TA":2, "Jobs":["nin","mnk","thf","rng","blu","cor","pup","dnc","run"]}
Herculean_Boots_QA = {"Name": "Herculean Boots", "STR":16, "DEX":24, "VIT":10, "AGI":43, "INT":0, "MND":11, "CHR":26, "Accuracy":10+35, "Attack":10+18,"Ranged Accuracy":10,"Ranged Attack":10,"Magic Accuracy":10+3,"Magic Attack":10+3,"Gear Haste":4,"TA":2,"QA":3, "Jobs":["nin","mnk","thf","rng","blu","cor","pup","dnc","run"]}
Hizamaru_Sune_Ate = {"Name": "Hizamaru Sune-ate +2", "STR":28, "DEX":31, "VIT":23, "AGI":34, "INT":0, "MND":3, "CHR":28, "Accuracy":42, "Attack":24, "Gear Haste":3, "Dual Wield":8, "Jobs":["nin","sam","mnk","pup"]}
Kendatsuba_Sune_Ate = {"Name": "Kendatsuba Sune-ate +1", "STR":20, "DEX":44, "VIT":21, "AGI":44, "INT":0, "MND":14, "CHR":26, "Accuracy":48, "Ranged Accuracy":43, "Gear Haste":3, "TA":4, "Crit Rate":5, "Jobs":["nin","sam","mnk"]}
Malignance_Boots = {"Name": "Malignance Boots", "STR":6, "DEX":40, "VIT":12, "AGI":49, "INT":0, "MND":15, "CHR":40, "Accuracy":50, "Ranged Accuracy":50, "Magic Accuracy":50, "Gear Haste":3, "Store TP":9, "PDL":2, "Jobs":["mnk", "rdm", "thf", "bst", "rng", "nin", "blu", "cor", "pup", "dnc"]}
Mochizuki_Kyahan = {"Name": "Mochizuki Kyahan +3", "STR":28, "DEX":29, "VIT":25, "AGI":48, "INT":0, "MND":22, "CHR":39, "Accuracy":43, "Attack":76, "Magic Accuracy":36, "Ninjutsu Skill":23, "Gear Haste":4, "Ninjutsu Damage":25, "Jobs":["nin"]}
Mpaca_Boots = {"Name": "Mpaca's Boots", "Name2": "Mpaca's Boots R25","STR":28,"DEX":32,"VIT":23,"AGI":34,"INT":0,"MND":11,"CHR":28,"Accuracy":40+10,"Attack":40+25,"Magic Accuracy":40+10,"Gear Haste":3,"TA":3,"Crit Rate":3,"Magic Attack":0+40, "Jobs":["nin","sam","mnk","pup"]}
Mummu_Gamashes = {"Name": "Mummu Gamashes +2", "STR":16, "DEX":37, "VIT":10, "AGI":57, "INT":0, "MND":11, "CHR":29, "Accuracy":42, "Ranged Accuracy": 42, "Magic Accuracy": 42, "Gear Haste":4, "Crit Rate":5, "Jobs":["nin","mnk","thf","rng","cor","dnc"]}
Nyame_Sollerets = {"Name": "Nyame Sollerets", "Name2": "Nyame Sollerets R25 B", "STR":23, "DEX":26, "VIT":24, "AGI":46, "INT":25, "MND":26, "CHR":38, "Accuracy":40, "Attack":30+30, "Gear Haste":3, "Weaponskill Damage":0+10, "Magic Accuracy":40, "Magic Attack":30, "Ranged Accuracy":40, "Ranged Attack":30+30,"DA":0+4,"Magic Burst Damage":5, "Jobs":all_jobs}
Rao_SuneAte_D = {"Name": "Rao Sune-ate +1", "Name2": "Rao Sune-ate +1 D", "STR":17, "DEX":26, "VIT":12, "AGI":34, "INT":0, "MND":16, "CHR":28,"Accuracy":41,"Crit Rate":0+4,"Gear Haste":4,"DA":0+4, "Jobs":["nin","sam","mnk"]}
Ratri_Sollerets = {"Name": "Ratri Sollerets +1", "STR":29, "DEX":26, "VIT":17, "AGI":32, "INT":0, "MND":16, "CHR":31, "Magic Accuracy":43, "Scythe Skill":52, "Gear Haste":3, "Weaponskill Damage":8,"Jobs":["drk"]}
Ryuo_SuneAte_D = {"Name": "Ryuo Sune-Ate +1", "Name2": "Ryuo Sune-ate +1 D", "STR":27+12, "DEX":19, "VIT":11, "AGI":38, "INT":0, "MND":5, "CHR":19,"Attack":32+25,"Ranged Attack":32,"Crit Rate":0+4,"Gear Haste":3, "Jobs":["nin","sam","mnk","pup"]}
Sakpata_Leggings = {"Name": "Sakpata's Leggings", "Name2": "Sakpata's Leggings R25", "STR":29,"DEX":20,"VIT":30,"AGI":35,"INT":0,"MND":19,"CHR":32,"Accuracy":40+10,"Magic Accuracy":40+10,"Attack":40+25,"Gear Haste":2,"DA":4,"PDL":4,"Jobs":["drk","war","pld"]}
Sulevia_Leggings = {"Name": "Sulevia's Leggings +2", "STR":29,"DEX":19,"VIT":29,"AGI":26,"INT":0,"MND":18,"CHR":32,"Accuracy":42,"Attack":46,"Gear Haste":1,"Weaponskill Damage":7,"Jobs":["drk","war","pld","drg"]}
Tatenashi_SuneAte = {"Name": "Tatenashi Sune-ate +1", "Name2": "Tatenashi Sune-ate +1 R15", "STR":16+10, "DEX":19+10, "VIT":16+10, "AGI":32+10, "INT":0+10, "MND":5+10, "CHR":19+10,"Accuracy":0+60,"Gear Haste":3,"Store TP":7,"TA":0+3, "Jobs":["nin","sam","mnk","war","rng"]}
Hattori_Kyahan = {"Name": "Hattori Kyahan +3", "STR":27,"DEX":39,"VIT":23,"AGI":54,"INT":0,"MND":22,"CHR":40,"Gear Haste":5,"Accuracy":60,"Attack":60,"Ranged Accuracy":60,"Magic Accuracy":60,"Weaponskill Damage":12,"Jobs":["nin"]}
Heathen_Sollerets = {"Name": "Heathen's Sollerets +3", "STR":33,"DEX":25,"VIT":30,"AGI":42,"INT":22,"MND":26,"CHR":38,"Gear Haste":3,"Accuracy":60,"Attack":60,"Ranged Accuracy":60,"Magic Accuracy":60,"Weaponskill Damage":12,"Jobs":["drk"]}
Amalric_Nails = {"Name":"Amalric Nails +1", "Name2":"Amalric Nails +1A",  "STR":6,"DEX":6,"VIT":6,"AGI":26,"INT":21,"MND":20,"CHR":33,"Magic Accuracy":0+20,"Magic Attack":32+20,"Magic Burst Damage":0,"Magic Burst Damage II":0,"Magic Damage":20,"Gear Haste":3,"Jobs":["blm","sch","rdm","geo","blu"]}
Ea_Pigaches = {"Name":"Ea Pigaches +1", "STR":11,"DEX":14,"VIT":15,"AGI":38,"INT":5,"MND":26,"CHR":39,"Magic Accuracy":48,"Magic Attack":32,"Magic Burst Damage":5, "Magic Burst Damage II":5,"Gear Haste":3,"Jobs":["blm", "rdm", "geo"]}
Agwu_Pigaches = {"Name":"Agwu's Pigaches", "Name2": "Agwu's Pigaches R25", "STR":21,"DEX":25,"VIT":8,"AGI":30,"INT":30,"MND":26,"CHR":39, "Accuracy":40+10, "Magic Accuracy":40+10,"Magic Attack":35+23,"Magic Burst Damage":6,"Magic Burst Damage II":0,"Magic Damage":20,"Gear Haste":3,"Jobs":["blm", "sch", "geo", "run"]}
Wicce_Sabots = {"Name":"Wicce Sabots +3", "STR":18,"DEX":21,"VIT":23,"AGI":44,"INT":36,"MND":32,"CHR":47, "Accuracy":60,"Magic Accuracy":60,"Magic Attack":50,"Magic Burst Damage":0,"Magic Burst Damage II":0,"Magic Damage":30,"Jobs":["blm"]}
Archmage_Sabots = {"Name":"Archmage's Sabots +3", "STR":20,"DEX":21,"VIT":20,"AGI":43,"INT":30,"MND":29,"CHR":44, "Magic Accuracy":42,"Magic Attack":54, "Elemental Magic Skill":17, "Accuracy":36,"Gear Haste":3,"Jobs":["blm"]}
Spaekona_Sabots = {"Name":"Spaekona Sabots +3", "STR":20,"DEX":21,"VIT":20,"AGI":43,"INT":32,"MND":29,"CHR":44,"Magic Accuracy":54,"Magic Damage":40,"Magic Attack":26,"Gear Haste":3,"Jobs":["blm"]}
Thereoid_Greaves = {"Name":"Thereoid Greaves","STR":13,"DEX":28,"VIT":13,"AGI":38,"INT":1,"MND":13,"CHR":31,"Attack":25,"Ranged Attack":25,"Gear Haste":4,"Crit Rate":4,"Crit Damage":5,"Jobs":["war","rdm","pld","drk","bst","rng","sam","drg","blu","run"]}
Gleti_Boots = {"Name":"Gleti's Boots", "Name2":"Gleti's Boots R25","STR":28,"DEX":29,"VIT":26,"AGI":33,"MND":12,"CHR":26,"Accuracy":40+10,"Attack":40+25,"Magic Accuracy":40+10,"Gear Haste":3,"PDL":5,"Crit Rate":4,"Jobs":["thf","bst","drg","blu","dnc"]}
Jhakri_Pigaches = {"Name":"Jhakri Pigaches +2","STR":25,"DEX":28,"VIT":3,"AGI":26,"INT":33,"MND":21,"CHR":34,"Accuracy":42,"Attack":42,"Magic Accuracy":42,"Magic Attack":39,"Gear Haste":0,"Magic Burst Damage":7,"Jobs":["blm","rdm","blu","sch","geo"]}
Vitiation_Boots = {"Name":"Vitiation Boots +3","STR":18,"DEX":19,"VIT":18,"AGI":41,"INT":30,"MND":32,"CHR":42,"Accuracy":36,"Magic Accuracy":43,"Magic Attack":55,"Gear Haste":3, "Jobs":["rdm"]}
Lethargy_Houseaux = {"Name":"Lethargy Houseaux +3","STR":22,"DEX":30,"VIT":22,"AGI":43,"INT":30,"MND":32,"CHR":43,"Accuracy":60,"Attack":60,"Magic Accuracy":60,"Magic Attack":50,"Magic Damage":30,"Gear Haste":3,"Weaponskill Damage":12,"Jobs":["rdm"]}
Vishap_Greaves = {"Name":"Vishap Greaves +3","STR":30,"DEX":27,"VIT":25,"AGI":42,"MND":20,"CHR":36,"Accuracy":46,"Attack":30,"Gear Haste":3,"Jobs":["drg"]}
Pteroslaver_Greaves = {"Name":"Pteroslaver Greaves +3","STR":28,"DEX":27,"VIT":25,"AGI":42,"MND":20,"CHR":36,"Accuracy":42,"Attack":73,"Magic Accuracy":36,"Gear Haste":3,"Jobs":["drg"]}
Peltasts_Schynbalds = {"Name":"Peltast's Schynbalds +3","STR":31,"DEX":34,"VIT":31,"AGI":40,"MND":20,"CHR":34,"Accuracy":60,"Attack":70,"Magic Accuracy":60,"Gear Haste":6,"Jobs":["drg"]}
Ayanmo_Gambieras = {"Name":"Ayanmo Gambieras +2","STR":16,"DEX":37,"VIT":10,"AGI":46,"MND":22,"CHR":26,"Accuracy":42,"Magic Accuracy":42,"Gear Haste":3,"Crit Rate":+6,"Jobs":["whm","rdm","brd","blu","run"]}
Bunzi_Sabots = {"Name":"Bunzi's Sabots", "Name2":"Bunzi's Sabots R25","STR":12, "DEX":12, "VIT":12, "AGI":32, "INT":32, "MND":33, "CHR":44, "Accuracy":40+10, "Attack":40+25, "Magic Accuracy":40+10, "Magic Attack":30, "Magic Damage":30+25, "Gear Haste":3, "Magic Burst Damage":6, "Jobs":["whm","rdm", "brd", "smn"]}
Piety_Duckbills = {"Name":"Piety Duckbills +3", "Name2":"Piety Duckbills +3 R25","STR":20, "DEX":21, "VIT":20, "AGI":43, "INT":27, "MND":29, "CHR":44, "Accuracy":36, "Attack":61, "Gear Haste":3, "Jobs":["whm"]}
Arbatel_Loafers = {"Name":"Arbatel Loafers +3","STR":18, "DEX":21, "VIT":23, "AGI":44, "INT":34, "MND":32, "CHR":47, "Accuracy":60, "Magic Accuracy":60, "Magic Attack":50, "Magic Damage":30, "Elemental Magic Skill":33, "Gear Haste":3, "Magic Burst Damage II":5, "Jobs":["sch"]}
Pummeler_Calligae = {"Name":"Pummeler's Calligae +3","STR":24, "DEX":26, "VIT":31, "AGI":43, "INT":0, "MND":21, "CHR":38, "Accuracy":46, "Attack":40, "Gear Haste":4, "DA":9, "Store TP":4, "Jobs":["war"]}
Agoge_Calligae = {"Name":"Agoge Calligae +3","STR":27, "DEX":29, "VIT":28, "AGI":43, "INT":0, "MND":21, "CHR":38, "Accuracy":43, "Attack":61, "Magic Accuracy":36, "Gear Haste":4, "Jobs":["war"]}
Boii_Calligae = {"Name":"Boii Calligae +3","STR":31, "DEX":34, "VIT":31, "AGI":40, "INT":0, "MND":20, "CHR":34, "Accuracy":60, "Attack":60, "Magic Accuracy":60, "Gear Haste":6, "Crit Damage":13, "Jobs":["war"]}
Wakido_SuneAte = {"Name":"Wakido Sune-Ate +3","STR":25, "DEX":27, "VIT":25, "AGI":42, "INT":0, "MND":20, "CHR":36, "Accuracy":56, "Attack":38, "Ranged Accuracy":40, "Ranged Attack":38, "Gear Haste":3, "Zanshin":5, "Hasso":2, "Jobs":["sam"]}
Sakonji_SuneAte = {"Name":"Sakonji Sune-Ate +3","STR":31, "DEX":27, "VIT":25, "AGI":42, "INT":0, "MND":20, "CHR":36, "Accuracy":36, "Attack":84, "Magic Accuracy":36, "Gear Haste":3, "Store TP":10, "Jobs":["sam"]}
Kasuga_SuneAte = {"Name":"Kasuga Sune-Ate +3","STR":31, "DEX":34, "VIT":31, "AGI":40, "INT":0, "MND":20, "CHR":34, "Accuracy":60, "Attack":70, "Magic Accuracy":60, "Gear Haste":3, "PDL":10, "Jobs":["sam"]}
Laksamana_Bottes = {"Name":"Laksamana's Bottes +3","STR":22, "DEX":34, "VIT":20, "AGI":49, "INT":0, "MND":22, "CHR":40, "Ranged Accuracy":33, "Magic Accuracy":52, "Gear Haste":4, "Quick Draw":20, "Jobs":["cor"]}
Lanun_Bottes = {"Name":"Lanun Bottes +3","STR":22, "DEX":34, "VIT":20, "AGI":49, "INT":19, "MND":22, "CHR":40, "Accuracy":43, "Ranged Attack":61, "Magic Accuracy":36, "Magic Attack":55, "Gear Haste":4, "Weaponskill Damage":10, "Jobs":["cor"]}
Chasseur_Bottes = {"Name":"Chasseur's Bottes +3","STR":29, "DEX":38, "VIT":19, "AGI":56, "INT":0, "MND":26, "CHR":38, "Accuracy":60, "Ranged Accuracy":60, "Ranged Attack":60, "Magic Accuracy":60, "Magic Attack":50, "Gear Haste":4, "Quick Draw II":31, "Jobs":["cor"]} # Quick Draw II boosts other elemental damage. Quick Draw boosts its own damage
Fili_Cothurnes = {"Name":"Fili Cothurnes +3","STR":17, "DEX":26, "VIT":17, "AGI":44, "INT":29, "MND":35, "CHR":53, "Accuracy":60, "Magic Accuracy":60, "Gear Haste":3, "Jobs":["brd"]}
Bihu_Slippers = {"Name":"Bihu Slippers +3","STR":17, "DEX":21, "VIT":17, "AGI":43, "INT":27, "MND":27, "CHR":48, "Accuracy":36, "Attack":61, "Magic Accuracy":36, "Gear Haste":3, "Jobs":["brd"]}
Brioso_Slippers = {"Name":"Brioso Slippers +3","STR":17, "DEX":21, "VIT":17, "AGI":43, "INT":27, "MND":27, "CHR":48, "Magic Accuracy":46, "Gear Haste":3, "Jobs":["brd"]}
Ikenga_Clogs = {"Name":"Ikenga's Clogs","STR":21, "DEX":33, "VIT":14, "AGI":52, "INT":0, "MND":16, "CHR":32, "Ranged Accuracy":40+10, "Ranged Attack":40+25, "Magic Accuracy":40+10, "Store TP":7, "PDL":3, "True Shot":9,"Jobs":["rng","cor"]}
Meghanada_Jambeaux = {"Name":"Meghanada Jambeaux +2","STR":23, "DEX":34, "VIT":8, "AGI":54, "INT":0, "MND":19, "CHR":34, "Accuracy":46, "Attack":42, "Ranged Accuracy":46, "Ranged Attack":42, "Gear Haste":2, "Jobs":["thf","rng","bst","cor","dnc","run"]}
Oshosi_Leggings = {"Name":"Oshosi Leggings +1","STR":26, "DEX":24, "VIT":15, "AGI":56, "INT":0, "MND":11, "CHR":34, "Ranged Accuracy":43, "Magic Accuracy":48, "Double Shot":4, "Triple Shot":3, "Crit Rate":10, "Jobs":["cor","rng"]}
feet = [Oshosi_Leggings,Meghanada_Jambeaux,Ikenga_Clogs,Fili_Cothurnes,Bihu_Slippers,Brioso_Slippers,Chasseur_Bottes,Lanun_Bottes,Laksamana_Bottes,Kasuga_SuneAte,Sakonji_SuneAte,Wakido_SuneAte,Boii_Calligae,Agoge_Calligae,Pummeler_Calligae,Arbatel_Loafers,Piety_Duckbills,Bunzi_Sabots,Ayanmo_Gambieras,Peltasts_Schynbalds,Pteroslaver_Greaves,Vishap_Greaves,Vitiation_Boots,Lethargy_Houseaux,Jhakri_Pigaches,Gleti_Boots,Thereoid_Greaves,Adhemar_Gamashes_A,Adhemar_Gamashes_B,Flamma_Gambieras,Hachiya_Kyahan,Herculean_Boots,Herculean_Boots_QA,Hizamaru_Sune_Ate,Kendatsuba_Sune_Ate,Malignance_Boots,Mochizuki_Kyahan,Mpaca_Boots,Mummu_Gamashes,Nyame_Sollerets,Rao_SuneAte_D,Ratri_Sollerets,Ryuo_SuneAte_D,Sakpata_Leggings,Sulevia_Leggings,Tatenashi_SuneAte,Hattori_Kyahan,Heathen_Sollerets,Amalric_Nails,Ea_Pigaches,Agwu_Pigaches,Wicce_Sabots,Archmage_Sabots,Spaekona_Sabots,]

# Confirm that the stats for each piece of gear being checked are spelled correctly.
# Compare each stat against a pre-made list of accepted stats.
available_stats = ["Double Shot", "True Shot","Zanshin", "Hasso", "Quick Draw", "Quick Draw II", "Triple Shot","Magic Crit Rate II","Magic Burst Accuracy","Fencer","JA Haste","Accuracy", "AGI", "Attack", "Axe Skill", "CHR", "Club Skill", "Crit Damage", "Crit Rate", "DA", "DA DMG", "Dagger Skill", "Daken", "Dark Affinity", "Dark Elemental Bonus", "Delay", "DEX", "DMG", "Dual Wield", "Earth Affinity", "Earth Elemental Bonus", "Elemental Bonus", "Elemental Magic Skill", "Fire Affinity", "Fire Elemental Bonus", "ftp", "Gear Haste", "Great Axe Skill", "Great Katana Skill", "Great Sword Skill", "Hand-to-Hand Skill", "Ice Affinity", "Ice Elemental Bonus", "INT", "Jobs", "Katana Skill", "Light Affinity", "Light Elemental Bonus", "Magic Accuracy Skill", "Magic Accuracy", "Magic Attack", "Magic Burst Damage II", "Magic Burst Damage", "Magic Damage", "MND", "Name", "Name2", "Ninjutsu Damage", "Ninjutsu Magic Attack", "Ninjutsu Skill", "OA2", "OA3", "OA4", "OA5", "OA6", "OA7", "OA8", "PDL", "Polearm Skill", "QA", "Ranged Accuracy", "Ranged Attack", "Scythe Skill", "Skill Type", "Skillchain Bonus", "Staff Skill", "Store TP", "STR", "Sword Skill", "TA", "TA DMG", "Throwing Skill", "Thunder Affinity", "Thunder Elemental Bonus", "TP Bonus", "Type", "Utu CHR", "VIT", "Water Affinity", "Water Elemental Bonus", "Weaponskill Accuracy", "Weaponskill Damage", "Weather", "Wind Affinity", "Wind Elemental Bonus","Polearm Skill","Marksmanship Skill","Archery Skill"]

typo = False
slots = [mains, subs, grips, ranged, ammos, heads, necks, ears, ears2, bodies, hands, rings, rings2, capes, waists, legs, feet]
for slot in slots:
  for gear in slot:
    keys = gear.keys()
    for key in keys:
      if key not in available_stats:
        print(f"Incorrect stat name found on \"{gear.get('Name2',gear['Name'])}\":  \"{key}\"")
        typo = True
    if not gear.get("Jobs",False):
        print(f"Missing the Jobs key-value pair: {gear['Name']}")

    # May as well add the "Name2" value to all items that do not have it. This is huge for cleaning up the main code
    # While they do not have a typed-out "Name2", as long as another code uses this code, then each piece of gear will have "Name2" available now.
    # I'll clean up the main code later.
    name2 = gear.get('Name2','None')
    if name2 == 'None':
        gear.update({'Name2': gear['Name']})

# Make sure each weapon, ammo, grip, shield, and ranged weapon has a "Type" and "Skill Type" key.
for k in mains+subs+grips+ranged:
    if not k.get("Skill Type", False):
        print(f"Add a \"Skill Type\" key to {k['Name2']}!  Typically: (Club, Dagger, Sword, Katana, . . . and None)\nOr make sure you put the item in the correct list. (arrows/bullets go in the \"ammos\" list)")

for k in mains+subs+grips+ranged+ammos:
    if k["Name"]=="Empty":
        continue
    if k.get("Type", "None") not in ["Weapon", "Grip", "Shield", "Gun", "Bow", "Shuriken", "Bullet", "Arrow", "Equipment", "Instrument"]:
        print(f"Add a \"Type\" key to {k['Name2']}!  The only options are: (Weapon, Grip, Shield, Gun, Bow, Shuriken, Bullet, Arrow, Equipment).")

if typo:
  print("Check the \"available_stats\" list at the end of the gear.py file for a list of accepted stat names.")
  import sys ; sys.exit()
