#
# BUild the test description.
#
test_blocked=$(egrep "^$TEST_NUM\|" $owd_test_cases_DIR/Docs/blocked_tests | awk 'BEGIN{FS="|"}{print $2}')

#
# If it's there, turn the bug into a hyperlink.
#
bugzilla_link="https://bugzilla.mozilla.org/show_bug.cgi?id="

x=$(echo "$bugzilla_link" | sed -e "s/\//\\\\\//g")
test_blocked=$(echo "$test_blocked" | sed -e "s/\([0-9][0-9]*\)/<a href=\"$x\1\">\1<\/a>/g")
test_blocked=${test_blocked:+"(BLOCKED BY $test_blocked) "}

test_desc=$(egrep "^$TEST_NUM\|" $owd_test_cases_DIR/Docs/test_descriptions | awk 'BEGIN{FS="|"}{print $2}')

if [ ! "$test_desc" ]
then
    #
    # Get test description.
    #
    test_desc=$(egrep "^$TEST_NUM|" $owd_test_cases_DIR/Docs/test_descriptions | awk 'BEGIN{FS="|"}{print "$NF"}')
    [ "$test_desc" ] && test_desc="(no description found in Docs/test_descriptions)"
fi

export test_desc="$test_blocked$test_desc"

# Pad the description to 70 chars - if it's over that put "..." on the end.
x=${#test_desc}
[ "$x" -gt 70 ] && dots="%-.70s..." || dots="%-70s   "
