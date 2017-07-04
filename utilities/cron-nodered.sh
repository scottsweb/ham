#!/bin/bash

UPDATED=$(curl -s 'http://192.168.11.2:8123/api/states/sensor.emoncms104856_feedid_104856' | jq -r '.attributes.LastUpdated')
TIMESTAMP=$(date +%s)
MINS=9000
COMPARE=$(($UPDATED + $MINS))

if (($TIMESTAMP >  $COMPARE)); then
	docker restart nodered
fi
