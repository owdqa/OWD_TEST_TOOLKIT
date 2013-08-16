export JOB_NAME="test"
export BUILD_NUMBER="123"

export RUN_ID=${JOB_NAME}_${BUILD_NUMBER}
export RESULT_DIR="/tmp/tests/$RUN_ID"
if [ ! -d "$RESULT_DIR" ]
then
	mkdir -p $RESULT_DIR
else
    rm -f $RESULT_DIR/*  >/dev/null 2>&1
    rm -f $RESULT_DIR/.* >/dev/null 2>&1
fi

export HTML_SUMMARIES=$RESULT_DIR/.html_lines
export HTML_INDEX=$RESULT_DIR/index.html

export ON_CI_SERVER="Y"

export FAKE_CI_SERVER="Y"