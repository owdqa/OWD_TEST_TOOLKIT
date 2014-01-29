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

#export RUN_ID=${JOB_NAME}_${BUILD_NUMBER}
# set RUN_ID + DEVICE + BRANCH
export RUN_ID=${JOB_NAME}_${BUILD_NUMBER}_${DEVICE}_${BRANCH}

export RESULT_DIR="/tmp/tests/$RUN_ID"
[ ! -d "$RESULT_DIR" ] && mkdir -p $RESULT_DIR || rm $RESULT_DIR/* 2>/dev/null

export HTML_SUMMARIES=$RESULT_DIR/.html_lines
export HTML_INDEX=$RESULT_DIR/index.html

cp /dev/null $HTML_SUMMARIES
cp /dev/null $HTML_INDEX

#
# A general logfile used for all setup and installation etc...
#
export LOGFILE=${RESULT_DIR}/@Dependencies@Clone_and_install_toolkit_etc...

