#!/usr/bin/env python3
import random
import os
import pathlib
from pathlib import Path
import sys


def child_containing_matching_f(root, ext=('opus', 'ogg', 'mp3',
'flac'),not_ext=('!qB',)):
    """Find child containg files with given ext, but not not_ext
    """
    # only compressed files
    candidates = []
    for x in ext:
        candidates.extend(c.parent for c in root.rglob('*.' + x)
                          if c.parent.name != '+')
    for x in not_ext:
        candidates = [c for c in candidates if not list(c.rglob('*.' + x))]
    candidates = list(set(candidates))
    if candidates:
        return random.choice(candidates)


def music_root(mpd_conf='~/.config/mpd/mpd.conf'):
    """Meant to be used to copy regular music, but too slow with NFS
    """
    with open(Path(mpd_conf).expanduser()) as fs:
        for l in fs:
            if l.startswith('music_directory'):
                # we don't want the temporary folders, only main one
                dir = Path(l.split('"')[1]).expanduser()
                assert dir.exists(), dir
                return dir


if __name__ == '__main__':
    rmusic_sources = sys.argv[1:]
    d = None
    for source in rmusic_sources:
        d = d or child_containing_matching_f(Path(source))

    if d is None or not d.exists():
        sys.exit(1)

    print(d)
