#! /bin/bash

sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' springer_free_crawler_1)
sudo truncate -s 0 $(docker inspect --format='{{.LogPath}}' springer_free_worker_1)