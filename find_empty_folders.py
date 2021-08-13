#!/usr/bin/env python3
from pathlib import Path

if __name__ == '__main__':
    for d in Path('.').rglob('*'):
        if not d.is_dir():
            continue
        for f in d.rglob('*'):
            break
        else:
            print(d)
