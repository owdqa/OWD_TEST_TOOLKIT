#!/bin/bash
#
# Script to create the html summary file etc...
#
# NOTE: This is intended to be run via the 'run_all_tests.sh' script
# and only works on the CI server (or if "$INSTALL_LOG" is set).
#
[ ! "$INSTALL_LOG" ] && exit

. $OWD_TEST_TOOLKIT_BIN/run_common_functions.sh

if [ ! -d "$HTML_FILEDIR" ]
then
	sudo mkdir -p $HTML_FILEDIR
	sudo chmod 777 $HTML_FILEDIR
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
" > $HTML_INDEX



#
# Start the table to display the results nicely.
#
echo "
        <table>" >> $HTML_INDEX

#
# Report the installation details (in order).
#
echo "  <tr class=\"install_log\"><th class=\"install_head\" colspan=4>Installation details ... </td></tr>" >> $HTML_INDEX
counter=1
ls -lrt $INSTALL_LOG* | awk '{print $NF}' | while read fnam
do
    logfile=$HTML_FILEDIR/$(basename $fnam).html

    #
    # Turn this result file into an html file.
    #
    echo "<html>
    <head>
        <base target=\"_blank\">
        <link rel="stylesheet" type="text/css" href="run_html.css">
    </head>
    <body class=\"details\">" > $logfile
    sed -e "s/$/<br>/" $fnam | \
    sed -e "s/ /\&nbsp/g"    >> $logfile
    echo "
    </body>
</html>" >> $logfile

    logname=$(basename $logfile)
    
	
	logdesc=$(echo $fnam | awk 'BEGIN{FS="."}{print $2}')
    logdesc=$(echo $logdesc | sed -e "s/_/ /g")
    echo "  <tr class=\"install_log\">
                <td colspan=4>
                    <div title=\"Click this to see the details.\">
                        <a href=\"./$logname\">
                        <b>${counter}.</b> $logdesc
                        </a>
                    </div>
                </td>
            </tr>" >> $HTML_INDEX
     
     counter=$(($counter+1))

done

#
# 'blank row'.
#
echo "  <tr class=\"install_log\"><td colspan=4> </td></tr>" >> $HTML_INDEX

#
# Start the summary details.
#  
echo "
            <tr>
                <th               >Test ID</th>
                <th               >Time<br>taken</th>
                <th               >Test<br>actions<br>passed</th>
                <th class=\"desc\">Description</th>
            </tr>" >> $HTML_INDEX

#
# Put the FAILED tests at the top so they're quick to debug.
#
sort -t$'\t' -k2,2r -k1,1 $HTML_SUMMARIES | while read line
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
            </tr>" >> $HTML_INDEX
done

echo "        </table>       
    </body>
</html>
" >> $HTML_INDEX


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
    sed -e "s,\("$RESULT_DIR"\/\)\([^<]*\),<a href=\"\2\">"$HTML_WEBDIR"\2<\/a>,g"  >> $fnam.html
    	
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
# COPY EVERYTHING INTO THE HTML_FILEDIR.
#
cd $RESULT_DIR
cp * $HTML_FILEDIR 2> /dev/null
