#
# Created by Kastra on Asura.
# Feel free to /tell in game or send a PM on FFXIAH you have questions, comments, or suggestions.
#
# Version date: 2022 December 03
#
# This file contains a list of buffs that may be provided to a gear set when simulating damage.
#
import numpy as np

# Simple list of buffs and their potencies.
# Currently incomplete and not necessarily in final form.

# Format is [Base, Bonus].
# For Example: GEO Acumen uses [15,3]. So with +6 geomancy, it would be Base+Bonus*6 = 15+3*6 Magic Attack with Acumen

cor = {"Chaos": {"Attack":[0.25, 32./1024]},
       "Samurai": {"Store TP":[32,4]},
       "Rogue": {"Crit Rate":[10,1]},
       "Fighter": {"DA":[10,1]},
       "Hunter": {"Accuracy":[40,5]},
       "Wizard": {"Magic Attack":[25,2]}}

brd_trust = {"Minuet": {"Attack": 32, "Ranged Attack": 32},
              "Minuet II": {"Attack": 64, "Ranged Attack": 64},
              "Minuet III": {"Attack": 96, "Ranged Attack": 96},
              "Minuet IV": {"Attack": 112, "Ranged Attack": 112},
              "Minuet V": {"Attack": 124, "Ranged Attack": 124},
              "Sword Madrigal": {"Accuracy": 45, "Ranged Accuracy": 45},
              "Blade Madrigal": {"Accuracy": 60, "Ranged Accuracy": 60},
              "Advancing March": {"Haste": 1+108./1024},
              "Victory March": {"Haste": 1+163./1024}}

brd = {"Minuet": {"Attack": [32+25, 3.2], "Ranged Attack": [32+25, 3.2]},
        "Minuet II": {"Attack": [64+25, 6.2], "Ranged Attack": [64+25, 6.2]},
        "Minuet III": {"Attack": [96+25, 9.5], "Ranged Attack": [96+25, 9.5]},
        "Minuet IV": {"Attack": [112+25, 11.2], "Ranged Attack": [112+25, 11.2]},
        "Minuet V": {"Attack": [124+25, 12.375], "Ranged Attack": [124+25, 12.375]},
        "Sword Madrigal": {"Accuracy": [45, 4.5]},
        "Blade Madrigal": {"Accuracy": [60, 6]},
        "Advancing March": {"Haste": [108./1024, 11.8/1024]},
        "Victory March": {"Haste": [163./1024, 16.25/1024]},
        "Honor March": {"Haste": [126./1024, 12./1024], "Attack": [168, 16], "Ranged Attack": [168, 16], "Accuracy": [42, 4], "Ranged Accuracy": [42, 4]}}

geo_trust = {"Acumen": {"Magic Attack": 21},
             "Focus": {"Magic Accuracy": 50},
             "Fury": {"Attack": 1.375, "Ranged Attack": 1.375},
             "Haste": {"Haste": 28.8},
             "Precision": {"Accuracy": 56, "Ranged Accuracy": 56}}

geo = {"Fury": {"Attack": [0.347,0.027], "Ranged Attack": [0.347,0.027]},
       "Acumen": {"Magic Attack": [15,3]},
       "Focus": {"Magic Accuracy":[50,5]},
       "Haste": {"Haste": [29.9/100, 1.1/100]},
       "Precision": {"Accuracy": [50,5], "Ranged Accuracy": [50,5]},
       "Frailty": {"Defense":[0.148,0.027]},
       "Torpor": {"Evasion":[50,5]},
       "Malaise": {"Magic Defense":[15,3]},
       "STR":{"STR":[25,2]},
       "DEX":{"DEX":[25,2]},
       "VIT":{"VIT":[25,2]},
       "AGI":{"AGI":[25,2]},
       "INT":{"INT":[25,2]},
       "MND":{"MND":[25,2]},
       "CHR":{"CHR":[25,2]}}

whm = {"Haste":{"Haste":150/1024},
       "Haste II":{"Haste":307/1024},
       "Boost-STR":{"STR":25},
       "Boost-DEX":{"DEX":25},
       "Boost-VIT":{"VIT":25},
       "Boost-AGI":{"AGI":25},
       "Boost-INT":{"INT":25},
       "Boost-MND":{"MND":25},
       "Boost-CHR":{"CHR":25}}
