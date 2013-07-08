#
# (For CI runs this is the only part we want emailed.)
#
export END_TIME="$(date '+%H:%M %d/%m/%Y')"
sep=$(printf "%0.1s" "#"{1..95})
printf "\n\n\n$sep\n\n"
printf "BUILD BEING TESTED  : %s\n\n\n" $DEVICE_BUILDNAME               

printf "Unexpected failures : %s\n\n\n" $TCFAILED

printf "Interactive report  : %s\n\n" "$($0.parts/create_run_results_web_page.sh)"

printf "Start time          : %s\n" "$RUN_TIME"
printf "End time            : %s\n\n" "$END_TIME"              

printf "Test cases passed   : %4s / %-4s\n" $TCPASS $TCTOTAL 
printf "Test actions passed : %4s / %-4s\n" $PASSED $TOTAL   
printf "Expected failures   : %4s\n" $BLOCKED              
printf "Ignored test cases  : %4s\n" $IGNORED              
printf "Unwritten test cases: %4s\n" $UNWRITTEN
printf "\n$sep\n\n\n"                          


