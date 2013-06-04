#Notes about creating tests

<b>1.</b> Copy this entire folder to the area you will develop your tests from, for example:

<pre>
cp -r example $HOME/projects/my_tests
</pre>

<b>2.</b> Change directory to <i>you copy of the example folder</i> (do not develop your tests in the example folder within the OWD_TEST_TOOLKIT, or they will be lost when you refresh this repo!!).

<pre>
cd $HOME/projects/my_tests
</pre>

<b>3.</b> In the "./run_tests.sh" script, set the <i>OWDToolkit</i> variable to point to your copy of the OWD_TEST_TOOLKIT.

<b>4.</b> Use the "./tests/test01.py" script as a template for developing your test cases ...

* Each script must be called "test_<i>*whatever*</i>.py".
* The description for this test must be defined with <b>_Description = ""</b> as it is in test01.py (this is used by the test reporter, as well as by the "bin/refresh_READ.sh" scripts).
* Sections marked (MANDATORY) should be left as they are.
* Use only one 'test_run' method (gaiatest will handle more than one, but the OWD_TEST_TOOLKIT will not report correctly if you do).
* The scripts have 3 main methods:
<table>
<tr><th>setUp</th><td>Actions to be performed before this test case is run.</td></tr>
<tr><th>tearDown</th><td>Actions to be performed after this test case has been run.</td></tr>
<tr><th>test_run</th><td>The test case actions to be perfromed.<br><i>Warning: any method called "test_*" will be treated as a separate test case by gaiatest, so make sure you only have this one!</i></td></tr>
</table>

<b>5.</b> Use the tests/resources folder for items like images etc... that you might want to push to the device. This folder can be anywhere you like (you specify the folder when you specify the file to be pushed), it's just put here as an example.

<b>6.</b> Use the tests/mocks folder for mock data - an example has been put here showing how to structure a mock contact.

<b>7.</b> Once you have created your test cases, use the "./run_tests.sh" script to execute them:

Execute <i>all</i> test cases:
<pre>
./run_tests.sh
</pre>

Execute <i>specific</i> test cases:
<pre>
./run_tests.sh 01 04 12
</pre>

<b>8.</b> To see details of a test run for a test case, use "<i>path/to/OWD_TEST_TOOLKIT</i>/bin/show_latest_test_run_details.sh <i>*test case*</i>". For example:
<pre>
$HOME/projects/OWD_TEST_TOOLKIT/bin/show_latest_test_run_details.sh 04
</pre>



* At the end of your README.md file, include the code below this line (look at the source code of this file because you need the 'testcoverage' tag) to get a table of tests covered which will be automatically refreshed and updated when you use "push_changes_to_repo.sh":

<!--testcoverage-->
TESTS COVERED
=============
<table>
  <tr>
    <th>Test Case</th><th>Description</th>
  </tr>

  <tr>
    <td  align=center>01</td><td  align=left>Create a contact via the contacts app.</td>
  </tr>

</table>

