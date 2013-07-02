#!/bin/bash
#
# Script to create the html summary file etc...
#
# NOTE: This is intended to be run via the 'run_all_tests.sh' script
# and only works on the CI server (or if "$INSTALL_LOG" is set).
#
[ ! "$INSTALL_LOG" ] && exit

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
# HEADER
#
echo "<html>
    <head>
        <base target=\"_blank\">
        <link rel="stylesheet" type="text/css" href="run_html.css">
    </head>
    <body>
" > $HTML_INDEX



#
# INSTALLATION DETAILS.
#
[ "$OWD_NO_BLOCKED" ] && blocked="No" || blocked="Yes"
[ "$OWD_USE_2ND_CHANCE" ] && chance2="Yes" || chance2="No"
echo "
        <table>
            <tr class=\"install\"><th class=\"install\">JOB NAME:</th><td class=\"job\">$JOB_NAME</td></tr>
            <tr class=\"install\"><th class=\"install\">BUILD NUMBER:</th><td class=\"job\">$BUILD_NUMBER</td></tr>
            <tr class=\"install\"><th class=\"install\">Run time:</th><td>$RUN_TIME</td></tr>
            <tr class=\"install\"><th class=\"install\">Run blocked tests:</th><td>$blocked</td></tr>
            <tr class=\"install\"><th class=\"install\">Try fails twice:</th><td>$chance2</td></tr>" >> $HTML_INDEX
        
ls -lrt $INSTALL_LOG* | awk '{print $NF}' | while read fnam
do
	tmp=$(basename $fnam)
    logHead=$(echo $tmp | awk 'BEGIN{FS="@"}{print $2}')
    logDets=$(echo $tmp | awk 'BEGIN{FS="@"}{print $3}')
    logfile=$HTML_FILEDIR/$logHead.html
    logname=$(basename $logfile)

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
    
    logtitle=$(echo $logHead | sed -e "s/_/ /g")
    logdesc=$( echo $logDets | sed -e "s/_/ /g")

    echo "
            <tr class=\"install\">
                <th class=\"install\">$logtitle:</th>
                <td>
                    <div title=\"Click this to see the details of this part of the installation.\">
                        <a href=\"./$logname\">
                        $logdesc
                        </a>
                    </div>
                </td>
            </tr>" >> $HTML_INDEX

done

# Close the table.
echo "        </table><br>" >> $HTML_INDEX


#
# SUMMARY DETAILS.
#  
echo "
        <table>
            <tr>
                <th class=\"center\">Test ID</th>
                <th class=\"center\">Time<br>taken</th>
                <th class=\"center\">Test<br>actions<br>passed</th>
                <th                 >Description</th>
            </tr>" >> $HTML_INDEX

#
# Put the FAILED tests at the top so they're quick to debug.
#
cat $HTML_SUMMARIES | while read line
do
    test_num=$(     echo "$line" | awk 'BEGIN{FS="\t"}{print $1}')
    test_failed=$(  echo "$line" | awk 'BEGIN{FS="\t"}{print $2}')
    test_passes=$(  echo "$line" | awk 'BEGIN{FS="\t"}{print $3}')
    test_total=$(   echo "$line" | awk 'BEGIN{FS="\t"}{print $4}')
    test_desc=$(    echo "$line" | awk 'BEGIN{FS="\t"}{print $5}')
    test_time=$(    echo "$line" | awk 'BEGIN{FS="\t"}{print $6}')
	
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
                <td class=\"center\"     >
                    <div title=\"Click this to see the test run details.\">
	                    <a href=\"./${test_num}_detail.html\">
	                        ${test_num}
	                    </a>
                    </div>
                </td>
                <td class=\"center\"   >$test_time</td>
                <td class=\"center\"   >$test_passes / $test_total</td>
                <td class=\"desc\"     >$test_desc $test_repeat</td>
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
    sed -e "s/$/<br>/" $fnam              | \
    sed -e "s/ /\&nbsp/g"                 | \
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
