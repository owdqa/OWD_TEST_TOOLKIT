#
# Flash device.
#
flash_device.sh $DEVICE eng $BRANCH NODOWNLOAD >$RESULT_DIR/flash_device 2>&1

export DEVICE_BUILDNAME=$(egrep "^Unpacking " $RESULT_DIR/flash_device | awk '{print $2}' | sed -e "s/^\(.*\).tgz$/\1/")
mv $RESULT_DIR/flash_device ${RESULT_DIR}/@Build_name@${DEVICE_BUILDNAME}

