#!/usr/bin/env python3
"""
Read iso-8601 timestamps and compute the maximal intervals containing them.
"""
import os
from pprint import pprint
from datetime import datetime
from datetime import timedelta
from pathlib import Path
from collections import defaultdict

if 'USERTMP' in os.environ:
    TIME_LOG_FILE = Path(os.environ['USERTMP']) / 'time_log'
else:
    TIME_LOG_FILE = Path(os.environ['HOME']) / '.tmp/time_log'

def within_threshold(d1, d2, threshold = timedelta(minutes=10)):
    """Returns whether d2 is less than threshold after d1.
    """
    return d2 - d1 < threshold

def print_intervals(intervals):
    """Prints extremities of the non-null intervals.
    """
    for interval in intervals:
        if interval[-1] - interval[0] != timedelta():
            print(f'[{interval[0]}, {interval[-1]}], {interval[-1] - interval[0]}')

def print_daily_durations(intervals):
    durations = defaultdict(timedelta)
    for interval in intervals:
        if interval[-1] - interval[0] != timedelta():
            durations[interval[0].date()] += (interval[-1] - interval[0])
    for k, v in durations.items():
        print(f'{k}: {v}')

def print_weekly_durations(intervals):
    durations = defaultdict(timedelta)
    for interval in intervals:
        if interval[-1] - interval[0] != timedelta():
            durations[interval[0].isocalendar().week] += (interval[-1] - interval[0])
    for k, v in durations.items():
        minutes = v.total_seconds() // 60
        hours = int(minutes // 60)
        minutes_left = int(minutes - hours * 60)
        print(f'Week {k}: {hours}h{minutes_left}m')

def main(log_file=TIME_LOG_FILE):
    with open(log_file) as fs:
        lines = fs.readlines()

    # remove linebreak from line
    dates = [datetime.fromisoformat(line.split()[0]) for line in lines if line]

    if not dates:
        return

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

if __name__ == '__main__':
    main()
