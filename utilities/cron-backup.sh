#!/bin/bash

rsync -vzrl --delete --progress --exclude 'homeassistant/.storage/auth' --exclude 'miniflux/db' --exclude 'plex' --exclude 'pihole/list.*' /media/data/Containers/ /media/backup/Containers/
