#!/bin/bash
#
# Script to create the html summary file etc...
#
# NOTE: This is intended to be run via the 'run_all_tests.sh' script
# and only works on the CI server (or if "$INSTALL_LOG" is set).
#
if [ ! "$ON_CI_SERVER" ]
then
	printf "(No results web page generated: we're not on the ci server.)"
	exit
fi

#
# Setup dependencies.
#
. $0.parts/setup_dependencies.sh

#
# Build table of any 'extra' setup details that are required.
#
. $0.parts/create_extra_setup_detail_rows.sh

#
# Build table of test case executions summaries.
#
. $0.parts/create_summary_types.sh

#
# Build the final details web page by substituting the variables into the template.
#
# (NOTE: for now, every variable that needs to be substituted has to be listed here.)
#
page_title="${JOB_NAME}-${BUILD_NUMBER}"

#
# Using only the 'unexpected fails' means the build can 'pass'
# even if there are expected failures (i.e. blocked tests that
# fail will not 'fail' the entire build).
#
UNEX_FAILS=${UNEX_FAILS:-"0"}
[ "$UNEX_FAILS" = "0" ] && BUILD_RESULT="pass" || BUILD_RESULT="fail"

ASSERTS_PASSED=${ASSERTS_PASSED:-0}
ASSERTS_TOTAL=${ASSERTS_TOTAL:-0}
if [ $ASSERTS_PASSED -lt $ASSERTS_TOTAL ]
then
	PERCENT_PASSED=$(($ASSERTS_PASSED * 100))
	PERCENT_PASSED=$(($PERCENT_PASSED / $ASSERTS_TOTAL))
else
    PERCENT_PASSED="100"
fi
export PERCENT_PASSED="$PERCENT_PASSED%"

x=$(ls $RESULT_DIR/@Flash_device* 2> /dev/null | egrep -v "html$" | awk 'BEGIN{FS="@"}{print $NF}')
[ "$x" ] && B2G_BUILD_NAME="$x" || B2G_BUILD_NAME="(unspecified)"

f_sub_variables_into_webpage    page_title          \
                                JOB_NAME            \
                                BUILD_NUMBER        \
                                RUN_INPUT_LIST      \
                                B2G_BUILD_NAME      \
                                RUN_TIME            \
                                blocked             \
                                chance2             \
                                EXTRA_SETUP_DETAILS \
                                SUMMARIES           \
                                END_TIME            \
                                UNEX_PASSES         \
                                UNEX_FAILS          \
                                EX_FAILS            \
                                EX_PASSES           \
                                ASSERTS_PASSED      \
                                ASSERTS_TOTAL       \
                                IGNORED             \
                                UNWRITTEN           \
                                BUILD_RESULT        \
                                PERCENT_PASSED      
                                

#
# Convert the run detail pages into html.
#
ls $RESULT_DIR/*_detail 2>/dev/null | while read fnam
do
    f_convert_textfile_to_html $fnam
done

    
##########################################################################
#
# CSS FILE
#
cp $0.parts/run_html.css $RESULT_DIR



##########################################################################
#
# COPY EVERYTHING INTO THE HTML_FILEDIR.
#
cd $RESULT_DIR
cp * $HTML_FILEDIR 2> /dev/null
sudo chmod 755 $HTML_FILEDIR

#
# Output the web page link.
#
if [ "$FAKE_CI_SERVER" ]
then
    printf "file://%s/index.html" "$HTML_FILEDIR"
else
    printf "$HTML_WEBDIR"
fi


