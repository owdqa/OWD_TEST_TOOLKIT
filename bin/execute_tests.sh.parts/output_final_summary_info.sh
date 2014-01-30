#
# (For CI runs this is the only part we want emailed.)
#
export END_TIME="$(date '+%H:%M %d/%m/%Y')"
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
        printf "JOB NAME,BUILD BEING TESTED,Possible regression failures,RUN DETAILS,Start time,End time,Automation failures,Test cases passed,Assertions passed,Expected failures,Ignored test cases,Unwritten test cases" | sudo tee $TOTAL_SUM_FILE
        sudo chmod 755 $TOTAL_SUM_FILE
    fi

    # print results in one line (each item is separated by tab char)
    printf "\n" | sudo tee -a $TOTAL_SUM_FILE
    printf "%s_%s," $JOB_NAME $BUILD_NUMBER | sudo tee -a $TOTAL_SUM_FILE
    printf "%s," $DEVICE_BUILDNAME | sudo tee -a $TOTAL_SUM_FILE
    printf "%s," $UNEX_FAILS | sudo tee -a $TOTAL_SUM_FILE
    printf "%s/," "$HTML_FILEDIR" | sudo tee -a $TOTAL_SUM_FILE
    printf "%s," "$RUN_TIME" | sudo tee -a $TOTAL_SUM_FILE
    printf "%s," "$END_TIME" | sudo tee -a $TOTAL_SUM_FILE
    printf "%4s," $AUTOMATION_FAILS | sudo tee -a $TOTAL_SUM_FILE
    printf "%4s / %-4s," $P $T | sudo tee -a $TOTAL_SUM_FILE
    printf "%4s / %-4s," $ASSERTS_PASSED $ASSERTS_TOTAL | sudo tee -a $TOTAL_SUM_FILE
    printf "%4s," $EX_FAILS | sudo tee -a $TOTAL_SUM_FILE
    printf "%4s," $IGNORED | sudo tee -a $TOTAL_SUM_FILE
    printf "%4s," $UNWRITTEN | sudo tee -a $TOTAL_SUM_FILE
    printf "\n" | sudo tee -a $TOTAL_SUM_FILE

fi
