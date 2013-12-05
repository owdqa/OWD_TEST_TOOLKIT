#!/bin/bash
. $HOME/.OWD_TEST_TOOLKIT_LOCATION

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
DATES_AVAILABLE=/tmp/${DEVICE}_date_available.html
LIST_FILE=/tmp/device_build_list_$(date +%Y%M%d).html
TARGET_DIR=$HOME/Downloads/device_flash_files
[ ! -d "$TARGET_DIR" ] && mkdir -p $TARGET_DIR

#
# The latest version sould be in the tid.es option (comment out the ci2 one if you want that method).
#
SOURCE_DIR=https://owd.tid.es/releases/DEVELOP/lastest-version
#SOURCE_DIR=http://ci2-owd/releases/DEVELOP/


#
# Get the latest date (if using the ci2-owd build).
#
x=$(echo $SOURCE_DIR | grep ci2-owd)
if [ "$x" ]
then
	#
	# Get list of files available in the release directory (in order of last modified descending).
	#
	attempts=10
	wget -O $DATES_AVAILABLE --no-check-certificate $SOURCE_DIR?C=M;O=D
    while read reldate
    do
    	attempts=$((attempts-1))
    	[ $attempts -le 0 ] && break
    	
    	echo "Looking in folder for $reldate for this build ..."
		#
		# Set this to be the name of the directory.
		#
		NEW_SOURCE_DIR=${SOURCE_DIR}${reldate}
		
		#
		# Get list of files available in the release directory (in order of last modified descending).
		#
		wget -O $LIST_FILE --no-check-certificate $NEW_SOURCE_DIR?C=M;O=D 
		
		#
		# Get the name of the newest release (which is at the top of the list).
		#
		REL_FILE=$(egrep -i "${DEVICE}.*\.${TYPE}\.${VERSION}" $LIST_FILE | head -1 | sed -e "s/.*href=\"//" | sed -e "s/\".*$//")
		
		#
		# Download the release file (takes about 15-20 mins on free network).
		#
		if [ "$REL_FILE" ]
		then
			printf "\n\n** Latest file detected is \"$REL_FILE\" from $reldate. **\n\n"
		    SOURCE_DIR="${NEW_SOURCE_DIR}"
			break
		fi
    done <<EOF
    $(grep "folder.gif" $DATES_AVAILABLE | sed -e "s/^.*href=\"//" | sed -e "s/\/.*$//" | egrep "^[0-9]" | sort -r)
EOF
else
	#
	# Get list of files available in the release directory (in order of last modified descending).
	#
	wget -O $LIST_FILE --no-check-certificate $SOURCE_DIR/?C=M;O=D
	
	
	#
	# Get the name of the newest 'eng' release (which is at the top of the list).
	#
	REL_FILE=$(egrep -i "${DEVICE}.*\.${TYPE}\.${VERSION}" $LIST_FILE | head -1 | sed -e "s/.*href=\"//" | sed -e "s/\".*$//")
fi

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
	echo "No new \"$VERSION\" build found for $DEVICE ($TYPE) in $SOURCE_DIR."
    exit 0
fi


# Is it more than 1 day old?
x=$(find . -name $REL_FILE -mtime -1)
if [ "$x" == "" ]
then
    printf "\n*** WARNING: Flash file is not from today. ***\n\n"
fi

exit 0

