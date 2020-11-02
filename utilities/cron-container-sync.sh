#!/bin/bash

rsync -vzrl --delete --progress --update --exclude 'homeassistant/.storage/auth' --exclude 'miniflux/db' --exclude 'plex' --exclude 'warrior/data' --exclude 'pihole/list.*' --exclude 'folding/data' /media/saga/Bonsai/Containers/ /media/saga/Media/Containers/
