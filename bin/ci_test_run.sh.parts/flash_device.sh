#
# Flash device.
#

# To get de build file: (without $4 parameter)
#flash_device.sh $DEVICE eng $BRANCH NODOWNLOAD >$RESULT_DIR/flash_device 2>&1
flash_device.sh $DEVICE eng $BRANCH >$RESULT_DIR/flash_device 2>&1

export DEVICE_BUILDNAME=$(egrep "^Unpacking " $RESULT_DIR/flash_device | awk '{print $2}' | sed -e "s/^\(.*\).tgz$/\1/")
mv $RESULT_DIR/flash_device ${RESULT_DIR}/@Flash_device@${DEVICE_BUILDNAME}

