#!/bin/sh
set -e
set -u

cat >> "$HOME"/.zshrc <<-EOF
export LC_CTYPE=en_US.UTF-8
export LC_ALL="en_US.UTF-8"
alias vi=vim
if [ "${TMUX:-x}" = "x" ]; then
  tmux && exit
fi
EOF
