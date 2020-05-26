#!/usr/bin/env python3
import random
import os
import pathlib
from pathlib import Path


def child_containing_matching_f(root, ext=('opus', 'ogg', 'mp3', 'flac')):
    # only compressed files
    candidates = []
    for x in ext:
        candidates.extend(c.parent for c in root.rglob('*.' + x)
                          if c.parent.name != '+')
    candidates = list(set(candidates))
    if candidates:
        return random.choice(candidates)


def music_root(mpd_conf='~/.config/mpd/mpd.conf'):
    with open(Path(mpd_conf).expanduser()) as fs:
        for l in fs:
            if l.startswith('music_directory'):
                # we don't want the temporary folders, only main one
                dir = Path(l.split('"')[1]).expanduser()
                assert dir.exists(), dir
                return dir


if __name__ == '__main__':
    d = child_containing_matching_f(Path(os.environ['RMUSIC_SOURCE'])
                                    if 'RMUSIC_SOURCE' in os.environ else music_root())
    print(d)
