#
# Created by Kastra on Asura.
# Feel free to /tell in game or send a PM on FFXIAH you have questions, comments, or suggestions.
#
# Version date: 2021 August 22
#
# Calculate the TP return from an attack round based on the number of swings that landed, the mdelay, and store TP.
# For weaponskills, only the first main and sub hits gain full TP, the others only get 10*(1+stp) TP so they don't use this function.
# The weapon skill part of the code does use this for the first main/sub hits if they pass the accuracy check.
#
def get_tp(swings, mdelay, stp):

    if mdelay <= 180.:
        base_tp = int(61.+((mdelay-180.)*63./360.))
    elif mdelay <= 540.:
        base_tp = int(61.+((mdelay-180.)*88./360.))

    return(swings*int(base_tp*(1.+stp)))
