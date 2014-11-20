#!/bin/bash

cmd_adb=$(which adb)
cmd_fastboot=$(which fastboot)

ADB_FOUND=`$cmd_adb devices | tail -2 | head -1 | cut -f 1 | sed 's/ *$//g'`
 
if [[ ${ADB_FOUND} == "List of devices attached" ]]; then
  printf "\nFirefoxOS device seems to be missing.\n"
  exit 
fi

if [ $# -eq 0 ]; then
  printf "\nNo arguments provided. RAM: [0|256-1024] (273 or 319 are the values we should use right now.\n"
  exit
else
  $cmd_adb reboot bootloader
  $cmd_fastboot oem mem $1 
  $cmd_fastboot reboot
fi
