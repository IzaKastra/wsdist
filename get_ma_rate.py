#
# Created by Kastra on Asura.
# Feel free to /tell in game or send a PM on FFXIAH you have questions, comments, or suggestions.
#
# Version date: 2022 December 15
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

@njit
def get_ma_rate2(nhits, qa, ta, da, oa3, oa2, sub_type, hitrate_matrix):
    #
    # Simulation-based function to determine number of hits per weapon.
    # Updated to perform attacks in the correct order.
    # This is not used in the main code, but only used as a sanity check against the results from my probability average.
    #

    dual_wield = True if sub_type == 'Weapon' else False # Check if the item equipped in the sub slot is a weapon. If this line returns an error, check the "gear.py" file to see if the item in the sub slot has a "Type" key. Python is case-sensitive too


    hitrate11 = hitrate_matrix[0][0] # Main hand hit rate with the bonus +100 accuracy. Caps at 99%
    hitrate21 = hitrate_matrix[0][1] # Off hand hit rate with the bonus +100 accuracy. Caps at 95%

    hitrate12 = hitrate_matrix[1][0] # Main hand hit rate. Caps at 99%
    hitrate22 = hitrate_matrix[1][1] # Off hand hit rate. Caps at 95%

    n_sim = 1000000
    main_hits_list = np.zeros(n_sim) # List containing number of main hits per simulation. Will take average of this later
    sub_hits_list = np.zeros(n_sim) # List containing number of sub hits per simuation. Will take average of this later
    for k in range(n_sim):
        main_hits = 0
        sub_hits = 0
        total_hits = 0

        main_hits += 1*hitrate11
        total_hits += 1

        sub_hits += 1*hitrate21 if dual_wield else 0
        total_hits +=1 if dual_wield else 0
        
        for l in range(nhits-1):

            if main_hits + sub_hits >= 8:
                continue

            main_hits += 1*hitrate12
            total_hits += 1

        # Add main MA
        if random.uniform(0,1) < qa:
            for m in range(3):
                if total_hits >= 8:
                    continue
                main_hits += 1*hitrate12
                total_hits += 1
        elif random.uniform(0,1) < ta:
            for m in range(2):
                if total_hits >= 8:
                    continue
                main_hits += 1*hitrate12
                total_hits += 1
        elif random.uniform(0,1) < da:
            for m in range(1):
                if total_hits >= 8:
                    continue
                main_hits += 1*hitrate12
                total_hits += 1
        elif random.uniform(0,1) < oa3:
            for m in range(2):
                if total_hits >= 8:
                    continue
                main_hits += 1*hitrate12
                total_hits += 1
        elif random.uniform(0,1) < oa2:
            for m in range(1):
                if total_hits >= 8:
                    continue
                main_hits += 1*hitrate12
                total_hits += 1

        # Add second MA
        if random.uniform(0,1) < qa:
            for m in range(3):
                if total_hits >= 8:
                    continue
                if dual_wield:
                    sub_hits += 1*hitrate22
                elif nhits > 1:
                    main_hits += 1*hitrate12
                total_hits += 1
        elif random.uniform(0,1) < ta:
            for m in range(2):
                if total_hits >= 8:
                    continue
                if dual_wield:
                    sub_hits += 1*hitrate22
                elif nhits > 1:
                    main_hits += 1*hitrate12
                total_hits += 1
        elif random.uniform(0,1) < da:
            for m in range(1):
                if total_hits >= 8:
                    continue
                if dual_wield:
                    sub_hits += 1*hitrate22
                elif nhits > 1:
                    main_hits += 1*hitrate12
                total_hits += 1
        elif random.uniform(0,1) < oa3:
            for m in range(2):
                if total_hits >= 8:
                    continue
                if dual_wield:
                    sub_hits += 1*hitrate22
                elif nhits > 1:
                    main_hits += 1*hitrate12
                total_hits += 1
        elif random.uniform(0,1) < oa2:
            for m in range(1):
                if total_hits >= 8:
                    continue
                if dual_wield:
                    sub_hits += 1*hitrate22
                elif nhits > 1:
                    main_hits += 1*hitrate12
                total_hits += 1

        main_hits_list[k] = main_hits
        sub_hits_list[k] = sub_hits

    main_hits = np.mean(main_hits_list)
    sub_hits = np.mean(sub_hits_list)

    # import matplotlib.pyplot as plt
    # plt.hist(main_hits_list,bins='scott')
    # plt.hist(sub_hits_list,bins='scott')
    # plt.show()

    return(main_hits, sub_hits)

# @njit
# def get_ma_rate3(nhits, qa, ta, da, oa3, oa2, dual_wield_type, hitrate_matrix):
#     dual_wield = True if dual_wield_type == 'Weapon' else False # Check if the item equipped in the dual_wield slot is a weapon. If this line returns an error, check the "gear.py" file to see if the item in the dual_wield slot has a "Type" key. Python is case-sensitive too

#     main_hits = 0
#     sub_hits = 0

#     hitrate11 = hitrate_matrix[0][0] # Main hand hit rate with the bonus +100 accuracy. Caps at 99%
#     hitrate21 = hitrate_matrix[0][1] # Off hand hit rate with the bonus +100 accuracy. Caps at 95%

#     hitrate12 = hitrate_matrix[1][0] # Main hand hit rate. Caps at 99%
#     hitrate22 = hitrate_matrix[1][1] # Off hand hit rate. Caps at 95%


#     main_hits += 1*hitrate11 # Add the first main hit (gets bonus accuracy)
#     main_hits += (nhits-1)*(hitrate12) # Add the remaining natural main hits

#     if dual_wield and main_hits+sub_hits < 8:
#         sub_hits += 1*hitrate21 # Add the first sub hit (gets bonus accuracy)

#     # Add main-hand multi-hits to the first natural hit.
#     main_hits += (max(0,min(3, 8-(main_hits + sub_hits))*qa) + \
#                   max(0,min(2, 8-(main_hits + sub_hits))*(1-qa)*ta) + \
#                   max(0,min(1, 8-(main_hits + sub_hits))*(1-qa)*(1-ta)*da) + \
#                   max(0,min(2, 8-(main_hits + sub_hits))*(1-qa)*(1-ta)*(1-da)*oa3) + \
#                   max(0,min(1, 8-(main_hits + sub_hits))*(1-qa)*(1-ta)*(1-da)*(1-oa3)*oa2))*hitrate12

#     if dual_wield:
#         # Add off-hand multi-hits to the first sub hit.
#         sub_hits += (max(0,min(3, 8-(sub_hits + main_hits)))*qa + \
#                      max(0,min(2, 8-(sub_hits + main_hits)))*(1-qa)*ta + \
#                      max(0,min(1, 8-(sub_hits + main_hits)))*(1-qa)*(1-ta)*da + \
#                      max(0,min(2, 8-(sub_hits + main_hits)))*(1-qa)*(1-ta)*(1-da)*oa3 + \
#                      max(0,min(1, 8-(sub_hits + main_hits)))*(1-qa)*(1-ta)*(1-da)*(1-oa3)*oa2)*hitrate22
#     elif nhits>1:
#         # Add main-hand multi-hits to the second natural hit if not dual wield and if nhits>1
#         main_hits += (max(0,min(3, 8-(sub_hits + main_hits)))*qa + \
#                       max(0,min(2, 8-(sub_hits + main_hits)))*(1-qa)*ta + \
#                       max(0,min(1, 8-(sub_hits + main_hits)))*(1-qa)*(1-ta)*da + \
#                       max(0,min(2, 8-(sub_hits + main_hits)))*(1-qa)*(1-ta)*(1-da)*oa3 + \
#                       max(0,min(1, 8-(sub_hits + main_hits)))*(1-qa)*(1-ta)*(1-da)*(1-oa3)*oa2)*hitrate12

#     return(main_hits, sub_hits)

@njit
def get_ma_rate3(nhits, qa, ta, da, oa3, oa2, dual_wield_type, hitrate_matrix, striking_flourish=False, ternary_flourish=False):
    dual_wield = True if dual_wield_type == 'Weapon' else False # Check if the item equipped in the dual_wield slot is a weapon. If this line returns an error, check the "gear.py" file to see if the item in the dual_wield slot has a "Type" key. Python is case-sensitive too

    main_hits = 0
    sub_hits = 0

    hitrate11 = hitrate_matrix[0][0] # Main hand hit rate with the bonus +100 accuracy. Caps at 99%
    hitrate21 = hitrate_matrix[0][1] # Off hand hit rate with the bonus +100 accuracy. Caps at 95%

    hitrate12 = hitrate_matrix[1][0] # Main hand hit rate. Caps at 99%
    hitrate22 = hitrate_matrix[1][1] # Off hand hit rate. Caps at 95%


    main_hits += 1*hitrate11 # Add the first main hit (gets bonus accuracy)
    main_hits += (nhits-1)*(hitrate12) # Add the remaining natural main hits

    if dual_wield and main_hits+sub_hits < 8:
        sub_hits += 1*hitrate21 # Add the first sub hit (gets bonus accuracy)


    # Striking flourish seems to set QA=0, TA=0, and DA=1.0 for the first MA hit only
    if striking_flourish:
        qa_main = 0 
        ta_main = 0
        da_main = 1
    elif ternary_flourish:
        qa_main = 0 
        ta_main = 1
        da_main = 0
    else:
        qa_main = qa
        ta_main = ta
        da_main = da


    # Add main-hand multi-hits to the first natural hit.
    main_hits += (max(0,min(3, 8-(main_hits + sub_hits))*qa_main) + \
                  max(0,min(2, 8-(main_hits + sub_hits))*(1-qa_main)*ta_main) + \
                  max(0,min(1, 8-(main_hits + sub_hits))*(1-qa_main)*(1-ta_main)*da_main) + \
                  max(0,min(2, 8-(main_hits + sub_hits))*(1-qa_main)*(1-ta_main)*(1-da_main)*oa3) + \
                  max(0,min(1, 8-(main_hits + sub_hits))*(1-qa_main)*(1-ta_main)*(1-da_main)*(1-oa3)*oa2))*hitrate12

    if dual_wield:
        # Add off-hand multi-hits to the first sub hit.
        sub_hits += (max(0,min(3, 8-(sub_hits + main_hits)))*qa + \
                     max(0,min(2, 8-(sub_hits + main_hits)))*(1-qa)*ta + \
                     max(0,min(1, 8-(sub_hits + main_hits)))*(1-qa)*(1-ta)*da + \
                     max(0,min(2, 8-(sub_hits + main_hits)))*(1-qa)*(1-ta)*(1-da)*oa3 + \
                     max(0,min(1, 8-(sub_hits + main_hits)))*(1-qa)*(1-ta)*(1-da)*(1-oa3)*oa2)*hitrate22
    elif nhits>1:
        # Add main-hand multi-hits to the second natural hit if not dual wield and if nhits>1
        main_hits += (max(0,min(3, 8-(sub_hits + main_hits)))*qa + \
                      max(0,min(2, 8-(sub_hits + main_hits)))*(1-qa)*ta + \
                      max(0,min(1, 8-(sub_hits + main_hits)))*(1-qa)*(1-ta)*da + \
                      max(0,min(2, 8-(sub_hits + main_hits)))*(1-qa)*(1-ta)*(1-da)*oa3 + \
                      max(0,min(1, 8-(sub_hits + main_hits)))*(1-qa)*(1-ta)*(1-da)*(1-oa3)*oa2)*hitrate12

    return(main_hits, sub_hits)



if __name__ == "__main__":

    nhits = 5
    qa = 0.05
    ta = 0.21
    da = 0.12
    oa3 = 0
    oa2 = 0

    hitrate_matrix = [[0.99,0.95],
                      [0.99,0.95]]
    dual_wield_type = "Weapon"

    main_hits, sub_hits = get_ma_rate(nhits, qa, ta, da, oa3, oa2, dual_wield_type, hitrate_matrix)
    print(main_hits, sub_hits, main_hits+sub_hits)
    main_hits, sub_hits = get_ma_rate2(nhits, qa, ta, da, oa3, oa2, dual_wield_type, hitrate_matrix)
    print(main_hits, sub_hits, main_hits+sub_hits)
    main_hits, sub_hits = get_ma_rate3(nhits, qa, ta, da, oa3, oa2, dual_wield_type, hitrate_matrix)
    print(main_hits, sub_hits, main_hits+sub_hits)
