#!/bin/bash

rsync -vzrl --delete --progress --exclude 'homeassistant/.storage/auth' --exclude 'miniflux/db' --exclude 'plex' --exclude 'pihole/list.*' /media/oak/Bonsai/Containers/ /media/oak/Media/Containers/
