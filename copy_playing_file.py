import os
import re
from pathlib import Path
import shutil

import mpd


def get_client(addr, port, password=None):
    client = mpd.MPDClient(use_unicode=True)
    client.connect(addr, port)

    if password is not None:
        client.password(password)

    return client


def playing_file_rel(client):
    rel_path = client.currentsong()['file']
    return rel_path


def music_root(home):
    with open(home + '/.config/mpd/mpd.conf') as fs:
        mpd_conf = fs.readlines()

    for line in mpd_conf:
        if re.match('^music_directory', line):
            return Path(re.search('".+"', line).group()[1:-1])
    else:
        raise KeyError


def main(tgt=Path('music/from_mpd')):
    home = os.getenv("HOME")
    mobile_dir = os.getenv("MOBILE_DIR")
    host = os.getenv("MPD_HOST").split("@")
    port = os.getenv("MPD_PORT")
    password = host[0] if len(host) == 2 else None
    addr = host[-1]

    client = get_client(addr, port, password)

    rel_path = playing_file_rel(client)

    root = music_root(home)

    abs_path_tgt = mobile_dir / tgt
    abs_path_tgt.mkdir(exist_ok=True)

    shutil.copy(str(root / rel_path), str(abs_path_tgt))


if __name__ == '__main__':
    main()
