#!/bin/sh
set -e
set -u
DIRECTORY="$1"

cd "$(dirname "$0")"

# if [ ! "$0" = "./$(basename "$0")" ]; then
#   echo "Execute from base directory"
#   exit 1
# fi
echo "Install the following in $DIRECTORY:"
for f in *; do
  if [ ! "$f" = "$(basename "$0")" ]; then
    echo "$f"
  fi
done
echo "Continue?"
read -r _
echo "ok"

for f in *; do
  if [ ! "$f" = "$(basename "$0")" ]; then
    ln -s -i "$(pwd)""/$f" "$DIRECTORY"
  fi
done
