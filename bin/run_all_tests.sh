#!/bin/bash
. $HOME/.OWD_TEST_TOOLKIT_LOCATION 2> /dev/null

#
# Now continue with the rest of the setup ...
#
. $OWD_TEST_TOOLKIT_BIN/run_common_functions.sh

mkdir /tmp/tests 2>/dev/null
chmod 777 /tmp/tests 2> /dev/null


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

# Check the xref file variable was set and is a readable file.
export GET_XREF="$OWD_TEST_TOOLKIT_BIN/get_xref.sh"
if [ ! "$OWD_XREF_FILE" ]
then
    printf "\n'OWD_XREF_FILE' variable not set!\n\n"
    exit 1
fi
if [ ! -f "$OWD_XREF_FILE" ]
then
    printf "\n$OWD_XREF_FILE is not a readable file!\n\n"
    exit 1
fi

# Location of test scripts.
export TESTDIR="./tests"

# Directory for all output.
export RUN_ID=$(date +%Y%m%d%H%M%S)
export RUN_TIME=$(date "+%H:%M %d/%m/%Y")
export RESULT_DIR="/tmp/tests/B2G_tests.$RUN_ID"
[ ! -d "$RESULT_DIR" ] && mkdir -p $RESULT_DIR

# Exit codes so the we know how the test runner script ended.
export EXIT_PASSED=0
export EXIT_FAILED=1
export EXIT_BLOCKED=2

# Variables related to building the HTML pages.
export TMP_VAR_FILE="$RESULT_DIR/.tmp_var_file"
export HTML_LINES="$RESULT_DIR/.html_lines"
export OUTHTML="http://owd-qa-server/owd_tests/$(basename $RESULT_DIR)"

echo "

*********************************************************************

To view the interactive test results for this run, please click this: 

$OUTHTML

*********************************************************************

"

################################################################################
#
# Set up test list (using test type, if specified, or test numbers.
#
export TEST_TYPE=$(echo "$@" | awk 'BEGIN{FS="{"}{print $2}' | awk 'BEGIN{FS="}"}{print $1}')
if [ "$TEST_TYPE" ]
then
	#
	# This is a specific test - get the list ...
	#
	TESTS=""
    while read orig
    do
    	# The first line is the header - just ignore it.
    	if [ ! "$TESTS" ]
    	then
    		TESTS=" "
    		continue
    	fi
    	
    	# Use the function to return a test (if there is one!)
        NEW=$($GET_XREF "$TEST_TYPE" "$orig")
    	if [ "$NEW" ]
    	then
    	   # This test is part of this test type.
    	   TESTS="$TESTS $orig"
    	fi
    done << EOF
    $(cat $OWD_XREF_FILE | awk 'BEGIN{FS=","}{print $1}')
EOF
else

	#
	# Did the caller just want to run certain tests?
	#
	TESTS="$@"
	if [ ! "$TESTS" ]
	then
	    #
	    # No specific tests requested, so default to all tests.
	    #
	    while read line
	    do
	        TESTS="$TESTS $line"
	    done <<EOF
	    $(ls ./tests/test_*.py | sed -e "s/^.*test_//" | sed -e "s/\..*//")
EOF
    fi
fi
	
#
# Order the list (uniquely and in order).
#
TEST_TMP="$TESTS"
TESTS=""
while read testnum
do
	TESTS="$TESTS $testnum"
done << EOF
$(echo "$TEST_TMP" | sed -e "s/ /\n/g" | sort -nu)
EOF



################################################################################
#
# NOW RUN THE TESTS ...
#

#
# Establsh connection to device (or quit if there was a problem).
#
$OWD_TEST_TOOLKIT_BIN/connect_device.sh
[ $? -ne 0 ] && exit 1

#
# Check to see if we are running blocked tests or ignoring them.
#
if [ "$OWD_NO_BLOCKED" ]
then
	printf "** NOTE: 'OWD_NO_BLOCKED' is set - ignoring blocked test cases. **\n\n"
fi

#
# Now run tests as required.
#
printf "\n\n(Temporary store for test run files = \"${RESULT_DIR}\".)\n\n"

PASSED=0
TOTAL=0
BLOCKED=0
TCPASS=0
TCTOTAL=0
TCFAILED=0
for i in $(echo $TESTS)
do
	#
	# Make sure there is a test file for this test id.
	#
    export TEST_FILE="./tests/test_${i}.py"
	if [ ! -f $TEST_FILE ]
	then
		echo "ERROR: $TEST_FILE not found, cannot find test for \"$i\"!"
		continue
	fi
	
	#
	# If this test is blocked AND OWD_NO_BLOCKED is set, then ignore it.
	#
	export test_blocked=$(egrep "^[^#]*_Description *= *.*BLOCKED BY" $TEST_FILE)
	if [ "$test_blocked" ] && [ "$OWD_NO_BLOCKED" ]
	then
		continue
	fi
	
	#
	# Set up some 'test id dependant' variables.
	#
	export TEST_NUM=$i
	export ERR_FILE=${RESULT_DIR}/error_output
	export SUM_FILE=${RESULT_DIR}/${TEST_NUM}_summary
	export DET_FILE=${RESULT_DIR}/${TEST_NUM}_detail

    #
    # Run the test and record the time taken...
    #
    test_time=$( (time $OWD_TEST_TOOLKIT_BIN/run_test_case.sh) 2>&1 )

    #
    # Gather the test run details.
    #
    test_failed=""
    [ -f "$SUM_FILE" ] && f_split_run_details "$(tail -1 $SUM_FILE)"

    if [ ! "$test_failed" ]
    then
        #
        # Total failure - didn't even get to the test part!
        #
        test_num="$TEST_NUM"
        test_failed="1" #(no. of fails - this just marks the test as 'did not pass')
        test_passes="?"
        test_total="?"
        test_desc=$(grep "_Description" $TEST_FILE | awk 'BEGIN{FS="="}{print $2}')
    fi

    #
    # Update the final summary totals.
    #
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
        	test_failed="(blocked)"
        else
            test_failed="*FAILED*"        
            TCFAILED=$(($TCFAILED+1))
	    fi
    fi

    TCTOTAL=$(($TCTOTAL+1))
    [ "$test_blocked" ] && BLOCKED=$(($BLOCKED+1))
    
    [ "$test_passes" = "?" ] && tp=0 || tp=$test_passes
    [ "$test_total"  = "?" ] && tt=0 || tt=$test_total
    
    [ $(echo "$tp" | egrep "^[0-9]*$") ] && PASSED=$(($PASSED+$tp))
    [ $(echo "$tt" | egrep "^[0-9]*$") ] && TOTAL=$(($TOTAL+$tt))

        
    #
    # Get the xref test number to report against (if applicable).
    #
    if [ "$TEST_TYPE" ]
    then
        export test_num=$($GET_XREF "$TEST_TYPE" "$test_num")
    fi

    #
    # Put the elapsed time for this test into a nice format.
    #
    z=$(echo "$test_time" | egrep "^real" | awk '{print $2}' | awk 'BEGIN{FS="."}{print $1}')
    z_mm=$(echo "$z" | awk 'BEGIN{FS="m"}{print $1}' | awk '{printf "%.2d", $0}')
    z_ss=$(echo "$z" | awk 'BEGIN{FS="m"}{print $2}' | awk '{printf "%.2d", $0}')
    export test_time="$z_mm:$z_ss"

    #    
    # OUTPUT SUMMARY FOR HTML PAGE BUILDER.
    #
    printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\n" \
           "$test_num"    \
           "$test_failed" \
           "$test_passes" \
           "$test_total"  \
           "$test_desc"   \
           "$test_time"   \
           "$test_repeat" >> $HTML_LINES
    
    #
    # OUTPUT SUMMARY TO STDOUT.
    #    
    # Pad the description to 70 chars - if it's over that put "..." on the end.
    x=${#test_desc}
    [ "$x" -gt 70 ] && dots="%-.70s..." || dots="%-70s   "
    
    printf "#%-6s %-10s (%s - %3s / %-3s): $dots %s\n" \
           "$test_num"    \
           "$test_failed" \
           "$test_time"   \
           "$test_passes" \
           "$test_total"  \
           "$test_desc"   

    
done

printf "\n*******************\n\n"
printf "Unexpected failures: %4s\n" $TCFAILED
printf "\n*******************\n\n"

printf "Test cases passed  : %4s / %-4s\n" $TCPASS $TCTOTAL 
printf "Test actions passed: %4s / %-4s\n" $PASSED $TOTAL
printf "Total blocked tests: %4s\n\n" $BLOCKED

printf "\nDONE.\n\n"


#
# RUN THE HTML PAGE BUILDER.
#
$OWD_TEST_TOOLKIT_BIN/run_create_html.sh


#
# For Jenkins - if we didn't pass every tests then exit as 'fail' (non-zero).
#
if [ $TCPASS -lt $TCTOTAL ]
then
    exit 1
fi