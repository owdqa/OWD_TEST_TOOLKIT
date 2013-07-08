#
# Add test case summary line.
#

TEST_ID="<td class=\"center\"     >
                        <div title=\"Click this to see the Jira page for this test case.\">
                            <a href=\"${USER_STORIES_BASEURL}${test_num}\">
                                ${test_num}
                            </a>
                        </div>
                    </td>"


RUN_DETAILS="<td class=\"center\"     >
                        <div title=\"$title\">
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
                    <td class=\"center\"   >$test_time</td>
                    <td class=\"center\"   >$test_passes / $test_total</td>
                    <td class=\"desc\"     >$test_desc $test_repeat</td>
                </tr>"

else
    #
    # This test was not executed, so just report the Jira link and
    # test description.
    #
    echo "
                <tr class=\"$rowclass\">
                    ${TEST_ID}
                    <td class=\"desc\"     >$test_desc $test_repeat</td>
                </tr>"
fi
