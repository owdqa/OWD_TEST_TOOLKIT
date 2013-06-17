#!/bin/bash
. $HOME/.OWD_TEST_TOOLKIT_LOCATION

#
# Some of these variables come from 'run_all_tests' ...
#
export ERR_FILE=${RESULT_DIR}/error_output
export SUM_FILE=${RESULT_DIR}/${TEST_NAME}_summary
export DET_FILE=${RESULT_DIR}/${TEST_NAME}_detail

TEST_IS_BLOCKED=$(echo "$TEST_DESC" | grep -i "blocked by")

#
# Make sure gaiatest isn't still running (sometimes a process is left after the run).
#
ps -ef | grep gaiatest | grep -v "grep" | awk '{print $2}' | while read pid
do
	kill $pid > /dev/null 2> /dev/null
done

TNAM=$(echo $TEST_NAME | awk '{printf "%-5s", $0}')


#
# At the moment things sometimes file the first time. This
# just allows us to try one more time.
#
_2ND_CHANCE=$1


#
# Function to report the end of the test.
#
_end_test(){
	EXIT_STR="$1"
	EXIT_CODE=$2
    [ "${_2ND_CHANCE}" ] && ATTEMPTS="(x2)" || ATTEMPTS=""
    echo "${EXIT_STR}${ATTEMPTS}"
    exit $EXIT_CODE
}


#
# Function to handle 2nd chances ...
#
_check_2nd_chance(){
    STROUT="$1"
    EXIT=$2
    
    # (Neve give a 2nd chance to a blocked test.)
    if [ "${_2ND_CHANCE}" ] || [ ! "$OWD_USE_2ND_CHANCE" ] || [ "$TEST_IS_BLOCKED" ]
    then
    	_end_test "$STROUT" $EXIT
    else
        # Try again.
        $0 Y
        exit $?
    fi
}


#
# Run the test using 'gaiatest', ignore STDOUT (because what we want is being
# writtin to a file), but capture STDERR.
#
# For speed, only restart the device if:
#
#   1. This is the 2nd chance.
#   2. The test case script has "_RESTART_DEVICE = True" in it.
#
#

# 1.
[ "${_2ND_CHANCE}" ] && RESTART="--restart" || RESTART=""

# 2.
x=$(egrep "^[^#]*_RESTART_DEVICE *= *True" $TEST_FILE) 
[ "${x}" ] && RESTART="--restart" || RESTART=""


#[ ! "$OWD_USE_2ND_CHANCE" ] && RESTART="" || RESTART="$RESTART"
TESTVARS="--testvars=${THISPATH}/gaiatest_testvars.json"
ADDRESS="--address=localhost:2828"

gaiatest $RESTART $TESTVARS $ADDRESS $TEST_FILE > /dev/null 2>$ERR_FILE

#
# Now append any Marionette output to the details file (sometimes it contains
# 'issues' that we don't catch).
#
x=$(grep -i error $ERR_FILE)
if [ "$x" ]
then
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
# Display the summary file.
# If there is an 'error' in the marionette output but we think our tests
# passed, this indicates a possible error with our test code.
#
if [ -f "$SUM_FILE" ]
then
    cat $SUM_FILE | while read line
    do
        result=$(echo $line | awk '{print $2}')
        
        failTest=$(echo "$result" | egrep -i "failed|blocked")
        if [ ! "$failTest" ]
        then
            x="$line"
            errChk=$(grep -i error $ERR_FILE)

            if [ "$errChk" ]
            then
            	#
            	# SOME marionette errors just need a little wait.
            	#
            	x=$(grep -i "Could not successfully complete transport of message to Gecko" $ERR_FILE)
            	if [ "$x" ]
            	then
            		# Try again, without 2nd chance being set.
            		_2ND_CHANCE=""
            		_check_2nd_chance "$x" $EXIT_FAILED
            	else
            	    #
            	    # This test failed.
                    #
            	    if [ "$TEST_IS_BLOCKED" ]
            	    then
            	    	subword="(blocked)"
            	    	EXIT_CODE=$EXIT_BLOCKED
            	    else
                        subword="*FAILED* "
                        EXIT_CODE=$EXIT_FAILED
                    fi
                    
	                x=$(echo "$line" | sed -e "s/#[^ ]*[^(]*/#$TNAM $subword /")
	                _check_2nd_chance "$x" $EXIT_CODE
                fi
            fi
            
            #
            # If we get here then all's well - just leave.
            #
            _end_test "$x" 0
        else
            #
            # It failed - at the moment, failures are often just
            # 'something odd' in Marionette or Gaiatest, which run
            # fine the next time you try.
            # Because this is so often the case, we'll give a failed
            # test case a second chance before giving up.
            #
            _check_2nd_chance "$line" $EXIT_FAILED
        fi
        _2ND_CHANCE="Y"
    done
else
    _check_2nd_chance "#$TNAM *FAILED*  (unknown - unknown): ${TEST_DESC:0:80}" $EXIT_FAILED
fi