#
# Update the run summary totals.
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
        
        if [ "$test_blocked" ]
        then
        	#
        	# It's blocked, but it passed!
        	#
            test_failed="*unblock?*"
            TCBLOCKPASS=$(($TCBLOCKPASS+1))
        else
            test_failed=""
        fi
    else
        #
        # Failed.
        #
        if [ "$test_blocked" ]
        then
            test_failed="$BLOCKED_STR"
            TCBLOCKFAIL=$(($TCBLOCKFAIL+1))
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
# It's easier to see all the variables we're setting if I finalize them here!
#
export TCPASS=${TCPASS:-"0"}
export TCFAILED=${TCFAILED:-"0"}
export TCTOTAL=${TCTOTAL:-"0"}
export PASSED=${PASSED:-"0"}
export TOTAL=${TOTAL:-"0"}
export BLOCKED=${BLOCKED:-"0"}
export IGNORED=${IGNORED:-"0"}
export UNWRITTEN=${UNWRITTEN:-"0"}


