. $HOME/.OWD_TEST_TOOLKIT_LOCATION 2> /dev/null

mkdir /tmp/tests 2>/dev/null
chmod 777 /tmp/tests 2> /dev/null

# Capture the starting time of this test (nicely formatted).
export RUN_TIME=$(date "+%H:%M %d/%m/%Y")


[ -f "$HTML_SUMMARIES" ] && cp /dev/null $HTML_SUMMARIES

# Directory for all output (only required if not coming from ci_test_run.sh).
NOWTIME=$(date +%Y%m%d%H%M)
export RUN_ID=${RUN_ID:-$NOWTIME}
export RESULT_DIR=${RESULT_DIR:-"/tmp/tests/B2G_tests.$RUN_ID"}
[ ! -d "$RESULT_DIR" ] && mkdir -p $RESULT_DIR


# File for realtime summary (so even though the CI output is minimal,
# you can still monitor the current position of the test run).
REALTIME_SUMMARY=$RESULT_DIR/realtime_summary

# File to record any warnings during setup.
RUNTIME_WARNINGS=$RESULT_DIR/.setup_warnings

# Exit codes so the we know how the test runner script ended, plus
# the exit strings.
export EXIT_PASSED=0
export EXIT_FAILED=1
export EXIT_BLOCKED=2
export NO_TEST_STR="NOTEST"
export IGNORED_TEST_STR="IGNORED"
export BLOCKED_STR="(blocked)"
export FAILED_STR="*FAILED*"

#
# Used for keeping running totals etc... as the tests are executed.
#
PASSED=0
TOTAL=0
BLOCKED=0
IGNORED=0
UNWRITTEN=0
TCPASS=0
TCTOTAL=0
TCFAILED=0

#
# Get the function used to run test files.
#
. $0.parts/f_execute_test_file.sh