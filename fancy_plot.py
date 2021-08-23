#
# Created by Kastra on Asura.
# Feel free to /tell in game or send a PM on FFXIAH you have questions, comments, or suggestions.
#
# Version date: 2021 August 22
#
# This code takes in a gear set and a list of damage values from N simulations to output a fancy plot showing the distribution and basic player stats.
#
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import matplotlib.image as mpimg
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

from init import *

# Create a fancy plot of a weapon skill distribution.

def get_images(gearset):
    import re
    gear = gearset.equipped
    gear_list = []
    for k in gear:
        if gear[k] != 'Empty':
            gear_list.append(gear[k])
    ids = np.empty(15,dtype='<U128') # Matrix containing item IDs for each equipped item for plotting. Hard-coded to ignore ranged slot.
    with open(items_file, encoding='utf-8') as ifile:
        for k in range(3):
            ifile.readline()
        a = ifile.readlines()
        for k in a: # Hard-coded to skip lines that threw errors at me while I tested the code.
            if "category=\"General" in k or "category=\"Maze" in k or "ring:" in k:
                continue
            if "category=\"Gil" in k:
                break
            k = " ".join(k.replace("=",":").split()[2:])[1:-2].replace("\"","") # Overly-complicated method to deal with the formatting in the "items_file" and obtain each item's ID
            res = np.array(re.split(',|:', k)).reshape(-1,2)
            for i,item_name in enumerate(gear_list):
                if item_name.lower() == res[3][1].lower() or item_name.lower() == res[1][1].lower():
                    ids[i] = res[0][1] # Matrix containing item IDs for each equipped item for plotting.

    return(ids)

def plot_final(damage, gearset, attack_cap, shortname, output_file_suffix, tp1, tp2, WS_name):

    rc('font',**{'family':['Courier New']})
    rc('text', usetex=False)

    sub_type = gearset.gear['sub'].get('Type', 'None') # Check if the item equipped in the sub slot is a weapon or a grip or nothing. If the item doesn't have a "Type" Key then return "None", meaning nothing is equipped.
    dual_wield = sub_type == 'Weapon'


    # https://jakevdp.github.io/PythonDataScienceHandbook/04.08-multiple-subplots.html
    fig = plt.figure(figsize=(10,5))
    ax   = fig.add_axes([0.175, 0.1, 0.8, 0.75])

    # 16 subplots, one for each equipment slot.
    ax1  = fig.add_axes([-0.1+0.11,        0.76,        0.15/4, 0.3/4],xticklabels=[],xticks=[],yticks=[],yticklabels=[])
    ax2  = fig.add_axes([-0.1+0.11+1*0.04, 0.76,        0.15/4, 0.3/4],xticklabels=[],xticks=[],yticks=[],yticklabels=[])
    ax3  = fig.add_axes([-0.1+0.11+2*0.04, 0.76,        0.15/4, 0.3/4],xticklabels=[],xticks=[],yticks=[],yticklabels=[])
    ax4  = fig.add_axes([-0.1+0.11+3*0.04, 0.76,        0.15/4, 0.3/4],xticklabels=[],xticks=[],yticks=[],yticklabels=[])
    ax5  = fig.add_axes([-0.1+0.11,        0.76-0.08,   0.15/4, 0.3/4],xticklabels=[],xticks=[],yticks=[],yticklabels=[])
    ax6  = fig.add_axes([-0.1+0.11+1*0.04, 0.76-0.08,   0.15/4, 0.3/4],xticklabels=[],xticks=[],yticks=[],yticklabels=[])
    ax7  = fig.add_axes([-0.1+0.11+2*0.04, 0.76-0.08,   0.15/4, 0.3/4],xticklabels=[],xticks=[],yticks=[],yticklabels=[])
    ax8  = fig.add_axes([-0.1+0.11+3*0.04, 0.76-0.08,   0.15/4, 0.3/4],xticklabels=[],xticks=[],yticks=[],yticklabels=[])
    ax9  = fig.add_axes([-0.1+0.11,        0.76-2*0.08, 0.15/4, 0.3/4],xticklabels=[],xticks=[],yticks=[],yticklabels=[])
    ax10 = fig.add_axes([-0.1+0.11+1*0.04, 0.76-2*0.08, 0.15/4, 0.3/4],xticklabels=[],xticks=[],yticks=[],yticklabels=[])
    ax11 = fig.add_axes([-0.1+0.11+2*0.04, 0.76-2*0.08, 0.15/4, 0.3/4],xticklabels=[],xticks=[],yticks=[],yticklabels=[])
    ax12 = fig.add_axes([-0.1+0.11+3*0.04, 0.76-2*0.08, 0.15/4, 0.3/4],xticklabels=[],xticks=[],yticks=[],yticklabels=[])
    ax13 = fig.add_axes([-0.1+0.11,        0.76-3*0.08, 0.15/4, 0.3/4],xticklabels=[],xticks=[],yticks=[],yticklabels=[])
    ax14 = fig.add_axes([-0.1+0.11+1*0.04, 0.76-3*0.08, 0.15/4, 0.3/4],xticklabels=[],xticks=[],yticks=[],yticklabels=[])
    ax15 = fig.add_axes([-0.1+0.11+2*0.04, 0.76-3*0.08, 0.15/4, 0.3/4],xticklabels=[],xticks=[],yticks=[],yticklabels=[])
    ax16 = fig.add_axes([-0.1+0.11+3*0.04, 0.76-3*0.08, 0.15/4, 0.3/4],xticklabels=[],xticks=[],yticks=[],yticklabels=[])
    gear_ax = [ax1, ax2, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, ax12, ax13, ax14, ax15, ax16]

    # Obtain player stats to be printed on the plot under the gear set.
    player_str = gearset.playerstats['STR']
    player_dex = gearset.playerstats['DEX']
    player_vit = gearset.playerstats['VIT']
    player_agi = gearset.playerstats['AGI']
    player_int = gearset.playerstats['INT']
    player_mnd = gearset.playerstats['MND']
    player_chr = gearset.playerstats['CHR']

    player_attack1 = gearset.playerstats['Attack1'] if not attack_cap else 99999
    player_attack2 = gearset.playerstats['Attack2'] if not attack_cap else 99999
    player_attack2 = 0 if not dual_wield else player_attack2
    player_accuracy1 = gearset.playerstats['Accuracy1']
    player_accuracy2 = gearset.playerstats['Accuracy2'] if dual_wield else 0

    anno = f"{'STR = ':>12s}{player_str:>4.0f}\n{'DEX = ':>12s}{player_dex:>4.0f}\n{'VIT = ':>12s}{player_vit:>4.0f}\n{'AGI = ':>12s}{player_agi:>4.0f}\n{'INT = ':>12s}{player_int:>4.0f}\n{'MND = ':>12s}{player_mnd:>4.0f}\n{'CHR = ':>12s}{player_chr:>4.0f}\n{'Attack1 = ':>12s}{player_attack1:>4.0f}\n{'Attack2 = ':>12s}{player_attack2:>4.0f}\n{'Accuracy1 = ':>12s}{player_accuracy1:>4.0f}\n{'Accuracy2 = ':>12s}{player_accuracy2:>4.0f}"

    bbox = dict(boxstyle="round", fc="1.0",)
    ax.annotate(anno, xycoords="figure fraction", xy=(0.015,0.15), bbox=bbox, fontsize=11) # Print the stats in a specific format

    ids = get_images(gearset)
    gear_list = [gearset.gear[k] for k in gearset.gear]
    for i,id in enumerate(ids):
        try:
            img = mpimg.imread(f"{icons_path}32/{id}.png") # Try to obtain the 32x32 pixel image if it exists. BG-wiki usually has the 32x32 versions you can download.
        except:
            img = mpimg.imread(f"{icons_path}{id}.bmp") # Use the .bmp version if the 32x32 image does not exist. If this fails then just download the 32x32 from BG-wiki and rerun the code.

        gear_ax[i].imshow(img)

    ax.hist(damage,bins=100,histtype='stepfilled',density=True,color='grey',alpha=0.25) # Filled-in distribution, grey
    ax.hist(damage,bins=100,histtype='step',density=True,color='black',alpha=1.0) # Solid black outline for the filled grey distribution.
    ax.axvline(x=np.average(damage),ymin=0,ymax=1,color='black',linestyle='--',label=f'Average = {int(np.average(damage))} damage.') # Vertical line at the average damage value.
    ax.set_xlabel('Damage')
    # ax.set_xlim([0,100000]) # Only plot damage between 0 and 100,000
    ax.tick_params(
        axis='y',
        which='both',
        bottom=True,
        top=False,
        left=False,
        labelleft=False,
        labelbottom=True)
    ax.set_title(f"{shortname}{output_file_suffix}_{tp1}_{tp2}.png\n{f'TP=[{tp1},{tp2}]':>15s} {'Minimum':>8s} {'Mean':>8s} {'Median':>8s} {'Maximum':>8s}\n{WS_name:>15s} {np.min(damage):>8} {int(np.average(damage)):>8} {int(np.median(damage)):>8} {np.max(damage):>8}",loc="left")
    # plt.legend()

    if save_img:
        plt.savefig(f'{savepath}{shortname}{output_file_suffix}_{tp1}_{tp2}.png') # Save the image using the predetermined filename. Currently results in something like "BladeShun_GrapeDaifuku_Dia2_1500_1800.png"
    else:
        try:
            plt.show()
        except:
            print("Unable to display output image. Command failed: \'plt.show()\'.")
            import sys ; sys.exit()

    if savetext:
        with open(f'{savepath}{shortname}{output_file_suffix}_{tp1}_{tp2}.txt', 'a') as ofile:
            ofile.write(f'\nWS TP Range: [{tp1},{tp2}]\n')
            ofile.write('WeaponSkill       Minimum    Average     Median    Maximum\n')
            ofile.write('_______________   _______    _______    _______    _______\n')
            ofile.write(f'{WS_name:<15s}  {np.min(damage):>8}   {int(np.average(damage)):>8}   {int(np.median(damage)):>8}   {np.max(damage):>8}\n')
        print('WeaponSkill       Minimum    Average     Median    Maximum')
        print(f'{WS_name:<15s}  {np.min(damage):>8}   {int(np.average(damage)):>8}   {int(np.median(damage)):>8}   {np.max(damage):>8}')
