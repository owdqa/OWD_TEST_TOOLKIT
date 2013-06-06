WARNING: USING THESE TESTS WILL RESULT IN ALL DATA BEING REMOVED FROM THE DEVICE!
=================================================================================



Installation
============

<b>1.</b> Install pre-requisites on your machine: 

<table>
  <tr> 
       <th>Requirement </th> 
       <th>OS          </th>     
       <th>Instructions</th> 
  </tr>
  <tr> 
       <td align=center><b>Git        </td> 
       <td align=center>All           </td>     
       <td align=left>http://git-scm.com/downloads</td>
  </tr>

  <tr> 
      <td rowspan=2 align=center><b>Python 2.7 </b></td> 
      <td align=center>Ubuntu                      </td>     
      <td align=left>
<pre>
sudo add-apt-repository ppa:fkrull/deadsnakes
sudo apt-get update
sudo apt-get install python2.7
</pre>
      </td> 
  </tr>
  <tr>
       <td align=center>Others    </td>     
       <td align=left>http://www.python.org/getit/</td> 
  </tr>

  <tr> 
       <td rowspan=2 align=center><b>ADB</b></td> 
       <td align=center>Ubuntu    </td>     
       <td align=left>
<pre>
sudo add-apt-repository ppa:nilarimogard/webupd8
sudo apt-get update
sudo apt-get install android-tools-adb android-tools-fastboot
</pre>
       </td>
  </tr>
  <tr>
       <td align=center>Others    </td>     
       <td align=left>http://www.google.com (sorry! ;o)</td> 
  </tr>
</table>

<b>2.</b> From a terminal, go to the directory you want the test toolkit to be in ("cd ~/projects" for example) then type:

<pre>
./install.sh
</pre>

<b>3.</b> You may want to add the *OWD_TEST_TOOLKIT/bin* folder to your PATH variable (makes it easier to use the scrtips in there):

(perhaps add this to your ~/.bashrc or ~/.profile file)
<pre>
export PATH="$PATH:/path/to/OWD_TEST_TOOLKIT"
</pre>


Creating a new test suite
=========================

<b>1.</b> The *./example* folder contains a working test for you to examine, adapt, copy etc... Copy the *./example/* folder to the destination for your new tests:

<pre>
cd OWD_TEST_TOOLKIT
cp -r ./example ../owd_mytests
cd ../owd_mytests
</pre>

<b>2.</b> Use the *./tests/test_01.py* as a template for developing your own tests (they must be in this *./tests* folder and called "test_*whatever*.py").


Running tests
=============

<b>1.</b> Make sure your device has been flashed with an 'eng' build (the 'user' build won't allow Marionette to run and the tests won't work). In the *OWD_TEST_TOOLKIT/bin* folder, type:
<pre>
sudo flash_device <i>Device</i> eng <i>branch</i>
</pre>

... for example:

<pre>
sudo flash_device unagi eng v1-train
</pre>


<b>2.</b> Make sure 'remote debugging' is *OFF* on your device (it must be like this for 'eng' builds):

*Settings > Device Information > More Information >  Developer > Remote debugging*


<b>3.</b> To run all tests, from your test folder (e.g. *owd_mytests/*) type:

<pre>
./run_tests
</pre>

... or specify particular tests. For example, this :

<pre>
./run_tests 0178 make_a_contact bugfix124
</pre>

... will run the tests from the files *test_0178.py*, *test_make_a_contact.py* and *test_bugfix124.py*.

... or specify particular test 'types' :

<pre>
./run_tests {REGRESSION}
</pre>

<b>4.</b> As each test is completed, a summary line (description / result) will be displayed. Once all tests have completed the overall test results will be displayed.

To see full details of the test run for a particular test case - in the *OWD_TEST_TOOLKIT/bin* folder, type:

<pre>
show_latest_test_run_details *<test name>*
</pre>


Some notes on running "run_tests" ...
-------------------------------------

You will be prompted for any input values required by the tests you have chosen (i.e. anything using *self.UTILS.get_os_variable()*).

* If you these values are stored in the file *$HOME/.OWD_TEST_PARAMETERS*, then you will not be prompted for them.

* If you specify the number of the device itself for sms tests, then they may timeout (because as soon as the device sends a text, the response is received and read so the statusbar notification for that response never happens). It is advisable, therefore, to use the number of a different device for sms tests.

