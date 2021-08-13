#!/usr/bin/env python3
"""
If there is only one argument, try to run rg on it. In case of failure, try to
rerun rg on all adjacent transpositions of the string. Useful in case of a
simple typo.
"""
import sys
from subprocess import run, CalledProcessError


if __name__ == '__main__':
    if len(sys.argv) == 2:
        s = sys.argv[1]
        try:
            run(['rg', s], check=True)
        except CalledProcessError:
            for i in range(len(s)-1):
                t = s[:i] + s[i+1] + s[i] + s[i+2:]
                print(t)
                run(['rg', t])
    else:
        run(['rg', sys.argv[1:]])
