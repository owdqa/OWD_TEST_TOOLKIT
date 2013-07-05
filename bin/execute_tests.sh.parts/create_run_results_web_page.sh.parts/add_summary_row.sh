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
