#!/bin/sh
if [ -f "$ZDOTDIR"/11_locals.zsh ]; then
  . "$ZDOTDIR"/11_locals.zsh
  find "$MOBILE_DIR"/msgs -type f -size +0 -exec notify-send "check msgs" \;
fi


tmux new-window -d sd

tum

day="$(python3 -c 'import datetime; print(datetime.datetime.today().weekday())')"
if [ "$day" -eq "2" ];then
  flink &
fi


wait
