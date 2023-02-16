#
# Created by Kastra on Asura.
# Feel free to /tell in game or send a PM on FFXIAH you have questions, comments, or suggestions.
#
# Version date: 2023 January 08
#
from get_dex_crit import *
import numpy as np

def check_weaponskill_bonus(ws_weapons, ws_name, gearset, tp, enemy_agi):
    #
    # Check main-hand weapon and weapon skill for synergy.
    # Example: Using Blade: Shun with an augmented Heishi will provide bonus damage.
    #

    bonuses = {'ws_bonus':0,  # Dictionary containing the possible bonuses for using specific weapons or weapon skills
               'oa3':0,
               'oa2':0,
               'crit_rate':0}

    main_wpn_name = ws_weapons[0]
    rng_wpn_name = ws_weapons[1]

    if main_wpn_name == 'Naegling':
        if ws_name == 'Savage Blade':
            bonuses['ws_bonus'] += 0.15
    elif main_wpn_name == 'Murgleis':
        bonuses['oa3'] += 0.2
        bonuses['oa2'] += 0.4
        if ws_name == 'Death Blossom':
            bonuses['ws_bonus'] += 0.495 # Hidden +30% Mythic WS damage * R15 +15% WS damage (1.3)*(1.15)
    elif main_wpn_name == 'Burtgang':
        bonuses['oa3'] += 0.2
        bonuses['oa2'] += 0.4
        if ws_name == 'Atonement':
            bonuses['ws_bonus'] += 0.3 # Hidden +30% Mythic WS damage
    elif main_wpn_name == "Tizona":
        bonuses['oa3'] += 0.2
        bonuses['oa2'] += 0.4
        if ws_name == "Expiacion":
            bonuses["ws_bonus"] += 0.495
    elif main_wpn_name == 'Almace':
        if ws_name == "Chant du Cygne":
            bonuses['ws_bonus'] += 0.1
    elif main_wpn_name == 'Excalibur':
        if ws_name == 'Knights of Round':
            bonuses['ws_bonus'] += 0.68 # Hidden 40% Relic WS damage * R15 +20% WS damage (1.4)*(1.2)
    elif main_wpn_name == "Sequence":
        if ws_name == 'Requiescat':
            bonuses['ws_bonus'] += 0.1
    elif main_wpn_name == 'Maxentius':
        if ws_name == 'Black Halo':
            bonuses['ws_bonus'] += 0.5
    elif main_wpn_name == 'Tishtrya':
        if ws_name == 'Realmrazer':
            bonuses['ws_bonus'] += 0.1
    elif main_wpn_name == 'Mjollnir':
        if ws_name == 'Randgrith':
            bonuses['ws_bonus'] += 0.68 # Hidden 40% Relic WS damage * R15 +20% WS damage (1.4)*(1.2)
    elif 'Yagrush' in main_wpn_name:
        bonuses['oa3'] += 0.2
        bonuses['oa2'] += 0.4
        if ws_name == 'Mystic Boon':
            bonuses['ws_bonus'] += 0.495 # Hidden +30% Mythic WS damage * R15 +15% WS damage (1.3)*(1.15)
    elif 'Idris' in main_wpn_name:
        bonuses['oa3'] += 0.2
        bonuses['oa2'] += 0.4
        if ws_name == 'Exudation':
            bonuses['ws_bonus'] += 0.15 # BG Wiki has no mention of a hidden +30% for this weapon+WS combo
    elif main_wpn_name == 'Epeolatry':
        bonuses['oa3'] += 0.2
        bonuses['oa2'] += 0.4
        if ws_name == 'Dimidiation':
            bonuses['ws_bonus'] += 0.15 # BG Wiki has no mention of a hidden +30% for this weapon+WS combo
    elif 'Kikoku' in main_wpn_name:
        if ws_name == 'Blade: Metsu':
            bonuses['ws_bonus'] += 0.68 # Hidden +40% Relic WS damage * R15 +20% WS damage (1.4)*(1.2)
    elif 'Kannagi' in main_wpn_name:
        if ws_name == 'Blade: Hi':
            bonuses['ws_bonus'] += 0.1
    elif 'Nagi' in main_wpn_name:
        bonuses['oa3'] += 0.2
        bonuses['oa2'] += 0.4
        if ws_name == 'Blade: Kamu':
            bonuses['ws_bonus'] += 0.495 # Hidden +30% Mythic WS damage * R15 +15% WS damage (1.3)*(1.15)
    elif 'Kenkonken' in main_wpn_name:
        bonuses['oa3'] += 0.2
        bonuses['oa2'] += 0.4
        if ws_name == 'Stringing Pummel':
            bonuses['ws_bonus'] += 0.495 # Hidden +30% Mythic WS damage * R15 +15% WS damage (1.3)*(1.15)
    elif 'Heishi' in main_wpn_name:
        if ws_name == 'Blade: Shun':
            bonuses['ws_bonus'] += 0.1
    elif main_wpn_name == 'Gokotai':
        if ws_name == 'Blade: Ku':
            bonuses['ws_bonus'] += 0.6
    elif main_wpn_name == 'Tauret':
        if ws_name == 'Evisceration':
            bonuses['ws_bonus'] += 0.5
    elif main_wpn_name == 'Aeneas':
        if ws_name == 'Exenterator':
            bonuses['ws_bonus'] += 0.1
    elif main_wpn_name == 'Mandau':
        if ws_name == 'Mercy Stroke':
            bonuses['ws_bonus'] += 0.68 # Hidden 40% Relic WS damage * R15 +20% WS damage (1.4)*(1.2)
    elif main_wpn_name == 'Karambit':
        if ws_name == "Asuran Fists":
            bonuses['ws_bonus'] += 0.5
    elif main_wpn_name == 'Dojikiri Yasutsuna':
        if ws_name == 'Tachi: Shoha':
            bonuses['ws_bonus'] += 0.1
    elif main_wpn_name == 'Kogarasumaru':
        bonuses['oa3'] += 0.2
        bonuses['oa2'] += 0.4
        if ws_name == 'Tachi: Rana':
            bonuses['ws_bonus'] += 0.495
    elif main_wpn_name == 'Masamune':
        if ws_name == 'Tachi: Fudo':
            bonuses['ws_bonus'] += 0.1
    elif main_wpn_name == 'Amanomurakumo':
        if ws_name == 'Tachi: Kaiten':
            bonuses['ws_bonus'] += 0.68
    elif main_wpn_name == 'Shining One':
        # # Shining One allows all weapon skills to crit. Seems pretty OP, but here we are...
        # # https://www.bg-wiki.com/ffxi/Shining_One
        # crit_rate = gearset.playerstats['Crit Rate']/100
        # crit_boost = [0.05, 0.10, 0.15]
        # crit_bonus = np.interp(tp, [1000,2000,3000], crit_boost)
        # crit_rate += crit_bonus
        # crit_rate += get_dex_crit(gearset.playerstats['DEX'], enemy_agi)
        # bonuses["crit_rate"] = crit_rate
        if ws_name == 'Impulse Drive':
            bonuses['ws_bonus'] += 0.4
    elif main_wpn_name == 'Gungnir':
        if ws_name == 'Geirskogul':
            bonuses['ws_bonus'] += 0.68 # Hidden 40% Relic WS damage * R15 +20% WS damage (1.4)*(1.2)
    elif main_wpn_name == "Rhongomiant":
        if ws_name == "Camlann's Torment":
            bonuses['ws_bonus'] += 0.1
    elif main_wpn_name == "Ryunohige":
        bonuses['oa3'] += 0.2
        bonuses['oa2'] += 0.4
        if ws_name == "Drakesbane":
            bonuses['ws_bonus'] += 0.495 # Hidden +30% Mythic WS damage * R15 +15% WS damage (1.3)*(1.15)
    elif main_wpn_name == "Trishula":
        if ws_name == "Stardiver":
            bonuses['ws_bonus'] += 0.1 # Hidden +30% Mythic WS damage * R15 +15% WS damage (1.3)*(1.15)
    elif main_wpn_name == 'Hachimonji':
        # Hachimonji does some weird stuff with store TP and multi-hits. I do not include such effects here.
        # https://www.bg-wiki.com/ffxi/Hachimonji
        if ws_name == 'Tachi: Kasha':
            bonuses['ws_bonus'] += 0.25
    elif main_wpn_name == "Apocalypse":
        if ws_name == "Catastrophe":
            bonuses["ws_bonus"] += 0.68
    elif main_wpn_name == "Liberator":
        bonuses['oa3'] += 0.2
        bonuses['oa2'] += 0.4
        if ws_name == "Insurgency":
            bonuses["ws_bonus"] += 0.495
    elif main_wpn_name == "Redemption":
        if ws_name == "Quietus":
            bonuses["ws_bonus"] += 0.1
    elif main_wpn_name == "Anguta":
        if ws_name == "Entropy":
            bonuses["ws_bonus"] += 0.1
    elif main_wpn_name == "Caladbolg":
        if ws_name == "Torcleaver":
            bonuses["ws_bonus"] += 0.1
    elif main_wpn_name == "Ragnarok":
        if ws_name == "Scourge":
            bonuses["ws_bonus"] += 0.68
    elif main_wpn_name == "Nandaka":
        if ws_name == "Ground Strike":
            bonuses["ws_bonus"] += 0.15
    elif main_wpn_name == "Lycurgos":
        if ws_name == "Steel Cyclone":
            bonuses["ws_bonus"] += 0.30
    elif main_wpn_name == "Conqueror":
        bonuses['oa3'] += 0.2
        bonuses['oa2'] += 0.4
        if ws_name == "King's Justice":
            bonuses["ws_bonus"] += 0.495
    elif main_wpn_name == "Ukonvasara":
        if ws_name == "Ukko's Fury":
            bonuses["ws_bonus"] += 0.1
    elif main_wpn_name == "Chango":
        if ws_name == "Upheaval":
            bonuses["ws_bonus"] += 0.1
    elif main_wpn_name == "Bravura":
        if ws_name == "Metatron Torment":
            bonuses["ws_bonus"] += 0.68
    elif main_wpn_name == "Dolichenus":
        if ws_name == "Decimation":
            bonuses["ws_bonus"] += 1.20
    elif main_wpn_name == "Guttler":
        if ws_name == "Onslaught":
            bonuses["ws_bonus"] += 0.68
    elif main_wpn_name == 'Aymur':
        bonuses['oa3'] += 0.2
        bonuses['oa2'] += 0.4
        if ws_name == 'Primal Rend':
            bonuses['ws_bonus'] += 0.495 # Hidden +30% Mythic WS damage * R15 +15% WS damage (1.3)*(1.15)
    elif main_wpn_name == 'Farsha':
        if ws_name == "Cloudsplitter":
            bonuses['ws_bonus'] += 0.1
    elif main_wpn_name == "Tri-edge":
        if ws_name == "Ruinator":
            bonuses["ws_bonus"] += 0.1
    elif main_wpn_name == "Lionheart":
        if ws_name == "Resolution":
            bonuses["ws_bonus"] += 0.1
    elif main_wpn_name == 'Twashtar':
        if ws_name == "Rudra's Storm":
            bonuses['ws_bonus'] += 0.1
    elif main_wpn_name == 'Carnwenhan':
        bonuses['oa3'] += 0.2
        bonuses['oa2'] += 0.4
        if ws_name == 'Mordant Rime':
            bonuses['ws_bonus'] += 0.495 # Hidden +30% Mythic WS damage * R15 +15% WS damage (1.3)*(1.15)
    elif main_wpn_name == 'Drepanum':
        if ws_name == 'Spiral Hell':
            bonuses['ws_bonus'] += 1.0
    elif main_wpn_name == 'Xoanon':
        if ws_name == 'Retribution':
            bonuses['ws_bonus'] += 0.2
    elif main_wpn_name == 'Khatvanga':
        if ws_name == 'Shattersoul':
            bonuses['ws_bonus'] += 0.1
    elif main_wpn_name == 'Vajra':
        bonuses['oa3'] += 0.2
        bonuses['oa2'] += 0.4
        if ws_name == 'Mandalic Stab':
            bonuses['ws_bonus'] += 0.495 # Hidden +30% Mythic WS damage * R15 +15% WS damage (1.3)*(1.15)
    elif main_wpn_name == 'Vajra':
        bonuses['oa3'] += 0.2
        bonuses['oa2'] += 0.4
        if ws_name == 'Pyrrhic Kleos':
            bonuses['ws_bonus'] += 0.495 # Hidden +30% Mythic WS damage * R15 +15% WS damage (1.3)*(1.15)
    elif main_wpn_name == "Glanzfaust":
        bonuses['oa3'] += 0.2
        bonuses['oa2'] += 0.4
        if ws_name == "Ascetic's Fury":
            bonuses["ws_bonus"] += 0.495
    elif main_wpn_name == "Verethragna":
        if ws_name == "Victory Smite":
            bonuses["ws_bonus"] += 0.1
    elif main_wpn_name == "Godhands":
        if ws_name == "Shijin Spiral":
            bonuses["ws_bonus"] += 0.1
    elif main_wpn_name == "Spharai":
        if ws_name == "Final Heaven":
            bonuses["ws_bonus"] += 0.68
    elif main_wpn_name == 'Tupsimati':
        bonuses['oa3'] += 0.2
        bonuses['oa2'] += 0.4
        if ws_name == 'Omniscience':
            bonuses['ws_bonus'] += 0.495 # Hidden +30% Mythic WS damage * R15 +15% WS damage (1.3)*(1.15)
    elif main_wpn_name == 'Laevateinn':
        bonuses['oa3'] += 0.2
        bonuses['oa2'] += 0.4
        if ws_name == 'Vidohunir':
            bonuses['ws_bonus'] += 0.495 # Hidden +30% Mythic WS damage * R15 +15% WS damage (1.3)*(1.15)


    # Do the same with ranged WSs now.
    if rng_wpn_name == "Yoichinoyumi":
        if ws_name == "Namas Arrow":
            bonuses["ws_bonus"] += 0.68
    elif rng_wpn_name == "Annihilator":
        if ws_name == "Coronach":
            bonuses["ws_bonus"] += 0.68
    elif rng_wpn_name == 'Gandiva':
        if ws_name == "Jishnu's Radiance":
            bonuses['ws_bonus'] += 0.1
    elif rng_wpn_name == 'Death Penalty':
        if ws_name == 'Leaden Salute':
            bonuses['ws_bonus'] += 0.495 # Hidden +30% Mythic WS damage * R15 +15% WS damage (1.3)*(1.15)
    elif rng_wpn_name == 'Armageddon':
        if ws_name == "Wildfire":
            bonuses['ws_bonus'] += 0.1
    elif rng_wpn_name == 'Gastraphetes':
        if ws_name == 'Trueflight':
            bonuses['ws_bonus'] += 0.495 # Hidden +30% Mythic WS damage * R15 +15% WS damage (1.3)*(1.15)
    elif rng_wpn_name == "Ullr":
        if ws_name == "Empyreal Arrow":
            bonuses["ws_bonus"] += 0.5
    elif rng_wpn_name == "Fomalhaut":
        if ws_name == "Last Stand":
            bonuses["ws_bonus"] += 0.1
    elif rng_wpn_name == "Fail-not":
        if ws_name == "Apex Arrow":
            bonuses["ws_bonus"] += 0.1


    return(bonuses)
