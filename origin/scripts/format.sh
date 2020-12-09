#!/bin/sh
set -ev
cd $(dirname $BASH_SOURCE)
cd ..

isort --apply -sl
autoflake . -ri --exclude 'venv, conftest.py' --remove-all-unused-imports --remove-unused-variables --ignore-init-module-imports
isort --apply 
black .
