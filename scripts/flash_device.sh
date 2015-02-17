#!/bin/bash

# Download and flash the latest available build, if required
#
# Set up variables.
#
MYNAME=$(basename $0)
if [ ! "$1" ] || [ ! "$2" ] || [ ! "$3" ]
then
    echo "

        Syntax: $MYNAME <unagi|keaon|etc...> <eng|user> <version>

        i.e. $MYNAME unagi eng v1-train
    "
    exit 2
fi

DEVICE=$1
TYPE=$2
VERSION=$3
LOGFILE=/tmp/${DEVICE}_flash_download.log
TARGET_DIR=$HOME/Downloads/device_flash_files
OWD_TEST_TOOLKIT_BIN=$PWD

# By default, get the build file too (just pass any parameter as $3 and it'll skip this).
if [ ! "$4" ]
then
    python get_latest_build.py -d $DEVICE -t $TYPE -b $VERSION -u owdmoz -p gaia -s http://ci-owd-misc-02/releases/DEVELOP/ -o $TARGET_DIR

    if [ $? -ne 0 ]
    then
        printf "\n*** ERROR: Problem getting the latest build - not flashing phone. ***\n\n"
        exit 1
    fi
fi

sudo python $OWD_TEST_TOOLKIT_BIN/flash_device.py -d $DEVICE

#
# Tidy up (remove the unpacked directory, but leave the flash file in case we need it again).
#
cd $TARGET_DIR
rm -rf $REL_DIR

printf "\n\nDevices\n"
sudo adb devices
printf "\n\nDevice forward 2828\n"
sudo adb forward tcp:2828 tcp:2828
printf "\n\nRunning apps\n"
gcli listrunningapps
printf "\n\nKilling apps\n"
gcli killapps

if [ "$DEVICE" = "flame-JB" ] || [ "$DEVICE" = "flame-KK" ]
then
    printf "\nFLAME device: adjusting RAM to 512Mb\n"
    sudo $OWD_TEST_TOOLKIT_BIN/adjustRAM.sh 512
fi

sudo adb wait-for-device

printf "\n\nDONE!\n"

