#!/bin/bash
. $HOME/.OWD_TEST_TOOLKIT_LOCATION 2> /dev/null

mkdir /tmp/tests 2>/dev/null
chmod 777 /tmp/tests 2> /dev/null

export NO_TEST_STR="NOTEST"
export IGNORED_TEST_STR="IGNORED"
export BLOCKED_STR="(blocked)"
export FAILED_STR="*FAILED*"
export START_TIME="$(date)"

export USER_STORIES_BASEURL="https://jirapdi.tid.es/browse/OWD-"

[ -f "$HTML_SUMMARIES" ] && cp /dev/null $HTML_SUMMARIES

################################################################################
#
# SET UP REQUIRED TEST VARIABLES
#

# Check parameters file.
$OWD_TEST_TOOLKIT_BIN/check_parameters_file.sh
[ $? -ne 0 ] && exit 1

# If it's okay, the load variables from this file.
export PARAM_FILE="$HOME/.OWD_TEST_PARAMETERS"
if [ -f "$PARAM_FILE" ]
then
    while read line
    do
        var=$(echo $line | awk 'BEGIN{FS="="}{print $1}' | awk '{print $NF}')
        x=$(eval echo \$${var})
        if [ ! "$x" ]
        then
            line="export $line"
            eval $line
        fi
    done <<EOF
    $(egrep -v "^#" $PARAM_FILE)
EOF
fi

# Location of test scripts.
export TESTDIR="./tests"

# Directory for all output.
export NOWTIME=$(date +%Y%m%d%H%M)
export RUN_ID=${RUN_ID:-$NOWTIME}
export RUN_TIME=$(date "+%H:%M %d/%m/%Y")
export RESULT_DIR=${RESULT_DIR:-"/tmp/tests/B2G_tests.$RUN_ID"}
[ ! -d "$RESULT_DIR" ] && mkdir -p $RESULT_DIR

# Exit codes so the we know how the test runner script ended.
export EXIT_PASSED=0
export EXIT_FAILED=1
export EXIT_BLOCKED=2


################################################################################
#
# Set up test list (using test type, if specified, or test numbers.
#
TESTS=""
for user_story in $(echo "$@")
do
	x=$(echo "$user_story" | egrep "^[0-9]+$")
	if [ "$x" ]
	then
		#
		# This is an id - no need to get the children for it.
		#
		TESTS="$TESTS $user_story"
		continue
	else
	    x=$($OWD_TEST_TOOLKIT_DIR/../owd_test_cases/bin/get_child_test_cases.sh $user_story)
	    if [ "$x" ]
	    then
	    	# This matched a parent code for jira, so add these children to the test list.
	    	TESTS="$TESTS $x"
	    fi
   fi
done	

#
# Order the list uniquely.
#
x=$(echo "$TESTS" | sed -e "s/ /\n/g" | sort -nu)
export TESTS="$x"

################################################################################
#
# NOW RUN THE TESTS ...
#

#
# Establsh connection to device (or quit if there was a problem).
#
if [ "$ON_CI_SERVER" ]
then
	#
	# We're catching the output (usually means we're on the ci server).
	#
    $OWD_TEST_TOOLKIT_BIN/connect_device.sh > ${RESULT_DIR}/@Connect_device@Click_here_for_details
else
    $OWD_TEST_TOOLKIT_BIN/connect_device.sh
fi
[ $? -ne 0 ] && exit 1



#
# RUN THE TESTS ...
#
PASSED=0
TOTAL=0
BLOCKED=0
IGNORED=0
UNWRITTEN=0
TCPASS=0
TCTOTAL=0
TCFAILED=0
NUMBER_OF_TESTS=$(echo "$TESTS" | wc -w)
cp /dev/null $RESULT_DIR/current_running_summary
for TEST_NUM in $(echo $TESTS)
do
	#
	# Get the test description.
	#
	test_blocked=$($OWD_TEST_TOOLKIT_BIN/is_test_blocked.sh $TEST_NUM)
	test_blocked=${test_blocked:+"(BLOCKED BY $test_blocked) "}

    test_desc=$($OWD_TEST_TOOLKIT_BIN/get_test_desc.sh $TEST_NUM)
    export test_desc="$test_blocked$test_desc"


    # Pad the description to 70 chars - if it's over that put "..." on the end.
    x=${#test_desc}
    [ "$x" -gt 70 ] && dots="%-.70s..." || dots="%-70s   "

    # Output start of the summary ...    
    x=$(printf "(%s tests left) #%-6s $dots %s: " \
           "$NUMBER_OF_TESTS" \
           "$TEST_NUM"        \
           "$test_desc"       )

    [ "$ON_CI_SERVER" ] && printf "$x" >> $RESULT_DIR/current_running_summary || printf "$x"
           
    NUMBER_OF_TESTS=$(($NUMBER_OF_TESTS-1))


	#
	# Set up some 'test id dependant' variables.
	#
	export TEST_NUM
	export ERR_FILE=${RESULT_DIR}/error_output
	export SUM_FILE=${RESULT_DIR}/${TEST_NUM}_summary
	export DET_FILE=${RESULT_DIR}/${TEST_NUM}_detail

    export TEST_FILE=$(find ./tests -name test_${TEST_NUM}.py)

    #
    # Mark if this test will be run or not.
    #
    if ([ "$OWD_NO_BLOCKED" ] && [ "$test_blocked" ]) || [ ! -f "$TEST_FILE" ]
    then
    	RUN_TEST=""
    else
        RUN_TEST="Y"
    fi

    if [ ! "$RUN_TEST" ]
    then
        #
        # This test isn't to be run - just report a blank.
        #
        printf "0\t0\t0"  >$SUM_FILE        
    else
        #
        # Run the test and record the time taken.
        #
        test_run_time=$( (time $OWD_TEST_TOOLKIT_BIN/run_test_case.sh) 2>&1 )
        
        #
        # Update the description in the details file.
        #
        test_desc_sedsafe=$(echo "$test_desc" | sed -e "s/\//\\\\\//g")
        sed -e "s/XXDESCXX/$test_desc_sedsafe/" $DET_FILE > $DET_FILE.tmp
        mv $DET_FILE.tmp $DET_FILE
    fi

    #
    # Gather the test run details.
    #
    test_failed=""
    test_passes=""
    test_total=""
    if [ -f "$SUM_FILE" ]
    then
    	line="$(tail -1 $SUM_FILE)"
        test_passes=$(  echo "$line" | awk 'BEGIN{FS="\t"}{print $1}')
	    test_failed=$(  echo "$line" | awk 'BEGIN{FS="\t"}{print $2}')
	    test_total=$(   echo "$line" | awk 'BEGIN{FS="\t"}{print $3}')
    fi

    #
    # A bit 'hacky', but if, for ANY reason, these are still
    # not set, then set them to 'something'.
    # (I'm finding certain build issues can cause a mess here!)
    #
    test_passes=${test_passes:-"?"}
    test_failed=${test_failed:-"1"}
    test_total=${test_total:-"?"}

    #
    # Update the final summary totals.
    #
    if [ ! "$RUN_TEST" ]
    then
	    if [ ! "$TEST_FILE" ]
	    then
	    	#
            # Test hasn't been written yet.
            #
	        test_failed="$NO_TEST_STR"
	        UNWRITTEN=$(($UNWRITTEN+1))
	    else
	        #
            # Test is blocked, and we aren't running blocked tests this time.
            #
            test_failed="$IGNORED_TEST_STR"
            IGNORED=$(($IGNORED+1))
        fi
    else
	    TCTOTAL=$(($TCTOTAL+1))
	    if [ "$test_failed" = "0" ]
	    then
	    	#
	    	# Passed.
	    	#
	        TCPASS=$(($TCPASS+1))
	        [ "$test_blocked" ] && test_failed="*unblock?*" || test_failed=""
	    else
	        #
	        # Failed.
	        #
	        if [ "$test_blocked" ]
	        then
	        	test_failed="$BLOCKED_STR"
	        else
	            test_failed="$FAILED_STR"        
	            TCFAILED=$(($TCFAILED+1))
		    fi
	    fi
    fi

    ([ "$test_blocked" ] && [ ! "$OWD_NO_BLOCKED" ]) && BLOCKED=$(($BLOCKED+1))
    
    [ "$test_passes" = "?" ] && tp=0 || tp=$test_passes
    [ "$test_total"  = "?" ] && tt=0 || tt=$test_total
    
    [ $(echo "$tp" | egrep "^[0-9]*$") ] && PASSED=$(($PASSED+$tp))
    [ $(echo "$tt" | egrep "^[0-9]*$") ] && TOTAL=$(($TOTAL+$tt))


    #
    # Put the elapsed time for this test into a nice format.
    #
    z=$(echo "$test_run_time" | egrep "^real" | awk '{print $2}' | awk 'BEGIN{FS="."}{print $1}')
    z_mm=$(echo "$z" | awk 'BEGIN{FS="m"}{print $1}' | awk '{printf "%.2d", $0}')
    z_ss=$(echo "$z" | awk 'BEGIN{FS="m"}{print $2}' | awk '{printf "%.2d", $0}')
    export test_run_time="$z_mm:$z_ss"

    #    
    # OUTPUT SUMMARY FOR HTML PAGE BUILDER.
    #
    if [ "$HTML_WEBDIR" ]
    then
	    printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\n" \
	           "$TEST_NUM"     \
	           "$test_failed"  \
	           "$test_passes"  \
	           "$test_total"   \
	           "$test_desc"    \
	           "$test_run_time">> $HTML_SUMMARIES
    fi
    
    #
    # OUTPUT SUMMARY (only if we ran this test).
    #
    if [ "$RUN_TEST" ]
    then	           
	    x=$(printf "(%s) %s\\\n" "$test_run_time" "$test_failed")
	    [ "$ON_CI_SERVER" ] && printf "$x" >> $RESULT_DIR/current_running_summary || printf "$x"
    else
        x=$(printf "(not run)\\\n")
        [ "$ON_CI_SERVER" ] && printf "$x" >> $RESULT_DIR/current_running_summary || printf "$x"
    fi
    
done

#
# This is the only part we want emailed.
#
sep=$(printf "%0.1s" "#"{1..95})
printf "\n\n$sep\n\n"
printf "BUILD BEING TESTED  : %s\n\n" $DEVICE_BUILDNAME               

printf "Unexpected failures : %s\n\n" $TCFAILED

printf "Interactive report  : %s\n\n" "$($OWD_TEST_TOOLKIT_BIN/run_create_html.sh)"

printf "Start time          : %s\n" "$START_TIME"
printf "End time            : %s\n\n" "$(date)"              

printf "Test cases passed   : %4s / %-4s\n" $TCPASS $TCTOTAL 
printf "Test actions passed : %4s / %-4s\n" $PASSED $TOTAL   
printf "Expected failures   : %4s\n" $BLOCKED              
printf "Ignored test cases  : %4s\n" $IGNORED              
printf "Unwritten test cases: %4s\n" $UNWRITTEN
printf "\n$sep\n\n\n"                          



#
# For Jenkins - if we didn't pass every tests then exit as 'fail' (non-zero).
#
if [ $TCPASS -lt $TCTOTAL ]
then
    exit 1
fi