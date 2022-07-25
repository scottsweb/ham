#!/bin/bash

rsync -vzrl --delete --progress --update --exclude 'miniflux/db' --exclude 'plex/config' --exclude 'plex/transcode' --exclude 'warrior/data' --exclude 'vpn/data' --exclude 'folding/data' --exclude 'jottacloud/data' /media/saga/Media/Containers/ /media/saga/Internxt/Backup/containers/
