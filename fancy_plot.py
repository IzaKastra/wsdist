#
# Created by Kastra on Asura.
# Feel free to /tell in game or send a PM on FFXIAH you have questions, comments, or suggestions.
#
# Version date: 2022 November 15
#
# This code takes in a gear set and a list of damage values from N simulations to output a fancy plot showing the distribution and basic player stats.
#
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import matplotlib.image as mpimg
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

# Create a fancy plot of a weapon skill distribution.

def get_image_ids(gearset):

    items_file = "item_list.txt"
    icons_path = "icons32/"

    item_ids, item_names = np.loadtxt(items_file, unpack=True, dtype=str, delimiter=';')
    item_ids = np.array(item_ids, dtype=int)
    item_names = np.array([k.lower() for k in item_names])

    gear = gearset.equipped
    gear_list = []
    for k in gear:
        gear_list.append(gear[k])

    ids = []
    for i,k in enumerate(gear_list):
        a = np.ravel(np.where(item_names == k.lower()))[-1]
        ids.append(item_ids[a])

    return(ids)

def plot_final(damage, gearset, tp1, tp2, WS_name):

    items_file = "item_list.txt"
    icons_path = "icons32/"

    output_file_suffix = ""
    shortname = "".join(WS_name.split())

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
    gear_ax = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, ax12, ax13, ax14, ax15, ax16]

    # Obtain player stats to be printed on the plot under the gear set.
    player_str = gearset.playerstats['STR']
    player_dex = gearset.playerstats['DEX']
    player_vit = gearset.playerstats['VIT']
    player_agi = gearset.playerstats['AGI']
    player_int = gearset.playerstats['INT']
    player_mnd = gearset.playerstats['MND']
    player_chr = gearset.playerstats['CHR']

    player_attack1 = gearset.playerstats['Attack1']
    player_attack2 = gearset.playerstats['Attack2']
    player_attack2 = 0 if not dual_wield else player_attack2
    player_accuracy1 = gearset.playerstats['Accuracy1']
    player_accuracy2 = gearset.playerstats['Accuracy2'] if dual_wield else 0

    anno = f"{'STR = ':>12s}{player_str:>4.0f}\n{'DEX = ':>12s}{player_dex:>4.0f}\n{'VIT = ':>12s}{player_vit:>4.0f}\n{'AGI = ':>12s}{player_agi:>4.0f}\n{'INT = ':>12s}{player_int:>4.0f}\n{'MND = ':>12s}{player_mnd:>4.0f}\n{'CHR = ':>12s}{player_chr:>4.0f}\n{'Attack1 = ':>12s}{player_attack1:>4.0f}\n{'Attack2 = ':>12s}{player_attack2:>4.0f}\n{'Accuracy1 = ':>12s}{player_accuracy1:>4.0f}\n{'Accuracy2 = ':>12s}{player_accuracy2:>4.0f}"

    bbox = dict(boxstyle="round", fc="1.0",)
    ax.annotate(anno, xycoords="figure fraction", xy=(0.015,0.15), bbox=bbox, fontsize=11) # Print the stats in a specific format

    ids = get_image_ids(gearset)
    # ids = [20977,21925,21391,25614,25491,27544,27545,26528,27118,28471,26175,26258,28440,25892,27496]
    gear_list = [gearset.gear[k] for k in gearset.gear]
    for i,id in enumerate(ids):
        id = int(id)
        try:
            img = mpimg.imread(f"{icons_path}{id}.png") # Try to obtain the 32x32 pixel image if it exists. BG wiki usually has the 32x32 versions you can download.
            gear_ax[i].imshow(img)
        except:
            item_ids, item_names = np.loadtxt(items_file, unpack=True, dtype=str, delimiter=';')
            item_ids = np.array(item_ids, dtype=int)
            item_names = np.array([k.lower() for k in item_names])
            a = np.where(item_ids == id)
            print(f"\nUnable to find image file: {icons_path}{id}.png ({item_names[a][0]})")
            print(f"Download the 32x32.png image icon for this item as {icons_path}{id}.png and try again.\n")

    ax.hist(damage,bins=200,histtype='stepfilled',density=True,color='grey',alpha=0.25) # Filled-in distribution, grey
    ax.hist(damage,bins=200,histtype='step',density=True,color='black',alpha=1.0) # Solid black outline for the filled grey distribution.
    ax.axvline(x=np.average(damage),ymin=0,ymax=1,color='black',linestyle='--',label=f'Average = {int(np.average(damage))} damage.') # Vertical line at the average damage value.
    ax.set_xlabel('Damage')

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

    savepath = "."
    # plt.savefig(f'{savepath}{shortname}{output_file_suffix}_{tp1}_{tp2}.png') # Save the image using the predetermined filename. Currently results in something like "BladeShun_GrapeDaifuku_Dia2_1500_1800.png"
    plt.show()
