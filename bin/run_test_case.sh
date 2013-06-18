#!/bin/bash
. $HOME/.OWD_TEST_TOOLKIT_LOCATION

#
# Some of these variables come from 'run_all_tests' ...
#
export ERR_FILE=${RESULT_DIR}/error_output
export SUM_FILE=${RESULT_DIR}/${TEST_NUM}_summary
export DET_FILE=${RESULT_DIR}/${TEST_NUM}_detail

#
# Make sure gaiatest isn't still running (sometimes a process is left after the run).
#
ps -ef | grep gaiatest | grep -v "grep" | awk '{print $2}' | while read pid
do
	kill $pid > /dev/null 2> /dev/null
done


#
# Function to split the line from the test reporter into variables.
#
f_split_run_details(){
	test_num=$(     echo "$1" | awk 'BEGIN{FS="\t"}{print $1}')
    test_result=$(  echo "$1" | awk 'BEGIN{FS="\t"}{print $2}')
    test_passes=$(  echo "$1" | awk 'BEGIN{FS="\t"}{print $3}')
    test_total=$(   echo "$1" | awk 'BEGIN{FS="\t"}{print $4}')
	test_desc=$(    echo "$1" | awk 'BEGIN{FS="\t"}{print $5}')
}

#
# Function to just output the result summary line.
#
f_output_run_details(){
	printf "%s\t%s\t%s\t%s\t%s\t%s\n" \
	       "$test_num"    \
           "$test_result" \
           "$test_passes" \
           "$test_total"  \
           "$test_desc"   \
           "$test_repeat"
}


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

	while read line
	do
	    f_split_run_details "$line"
	    break
    done <<EOF
    $(gaiatest $RESTART $TESTVARS $ADDRESS $TEST_FILE 2>$ERR_FILE | egrep "^#")
EOF
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
            test_repeat="(x2)"
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

if [ ! "$test_num" ]
then
    #
    # Total failure - didn't even get to the test part!
    #
    test_num="$TEST_NUM"
    test_result="1" #(no. of fails - this just marks the test as 'did not pass')
    test_passes="?"
    test_total="?"
    test_desc=$(grep "_Description" $TEST_FILE | awk 'BEGIN{FS="="}{print $2}')
fi


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


#
# Finally, output the final details (tab separated).
#
f_output_run_details