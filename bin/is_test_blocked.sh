#!/bin/bash
#
# Returns a value if this test id is blocked.
#
HERE=$(dirname $0)
TESTID=${1:?"Syntax: $0 <test id>"}

egrep "^$TESTID\|" $HERE/../../owd_test_cases/Docs/blocked_tests | awk 'BEGIN{FS="|"}{print $2}'