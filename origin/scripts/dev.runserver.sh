#!/bin/sh
set -e

while [[ "$#" -gt 0 ]]; do
    case $1 in
        -c|--clear) clear=1 ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

cd $(dirname $BASH_SOURCE)
cd ..
source venv/bin/activate

export DJANGO_SETTINGS_MODULE="origin.settings.dev"

if [[ $clear ]]; then
    sh scripts/rm-db.sh
fi

python manage.py migrate
python manage.py runserver
