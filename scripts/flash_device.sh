#!/bin/bash

# Download and flash the latest available build, if required
if [ "$DEVICE" = "certification" ]
then
    printf "\n\n CERTIFICATION BUILD PREINSTALLED. NOT FLASHING DEVICE!)\n"
    export DEVICE_BUILDNAME="Cert_preinstalled"
else
    if [ "$DEVICE" = "build_preinstalled" ]
    then
        printf "\n\n CERTIFICATION BUILD PREINSTALLED. NOT FLASHING DEVICE!)\n"
        export DEVICE_BUILDNAME="Build_preinstalled"
    else
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

        printf "Getting device_buildname from $RESULT_DIR/flash_device\n"

        # I hate this line, and I will be back to blow it up
        export DEVICE_BUILDNAME=$(egrep "^Device build name: " $RESULT_DIR/flash_device | awk '{print $4}' | sed -e "s/^\(.*\).tgz$/\1/")
        cd $TARGET_DIR/$DEVICE_BUILDNAME
        sudo python $OWD_TEST_TOOLKIT_BIN/flash_device.py -d $DEVICE -t $TARGET_DIR -b $DEVICE_BUILDNAME

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

        sudo adb "wait-for-device"

        printf "\n\nDONE!\n"

        mv $RESULT_DIR/flash_device ${RESULT_DIR}/@Flash_device@${DEVICE_BUILDNAME}

    fi
fi
