#!/bin/bash

rsync -vzrl --delete --progress --update --exclude 'homeassistant/.storage/auth' --exclude 'miniflux/db' --exclude 'plex' --exclude 'warrior/data' --exclude 'pihole/list.*' --exclude 'folding/data' /media/oak/Bonsai/Containers/ /media/oak/Media/Containers/
