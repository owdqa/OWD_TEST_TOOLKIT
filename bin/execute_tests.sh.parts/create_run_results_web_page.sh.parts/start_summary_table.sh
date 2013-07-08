#
# Start the summary table.
#
echo "
            <table>
                <tr>"
    
if [ "$linkme" ]
then
    #
    # This test was executed, so report the full details.
    #
    echo "
                    <th class=\"center\">Test ID</th>
                    <th class=\"center\">Run details</th>
                    <th class=\"center\">Time<br>taken</th>
                    <th class=\"center\">Test<br>actions<br>passed</th>
                    <th                 >Description</th>
                </tr>"
else
    #
    # This test was not executed, so just report the Jira link and
    # test description.
    #
    echo " 
                    <th class=\"center\">Test ID</th>
                    <th                 >Description</th>
                </tr>"
