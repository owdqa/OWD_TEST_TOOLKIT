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
sudo adb wait-for-device

sleep 35

sudo adb forward tcp:2828 tcp:2828


