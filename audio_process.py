#!/usr/bin/env python3
# move all non audio files to a + directory at the same level in the hierarchy
# complete extensions
# run replaygain
# TODO
# check that the track numbers are consecutive and unique
import fnmatch
import os
import re
import shutil
import multiprocessing
from pathlib import Path
import subprocess

# case should be ok by now
IGNORE = ('folder.jpg', '+')
EXT = ('flac', 'opus', 'ogg', 'mp3')
DEL_EXT = ('m3u', 'db', 'DS_Store')


def move_file_anyway(f):
    if re.search(r'00-.*pregap\.', str(f)):
        return True
    else:
        return False


def child_containing_matching_f(root, ext=EXT):
    """
    Yields folders containing files of specified extension.
    """
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
    """
    Moves irrelevant files to a '+' folder.
    """
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

def rename_cue_files():
    root = Path('.')
    for d in child_containing_matching_f(root):
        # XXX: should be case insensitive...
        for f in d.rglob('*.cue'):
            new_path = f.parent.absolute() / (f.name + '.ignore')
            f.rename(new_path)


def get_artist_name_from_folder_name(s):
    pattern = re.compile(
        r"(?P<artist>.*) - (.*) \((?P<year>\d{4})\)")
    match = pattern.match(s)
    if match:
        return match.group("artist")


def test_get_artist_name_from_folder_name():
    s = 'Archive - Londinium (1996) (CD) (524 285 - 2; ARKCD 1001)'
    assert get_artist_name_from_folder_name(s) == 'Archive'

    s = 'Run-D.M.C. - Tougher than Leather (1988) (Vinyl) (ve)'
    assert get_artist_name_from_folder_name(s) == 'Run-D.M.C.'

    s = 'CYNE - Pretty Dark Things (2008) (CD)'
    assert get_artist_name_from_folder_name(s) == 'CYNE'


def move_to_artist_folder():
    root = Path('.')
    for d in child_containing_matching_f(root):
        assert d.is_dir(), d
        artist = get_artist_name_from_folder_name(d.name)

        if artist is None:
            print(f'Could not find artist name for {d.name}')
            continue
        elif d.parent.name != artist:
            artist_folder = d.parent / artist
            artist_folder.mkdir(exist_ok=True)
            shutil.move(str(d), str(artist_folder))


def run_cmd_on_files(d, cmd, x):
    print('Running on ' + str(d) + ', ' + x + ' files.')
    subprocess.run(cmd + [str(p) for p in
                          d.glob('*.' + x)])


def compute_replay_gain():
    root = Path('.')
    ext = 'flac'

    cmd_to_run_in_pool = []

    for d in child_containing_matching_f(root, (ext,)):
        assert d.is_dir(), d
        cmd_to_run_in_pool.append(
            (d, ['metaflac', '--add-replay-gain'], ext))

    with multiprocessing.Pool() as p:
        p.starmap(run_cmd_on_files, cmd_to_run_in_pool)


if __name__ == '__main__':
    os.nice(40)

    move_to_artist_folder()
    clean_files()

    rename_cue_files()

    compute_replay_gain()
