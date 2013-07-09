#
# BUild the test description.
#
test_blocked=$(egrep "^$TEST_NUM\|" $owd_test_cases_DIR/Docs/blocked_tests | awk 'BEGIN{FS="|"}{print $2}' | awk '{print $NF}')

#
# If it's there, turn the bug into a hyperlink.
#
test_blocked=${test_blocked:+"<a href=\"https://bugzilla.mozilla.org/show_bug.cgi?id=$test_blocked\">$test_blocked</a>"}
test_blocked=${test_blocked:+"(BLOCKED BY BUG $test_blocked) "}

test_desc=$(egrep "^$TEST_NUM\|" $owd_test_cases_DIR/Docs/test_descriptions | awk 'BEGIN{FS="|"}{print $2}')

if [ ! "$test_desc" ]
then
    #
    # Try getting it from Jira using the test cases script.
    #
    test_desc=$($owd_test_cases_DIR/bin/get_test_description.sh $TEST_NUM)
fi

export test_desc="$test_blocked$test_desc"

# Pad the description to 70 chars - if it's over that put "..." on the end.
x=${#test_desc}
[ "$x" -gt 70 ] && dots="%-.70s..." || dots="%-70s   "
