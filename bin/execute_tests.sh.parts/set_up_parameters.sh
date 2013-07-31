. $HOME/.OWD_TEST_TOOLKIT_LOCATION 2> /dev/null

mkdir /tmp/tests 2>/dev/null
chmod 777 /tmp/tests 2> /dev/null

[ -f "$HTML_SUMMARIES" ] && cp /dev/null $HTML_SUMMARIES

#
# Capture the starting time of this test (nicely formatted).
#
export RUN_TIME=$(date "+%H:%M %d/%m/%Y")

#
# Directory for all output (only required if not coming from ci_test_run.sh).
#
if [ ! "$RESULT_DIR" ]
then
	. $0.parts/fake_ci_server.sh
fi
#NOWTIME=$(date +%Y%m%d%H%M)
#export RUN_ID=${RUN_ID:-$NOWTIME}
#export RESULT_DIR=${RESULT_DIR:-"/tmp/tests/B2G_tests.$RUN_ID"}
#[ ! -d "$RESULT_DIR" ] && mkdir -p $RESULT_DIR
rm -f $RESULT_DIR/* >/dev/null 2>&1
rm -f $RESULT_DIR/.* >/dev/null 2>&1

#
# File for realtime summary (so even though the CI output is minimal,
# you can still monitor the current position of the test run).
#
REALTIME_SUMMARY=$RESULT_DIR/realtime_summary

#
# File to record any warnings during setup.
#
export RUNTIME_WARNINGS=$RESULT_DIR/.setup_warnings
cp /dev/null $RUNTIME_WARNINGS

#
# Exit codes so the we know how the test runner script ended, plus
# the exit strings.
#
export UNWRITTEN_STR="(unwritten)"
export IGNORED_STR="(ignored)"
export EX_FAILS_STR="(blocked)"
export EX_PASSES_STR="passed"
export UNEX_PASSES_STR="* unblock? *"
export UNEX_FAILS_STR="*FAILED*"

#
# Used for keeping running totals etc... as the tests are executed.
#
EX_PASSES=0
EX_FAILS=0
UNEX_PASSES=0
UNEX_FAILS=0
IGNORED=0
UNWRITTEN=0
ASSERTS_PASSED=0
ASSERTS_TOTAL=0

#
# Get the function used to run test files.
#
. $0.parts/f_execute_test_file.sh