#! /usr/bin/env bash

set -e

PS4='# '
set -x

wait-for-it mongo:27017

exec "$@"