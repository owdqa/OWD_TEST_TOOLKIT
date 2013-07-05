#!/bin/bash
. $HOME/.OWD_TEST_TOOLKIT_LOCATION

printf "Making sure ADB is up to date ...\n\n"

sudo add-apt-repository ppa:nilarimogard/webupd8
sudo apt-get update
sudo apt-get install android-tools-adb android-tools-fastboot
