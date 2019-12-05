#!/usr/bin/env python3
import random
import pathlib
from pathlib import Path


def child_containing_matching_f(root, ext=('flac', 'opus', 'ogg', 'mp3')):
    candidates = []
    for x in ext:
        candidates.extend(c.parent for c in root.rglob('*.' + x))
    candidates = list(set(candidates))
    if candidates:
        return random.choice(candidates)


def music_root(mpd_conf='~/.config/mpd/mpd.conf'):
    with open(Path(mpd_conf).expanduser()) as fs:
        for l in fs:
            if l.startswith('music_directory'):
                dir = Path(l.split('"')[1]).expanduser()
                assert dir.exists()
                return dir


root = music_root()
d = child_containing_matching_f(root)
print(d)
