#
# (For CI runs this is the only part we want emailed.)
#
export END_TIME="$(date '+%H:%M %d/%m/%Y')"
sep=$(printf "%0.1s" "#"{1..95})
printf "\n\n\n$sep\n\n"
printf "BUILD BEING TESTED        : %s\n\n\n" $DEVICE_BUILDNAME

printf "Unexpected failures       : %s\n\n\n" $UNEX_FAILS

printf "CLICK HERE FOR RUN DETAILS: %s\n\n" "$($0.parts/create_run_results_web_page.sh)"

printf "Start time                : %s\n" "$RUN_TIME"
printf "End time                  : %s\n\n" "$END_TIME"              

P=$(($EX_PASSES + $UNEX_PASSES))
F=$(($EX_FAILS + $UNEX_FAILS))
T=$(($P + $F))
printf "Test cases passed         : %4s / %-4s\n" $P $T 
printf "Assertions passed         : %4s / %-4s\n" $ASSERTS_PASSED $ASSERTS_TOTAL   
printf "Expected failures         : %4s\n" $EX_FAILS               
printf "Ignored test cases        : %4s\n" $IGNORED              
printf "Unwritten test cases      : %4s\n" $UNWRITTEN
printf "\n$sep\n\n\n"                          

if [ "$FAKE_CI_SERVER" ]
then
	printf "For debugging etc... point your browser to: file:///var/www/html/owd_tests/test_123/index.html\n\n"
fi
