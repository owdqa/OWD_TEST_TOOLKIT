#
# Splits the current '$line' into components, decides which css palette to use and creates
# the table row.
#
test_num=$(     echo "$line" | awk 'BEGIN{FS="\t"}{print $1}')
test_failed=$(  echo "$line" | awk 'BEGIN{FS="\t"}{print $2}')
test_passes=$(  echo "$line" | awk 'BEGIN{FS="\t"}{print $3}')
test_total=$(   echo "$line" | awk 'BEGIN{FS="\t"}{print $4}')
test_desc=$(    echo "$line" | awk 'BEGIN{FS="\t"}{print $5}'| sed -e "s/\(blocked\)/<b>\1<\/b>/I")
test_time=$(    echo "$line" | awk 'BEGIN{FS="\t"}{print $6}')

#
# Color this row depending on what happened.
#
title="Click this to see the test run details."
if [ "$test_failed" ]
then
    if [ "$test_failed" = "$IGNORED_TEST_STR" ]
    then
        rowclass="ignored"
        title="This test was ignored."
    elif [ "$test_failed" = "$NO_TEST_STR" ]
    then
        rowclass="no_test"
        title="This test has not been automated yet."
    else
        rowclass="failed"
    fi
else
    rowclass="passed"
fi

#
# Create the summary row if this is the 'type' we are wanting this time.
#
[ "$TYPE" = "$rowclass" ] && . $0.parts/add_summary_row.sh
