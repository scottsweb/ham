#!/bin/bash

rsync -vzrl --delete --progress --update --exclude 'homeassistant/.storage/auth' --exclude 'miniflux/db' --exclude 'plex' --exclude 'warrior/data' --exclude 'pihole/list.*' /media/oak/Bonsai/Containers/ /media/oak/Media/Containers/
