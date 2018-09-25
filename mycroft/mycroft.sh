#!/bin/bash
COMMAND=${1}
CONTEXT=${2}
#MYCROFT=$(docker exec -it mycroft pgrep -f "startup.sh")

case $COMMAND in
(create)
	docker-compose up -d
;;
(start|on)
	docker exec -it mycroft ./start-mycroft.sh all
;;
(stop|off)
	docker exec -it mycroft ./stop-mycroft.sh
;;
(debug)
	docker exec -it mycroft ./start-mycroft.sh cli
;;
(install)
	docker exec -it mycroft msm install $CONTEXT
;;
(remove)
	docker exec -it mycroft msm remove $CONTEXT
;;
(status)
	if [[ $MYCROFT == "" ]] ; then
		echo "Tunnel INACTIVE"
	else
		echo "Tunnel ACTIVE, PID=$TUNNEL"
	fi
;;
(*)
	SCRIPT_NAME=`basename "$0"`
	echo "Usage: $SCRIPT_NAME {start|stop|debug|install|remove|status}"
;;
esac

