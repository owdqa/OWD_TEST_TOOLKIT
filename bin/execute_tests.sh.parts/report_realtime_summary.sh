#    
# OUTPUT SUMMARY FOR HTML PAGE BUILDER.
#
if [ "$ON_CI_SERVER" ]
then
    printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\n" \
           "$TEST_NUM"          \
           "$test_result_str"   \
           "$test_passes"       \
           "$test_total"        \
           "$test_desc"         \
           "$test_run_time">> $HTML_SUMMARIES
fi

#
# UPDATE SUMMARY TO STDOUT (only if we ran this test).
#
if [ "$RUN_TEST" ]
then               
    x="($test_run_time) $test_result_str"
    [ "$ON_CI_SERVER" ] && printf "$x\n" >> $REALTIME_SUMMARY || printf "$x\n"
else
    x="(not run)"
    [ "$ON_CI_SERVER" ] && printf "$x\n" >> $REALTIME_SUMMARY || printf "$x\n"
fi

