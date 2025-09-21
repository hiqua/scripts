#!/usr/bin/env python3
"""
Picks an album folder at random.

Using mpd to avoid slow network access.
"""
import os
import subprocess
import sys
import random
from pathlib import Path




def mpd_ls(path):
    res = subprocess.run(['mpc', 'ls',path], capture_output=True, check=True)
    return res.stdout.decode('utf-8').split('\n')[:-1]


if __name__ == '__main__':
    root = Path(os.environ['HOME'] + '/90_99_entertainment/01_music')
    mpd_root = 'musique'
    artist_folders = mpd_ls(mpd_root)
    artist_path = random.choice(artist_folders)
    album_paths = mpd_ls(artist_path)
    album = root / random.choice(album_paths)
    if album.exists():
        print(album)
    else:
        sys.exit(1)
