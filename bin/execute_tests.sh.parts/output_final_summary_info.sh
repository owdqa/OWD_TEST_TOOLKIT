#!/bin/sh
#
# (For CI runs this is the only part we want emailed.)
#
export END_TIME="$(date '+%d/%m/%Y %H:%M')"
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

# Calculating error rate
if [ $T -gt 0 ]
then
    ERROR_RATE=$((($F*100)/$T))
else
    ERROR_RATE=0
fi

printf "Automation failures                : %4s\n" $AUTOMATION_FAILS
printf "Test cases passed                  : %4s / %-4s\n" $P $T
printf "Assertions passed                  : %4s / %-4s\n" $ASSERTS_PASSED $ASSERTS_TOTAL
printf "Expected failures                  : %4s\n" $EX_FAILS
printf "Ignored test cases                 : %4s\n" $IGNORED
printf "Unwritten test cases               : %4s\n" $UNWRITTEN
printf "\n$sep\n\n\n"

# WEEKLY CSV with all data
# (weekly: there must be one jenkins job to delete this file and to be renewed per week)...

TOTAL_CSV_FILE="/var/www/html/owd_tests/total_csv_file.csv"

if [ "$ON_CI_SERVER" ] && [ ! "$FAKE_CI_SERVER" ]
then
    if [ ! -f "$TOTAL_CSV_FILE" ]
    then
        # print the header
        printf "WEEK NUMBER: %s\n" $(date '+%V') | sudo tee $TOTAL_CSV_FILE
        #printf "TEST_SUITE,BUILD_NUMBER,DEVICE,VERSION,BUILD_BEING_TESTED,URL_RUN_DETAILS,START_TIME,END_TIME,TEST_CASES_PASSED,UNEXPECTED_FAILURES,AUTOMATION_FAILURES,UNEX_PASSES,EX_FAILS,EX_PASSES,IGNORED,UNWRITTEN,PERCENT_FAILED\n" | sudo tee -a $TOTAL_CSV_FILE
        #printf "START_TIME,END_TIME,TEST_SUITE,BUILD_NUMBER,TEST_CASES_PASSED,UNEXPECTED_FAILURES,AUTOMATION_FAILURES,UNEX_PASSES,EX_FAILS,EX_PASSES,IGNORED,UNWRITTEN,PERCENT_FAILED,DEVICE,VERSION,BUILD_BEING_TESTED,URL_RUN_DETAILS\n" | sudo tee -a $TOTAL_CSV_FILE
        printf "START_TIME,DATE,TEST_SUITE,TEST_CASES_PASSED,FAILURES,AUTOMATION_FAILURES,UNEX_PASSES,KNOWN_BUGS,EX_PASSES,IGNORED,UNWRITTEN,PERCENT_FAILED,DEVICE,VERSION,BUILD,TEST_DETAILS\n" | sudo tee -a $TOTAL_CSV_FILE
        sudo chmod 755 $TOTAL_CSV_FILE
    fi

    # print results in one line (comma separated)
    printf "\n" | sudo tee -a $TOTAL_CSV_FILE
    printf "%s," "$RUN_TIME" | sudo tee -a $TOTAL_CSV_FILE
    printf "%s," "$END_TIME" | sudo tee -a $TOTAL_CSV_FILE
    printf "%s_%s," $JOB_NAME $BUILD_NUMBER | sudo tee -a $TOTAL_CSV_FILE
    printf "%4s / %-4s," $P $T | sudo tee -a $TOTAL_CSV_FILE
    printf "%s," $UNEX_FAILS | sudo tee -a $TOTAL_CSV_FILE
    printf "%s," $AUTOMATION_FAILS | sudo tee -a $TOTAL_CSV_FILE
    printf "%s," $UNEX_PASSES | sudo tee -a $TOTAL_CSV_FILE
    printf "%s," $EX_FAILS | sudo tee -a $TOTAL_CSV_FILE
    printf "%s," $EX_PASSES | sudo tee -a $TOTAL_CSV_FILE
    printf "%s," $IGNORED | sudo tee -a $TOTAL_CSV_FILE
    printf "%s," $UNWRITTEN | sudo tee -a $TOTAL_CSV_FILE
    printf "%s%%," $ERROR_RATE | sudo tee -a $TOTAL_CSV_FILE
    printf "%s," $DEVICE | sudo tee -a $TOTAL_CSV_FILE
    printf "%s," $BRANCH | sudo tee -a $TOTAL_CSV_FILE
    # Only first substring of $DEVICE_BUILDNAME
    printf "%s," $DEVICE_BUILDNAME | sed -e "s/.Gecko.*/,/g" | sudo tee -a $TOTAL_CSV_FILE
    # URL without prefix (http://hostname/owd-qa)
    printf "%s/" "$HTML_FILEDIR" | sed -e "s/http:\/\/owd-qa-server\/owd_tests//g" | sudo tee -a $TOTAL_CSV_FILE
    printf "\n" | sudo tee -a $TOTAL_CSV_FILE

    # TODO 1: Done from Jenkins
    # total_weekly: python que lo genere a partir del total_csv con selección de campos (al final de cada job) order: by date desc

    # TODO 2: Done from Jenkins
    # partial_weekly: python que lo genere a partir del total_csv con cada device y version. (al final de cada job): order by date desc


fi



# DAILY CSV partial (device & version) CSV with all data...
# (DAILY: from Jenkins, "partial_csv_file.csv" is replaced for "partial_csv_file_NEW.csv" at the end of complete testing per version.)

PARTIAL_CSV_FILE="/var/www/html/owd_tests/$DEVICE/$BRANCH/partial_csv_file_NEW.csv"

if [ "$ON_CI_SERVER" ] && [ ! "$FAKE_CI_SERVER" ]
then
    if [ ! -f "$PARTIAL_CSV_FILE" ]
    then
        # print the header
        printf "Last test executions, DATE: %s %s\n" $(date '+%m-%d-%Y') $(date '+%T') | sudo tee $PARTIAL_CSV_FILE
        printf "Device: %s\n" $DEVICE | sudo tee -a $PARTIAL_CSV_FILE
        printf "Version: %s\n" $BRANCH | sudo tee -a $PARTIAL_CSV_FILE

        #printf "START_TIME,END_TIME,TEST_SUITE,BUILD_NUMBER,DEVICE,VERSION,BUILD_BEING_TESTED,URL_RUN_DETAILS,TEST_CASES_PASSED,UNEXPECTED_FAILURES,AUTOMATION_FAILURES,UNEX_PASSES,EX_FAILS,EX_PASSES,IGNORED,UNWRITTEN,PERCENT_FAILED\n" | sudo tee -a $PARTIAL_CSV_FILE
        printf "START_TIME,DATE,TEST_SUITE,TEST_CASES_PASSED,FAILURES,AUTOMATION_FAILURES,UNEX_PASSES,KNOWN_BUGS,EX_PASSES,IGNORED,UNWRITTEN,PERCENT_FAILED,DEVICE,VERSION,BUILD,TEST_DETAILS\n" | sudo tee -a $PARTIAL_CSV_FILE
        sudo chmod 755 $PARTIAL_CSV_FILE
    fi

    # print results in one line (comma separated)
    printf "\n" | sudo tee -a $PARTIAL_CSV_FILE
    printf "%s," "$RUN_TIME" | sudo tee -a $PARTIAL_CSV_FILE
    printf "%s," "$END_TIME" | sudo tee -a $PARTIAL_CSV_FILE
    printf "%s_%s," $JOB_NAME $BUILD_NUMBER | sudo tee -a $PARTIAL_CSV_FILE
    printf "%4s / %-4s," $P $T | sudo tee -a $PARTIAL_CSV_FILE
    printf "%s," $UNEX_FAILS | sudo tee -a $PARTIAL_CSV_FILE
    printf "%s," $AUTOMATION_FAILS | sudo tee -a $PARTIAL_CSV_FILE
    printf "%s," $UNEX_PASSES | sudo tee -a $PARTIAL_CSV_FILE
    printf "%s," $EX_FAILS | sudo tee -a $PARTIAL_CSV_FILE
    printf "%s," $EX_PASSES | sudo tee -a $PARTIAL_CSV_FILE
    printf "%s," $IGNORED | sudo tee -a $PARTIAL_CSV_FILE
    printf "%s," $UNWRITTEN | sudo tee -a $PARTIAL_CSV_FILE
    printf "%s%%," $ERROR_RATE | sudo tee -a $PARTIAL_CSV_FILE
    printf "%s," $DEVICE | sudo tee -a $PARTIAL_CSV_FILE
    printf "%s," $BRANCH | sudo tee -a $PARTIAL_CSV_FILE
    # Only first substring of $DEVICE_BUILDNAME
    printf "%s," $DEVICE_BUILDNAME | sed -e "s/.Gecko.*/,/g" | sudo tee -a $PARTIAL_CSV_FILE
    # URL without prefix (http://hostname/owd-qa)
    printf "%s/" "$HTML_FILEDIR" | sed -e "s/http:\/\/owd-qa-server\/owd_tests//g" | sudo tee -a $PARTIAL_CSV_FILE
    printf "\n" | sudo tee -a $PARTIAL_CSV_FILE

    # TODO 3: Done from Jenkins
    # partial_daily: python que lo genere a partir del partial_csv con selección de campos y sólo bugs (al final de cada tanda) order: by bugs desc

fi
