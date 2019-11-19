#!/usr/bin/env python3
# move all non audio files to a + directory at the same level in the hierarchy
# complete extensions
import os
import re
import shutil
from pathlib import Path

# case should be ok by now
IGNORE = ('folder.jpg', '+')
EXT = ('flac', 'opus', 'ogg', 'mp3')
DEL_EXT = ('m3u', 'db', 'DS_Store')


def move_file_anyway(f):
    if re.search('00-.*pregap\.', str(f)):
        return True


def child_containing_matching_f(root, ext=EXT):
    seen = set()
    for x in ext:
        # no yield from rglob, as it might create an exception for rmed files
        for c in list(root.rglob('*.' + x)):
            if not c.exists():
                continue
            if (not move_file_anyway(c.name) and
                '+' not in (d.name for d in c.absolute().parents)
                    and c.parent.exists()):
                if c.parent not in seen:
                    yield c.parent
                    seen.add(c.parent)


def clean_files():
    root = Path('.')
    for d in child_containing_matching_f(root):
        assert d.is_dir(), d
        dst = d / '+'
        dst.mkdir(exist_ok=True)
        for f in d.glob('*'):
            if f.name in IGNORE:
                continue

            ext = str(f.suffix)[1:]

            if ext in DEL_EXT:
                f.unlink()
            elif ext not in EXT or move_file_anyway(f):
                print(f'moving {f}')
                try:
                    shutil.move(str(f), str(dst))
                except shutil.Error:
                    f.unlink()


def move_to_artist_folder():
    root = Path('.')
    for d in child_containing_matching_f(root):
        assert d.is_dir(), d
        spl = d.name.split(' - ')
        artist = None
        if len(spl) == 2:
            artist = spl[0]
        else:
            print(f'Could not find artist name for {spl}')
            continue

        if d.parent.name != artist:
            artist_folder = d.parent / artist
            artist_folder.mkdir(exist_ok=True)
            shutil.move(str(d), str(artist_folder))


if __name__ == '__main__':
    move_to_artist_folder()
    clean_files()
