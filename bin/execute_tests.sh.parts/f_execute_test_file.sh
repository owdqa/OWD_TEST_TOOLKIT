#!/bin/bash
#
# Function to run a test case ...
#
_f_run_test(){
	#
	# Does this test require a 'clear_and_reboot' before running?
	#
    x=$(egrep "^[^#]*_RESTART_DEVICE *= *True" $TEST_FILE)
    if [ "$x" ]
    then
    	$OWD_TEST_TOOLKIT_BIN/clear_and_reboot.sh
    	
    	#
    	# This test gets no 2nd chance if this is set.
    	#
    	export NO_2ND_CHANCE="Y"
    else
        unset NO_2ND_CHANCE
    fi

	TESTVARS="--testvars=${OWD_TEST_TOOLKIT_CONFIG}/gaiatest_testvars.json"
	ADDRESS="--address=localhost:2828"
	
    #
    # Run the test and update the variables with the results.
    #
	gaiatest $RESTART $TESTVARS $ADDRESS $TEST_FILE >$ERR_FILE 2>&1
    line="$(tail -1 $SUM_FILE)"
    test_passes=$(  echo "$line" | awk 'BEGIN{FS="\t"}{print $1}')
    test_result=$(  echo "$line" | awk 'BEGIN{FS="\t"}{print $2}')
    test_total=$(   echo "$line" | awk 'BEGIN{FS="\t"}{print $3}')
	
	if [ "$test_result" = "0" ]
	then
		# Passed our tests, but check if marionette reported an error.
		#
        x=$(egrep -i "error|exception" $ERR_FILE)
        if [ "$x" ]
        then
        	test_result="1"
        fi
	fi
}

#
# Function to see if we can use 2nd chance.
#
_f_2nd_chance(){
    #
    # The rules are ...
    #
    # - only if $OWD_USE_2ND_CHANCE is set.
    # - if not blocked.
    # - restart device always on 2nd chance.
    #
    if [ ! "$test_blocked" ] && [ "$OWD_USE_2ND_CHANCE" ] && [ ! "$NO_2ND_CHANCE" ]
    then
	    if [ "$test_result" != "0" ]
	    then
	    	#
	    	# This is an ADB 'reboot' (which sometimes solves a
	    	# problem that gaiatest 'restart' doesn't).
	    	#
			$OWD_TEST_TOOLKIT_BIN/clear_and_reboot.sh

            _f_run_test
            
        fi
    fi
}

f_execute_test_file(){
	#
	# Make sure gaiatest isn't still running (sometimes a process is left after the run).
	#
	ps -ef | grep gaiatest | grep -v "grep" | awk '{print $2}' | while read pid
	do
	    kill $pid > /dev/null 2> /dev/null
	done
	
	#
	# Run the test.
	#
	RESTART=""
	_f_run_test
	
	#
	# Check for 2nd chance.
	#
	_f_2nd_chance
	
	
	#
	# Get the summary details
	#
	line="$(tail -1 $SUM_FILE)"
	test_passes=$(  echo "$line" | awk 'BEGIN{FS="\t"}{print $1}')
	test_result=$(  echo "$line" | awk 'BEGIN{FS="\t"}{print $2}')
	test_total=$(   echo "$line" | awk 'BEGIN{FS="\t"}{print $3}')
	
	
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
		[ "$test_result" -le 0 ] && test_result=1
		
		#
		# Append the marionette stacktrace to the end of the details file.
		#
	    echo "

<span style=\"color:#ff0000\">
################################################################################
#
# AN ISSUE WAS REPORTED BY MARIONETTE ....
# ========================================
#

$(cat $ERR_FILE)
</span>
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
	printf "%s\t%s\t%s\t%s\t%s\n" \
		   "$test_passes"         \
	       "$test_result"         \
		   "$test_total"          > $SUM_FILE	
}