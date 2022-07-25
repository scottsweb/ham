#!/bin/bash

rsync -vrl --delete --progress --update --exclude 'Containers' --exclude 'lost+found' --exclude 'Sort' /media/saga/Media/ /media/saga/Backup/
