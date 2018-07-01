#!/bin/sh
set -e
set -u

MAKE="$(which -a make | tail -n 1)"

if [ ! -z "$TMUX" ]; then
  $MAKE "$@" || tmux display "make error"
else
  $MAKE "$@"
fi
