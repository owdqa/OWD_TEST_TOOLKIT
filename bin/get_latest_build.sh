#!/bin/bash
#
# Relies on user and password being set in ~/.wgetrc

#
# Make sure pre-requisited are in place.
#
if [ ! -f "$HOME/.wgetrc" ]
then
    echo "
    $HOME/.wgetrc - file not found!
    
    You must create this file with the following lines:
    
    user=<username for release website>
    password=<password for release website>
    
    ... then re-run this script.
    "

    exit 1
fi

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
LOG_FILE=/tmp/${DEVICE}_flash_download.log
LIST_FILE=/tmp/device_build_list_$(date +%Y%M%d%H%M%S).html
SOURCE_DIR=https://owd.tid.es/releases/DEVELOP/lastest-version
SCRIPT=$(readlink -f $0)
SCRIPTPATH=$(dirname $SCRIPT)
CONN_ABD=${SCRIPTPATH}/connect_device
TARGET_DIR=$HOME/Downloads/device_flash_files
[ ! -d "$TARGET_DIR" ] && mkdir -p $TARGET_DIR


#
# Get list of files available in the release directory (in order of last modified descending).
#
wget -O $LIST_FILE --no-check-certificate $SOURCE_DIR/?C=M;O=D


#
# Get the name of the newest 'eng' release (which is at the top of the list).
#
REL_FILE=$(egrep -i "${DEVICE}.*${TYPE}.*${VERSION}" $LIST_FILE | head -1 | sed -e "s/.*href=\"//" | sed -e "s/\".*$//")


#
# Download the release file (takes about 15-20 mins on free network).
#
if [ "$REL_FILE" ]
then
	echo "Fetching $REL_FILE ..."
	cd $TARGET_DIR
    
    #
    # Remove any previous attempts.
    #
    ls | while read fnam
    do
        if [ "$(echo $fnam | grep $REL_FILE)" ]
        then
            rm -f $fnam
        fi
    done
	
    x=$(wget --no-check-certificate $SOURCE_DIR/$REL_FILE | tee $LOG_FILE)
else
	echo "No new \"$TYPE\" build found for $DEVICE in $SOURCE_DIR."
    exit 0
fi


# Is it more than 1 day old?
x=$(find . -name $REL_FILE -mtime -1)
if [ "$x" == "" ]
then
    printf "\n*** WARNING: Flash file is not from today. ***\n\n"
fi

exit 0

