#
# Update the run summary totals.
#
if [ ! "$RUN_TEST" ]
then
	#
	# This test was ignored.
	#
    if [ ! "$TEST_FILE" ]
    then
        #
        # Test hasn't been written yet.
        #
        test_result_str="$UNWRITTEN_STR"
        UNWRITTEN=$(($UNWRITTEN+1))
    else
        #
        # Test was ignored.
        #
        test_result_str="$IGNORED_STR"
        IGNORED=$(($IGNORED+1))
    fi
else
    #
    # This test ran.
    #
    if [ "$test_result" = "0" ]
    then
        #
        # Passed.
        #        
        if [ "$test_blocked" ]
        then
        	#
        	# Not expected to pass.
        	#
            test_result_str="$UNEX_PASSES_STR"
            UNEX_PASSES=$(($UNEX_PASSES+1))
        else
            #
            # Expected to pass.
            #
            test_result_str="$EX_PASSES_STR"
            EX_PASSES=$(($EX_PASSES+1))
        fi
    else
        #
        # Failed.
        #
        if [ "$test_blocked" ]
        then
        	#
        	# Expected to fail.
        	#
            test_result_str="$EX_FAILS_STR"
            EX_FAILS=$(($EX_FAILS+1))
        else
            #
            # Not expected to fail.
            #
            test_result_str="$UNEX_FAILS_STR"        
            UNEX_FAILS=$(($UNEX_FAILS+1))
        fi
    fi
fi

#([ "$test_blocked" ] && [ ! "$OWD_NO_BLOCKED" ]) && EX_FAILS=$(($EX_FAILS+1))

#
# Update the number of 'asserts' (any "UTILS.TEST()" calls) that have passed in total.
#
[ "$test_passes" = "?" ] && a_p=0 || a_p=$test_passes
[ "$test_total"  = "?" ] && a_t=0 || a_t=$test_total
[ $(echo "$a_p" | egrep "^[0-9]*$") ] && ASSERTS_PASSED=$(($ASSERTS_PASSED+$a_p))
[ $(echo "$a_t" | egrep "^[0-9]*$") ] && ASSERTS_TOTAL=$(($ASSERTS_TOTAL+$a_t))

#
# It's easier to see all the variables we're setting if I finalize them here!
#
export ASSERTS_PASSED=${ASSERTS_PASSED:-"0"}
export ASSERTS_TOTAL=${ASSERTS_TOTAL:-"0"}
export UNEX_FAILS=${UNEX_FAILS:-"0"}
export EX_PASSES=${EX_PASSES:-"0"}
export UNEX_PASSES=${UNEX_PASSES:-"0"}
export EX_FAILS=${EX_FAILS:-"0"}
export IGNORED=${IGNORED:-"0"}
export UNWRITTEN=${UNWRITTEN:-"0"}

