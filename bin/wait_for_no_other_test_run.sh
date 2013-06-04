#!/bin/bash
#
# Waits until no other test runs are detected (to avoid conflicts on Ci server).
#
TEST_RUN_SCRIPT="run_tests.sh"
PID=${1:-$$}

FIRST_TIME="Y"
while true
do
	x=$(ps -e | grep "$TEST_RUN_SCRIPT" | awk '{print $1}' | egrep -v "^$PID$")
	
	if [ ! "$x" ]
	then
		[ "$FIRST_TIME" = "N" ] && printf " done.\n"
		break
	else
	   if [ "$FIRST_TIME" = "Y" ]
	   then
	       FIRST_TIME="N"
           printf "\nA conflicting test is currently running, waiting for it to stop ..."
	   else
	       printf "."
	   fi
	   sleep 10
    fi
done