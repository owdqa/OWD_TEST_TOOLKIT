#!/bin/bash
. $HOME/.OWD_TEST_TOOLKIT_LOCATION
. $OWD_TEST_TOOLKIT_BIN/run_common_functions.sh

#
# Make sure gaiatest isn't still running (sometimes a process is left after the run).
#
ps -ef | grep gaiatest | grep -v "grep" | awk '{print $2}' | while read pid
do
	kill $pid > /dev/null 2> /dev/null
done

#
# Function to run a test case ...
#
f_run_test(){
    #
    # Run the test and update the variables with the results.
    #
    if [ ! "$test_blocked" ]
    then
	    x=$(egrep "^[^#]*_RESTART_DEVICE *= *True" $TEST_FILE)
	    [ "$x" ] && RESTART="--restart"
    fi
	TESTVARS="--testvars=${OWD_TEST_TOOLKIT_BIN}/gaiatest_testvars.json"
	ADDRESS="--address=localhost:2828"
	
	gaiatest $RESTART $TESTVARS $ADDRESS $TEST_FILE >$ERR_FILE 2>&1
	f_split_run_details "$(cat $SUM_FILE)"
	
	if [ "$test_failed" = "0" ]
	then
		# Passed our tests, but check if marionette reported an error.
		#
        x=$(egrep -i "error|exception" $ERR_FILE)
        if [ "$x" ]
        then
        	test_failed="1"
        fi
	fi
}

#
# Function to see if we can use 2nd chance.
#
f_2nd_chance(){
    #
    # The rules are ...
    #
    # - only if $OWD_USE_2ND_CHANCE is set.
    # - if not blocked.
    # - restart device always on 2nd chance.
    #
    if [ ! "$test_blocked" ] && [ "$OWD_USE_2ND_CHANCE" ]
    then
	    if [ "$test_failed" != "0" ]
	    then
	    	#
	    	# This is an ADB 'reboot' (which sometimes solves a
	    	# problem that gaiatest 'restart' doesn't).
	    	#
			sudo adb reboot
			sudo adb wait-for-device
			sleep 20
			$OWD_TEST_TOOLKIT_BIN/connect_device.sh >/dev/null

            f_run_test
            
            #
            # Add the repeat to the end of the test summary file.
            #
            test_repeat="(x2) "
        fi
    fi
}

#
# Run the test.
#
RESTART=""
test_repeat=""
f_run_test

#
# Check for 2nd chance.
#
f_2nd_chance


#
# Get the summary details
#
f_split_run_details "$(cat $SUM_FILE)"


#
# Append any Marionette output to the details file (sometimes it contains
# 'issues' that we don't catch).
#
x=$(egrep -i "error|exception" $ERR_FILE)
if [ "$x" ]
then
	#
	# Set the test result status to 'something failed'.
	#
	test_failed="1"
	
	#
	# Append the marionette stacktrace to the end of the details file.
	#
    echo "


################################################################################
#
# AN ISSUE WAS REPORTED BY MARIONETTE ....
# ========================================
#

$(cat $ERR_FILE)
" >> $DET_FILE

    #
    # Record details of all iframes.
    #
    printf "\n\n************ Gathering details of all iframes ... ************\n\n"
    $OWD_TEST_TOOLKIT_BIN/DEBUG_get_iframe_details.py $RESULT_DIR >> $DET_FILE

fi

#
# Update the summary file (because Marionette issues won't be caught in it yet).
#
printf "#%s\t%s\t%s\t%s\t%s\t%s\n" \
       "$test_num"                 \
	   "$test_failed"              \
	   "$test_passes"              \
	   "$test_total"               \
	   "$test_repeat$test_desc"    > $SUM_FILE

