#!/bin/bash

DEVICES=$(curl -s 'http://192.168.11.2:5556/devices/list' | jq '.devices.luther.state')

if [ "$DEVICES" == "" ]; then
	docker restart firetv
fi
