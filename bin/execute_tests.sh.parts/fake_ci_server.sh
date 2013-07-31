export JOB_NAME="test"
export BUILD_NUMBER="123"

export RUN_ID=${JOB_NAME}_${BUILD_NUMBER}
export RESULT_DIR="/tmp/tests/$RUN_ID"
[ ! -d "$RESULT_DIR" ] && mkdir -p $RESULT_DIR || rm $RESULT_DIR/* 2>/dev/null

export HTML_SUMMARIES=$RESULT_DIR/.html_lines
export HTML_INDEX=$RESULT_DIR/index.html

export ON_CI_SERVER="Y"

export FAKE_CI_SERVER="Y"