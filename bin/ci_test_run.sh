#!/bin/bash
#
# Prepare the dependencies for running OWD tests on the CI server.
#
# NOTE: If you create a file called "${INSTALL_LOG}...something" it
#       will be included in the 'setup' part of the results web page.
#       The filename must have 2 sections in it, separated by "@",
#       i.e.:
#               ${INSTALL_LOG}@title@description
#
#       The 'description' part will become a link you can click to
#       see the file contents.
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
export INSTALL_LOG="/tmp/B2GtestRun"
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
printf "\nFlashing device with BRANCH $BRANCH...\n"
flash_device.sh $DEVICE eng $BRANCH NODOWNLOAD          > /tmp/flash_device 2>&1

buildname=$(egrep "^Unpacking " /tmp/flash_device | awk '{print $2}' | sed -e "s/^\(.*\).tgz$/\1/")
cp /tmp/flash_device ${INSTALL_LOG}@Build_name@${buildname}

# (for the CI output)
printf "\n\nTests running against build: $buildname\n"

cd $HOME/projects/OWD_TEST_TOOLKIT
printf "\nInstalling toolkit (can take a few minutes) ...\n"
echo "Setting up OWD_TEST_TOOLKIT ..."  >> ${INSTALL_LOG}@Dependencies@Clone_and_install_toolkit_etc... 2>&1

cd $HOME/projects/owd_test_cases



#################################################
#
# A quick 'hack' at this point, so I can test changes to this script.
#
if [ "$TEST_TYPE" = "ROYTEST" ]
then
	./run_tests.sh 19354
	
	exit
fi
#################################################


#
# There are some 'special' tests we can run (like 'blocked').
#
if [ "$TEST_TYPE" = "BLOCKED" ]
then
	printf "\nRunning BLOCKED test cases only ...\n\n"
	TEST_LIST=$(egrep -l "^[ \t]*_Description *= *.*BLOCKED BY" tests/test_*.py | awk 'BEGIN{FS="/"}{print $NF}' | awk 'BEGIN{FS="_"}{print $2}' | awk 'BEGIN{FS="."}{print $1}')

	./run_tests.sh $TEST_LIST
else
	./run_tests.sh {$TEST_TYPE}
fi

