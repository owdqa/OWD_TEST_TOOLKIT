#!/bin/bash
#
# Script to get screenshot and html dump of the current iframes on the device.
#
# Because I don't know which frame is currently 'on top', I have to just loop
# through them all!
#
. $HOME/.OWD_TEST_TOOLKIT_LOCATION
$OWD_TEST_TOOLKIT_BIN/connect_device.sh

echo "
*
* Please note: 
* As there is no way for this script to know which iframe is currently
* on top, it will just provide details for all current iframes.
*" 

LOGDIR=/tmp/tests/current_screen
[ ! -d "$LOGDIR" ] && mkdir -p $LOGDIR

rm $LOGDIR/* 2>/dev/null
python current_screen_details.py "$LOGDIR"