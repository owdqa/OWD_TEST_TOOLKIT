f_create_summary_table(){   
    #
    # Creates a summary table for this "$TYPE"
    #
    TYPE="$1"

    #
    # create relevant variables for this TYPE.
    #
    unexpected_fail=""
    case "$TYPE" in
    	"1")
            TYPE="$UNEX_FAILS_STR"
            COUNT=${UNEX_FAILS:-0}
            linkme="Y"
            pass_or_fail="fail"
            unexpected_fail="unexpected_fail"
            tooltip="Unexpected failures - please investigate."
            DESC="unexpected failures";;
        "2")
            TYPE="$UNEX_PASSES_STR"
            COUNT=${UNEX_PASSES:-0}
            linkme="Y"
            pass_or_fail="pass"
            tooltip="We were expecting these to fail - if any test cases are listed here, please investigate."
            DESC="unexpected passes";;
    	"3")
            TYPE="$EX_FAILS_STR"
            COUNT=${EX_FAILS:-0}
            linkme="Y"
            pass_or_fail="fail"
            tooltip="Expected failures (blocked by other bugs etc...)."
            DESC="expected failures";;
        "4")
            TYPE="$EX_PASSES_STR"
            COUNT=${EX_PASSES:-0}
            linkme="Y"
            pass_or_fail="pass"
            tooltip="Test cases which passed."
            DESC="expected passes";;
        "5")
            TYPE="$IGNORED_STR"
            COUNT=${IGNORED:-0}
            linkme=""
            pass_or_fail="neutral"
            tooltip="Test cases we ignored during this run."
            DESC="ignored test cases";;
        "6")
            TYPE="$UNWRITTEN_STR"
            COUNT=${UNWRITTEN:-0}
            linkme=""
            pass_or_fail="neutral"
            tooltip="Test cases that have not been automated yet."
            DESC="unwritten test cases";;
    esac
            
    DESC="$COUNT $DESC"

    #
    # Create the summary tabs first.
    #
    cat $HTML_SUMMARIES | while read line
    do
        . $0.parts/create_summary_detail_row.sh
    done > $HTML_INDEX.tmp
    
    #
    # Now add the summary row for this type.
    #    
    x=$(wc -l $HTML_INDEX.tmp 2>/dev/null | awk '{print $1}')
    if [ "$x" -gt 0 ]
    then
    	#
    	# We have some details for this type, so create the details table
    	# as well as the type header.
    	#
        echo "
            <tr>
                <td class=\"summary_type $unexpected_fail with_data\" 
                    onclick=\"toggleVisibility('$TYPE')\"
                    title=\"$tooltip\">
                        $DESC
                </td>
            </tr>
            <tr><td></td></tr>
            <tr id=\"$TYPE\" class=\"summary_table\" style=\"display:none\">
                <td class=\"summary_table\">"
        
        #
        # Create the run details table and close this row.
        #
        . $0.parts/create_summary_detail_table.sh

    else
        #
        # Nothing to report for this type, so just create the
        # type header.
        #
        echo "
            <tr>
                <td class=\"summary_type without_data\" title=\"$tooltip\">
                    $DESC
                </td>
            </tr>
            <tr><td></td></tr>$extra_row"
    fi
}

#
# Now 'do it' for these various types ...
#
SUMMARIES=""
for i in {1..6}
do
    SUMMARIES="$SUMMARIES $(f_create_summary_table $i)"
done
