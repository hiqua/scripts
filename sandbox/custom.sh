#!/bin/sh
set -e
set -u

cat >> "$HOME"/.zshrc <<-EOF
export LC_ALL="en_US.UTF-8"
alias vi=vim
tmux && exit
EOF
