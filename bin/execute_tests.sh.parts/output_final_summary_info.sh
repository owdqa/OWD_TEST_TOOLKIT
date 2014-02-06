#
# (For CI runs this is the only part we want emailed.)
#
export END_TIME="$(date '+%H:%M %d/%m/%Y')"
export WEEK="$(date '+%V')"
sep=$(printf "%0.1s" "#"{1..95})
printf "\n\n\n$sep\n\n"
printf "BUILD BEING TESTED                 : %s\n\n\n" $DEVICE_BUILDNAME

printf "Possible regression failures       : %s\n\n\n" $UNEX_FAILS

HTML_FILEDIR=$($0.parts/create_run_results_web_page.sh)
#printf "CLICK HERE FOR RUN DETAILS         : %s\n\n" "$($0.parts/create_run_results_web_page.sh)"
printf "CLICK HERE FOR RUN DETAILS         : %s\n\n" "$HTML_FILEDIR"

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

TOTAL_SUM_FILE="/var/www/html/owd_tests/total_sum_file.csv"

if [ "$ON_CI_SERVER" ] && [ ! "$FAKE_CI_SERVER" ]
then
    if [ ! -f "$TOTAL_SUM_FILE" ]
    then
        # print the header
        printf "WEEK NUMBER: %d\n" $(date '+%V') | sudo tee $TOTAL_SUM_FILE
        printf "TEST SUITE,DEVICE,VERSION,BUILD BEING TESTED,FAILURES,LINK to RUN DETAILS,Test cases passed\n" | sudo tee -a $TOTAL_SUM_FILE
        sudo chmod 755 $TOTAL_SUM_FILE
    fi

    # print results in one line (comma separated)
    printf "\n" | sudo tee -a $TOTAL_SUM_FILE
    printf "%s," $JOB_NAME | sudo tee -a $TOTAL_SUM_FILE
    printf "%s," $DEVICE | sudo tee -a $TOTAL_SUM_FILE
    printf "%s," $BRANCH | sudo tee -a $TOTAL_SUM_FILE
    printf "%s," $DEVICE_BUILDNAME | sudo tee -a $TOTAL_SUM_FILE
    printf "%s," $UNEX_FAILS | sudo tee -a $TOTAL_SUM_FILE
    printf "%s/," "$HTML_FILEDIR" | sudo tee -a $TOTAL_SUM_FILE
    printf "%4s / %-4s" $P $T | sudo tee -a $TOTAL_SUM_FILE
    printf "\n" | sudo tee -a $TOTAL_SUM_FILE

fi

# Summary to partial file (device & version)...

PARTIAL_SUM_FILE="/var/www/html/owd_tests/$DEVICE/$BRANCH/partial_sum_file.csv"

if [ "$ON_CI_SERVER" ] && [ ! "$FAKE_CI_SERVER" ]
then
    if [ ! -f "$PARTIAL_SUM_FILE" ]
    then
        # print the header
        printf "Week num: %d\n" $(date '+%V') | sudo tee $PARTIAL_SUM_FILE
        printf "Device: %s\n" $DEVICE | sudo tee -a $PARTIAL_SUM_FILE
        printf "Version: %s\n" $BRANCH | sudo tee -a $PARTIAL_SUM_FILE

        printf "TEST SUITE,BUILD BEING TESTED,FAILURES,LINK to RUN DETAILS,Test cases passed\n" | sudo tee -a $PARTIAL_SUM_FILE
        sudo chmod 755 $PARTIAL_SUM_FILE
    fi

    # print results in one line (comma separated)
    printf "\n" | sudo tee -a $PARTIAL_SUM_FILE
    printf "%s," $JOB_NAME | sudo tee -a $PARTIAL_SUM_FILE
    printf "%s," $DEVICE_BUILDNAME | sudo tee -a $PARTIAL_SUM_FILE
    printf "%s," $UNEX_FAILS | sudo tee -a $PARTIAL_SUM_FILE
    printf "%s/," "$HTML_FILEDIR" | sudo tee -a $PARTIAL_SUM_FILE
    printf "%4s / %-4s" $P $T | sudo tee -a $PARTIAL_SUM_FILE
    printf "\n" | sudo tee -a $PARTIAL_SUM_FILE

fi



# CSV with all data...

TOTAL_CSV_FILE="/var/www/html/owd_tests/total_csv_file.csv"

if [ "$ON_CI_SERVER" ] && [ ! "$FAKE_CI_SERVER" ]
then
    if [ ! -f "$TOTAL_CSV_FILE" ]
    then
        # print the header
        printf "WEEK NUMBER: %d\n" $(date '+%V') | sudo tee $TOTAL_CSV_FILE
        printf "TEST_SUITE,BUILD_NUMBER,DEVICE,VERSION,BUILD_BEING_TESTED,URL_RUN_DETAILS,START_TIME,END_TIME,TEST_CASES_PASSED,UNEXPECTED_FAILURES,AUTOMATION_FAILURES,UNEX_PASSES,EX_FAILS,EX_PASSES,IGNORED,UNWRITTEN,PERCENT_PASSED\n" | sudo tee -a $TOTAL_CSV_FILE
        sudo chmod 755 $TOTAL_CSV_FILE
    fi

    # print results in one line (comma separated)
    printf "\n" | sudo tee -a $TOTAL_CSV_FILE
    printf "%s," $JOB_NAME | sudo tee -a $TOTAL_CSV_FILE
    printf "%s," $BUILD_NUMBER | sudo tee -a $TOTAL_CSV_FILE
    printf "%s," $DEVICE | sudo tee -a $TOTAL_CSV_FILE
    printf "%s," $BRANCH | sudo tee -a $TOTAL_CSV_FILE
    #printf "%s," $DEVICE_BUILDNAME | sudo tee -a $TOTAL_CSV_FILE
    printf "%s," $B2G_BUILD_NAME | sudo tee -a $TOTAL_CSV_FILE
    printf "%s/," "$HTML_FILEDIR" | sudo tee -a $TOTAL_CSV_FILE
    printf "%s/," "$RUN_TIME" | sudo tee -a $TOTAL_CSV_FILE
    printf "%s/," "$END_TIME" | sudo tee -a $TOTAL_CSV_FILE
    printf "%4s / %-4s" $P $T | sudo tee -a $TOTAL_CSV_FILE
    printf "%s," $UNEX_FAILS | sudo tee -a $TOTAL_CSV_FILE
    printf "%s," $AUTOMATION_FAILS | sudo tee -a $TOTAL_CSV_FILE
    printf "%s," $UNEX_PASSES | sudo tee -a $TOTAL_CSV_FILE
    printf "%s," $EX_FAILS | sudo tee -a $TOTAL_CSV_FILE
    printf "%s," $EX_PASSES | sudo tee -a $TOTAL_CSV_FILE
    printf "%s," $IGNORED | sudo tee -a $TOTAL_CSV_FILE
    printf "%s," $UNWRITTEN | sudo tee -a $TOTAL_CSV_FILE
    printf "%s," $PERCENT_PASSED | sudo tee -a $TOTAL_CSV_FILE
    printf "\n" | sudo tee -a $TOTAL_CSV_FILE

fi