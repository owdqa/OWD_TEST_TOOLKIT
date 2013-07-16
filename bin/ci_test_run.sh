#!/bin/bash
#
# Prepare the dependencies for running OWD tests on the CI server.
#
# It is assumed that the OWD_TEST_TOOLKIT has already been cloned
# (or this script would not exist to run!).
#
export DEVICE=${1:-"unagi"}
export BRANCH=${2:-"v1-train"}
export TEST_TYPE=${3:-"REGRESSION"}


. $0.parts/set_up_parameters.sh

. $0.parts/install_toolkit_and_test_cases.sh

printf "\n\nROY NOT FLASHING!\n\n"
#. $0.parts/flash_device.sh


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
	./run_tests.sh 26849
else
	./run_tests.sh $TEST_TYPE
fi
