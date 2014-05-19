#
# Flash device.
#
#flash_device.sh $DEVICE eng $BRANCH NODOWNLOAD >$RESULT_DIR/flash_device 2>&1
# forcing to download the build file

if [ "$DEVICE" = "certification" ]
then
    printf "\n\n CERTIFICATION BUILD PREINSTALLED. NOT FLASHING DEVICE!)\n"
    export DEVICE_BUILDNAME="Certification preinstalled build"
else
    printf "\n\nFLASHING DEVICE - DO NOT DISTURB! :)\n"
    flash_device.sh $DEVICE eng $BRANCH >$RESULT_DIR/flash_device 2>&1

    export DEVICE_BUILDNAME=$(egrep "^Unpacking " $RESULT_DIR/flash_device | awk '{print $2}' | sed -e "s/^\(.*\).tgz$/\1/")
    mv $RESULT_DIR/flash_device ${RESULT_DIR}/@Flash_device@${DEVICE_BUILDNAME}
fi
