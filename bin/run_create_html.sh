#!/bin/bash
#
# Script to create the html summary file etc...
#
# NOTE: This is intended to be run via the 'run_all_tests.sh' script.
#
. $OWD_TEST_TOOLKIT_BIN/run_common_functions.sh

#
# This is where the test run details will be put.
#
RUN_DIR=$(basename $RESULT_DIR)
OUTDIR=/var/www/html/owd_tests/$RUN_DIR
OUTHTML="http://owd-qa-server/owd_tests/$RUN_DIR"
export SUMMARY_HTML=$RESULT_DIR/index.html

if [ ! -d "$OUTDIR" ]
then
	sudo mkdir -p $OUTDIR
	sudo chmod 777 $OUTDIR
fi

##########################################################################
#
# SUMMARY HTML PAGE.
#

#
# HTML file header.
#
echo "<html>
    <head>
        <base target=\"_blank\">
        <link rel="stylesheet" type="text/css" href="run_html.css">
    </head>
    <body>
        <h1>Results summary for test run id $RUN_ID</h1>
        <h2>($RUN_TIME)</h2>
" > $SUMMARY_HTML



#
# Summary details in a table.
#
echo "
        <table>
            <tr>
                <th               >Test ID</th>
                <th               >Time<br>taken</th>
                <th               >Test<br>actions<br>passed</th>
                <th class=\"desc\">Description</th>
            </tr>" >> $SUMMARY_HTML

#
# Put the FAILED tests at the top so they're quick to debug.
#
sort -t$'\t' -k2,2r -k1,1 $HTML_LINES | while read line
do
	f_split_run_details "$line"
	
	#
	# Make 'Blocked' bold so it's clear.
	#
	test_desc=$(echo "$test_desc" | sed -e "s/\(blocked\)/<b>\1<\/b>/I")
	
	[ "$test_failed" ] && rowclass="failed" || rowclass="passed"
	
    #
    # Add test case summary line.
    #
    echo "
            <tr class=\"$rowclass\">
                <td class=\"id\"     >
                    <div title=\"Click this to see the test run details.\">
	                    <a href=\"./${test_num}_detail.html\">
	                        ${test_num}
	                    </a>
                    </div>
                </td>
                <td class=\"time\"   >$test_time</td>
                <td class=\"results\">$test_passes / $test_total</td>
                <td class=\"desc\"   >$test_desc $test_repeat</td>
            </tr>" >> $SUMMARY_HTML
done

echo "        </table>       
    </body>
</html>
" >> $SUMMARY_HTML


##########################################################################
#
# DETAIL HTML PAGE
#
#
# Copy all the detail files to be htmls.
#
ls $RESULT_DIR/*_detail | while read fnam
do
	#
	# Add some header info.
	#
    echo "<html>
    <head>
        <base target=\"_blank\">
        <link rel="stylesheet" type="text/css" href="run_html.css">
    </head>
    <body class=\"details\">" > $fnam.html
    
    #
    # Put the file contents in the html (change newlines to html code etc...).
    #
    sed -e "s/$/<br>/" $fnam | \
    sed -e "s/ /\&nbsp/g"    | \
    sed -e "s,\("$RESULT_DIR"\/\)\([^<]*\),<a href=\"\2\">"$OUTHTML"\2<\/a>,g"  >> $fnam.html
    	
	#
	# Finish the file off.
	#
	echo "
	</body>
</html>" >> $fnam.html
	
done
    
##########################################################################
#
# CSS FILE
#
cp $OWD_TEST_TOOLKIT_BIN/run_html.css $RESULT_DIR



##########################################################################
#
# COPY EVERYTHING INTO THE OUTDIR.
#
cd $RESULT_DIR
cp * $OUTDIR 2> /dev/null

printf "\nTo analyse the details of this run, navigate to: $OUTHTML\n\n"