#
# Set up parameters.
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
if [ ! "$JOB_NAME" ] || [ ! "$BUILD_NUMBER" ]
then
	printf "\n** Either JOB_NAME or BUILD_NUMBER are not set (this is not a CI run) - exiting. **\n\n"
	exit 1
fi

export ON_CI_SERVER="Y"

#
# If we have installed this before now, then use that
# configuration, else default to $HOME/projects.
#
if [ ! -f "$HOME/.OWD_TEST_TOOLKIT_LOCATION" ]
then
    [ ! "$HOME" ] && export HOME=/home/develenv
    [ ! -d "$HOME/projects" ] && mkdir $HOME/projects

    export OWD_TEST_TOOLKIT_DIR=$HOME/projects/OWD_TEST_TOOLKIT
    export owd_test_cases_DIR=$OWD_TEST_TOOLKIT_DIR/../owd_test_cases
    export OWD_TEST_TOOLKIT_BIN=$OWD_TEST_TOOLKIT_DIR/bin
else
    . $HOME/.OWD_TEST_TOOLKIT_LOCATION 
fi

export PATH=$PATH:/usr/android-sdk/platform-tools/adb:$OWD_TEST_TOOLKIT_DIR/bin
export RUN_ID=${JOB_NAME}_${BUILD_NUMBER}

export RESULT_DIR="/tmp/tests/$RUN_ID"
[ ! -d "$RESULT_DIR" ] && mkdir -p $RESULT_DIR

export HTML_SUMMARIES=$RESULT_DIR/.html_lines
export HTML_INDEX=$RESULT_DIR/index.html

cp /dev/null $HTML_SUMMARIES
cp /dev/null $HTML_INDEX

#
# A general logfile used for all setup and installation etc...
#
export LOGFILE=${RESULT_DIR}/@Dependencies@Clone_and_install_toolkit_etc...

