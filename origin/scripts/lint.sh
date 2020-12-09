#!/bin/sh
set -ev
cd $(dirname $BASH_SOURCE)
cd ..

pylint .
bandit -r . -c .bandit
