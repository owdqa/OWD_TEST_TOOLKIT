# Output start of the summary ...    
x=$(printf "(%s tests left) #%-6s $dots %s: " \
       "$NUMBER_OF_TESTS" \
       "$TEST_NUM"        \
       "$test_desc"       )

[ "$ON_CI_SERVER" ] && printf "$x" >> $REALTIME_SUMMARY || printf "$x"
       
NUMBER_OF_TESTS=$(($NUMBER_OF_TESTS-1))

