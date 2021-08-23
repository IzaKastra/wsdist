# wsdist
Python3-based weapon skill simulator for Final Fantasy XI.
Created by Kastra on Asura. First published 2021 August 23
Feel free to /tell me in game or message me on FFXIAH (https://www.ffxiah.com/player/Asura/Kastra) if you have any comments, questions, or suggestions.

The code is working as intended, but it currently only supports Ninja and Samurai main jobs. Adding other jobs is tedious, but incredibly simple. I will work on adding other jobs sometime later. For now, I encourage other users to download the code and add the jobs themselves until I get around to doing it on the official release.

On my computer, the code takes 3 seconds to find the best set and 10 seconds to plot it when only changing one piece of gear at a time.
  This is increased to 190 seconds to find the best set and 10 seconds to plot it when changing two pieces of gear simultaneously. This could be significantly faster if we include multiprocessing.

Requires numpy and scipy

Has references to cProfile, datetime, matplotlib, mpl_toolkits, numba, os, pstats, random, re, and sys. These libraries are technically optional if you're willing to make some minor modifications to the code.

The plotting output for this code heavily relies on the Windower/res/items.lua file and the Windower/addons/equipviewer/icons/ directory. It should be relatively straightforward to remove references to these within the fancy_plot.py file and still see the resulting distribution output. I will add support for this option by giving the user the options of "simple" and "fancy" plot formats within the init.py file sometime in the future.

Process to run the simulator:
1) Open gear.py to select which pieces of gear you're interested in testing in each slot. I recommend just keeping everything included for now.

     Manually type out each item's variable/list name inside the individual slot lists
     
        mains = [Heishi, Kannagi, Kikoku, Nagi, Gokotai] # Checks only Heishi, Kannagi, Kikoku, Nagi, and Gokotai in the main hand slot
        subs = [Ternion, Kunimitsu, Gleti_Knife, Tauret, Gokotai, Crepsecular_Knife] # Checks only Ternion Dagger, Kunimitsu, Gleti's Knife, Tauret, Gokotai, and Crepsecular Knife in the off-hand slot.
        

2) Open init.py and verify/modify the variables to match what you want to simulate.

     This file lets you set which weapon skill to simulate, the TP range to use the weapon skill at, the enemy stats, the player buffs, etc
     
3) Open a terminal or command prompt with Python3 installed and run the wsdist.py code.
     
     I run the file using "python wsdist.py" with the Windows10 command prompt or "python3 wsdist.py" on my MacBook Pro.
     
     If you set savetext=True in init.py, then the code's final best set will be saved to a .txt file in the directory you specified as the savepath variable in init.py
     
     If you set save_img=True in init.py, then the code will save the final plot in the "savepath" directory, otherwise it'll try a plt.show()
