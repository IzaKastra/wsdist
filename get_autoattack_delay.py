#
# Created by Kastra on Asura.
# Feel free to /tell in game or send a PM on FFXIAH you have questions, comments, or suggestions.
#
# Version date: 2021 August 22
#
# Return the total real-time between attack rounds given weapon delay and haste.
# Not used for weapon skills. Only used for melee round simulations, but I haven't touched that part of the code in about a year.
#
def get_delay_timing(mdelay, haste):

    return(mdelay/60. * (1-haste)) # in seconds
