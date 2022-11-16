#
# Created by Kastra on Asura.
# Feel free to /tell in game or send a PM on FFXIAH you have questions, comments, or suggestions.
#
# Version date: 2022 January 22
#
# This code contains the function used to estimate the average number of attacks per attack round given multi-attack stats and accuracy.
#
from numba import njit
import numpy as np
import random

@njit
def get_ma_rate(nhits, qa, ta, da, oa3, oa2, sub_type, hitrate_matrix):
    #
    # Estimate the number of attacks per weapon through simulation.
    # You can use things like:
    #     ta_rate = (1-qa)*ta
    #     da_rate = (1-qa)*(1-ta)*da
    #     oa3_rate = (1-qa)*(1-ta)*(1-da)*oa3
    #   but you'd need an increasingly-complicated correction term in each formula to deal with the 8-hit maximum preventing some of the hits from taking place
    # It's easier for me to just run 50,000 simulations to estimate the true values than sit down and calculate the correction term by hand and then type it out here
    #
    dual_wield = True if sub_type == 'Weapon' else False # Check if the item equipped in the sub slot is a weapon. If this line returns an error, check the "gear.py" file to see if the item in the sub slot has a "Type" key. Python is case-sensitive too

    n_sim = 50000
    main_hits_list = np.zeros(n_sim) # List containing number of main hits per simulation. Will take average of this later
    sub_hits_list = np.zeros(n_sim) # List containing number of sub hits per simuation. Will take average of this later
    for k in range(n_sim):
        main_hits = 0
        sub_hits = 0
        total_hits = 0

        for l in range(nhits):

            if l==0:
                first = 1
            else:
                first = 0


            hitrate1 = hitrate_matrix[first][0] # Main hand hit rate. Caps at 99%
            hitrate2 = hitrate_matrix[first][1] # Off hand hit rate. Caps at 95%

            if total_hits >= 8:
                continue
            main_hits += 1*hitrate1
            total_hits += 1
            if l == 0 or (l == 1 and not dual_wield): # Main hit gets two multi-attack proc checks if not dual wielding
                if random.uniform(0,1) < qa:
                    for m in range(3):
                        if total_hits >= 8:
                            continue
                        main_hits += 1*hitrate1
                        total_hits += 1
                elif random.uniform(0,1) < ta:
                    for m in range(2):
                        if total_hits >= 8:
                            continue
                        main_hits += 1*hitrate1
                        total_hits += 1
                elif random.uniform(0,1) < da:
                    for m in range(1):
                        if total_hits >= 8:
                            continue
                        main_hits += 1*hitrate1
                        total_hits += 1
                elif random.uniform(0,1) < oa3:
                    for m in range(2):
                        if total_hits >= 8:
                            continue
                        main_hits += 1*hitrate1
                        total_hits += 1
                elif random.uniform(0,1) < oa2:
                    for m in range(1):
                        if total_hits >= 8:
                            continue
                        main_hits += 1*hitrate1
                        total_hits += 1

            if l == 0: # Check sub hit after the first main hit
                if dual_wield:
                    sub_hits += 1*hitrate2
                    total_hits += 1
                    if random.uniform(0,1) < qa:
                        for m in range(3):
                            if total_hits >= 8:
                                continue
                            sub_hits += 1*hitrate2
                            total_hits += 1
                    elif random.uniform(0,1) < ta:
                        for m in range(2):
                            if total_hits >= 8:
                                continue
                            sub_hits += 1*hitrate2
                            total_hits += 1
                    elif random.uniform(0,1) < da:
                        for m in range(1):
                            if total_hits >= 8:
                                continue
                            sub_hits += 1*hitrate2
                            total_hits += 1

        main_hits_list[k] = main_hits
        sub_hits_list[k] = sub_hits

    main_hits = np.mean(main_hits_list)
    sub_hits = np.mean(sub_hits_list)

    return(main_hits, sub_hits)
