#!/usr/bin/env python3
"""
Read iso-8601 timestamps and compute the maximal intervals containing them.
"""
import os
import logging

from pprint import pprint
from datetime import datetime
from datetime import timedelta
from pathlib import Path
from collections import defaultdict

logging.basicConfig(level=logging.INFO)

if "TIME_LOG_FOLDER" in os.environ:
    ROOT_LOG_FILES = Path(os.environ["TIME_LOG_FOLDER"])
else:
    ROOT_LOG_FILES = Path(os.environ["HOME"]) / ".tmp/timelogs"

TIME_LOG_FILES = list(ROOT_LOG_FILES.glob("*"))

logging.info("Log files: %s", list(TIME_LOG_FILES))


def within_threshold(d1, d2, threshold=timedelta(minutes=10)):
    """Returns whether d2 is less than threshold after d1."""
    return d2 - d1 < threshold


def print_intervals(intervals):
    """Prints extremities of the non-null intervals."""
    for interval in intervals:
        if interval[-1] - interval[0] != timedelta():
            print(f"[{interval[0]}, {interval[-1]}], {interval[-1] - interval[0]}")


def print_daily_durations(intervals, num_of_days=14):
    durations = defaultdict(timedelta)
    for interval in intervals:
        if interval[-1] - interval[0] != timedelta():
            durations[interval[0].date()] += interval[-1] - interval[0]
    for k, v in list(durations.items())[-num_of_days:]:
        print(f"{k}: {v}")


def print_weekly_durations(intervals, num_of_weeks=20):
    durations = defaultdict(timedelta)
    for interval in intervals:
        if interval[-1] - interval[0] != timedelta():
            durations[interval[0].isocalendar().week] += interval[-1] - interval[0]
    for k, v in list(durations.items())[-num_of_weeks:]:
        minutes = v.total_seconds() // 60
        hours = int(minutes // 60)
        minutes_left = int(minutes - hours * 60)
        print(f"Week {k}: {hours:02d}h{minutes_left:02d}m")


def main(log_files=TIME_LOG_FILES):
    dates = []
    for log_file in log_files:
        with open(log_file) as fs:
            lines = fs.readlines()

        # remove linebreak from line
        dates.extend(datetime.fromisoformat(line.split()[0]) for line in lines if line)

    if not dates:
        logging.warning("No log found, suspicious")
        return

    dates.sort()

    # Contains only non-empty list
    intervals = [[dates[0]]]

    # We assume dates are sorted
    for date in dates[1:]:
        if within_threshold(intervals[-1][-1], date):
            intervals[-1].append(date)
        else:
            intervals.append([date])

    assert sum(len(l) for l in intervals) == len(dates)
    print_intervals(intervals)
    print_daily_durations(intervals)
    print_weekly_durations(intervals)


if __name__ == "__main__":
    main()
