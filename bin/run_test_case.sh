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
	f_split_run_details
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
	    if [ "$test_result" != "0" ]
	    then
            export RESTART="--restart"
            f_run_test
            
            #
            # Add the repeat to the end of the test summary file.
            #
            printf "\t(x2)" >> $SUM_FILE
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
# Append any Marionette output to the details file (sometimes it contains
# 'issues' that we don't catch).
#
x=$(grep -i error $ERR_FILE)
if [ "$x" ]
then
	#
	# Set the test result status to 'something failed'.
	#
	test_result="1"
	
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

fi
