if [ ! "$RUN_TEST" ]
then
    #
    # This test will not be executed - just report a blank.
    #
    printf "0\t0\t0"  >$SUM_FILE
    export test_run_time="00:00"
else
    #
    # Ensure the device is connected (reset each time to be sure nothing
    # 'old' is kicking around).
    #
    sudo adb kill-server
    $OWD_TEST_TOOLKIT_BIN/connect_device.sh >/dev/null 2>&1

    #
    # Run the test and record the time taken.
    #
    test_run_time=$( (time f_execute_test_file) 2>&1 )
    
	#
	# Put the elapsed time for this test into a nice format.
	#
	z=$(echo "$test_run_time" | egrep "^real" | awk '{print $2}' | awk 'BEGIN{FS="."}{print $1}')
	z_mm=$(echo "$z" | awk 'BEGIN{FS="m"}{print $1}' | awk '{printf "%.2d", $0}')
	z_ss=$(echo "$z" | awk 'BEGIN{FS="m"}{print $2}' | awk '{printf "%.2d", $0}')
	export test_run_time="$z_mm:$z_ss"

    #
    # Update the description in the details file.
    #
    test_desc_sedsafe=$(echo "$test_desc" | sed -e "s/\//\\\\\//g")
    sed -e "s/XXDESCXX/$test_desc_sedsafe/" $DET_FILE > $DET_FILE.tmp 2>/dev/null
    mv $DET_FILE.tmp $DET_FILE
fi
