#
# Start the summary table.
#
echo "
            <table class=\"summary\">
                <tr>"
    
if [ "$linkme" ]
then
    #
    # This test was executed, so report the full details.
    #
    echo "
                    <th class=\"sum_table_header center\">Test ID</th>
                    <th class=\"sum_table_header center\">Run details</th>
                    <th class=\"sum_table_header center\">Time<br>taken</th>
                    <th class=\"sum_table_header center\">Test<br>actions<br>passed</th>
                    <th class=\"sum_table_header\">Description</th>
                </tr>"
else
    #
    # This test was not executed, so just report the Jira link and
    # test description.
    #
    echo " 
                    <th class=\"sum_table_header center\">Test ID</th>
                    <th class=\"sum_table_header\">Description</th>
                </tr>"
fi

#
# Add the rows and finish the table off.
#
cat $HTML_INDEX.tmp
rm $HTML_INDEX.tmp 2>/dev/null

echo "
            </table>
        </td>
    </tr>"
