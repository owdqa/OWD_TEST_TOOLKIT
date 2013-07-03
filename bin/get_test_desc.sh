#!/bin/bash
#
# Get the description for a test id.
#
HERE=$(dirname $0)
TESTID=${1:?"Syntax: $0 <test id>"}

x=$(egrep "^$TESTID\|" $HERE/../../owd_test_cases/Docs/test_descriptions | awk 'BEGIN{FS="|"}{print $2}')

if [ "$x" ]
then
    echo "$x"
else
    #
    # Try getting it from Jira.
    #
    $HERE/../../owd_test_cases/bin/get_test_description.sh $TESTID
fi
