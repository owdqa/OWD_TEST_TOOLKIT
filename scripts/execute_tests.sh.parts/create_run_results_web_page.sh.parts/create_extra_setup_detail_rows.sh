#
# Build dynamic list of other installation details (in the order that they happened).
#

TMP_ROWS=""
counter=0
total_success=0
while read fnam
do
	counter=$(($counter+1))
	fnam_base=$(basename $fnam)
    logHead=$(echo $fnam_base | awk 'BEGIN{FS="@"}{print $2}')
    logDets=$(echo $fnam_base | awk 'BEGIN{FS="@"}{print $3}')
    linkFile=${logHead}.html

    #
    # Turn this result file into an html file.
    #
    f_convert_textfile_to_html $fnam
    cp $fnam.html ${HTML_FILEDIR}/$linkFile

    #
    # Split the filename into title and description parts.
    #
    logtitle=$(echo $logHead | sed -e "s/_/ /g")
    logdesc=$( echo $logDets | sed -e "s/_/ /g")

    #
	# Check for warnings.
	#
	setup_success="setup_ok"
	title_str="Click this to see the details of this part of the installation."
	x=$(egrep -i "error|warning" $fnam | grep -v "OWDTestToolkit")
	if [ "$x" ]
	then
		setup_success="setup_warnings"
		total_success=1
		title_str="WARNING: Possible issues were reported during this part of the installation."
	fi
	    
    TMP_ROWS="$TMP_ROWS
                        <tr class=\"$setup_success\">
                            <td class=\"left\"><b>$counter.</b> $logtitle</td>
                            <td class=\"center\">:</td>
                            <td class=\"build_detail left\">
                                <div title=\"$title_str\">
                                    <a href=\"./$linkFile\">
                                    $logdesc
                                    </a>
                                </div>
                            </td>
                        </tr>"

done <<EOF
$(ls -lrt $RESULT_DIR/@* | egrep -v "\.html$" | awk '{print $NF}')
EOF

if [ "$total_success" = "0" ]
then
    extra_info_success="extra_info_ok"
else
    warning_str="<br><br><span style=\"color:#ff0000\">(<b>WARNING:</b> possible issues detected!)</span>"
    extra_info_success="extra_info_warnings"
fi

EXTRA_SETUP_DETAILS="
            <tr>
                <td class=\"$extra_info_success\" colspan=2>
                    <div style=\"cursor:pointer;padding:5px;\"
                         onclick=\"toggleVisibility('setup_details')\"
                         title=\"Click here to see the setup and installation results.\">
                        Click here to show / hide installation and setup details $warning_str
                    </div>
                    <table class=\"summary_table extra_info\" id=\"setup_details\" style=\"display:none\">
                       <tr class=\"invisible\"><td> </td></tr>
                       $TMP_ROWS
                       </tr>
                    </table>
                </td>
            </tr>"
                    