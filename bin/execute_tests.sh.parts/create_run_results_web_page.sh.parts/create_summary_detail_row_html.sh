#
# Add test case summary line.
#

TEST_ID="<td class=\"center $pass_or_fail\"     >
                        <div title=\"Click this to see the Jira page for this test case.\">
                            <a href=\"${USER_STORIES_BASEURL}${test_num}\">
                                ${test_num}
                            </a>
                        </div>
                    </td>"


RUN_DETAILS="<td class=\"center $pass_or_fail\"     >
                        <div title=\"Click this to see the test run details.\">
                            <a href=\"./${test_num}_detail.html\">
                                Run details
                            </a>
                        </div>
                    </td>"


if [ "$linkme" ]
then
	#
	# This test was executed, so report the full details.
	#
    echo "
                <tr class=\"$rowclass\">
                    ${TEST_ID}
                    ${RUN_DETAILS}
                    <td class=\"center $pass_or_fail\"   >$test_time</td>
                    <td class=\"center $pass_or_fail\"   >$test_passes / $test_total</td>
                    <td class=\"left size10 $pass_or_fail\"     >$test_desc $test_repeat</td>
                </tr>"

else
    #
    # This test was not executed, so just report the Jira link and
    # test description.
    #
    echo "
                <tr class=\"$rowclass\">
                    ${TEST_ID}
                    <td class=\"summary_col left size10 $pass_or_fail\"     >$test_desc $test_repeat</td>
                </tr>"
fi
