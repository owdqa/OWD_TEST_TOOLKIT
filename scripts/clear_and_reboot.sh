#!/bin/bash
#
# Script to work around the fact that we have some blocking bugs
# preventing us from removing all SMS threads.
#
if [ "$1" != "NOCLEAR" ]
then
	sudo adb shell rm -r "/data/local/indexedDB"
	sudo adb shell rm -r "data/b2g/mozilla"
fi

sudo adb reboot

sleep 35

#
# Wait until the device is ready.
#
timeoutLoops=10
while true
do
	sudo adb start-server >/dev/null 2>&1
	[ $? -eq 0 ] && break
	
	$timeoutLoops=$(($timeoutLoops-1))
	[ $timeoutLoops -le 0 ] && break
	
	sleep 5
done

sleep 15
sudo adb start-server
sudo adb forward tcp:2828 tcp:2828


