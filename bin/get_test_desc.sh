#!/bin/bash
#
# Get the description for a test id.
#
HERE=$(dirname $0)
TESTID=${1:?"Syntax: $0 <test id>"}

egrep "^$TESTID\|" $HERE/../../owd_test_cases/Docs/test_descriptions | awk 'BEGIN{FS="|"}{print $2}'
