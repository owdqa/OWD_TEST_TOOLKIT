#!/bin/bash
#
# Script to work around the fact that we have some blocking bugs
# preventing us from removing all SMS threads.
#
sudo adb shell rm -r "/data/local/indexedDB"
sudo adb shell rm -r "data/b2g/mozilla"
sudo adb reboot
sudo adb wait-for-device
sudo adb forward tcp:2828 tcp:2828

x=0
while true
do
	#
	# For safety, this will only loop 20 times before
	# timing out.
	#
	x=$(($x+1))
	if [ $x -gt 20 ]
	then
		printf "\nERROR: $0: Timeout waiting for device to reboot!\n\n"
		exit 1
	fi
	
	#
	# Wait for the FTU screen to be displayed.
	#
	/usr/bin/python2.7 <<!
from marionette import Marionette
marionette = Marionette(host='localhost', port=2828)  
marionette.start_session()
marionette.set_search_timeout(1000)
marionette.switch_to_frame()
try:
    x = marionette.find_element("xpath", "//iframe[contains(@src,'ftu')]")
    marionette.switch_to_frame(x)
    x = marionette.find_element("id", "activation-screen")
    if not x.is_displayed():
        exit(1)
except:
    exit(1)
!
    if [ $? -ne 0 ]
    then
    	sleep 3
    else
        break
    fi
done

#
# ... and just to be totally sure ...
#
sleep 5