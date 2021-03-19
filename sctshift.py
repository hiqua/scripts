#!/usr/bin/env python3
import subprocess
from time import localtime
"""
A simple wrapper around sct to compute the desired light temperature and set it.

From morning to mid afternoon: high
mid afternoon to early evening: decrease linearly
early evening til morning: low
"""
LOW_TEMP = 2500
HIGH_TEMP = 7500
morningh = 7
midafterh = 14
eveningh = 20

def set_temperature(t):
    command = ["sct", t]
    subprocess.run(command)

def compute_temperature():
    tm = localtime()
    hour = tm.tm_hour
    minutes = tm.tm_min

    if morningh <= hour < midafterh:
        temp = HIGH_TEMP
    elif midafterh <= hour < eveningh:
        temp = HIGH_TEMP - (hour + minutes / 60 - midafterh) / (eveningh - midafterh) * (HIGH_TEMP - LOW_TEMP)
    else:
        temp = LOW_TEMP

    return temp



def main():
    temp = compute_temperature()
    set_temperature(str(temp))

if __name__ == "__main__":
    main()
