#! /usr/bin/env bash

set -e

PS4='# '
set -x

wait-for-it redis:6379

exec "$@"