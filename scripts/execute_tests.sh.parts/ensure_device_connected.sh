#
# Establsh connection to device (or die trying!).
#
if [ "$ON_CI_SERVER" ]
then
    #
    # We're catching the output (usually means we're on the ci server).
    #
    $OWD_TEST_TOOLKIT_BIN/connect_device.sh > ${RESULT_DIR}/@Test_device_connection@Click_here_for_details
else
    $OWD_TEST_TOOLKIT_BIN/connect_device.sh
    echo ""
fi
[ $? -ne 0 ] && exit 1


