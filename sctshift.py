#!/usr/bin/env python3
import subprocess
import os

from time import localtime

"""
A simple wrapper around xsct to compute the desired light temperature and set it.

From morning to mid afternoon: high
mid afternoon to early evening: decrease linearly
early evening til morning: low
"""
LOW_TEMP = 2500
HIGH_TEMP = 7500


def set_temperature(t):
    command = ["xsct", t]
    display = os.environ.get("DISPLAY", ":1")
    subprocess.run(command, env={"DISPLAY": display})


def compute_temperature(morningh, midafterh, eveningh):
    tm = localtime()
    hour = tm.tm_hour
    minutes = tm.tm_min

    if morningh <= hour < midafterh:
        temp = HIGH_TEMP
    elif midafterh <= hour < eveningh:
        temp = HIGH_TEMP - (hour + minutes / 60 - midafterh) / (
            eveningh - midafterh
        ) * (HIGH_TEMP - LOW_TEMP)
    else:
        temp = LOW_TEMP

    return temp


def main():
    morningh = int(os.environ.get("REDSHIFT_MORNING", 8))
    midafterh = int(os.environ.get("REDSHIFT_MIDAFTER", 17))
    eveningh = int(os.environ.get("REDSHIFT_EVENING", 21))

    temp = compute_temperature(morningh, midafterh, eveningh)
    set_temperature(str(temp))


if __name__ == "__main__":
    main()
