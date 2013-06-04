#!/bin/bash

# Because 'su' may not have the correct path to 'adb' ...
cmd_adb=$(which adb)

# A nice marker so we know what's happening
export X="(adb check) "

# Do nothing as 'sudo' just to get 'sudo' ready for later on.
sudo date > /dev/null

# Check to see if port is already forwarding ...
fwdPorts=$(netstat -an | grep "LISTEN " | grep 2828)

#
# Function to display currentl devices ...
#
showDevices(){
	devices=$($cmd_adb devices 2>/dev/null | grep -iv "List of devices attached")
	if [ ! "$devices" ]
	then
		echo "$X "
		echo "$X *** ERROR: No devices are listed as connected to this machine! ***"
		echo "$X "
		echo ""
		exit 1
	else
		echo "$X The following devices are currently connected:"
		echo "$X"
 		echo "$devices" | awk 'X=ENVIRON["X"]{print X "          " $1}'
		echo "$X"
	fi
}

if [ "$fwdPorts" ]
then
	echo ""
	echo "$X"
	echo "$X Port 2828 is already being forwarded."
	echo "$X"
	showDevices
else
	echo ""
	echo "$X "
	echo "$X Establishing connection to device (and forwarding the port)..."

	sudo $cmd_adb kill-server > /dev/null
	sudo $cmd_adb start-server > /dev/null
	sudo $cmd_adb forward tcp:2828 tcp:2828 > /dev/null 2>/dev/null

	echo "$X"
	showDevices
fi

echo "$X DONE."
echo "$X"
