#!/bin/bash

rsync -vzrl --delete --progress --exclude 'Containers' --exclude 'lost+found' --exclude 'Sort' /media/oak/Media/ /media/oak/Backup/
