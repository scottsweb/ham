#!/bin/bash

rsync -vrl --delete --progress --exclude 'homeassistant/.storage/auth' --exclude 'miniflux/db' --exclude 'plex' --exclude 'warrior/data' --exclude 'pihole/list.*' /media/data/Containers/ /media/backup/Containers/
