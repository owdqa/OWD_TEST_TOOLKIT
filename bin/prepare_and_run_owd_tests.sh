#!/bin/bash
#
# Prepare the dependencies for running OWD tests on the CI server.
#
[ ! "$HOME" ] && export HOME=/home/develenv
[ ! -d "$HOME/projects" ] && mkdir $HOME/projects
cd $HOME/projects

export OWD_TEST_TOOLKIT_DIR=$HOME/projects/OWD_TEST_TOOLKIT
export PATH=$PATH:/usr/android-sdk/platform-tools/adb:$OWD_TEST_TOOLKIT_DIR/bin
export RUN_ID=${JOB_NAME}_${BUILD_NUMBER}
export RESULT_DIR="/tmp/tests/$RUN_ID"
export HTML_SUMMARIES=$RESULT_DIR/.html_lines
export HTML_INDEX=$RESULT_DIR/index.html
export HTML_WEBDIR="http://owd-qa-server/owd_tests/$RUN_ID"
export HTML_FILEDIR=/var/www/html/owd_tests/$RUN_ID

export DEVICE=${1:-"unagi"}
export BRANCH=${2:-"v1-train"}
export TEST_TYPE=${3:-"REGRESSION"}

[ ! -d "$RESULT_DIR" ] && mkdir $RESULT_DIR
cp /dev/null $HTML_SUMMARIES

#
# Use this filename convention to store details for the html page results
# for this run.
#
export INSTALL_LOG="/tmp/B2GtestRun."
rm ${INSTALL_LOG}* 2>/dev/null

echo "

*********************************************************************

Interactive test details for this run: 

$HTML_WEBDIR

*********************************************************************
"

#
# Flash device.
#
printf "\n\nFlashing device with BRANCH $BRANCH...\n\n"
flash_device.sh $DEVICE eng $BRANCH NODOWNLOAD          > ${INSTALL_LOG}Flash_the_device 2>&1



#
# Install correct versions of the test suite.
#

# Clear out everything (using sudo, so be paranoid about the folder we're in!!!).
cd
sudo rm -rf projects/*

printf "\nCloning OWD_TEST_TOOLKIT and test cases (takes a few minutes) ...\n\n"
cd $HOME/projects
git clone https://github.com/owdqa/OWD_TEST_TOOLKIT.git > ${INSTALL_LOG}Install_toolkit_and_tests 2>&1

cd $HOME/projects/OWD_TEST_TOOLKIT
export REINSTALL_OWD_TEST_CASES="Y"
./install.sh $LOGFILE $BRANCH                          >> ${INSTALL_LOG}Install_toolkit_and_tests 2>&1



#################################################
#
# A quick 'hack' so I can test Jenkins changes away from the 'live' builds.
# I've kept this totally separate so I can put it anywhere in this script that I like.
#
if [ "$TEST_TYPE" = "ROYTEST" ]
then
	#
	# Run a couple of quick test cases so I can test whatever I'm testing.
	#
	cd $HOME/projects/owd_test_cases
	./run_tests.sh 19354
	
	exit
fi
#################################################




#
# There are some 'special' tests we can run (like 'blocked').
#
cd $HOME/projects/owd_test_cases

if [ "$TEST_TYPE" = "BLOCKED" ]
then
	printf "\nRunning BLOCKED test cases only ...\n\n"
	TEST_LIST=$(egrep -l "^[ \t]*_Description *= *.*BLOCKED BY" tests/test_*.py | awk 'BEGIN{FS="/"}{print $NF}' | awk 'BEGIN{FS="_"}{print $2}' | awk 'BEGIN{FS="."}{print $1}')

	./run_tests.sh $TEST_LIST
else
	./run_tests.sh {$TEST_TYPE}
fi

