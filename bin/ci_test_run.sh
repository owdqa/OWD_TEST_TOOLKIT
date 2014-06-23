#!/bin/bash
#
# Prepare the dependencies for running OWD tests on the CI server.
#
# It is assumed that the OWD_TEST_TOOLKIT has already been cloned
# (or this script would not exist to run!).
#
export DEVICE=${1:-"flame"}
export BRANCH=${2:-"v2.0"}
export TEST_TYPE=${3:-"REGRESSION"}

printf "\n<b>=========================================</b>\n" | tee -a $LOGFILE
printf "\n<b>Switching to branch $INTEGRATION$BRANCH of OWD_TEST_TOOLKIT ...</b>\n\n" | tee -a $LOGFILE
git checkout $INTEGRATION$BRANCH 2> >( tee -a $LOGFILE)
printf "\n<b>Now using OWD_TEST_TOOLKIT branch \"$(git branch | grep '*')\".</b>\n\n" | tee -a $LOGFILE


. $0.parts/set_up_parameters.sh

. $0.parts/install_toolkit_and_test_cases.sh

. $0.parts/flash_device.sh


#
# There are some 'special' tests we can run (like 'blocked').
#
#cd $owd_test_cases_DIR
cd $OWD_TEST_TOOLKIT_DIR/../owd_test_cases

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
