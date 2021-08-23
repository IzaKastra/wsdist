#
# Created by Kastra on Asura.
# Feel free to /tell in game or send a PM on FFXIAH you have questions, comments, or suggestions.
#
# Version date: 2021 August 22
#
# Calculate the mDelay term using the formula on BG wiki
# This is just the average of the delay of your weapons, corrected for dual wield stat
# https://www.bg-wiki.com/ffxi/Dual_Wield
# Used to calculate delay between melee swings (and maybe TP return too?)
#
def get_mdelay(delay1, delay2, dw):

    if delay2 == 0:
        return(delay1)
    else:
        return( (delay1+delay2)/2. * (1.-dw) )
