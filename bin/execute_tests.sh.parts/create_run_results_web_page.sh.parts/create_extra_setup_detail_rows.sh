#
# Build dynamic list of other installation details.
#
EXTRA_SETUP_DETAILS=""
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

    EXTRA_SETUP_DETAILS="$EXTRA_SETUP_DETAILS
            <tr class=\"install\">
                <th class=\"install normal\">$logtitle:</th>
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
