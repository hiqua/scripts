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
import subprocess
from dataclasses import dataclass, field


@dataclass
class Interval:
    timestamps: list[datetime] = field(default_factory=list)

    def __getitem__(self, idx):
        return self.timestamps[idx]

    def __len__(self):
        return len(self.timestamps)

    def append(self, dt: datetime) -> None:
        self.timestamps.append(dt)

    @property
    def start(self) -> datetime:
        return self.timestamps[0]

    @property
    def end(self) -> datetime:
        return self.timestamps[-1]

    @property
    def duration(self) -> timedelta:
        return self.end - self.start


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


def print_intervals(intervals: list[Interval]) -> None:
    """Prints extremities of the non-null intervals."""
    for interval in intervals:
        if len(interval) >= 2 and interval.duration != timedelta():
            print(f"[{interval.start}, {interval.end}], {interval.duration}")


def print_daily_durations(intervals: list[Interval], num_of_days: int = 14) -> None:
    durations = defaultdict(timedelta)
    for interval in intervals:
        if len(interval) >= 2 and interval.duration != timedelta():
            durations[interval.start.date()] += interval.duration
    for k, v in list(durations.items())[-num_of_days:]:
        print(f"{k}: {v}")


def print_weekly_durations(intervals: list[Interval], num_of_weeks: int = 20) -> None:
    durations = defaultdict(timedelta)
    for interval in intervals:
        if len(interval) >= 2 and interval.duration != timedelta():
            durations[interval.start.isocalendar().week] += interval.duration
    for k, v in list(durations.items())[-num_of_weeks:]:
        minutes = v.total_seconds() // 60
        hours = int(minutes // 60)
        minutes_left = int(minutes - hours * 60)
        print(f"Week {k}: {hours:02d}h{minutes_left:02d}m")


def compute_today_duration(interval: Interval) -> timedelta:
    """Computes the amount of time of today that's in the interval."""
    if len(interval) < 2:
        return timedelta()
    today = datetime.now().date()
    total = timedelta()
    for i in range(1, len(interval)):
        prev, curr = interval[i - 1], interval[i]
        # Only count segments that are within today
        if prev.date() == today and curr.date() == today:
            total += curr - prev
        elif prev.date() == today and curr.date() != today:
            # Segment ends after today
            end_of_today = datetime.combine(today, datetime.max.time())
            total += end_of_today - prev
        elif prev.date() != today and curr.date() == today:
            # Segment starts before today
            start_of_today = datetime.combine(today, datetime.min.time())
            total += curr - start_of_today
    return total


def notify_on_today_full_hours(intervals: list[Interval]) -> None:
    """Notifies on full hours reached today.

    Sums today's durations over all intervals. If a new full hour is reached,
    send a notification and track it via a witness file.
    """
    today = datetime.now().date()
    total_today = timedelta()
    for interval in intervals:
        total_today += compute_today_duration(interval)
    total_hours = int(total_today.total_seconds() // 3600)
    if total_hours >= 1:
        notif_file = (
            f"/tmp/parse_time_log_today_{today.strftime('%Y%m%d')}_{total_hours}"
        )
        if not os.path.exists(notif_file):
            seconds = int(total_today.total_seconds())
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            secs = seconds % 60
            duration_str = f"{hours:02d}:{minutes:02d}:{secs:02d}"
            msg = f"You've reached {total_hours} hour(s) today in total! (Exact: {duration_str})"
            subprocess.run(["notify-send", "Time Log", msg])
            Path(notif_file).touch()


def parse_dates_from_logs(log_files) -> list[datetime]:
    dates = []
    for log_file in log_files:
        with open(log_file) as fs:
            lines = fs.readlines()

        # remove linebreak from line
        dates.extend(datetime.fromisoformat(line.split()[0]) for line in lines if line)
    return dates


def create_intervals(dates: list[datetime]) -> list[Interval]:
    dates.sort()
    intervals: list[Interval] = [Interval([dates[0]])]
    for date in dates[1:]:
        if within_threshold(intervals[-1][-1], date):
            intervals[-1].append(date)
        else:
            intervals.append(Interval([date]))
    return intervals


def main(log_files=TIME_LOG_FILES):
    dates = parse_dates_from_logs(log_files)

    if not dates:
        logging.warning("No log found in '%s', suspicious", ",".join(log_files))
        return

    intervals = create_intervals(dates)

    assert sum(len(l) for l in intervals) == len(dates)
    print_intervals(intervals)
    print_daily_durations(intervals)
    print_weekly_durations(intervals)
    notify_on_today_full_hours(intervals)


if __name__ == "__main__":
    main()
