#!/bin/bash
/opt/mycroft/./start-mycroft.sh bus && sleep 15
/opt/mycroft/./start-mycroft.sh skills && sleep 15
/opt/mycroft/./start-mycroft.sh voice && sleep 15
/opt/mycroft/./start-mycroft.sh audio && sleep 15
/opt/mycroft/./start-mycroft.sh enclosure
tail -f /opt/mycroft/scripts/logs/mycroft-skills.log
