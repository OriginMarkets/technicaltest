#!/bin/sh
set -ev
cd $(dirname $BASH_SOURCE)
cd ..

for directory in origin bonds; do

  target=$(pwd)/$directory/migrations
  read -p "Would you like to delete $target? `echo $'\n> '`"

  if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Trying to delete $target"
    if [ -d "$target" ]; then
      rm -rf $target
      echo "Deleted $target"
    else
      echo "Cannot find $target"
    fi
  
  else
    echo "Skipping $target"
  fi
done
