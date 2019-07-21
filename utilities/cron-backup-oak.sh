#!/bin/bash

rsync -vrl --delete --progress --update --exclude 'Containers' --exclude 'lost+found' --exclude 'Sort' /media/oak/Media/ /media/oak/Backup/
