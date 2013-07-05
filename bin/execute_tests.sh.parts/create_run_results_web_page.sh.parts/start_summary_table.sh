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
