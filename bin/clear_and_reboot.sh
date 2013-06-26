#!/bin/bash
#
# Script to work around the fact that we have some blocking bugs
# preventing us from removing all SMS threads.
#
sudo adb shell rm -r "/data/local/indexedDB"
sudo adb shell rm -r "data/b2g/mozilla"
sudo adb reboot
sudo adb wait-for-device
sleep 30
sudo adb kill-server
sudo adb start-server
sudo adb forward tcp:2828 tcp:2828

#/usr/bin/python2.7 <<!
#from marionette import Marionette
#marionette = Marionette(host='localhost', port=2828)  
#marionette.start_session()
#!

