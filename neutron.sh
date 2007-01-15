#!/bin/bash

NEUTRON=./neutron.py

PIDPATH=.
PIDFILE=$PIDPATH/neutron.pid

case "$1" in
  start)
	echo -n "Starting Neutron: "
	if ([[ -w $PIDFILE ]])
	then 
		echo "ERROR: Neutron already started (PID file found)"
		exit 1
	fi
	$NEUTRON --pid-file=$PIDFILE >/dev/null &
	echo "done"
    ;;
  stop)
	echo -n "Stopping Neutron: "
	if !([[ -w $PIDFILE ]])
	then 
		echo "ERROR: Neutron is not running (PID file not found)"
		exit 1
	fi
	kill `cat $PIDFILE`
	rm $PIDFILE
	echo "done"
    ;;
  *)
    echo "Usage: $0 {start|stop}" >&2
    exit 1
    ;;
esac

exit 0
