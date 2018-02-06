#!/bin/sh
set -e
set -u
DIRECTORY="$1"

LINK_CMD="ln -i -s"
safe_link(){
  if [ -L "$2" ]; then
    curr="$(readlink -n "$2")"
    if [ "$curr" = "$1" ]; then
      # do nothing
      true
    else
      echo "Changing symbolic link from:"
      echo "$curr"
      echo "To:"
      echo "$1"
      $LINK_CMD "$1" "$2"
    fi
  else
    printf "Creating link: %s\n" "$2"
    $LINK_CMD "$1" "$2"
  fi
  unset curr
}

cd "$(dirname "$0")"

# if [ ! "$0" = "./$(basename "$0")" ]; then
#   echo "Execute from base directory"
#   exit 1
# fi
echo "Install in $DIRECTORY:"
echo "Continue?"
read -r _

for f in *; do
  if [ ! "$f" = "$(basename "$0")" ] && [ -x "$f" ] ; then
    safe_link "$(pwd)/$f" "$DIRECTORY/$f"
  fi
done
