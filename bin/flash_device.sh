#!/bin/bash
. $HOME/.OWD_TEST_TOOLKIT_LOCATION

#
# Organises downloading the latest build and flashing the
# device with it.
#
# Relies on user and password being set in ~/.wgetrc
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

#
# Make sure nothing else is running first.
#
$OWD_TEST_TOOLKIT_BIN/wait_for_no_other_test_run.sh $$


# By default, get the build file too (just pass any parameter as $3 and it'll skip this).
if [ ! "$4" ]
then
    $OWD_TEST_TOOLKIT_BIN/get_latest_build.sh $DEVICE $TYPE $VERSION

    if [ $? -ne 0 ]
    then
        printf "\n*** ERROR: Problem getting the latest build - not flashing phone. ***\n\n"
        exit 1
    fi
fi

#
# Get the latest build file.
#
cd $TARGET_DIR
REL_FILE=$(ls -lrt | grep -vi "^total" | egrep "${DEVICE}.*\.${TYPE}\.${VERSION}" | tail -1 | awk '{print $NF}')
if [ ! "$REL_FILE" ]
then
    printf "\n*** WARNING: NO BUILD FILES FOUND IN $TARGET_DIR! ***\n\n"
    exit 0
fi

#
# If the file's still being updated then wait for it to finish (better to wait a few minutes
# and run the tests against the very latest build).
#
if [ "$(fuser $REL_FILE 2>/dev/null)" ]
then
	printf "Waiting for file to finish downloading " >> $LOGFILE
	while [ "$(fuser $REL_FILE 2>/dev/null)" ]
	do
		printf "." >> $LOGFILE
		sleep 5
	done
    printf " done.\n" >> $LOGFILE
fi


#
# Unpack the file.
#
echo "Unpacking $REL_FILE ..."
tar xvfz $REL_FILE


#
# Go into the release directory (if you can).
#
REL_DIR=${REL_FILE%.tgz} 
if [ ! -d "$REL_DIR" ]
then
    printf "\n***** ERROR: $REL_DIR does not exist!\n\n"
    echo "Perhaps there was a problem with the tarfile! Aborting ..."
    exit 4
fi

cd $REL_DIR


#
# Restart adb service (just to be sure we're pointing to the correct device).
#
# In case 'su' doesn't have the path to adb, grab it first ...
cmd_adb=$(which adb)
if [ ! "$cmd_adb" ]
then
    printf "\nCould not find 'adb' - please check your installation! Aborting ...\n\n"
    exit 5
fi
sudo $cmd_adb kill-server > /dev/null
sudo $cmd_adb start-server > /dev/null
sudo $cmd_adb forward tcp:2828 tcp:2828 > /dev/null


#
# Do the flash.
#
printf "\n\nFLASHING DEVICE - DO NOT DISTURB! :)\n"
if [ "$DEVICE" = "hamachi_light" ]
then
    sudo ./update-gecko-gaia.sh 
else
    sudo ./flash.sh
fi

# Need to sleep while the phone boots up ('flash' doesn't track this event).
sleep 40

#
# Tidy up (remove the unpacked directory, but leave the flash file in case we need it again).
#
cd $TARGET_DIR
rm -rf $REL_DIR

printf "\n\nDONE!\n"
exit 0
