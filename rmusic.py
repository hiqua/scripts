#!/usr/bin/env python3
import random
import pathlib
from pathlib import Path


ext = ['flac', 'opus', 'ogg', 'mp3']


def child_containing_matching_f(root):
    candidates = []
    for x in ext:
        candidates.extend([c.parent for c in root.rglob('*.' + x)])
    candidates = list(set(candidates))
    if candidates:
        return random.choice(candidates)


def music_root():
    with open(Path('~/.config/mpd/mpd.conf').expanduser()) as fs:
        lines = fs.readlines()
    for l in lines:
        if l.startswith('music_directory'):
            return Path(l.split('"')[1]).expanduser()


root = music_root()
d = child_containing_matching_f(root)
print(d)
