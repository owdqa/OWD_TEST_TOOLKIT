#
# (For CI runs this is the only part we want emailed.)
#
export END_TIME="$(date '+%H:%M %d/%m/%Y')"
sep=$(printf "%0.1s" "#"{1..95})
printf "\n\n\n$sep\n\n"
printf "BUILD BEING TESTED                 : %s\n\n\n" $DEVICE_BUILDNAME

printf "Possible regression failures       : %s\n\n\n" $UNEX_FAILS

printf "CLICK HERE FOR RUN DETAILS         : %s\n\n" "$($0.parts/create_run_results_web_page.sh)"

printf "Start time                         : %s\n" "$RUN_TIME"
printf "End time                           : %s\n\n" "$END_TIME"              

P=$(($EX_PASSES + $UNEX_PASSES))
F=$(($EX_FAILS + $UNEX_FAILS))
T=$(($P + $F))
printf "Automation failures                : %4s\n" $AUTOMATION_FAILS 
printf "Test cases passed                  : %4s / %-4s\n" $P $T 
printf "Assertions passed                  : %4s / %-4s\n" $ASSERTS_PASSED $ASSERTS_TOTAL   
printf "Expected failures                  : %4s\n" $EX_FAILS               
printf "Ignored test cases                 : %4s\n" $IGNORED              
printf "Unwritten test cases               : %4s\n" $UNWRITTEN
printf "\n$sep\n\n\n"



# Summary to general file...


TOTAL_SUM_FILE="http://owd-qa-server/owd_tests/total_sum_file"

if [ "$ON_CI_SERVER" ] && [ ! "$FAKE_CI_SERVER" ]
then
    if [ ! -f "$TOTAL_SUM_FILE" ]
    then
        # print the header
        printf "BUILD BEING TESTED\tPossible regression failures\tRUN DETAILS\tStart time\tEnd time\tAutomation failures\tTest cases passed\tAssertions passed\tExpected failures\tIgnored test cases\tUnwritten test cases" > $TOTAL_SUM_FILE
        sudo chmod 755 $TOTAL_SUM_FILE
    fi

    # print results in one line (each item is separated by tab char)
    printf "\n" >> $TOTAL_SUM_FILE
    printf "%s\t" $DEVICE_BUILDNAME >> $TOTAL_SUM_FILE
    printf "%s\t" $UNEX_FAILS >> $TOTAL_SUM_FILE
    printf "file://%s/index.html\t" "$HTML_FILEDIR" >> $TOTAL_SUM_FILE
    printf "%s\t" "$RUN_TIME" >> $TOTAL_SUM_FILE
    printf "%s\t" "$END_TIME" >> $TOTAL_SUM_FILE
    printf "%4s\n" $AUTOMATION_FAILS >> $TOTAL_SUM_FILE
    printf "%4s / %-4s\n" $P $T >> $TOTAL_SUM_FILE
    printf "%4s / %-4s\n" $ASSERTS_PASSED $ASSERTS_TOTAL >> $TOTAL_SUM_FILE
    printf "%4s\n" $EX_FAILS >> $TOTAL_SUM_FILE
    printf "%4s\n" $IGNORED >> $TOTAL_SUM_FILE
    printf "%4s\n" $UNWRITTEN >> $TOTAL_SUM_FILE
    printf "\n" >> $TOTAL_SUM_FILE

fi
