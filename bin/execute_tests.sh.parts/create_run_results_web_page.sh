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

. $0.parts/setup_dependencies.sh


##########################################################################
#
# Functions ...
#
f_start_summary_table(){
    #
    # Start the summary table.
    #
    echo "
	        <table>
	            <tr>"
	
	if [ "$linkme" ]
	then
		echo "
                    <th class=\"center\">Run details</th>"
	fi
	
	echo " 
                    <th class=\"center\">Test ID</th>
	                <th class=\"center\">Time<br>taken</th>
	                <th class=\"center\">Test<br>actions<br>passed</th>
	                <th                 >Description</th>
	            </tr>"
}

f_add_summary_row(){
	#
    # Add test case summary line.
    #
    
    # Start the row.
    echo "
	            <tr class=\"$rowclass\">"
                    
    # Only add the test run details column if it's relevant.
    if [ "$linkme" ]
    then
        echo "
                    <td class=\"center\"     >
                        <div title=\"$title\">
	                        <a href=\"./${test_num}_detail.html\">
	                            Run details
	                        </a>
	                    </div>
	                </td>
	                "
    fi
    
    # Add the summary info columns.
    echo "
                    <td class=\"center\"     >
                        <div title=\"Click this to see the Jira page for this test case.\">
                            <a href=\"${USER_STORIES_BASEURL}${test_num}\">
                                ${test_num}
                            </a>
                        </div>
                    </td>
	                <td class=\"center\"   >$test_time</td>
	                <td class=\"center\"   >$test_passes / $test_total</td>
	                <td class=\"desc\"     >$test_desc $test_repeat</td>
                </tr>"
}

f_finish_summary_table(){
	#
	# Finish the summary table.
	#
    echo "          </table>"
}

f_create_summary_row(){	
	#
	# Splits the current '$line' into components, decides which css palette to use and creates
	# the table row.
	#
	TYPE="$1"

    test_num=$(     echo "$line" | awk 'BEGIN{FS="\t"}{print $1}')
    test_failed=$(  echo "$line" | awk 'BEGIN{FS="\t"}{print $2}')
    test_passes=$(  echo "$line" | awk 'BEGIN{FS="\t"}{print $3}')
    test_total=$(   echo "$line" | awk 'BEGIN{FS="\t"}{print $4}')
    test_desc=$(    echo "$line" | awk 'BEGIN{FS="\t"}{print $5}'| sed -e "s/\(blocked\)/<b>\1<\/b>/I")
    test_time=$(    echo "$line" | awk 'BEGIN{FS="\t"}{print $6}')
    
    #
    # Color this row depending on what happened.
    #
    title="Click this to see the test run details."
    if [ "$test_failed" ]
    then
        if [ "$test_failed" = "$IGNORED_TEST_STR" ]
        then
            rowclass="ignored"
            title="This test was ignored."
        elif [ "$test_failed" = "$NO_TEST_STR" ]
        then
            rowclass="no_test"
            title="This test has not been automated yet."
        else
            rowclass="failed"
        fi
    else
        rowclass="passed"
    fi
    
    #
    # Create the summary row if this is the 'type' we are wanting this time.
    #
    [ "$TYPE" = "$rowclass" ] && f_add_summary_row
}

f_create_summary_table(){
	#
	# Creates a summary table for this "$TYPE"
	#
	TYPE="$1"
	DESC="$2"
	
	#
	# Only create the 'run detail' column if it's relevant.
	#
	if [ "$TYPE" = "passed" ] || [ "$TYPE" = "failed" ]
	then
		linkme="Y"
	else
        linkme=""
    fi

    #
    # Create the rows first (so we can test if we have any before creating a
    # header for nothing).
    #
    cat $HTML_SUMMARIES | while read line
    do
        f_create_summary_row "$TYPE"
    done > $HTML_INDEX.tmp
    
    #
    # Now build the table (if we have anything to build).
    #
    x=$(wc -l $HTML_INDEX.tmp 2>/dev/null | awk '{print $1}')
    if [ "$x" -gt 0 ]
    then
    	echo "
            <tr class=\"items\">
                <th colspan=2 class=\"items\" 
                    onclick=\"toggleVisibility('$TYPE')\">
                    $DESC
                </th>
            </tr>
            <tr id=\"$TYPE\" class=\"item_table\" style=\"display:none\">
                <td class=\"blank\"></td><td>"
	
		f_start_summary_table
		cat $HTML_INDEX.tmp
		rm $HTML_INDEX.tmp
		f_finish_summary_table

        echo "
                </td>
            </tr>"
    else
        echo "
            <tr class=\"items\"><th class=\"items_none\">$DESC</th></tr>"
    fi
}

##########################################################################
#
# START THE HTML PAGE.
#

#
# Build dynamic list of other installation details.
#
DYNAMIC_LIST=""
while read fnam
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
    
    logtitle=$(echo $logHead | sed -e "s/_/ /g")
    logdesc=$( echo $logDets | sed -e "s/_/ /g")

    DYNAMIC_LIST="$DYNAMIC_LIST
            <tr class=\"install\">
                <th class=\"install\">$logtitle:</th>
                <td>
                    <div title=\"Click this to see the details of this part of the installation.\">
                        <a href=\"./$logname\">
                        $logdesc
                        </a>
                    </div>
                </td>
            </tr>"

done <<EOF
$(ls -lrt $RESULT_DIR/@* | awk '{print $NF}')
EOF

#
# SUMMARY DETAILS TABLES.
#  

#
# Process the summaries.
#
SUMMARIES="$(f_create_summary_table 'failed'  'Failed test cases')"
SUMMARIES="$SUMMARIES $(f_create_summary_table 'passed'  'Passed test cases')"
SUMMARIES="$SUMMARIES $(f_create_summary_table 'ignored' 'Ignored test cases.')"
SUMMARIES="$SUMMARIES $(f_create_summary_table 'no_test' 'Test cases which have not been automated yet.')"



#
# Build the run details web page by substituting the variables into the template.
#
# (NOTE: for now, every variable that needs to be substituted has to be listed here.)
#
. $0.parts/f_sub_variables_into_webpage.sh
f_sub_variables_into_webpage JOB_NAME BUILD_NUMBER RUN_TIME blocked chance2 DYNAMIC_LIST SUMMARIES


##########################################################################
#
# DETAIL HTML PAGES
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
cp $0.parts/run_html.css $RESULT_DIR



##########################################################################
#
# COPY EVERYTHING INTO THE HTML_FILEDIR.
#
cd $RESULT_DIR
cp * $HTML_FILEDIR 2> /dev/null

#
# Output the web page link.
#
printf "$HTML_WEBDIR"


