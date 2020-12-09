#!/bin/sh
set -ev
cd $(dirname $BASH_SOURCE)
cd ..

python manage.py makemigrations origin bonds
python manage.py flush --no-input
rm -f sqlite3
