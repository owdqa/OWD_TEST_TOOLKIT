#!/bin/bash
#
# Prepare the dependencies for running OWD tests on the CI server.
#
# It is assumed that the OWD_TEST_TOOLKIT has already been cloned
# (or this script would not exist to run!).
#
export DEVICE=${1:-"unagi"}
export BRANCH=${2:-"v1.3"}
export TEST_TYPE=${3:-"REGRESSION"}


printf "\n\Antes de set_up_parameters\n\n"
. $0.parts/set_up_parameters.sh
printf "\n\nDespués de set_up_parameters\n\n"
printf "\n\nRUN_ID = %s\n\n" $RUN_ID
printf "\n\nDEVICE = %s\n\n" $DEVICE
printf "\n\nBRANCH = %s\n\n" $BRANCH
printf "\n\nVERSION = %s\n\n" $VERSION


. $0.parts/install_toolkit_and_test_cases.sh

. $0.parts/flash_device.sh

printf "\n\nDespués de flash\n\n"
printf "\n\nRUN_ID = %s\n\n" $RUN_ID
printf "\n\nDEVICE = %s\n\n" $DEVICE
printf "\n\nBRANCH = %s\n\n" $BRANCH
printf "\n\nVERSION = %s\n\n" $VERSION


#
# There are some 'special' tests we can run (like 'blocked').
#
cd $owd_test_cases_DIR
if [ "$TEST_TYPE" = "BLOCKED" ]
then
	printf "\nRunning BLOCKED test cases only ...\n\n"
	TEST_LIST=$(egrep -v "^$|^#" Docs/blocked_tests | awk 'BEGIN{FS="|"}{print $1}')

	./run_tests.sh $TEST_LIST
elif [ "$TEST_TYPE" = "ROYTEST" ]
then
	./run_tests.sh 123456
else
	./run_tests.sh $TEST_TYPE
fi
