# Notes about using 'utils' classes

To implement these, put this in the import section of your code:

<pre>
from OWDTestToolkit import *
</pre>

Then in the 'setUp() method of your code, put:

<pre>
self.UTILS   = UTILS(self)
</pre>

Then you can use these methods in your code like this:

<pre>
self.UTILS.TEST(True, "I am using the utils classes!")
</pre>


<!--api-->
<table>
  <tr>
    <th>Method</th><th>Parameters and defaults</th><th>Description</th>
  </tr>

    <tr>
        <td align=center>quitTest</td>
        <td align=left>p_msg=False</td>
        <td align=left>Quit this test suite.</td>
    </tr>


    <tr>
        <td align=center>TEST</td>
        <td align=left>p_result<br>p_msg<br>p_stop = False</td>
        <td align=left>Test that p_result is true.   One advantage of this over the standard 'assert's is that  this continues past a failure if p_stop is False.  However, it also takes a screenshot and dumps the html source  if p_result is False.</td>
    </tr>


    <tr>
        <td align=center>switchToFrame</td>
        <td align=left>p_attrib<br>p_str<br>p_quitOnError=True<br>p_viaRootFrame=True</td>
        <td align=left>Switch to the iframe containing the attribute value <b>p_str</b>.<br>  For example: ("src", "contacts") or ("src", "sms") etc...<br><br>  NOTE: You *usually* need to do this via the 'root' frame (almost all iframes  are contained in the root-level frame).</td>
    </tr>


    <tr>
        <td align=center>currentIframe</td>
        <td align=left>p_attribute="src"</td>
        <td align=left>Returns the "src" attribute of the current iframe  (very useful if you need to return to this iframe).<br>  The 'p_attribute' is the attribute that would contain  this url.</td>
    </tr>


    <tr>
        <td align=center>viewAllIframes</td>
        <td align=left></td>
        <td align=left>DEV TOOL: this will loop through every iframe,  report all attributes ("src","id" etc...), take a screenshot and capture the html.   Because this is only meant as a dev aid (and shouldn't be in any released test  scripts), it reports to ERROR instead of COMMENT.</td>
    </tr>


    <tr>
        <td align=center>scrollHomescreenRight</td>
        <td align=left></td>
        <td align=left>Scroll to next page (right).  Should change this to use marionette.flick() when it works.</td>
    </tr>


    <tr>
        <td align=center>goHome</td>
        <td align=left></td>
        <td align=left>Return to the home screen.</td>
    </tr>


    <tr>
        <td align=center>scrollHomescreenLeft</td>
        <td align=left></td>
        <td align=left>Scroll to previous page (left).  Should change this to use marionette.flick() when it works.</td>
    </tr>


    <tr>
        <td align=center>touchHomeButton</td>
        <td align=left></td>
        <td align=left>Touch the home button (sometimes does something different to going home).</td>
    </tr>


    <tr>
        <td align=center>holdHomeButton</td>
        <td align=left></td>
        <td align=left>Long hold the home button to bring up the 'current running apps'.</td>
    </tr>


    <tr>
        <td align=center>findAppIcon</td>
        <td align=left>p_appName<br>p_reloadHome=True</td>
        <td align=left>Scroll around the homescreen until we find our app icon.</td>
    </tr>


    <tr>
        <td align=center>launchAppViaHomescreen</td>
        <td align=left>p_appName</td>
        <td align=left>Launch an app via the homescreen.</td>
    </tr>


    <tr>
        <td align=center>isAppInstalled</td>
        <td align=left>p_appName</td>
        <td align=left>Return whether an app is present on the homescreen (i.e. 'installed').</td>
    </tr>


    <tr>
        <td align=center>uninstallApp</td>
        <td align=left>p_appName</td>
        <td align=left>Remove an app using the UI.</td>
    </tr>


    <tr>
        <td align=center>setPermission</td>
        <td align=left>p_app<br>p_item<br>p_val<br>p_silent=False</td>
        <td align=left>Just a container function to catch any issues when using gaiatest's  'set_permission()' function.</td>
    </tr>


    <tr>
        <td align=center>displayStatusBar</td>
        <td align=left></td>
        <td align=left>Displays the status / notification bar in the home screen.   The only reliable way I have to do this at the moment is via JS  (tapping it only worked sometimes).</td>
    </tr>


    <tr>
        <td align=center>isIconInStatusBar</td>
        <td align=left>p_dom<br>p_returnFrame=False</td>
        <td align=left>Check an icon is in the statusbar, then return to the  given frame (doesn't wait, just expects it to be there).</td>
    </tr>


    <tr>
        <td align=center>hideStatusBar</td>
        <td align=left></td>
        <td align=left>Displays the status / notification bar in the home screen.   The only reliable way I have to do this at the moment is via JS  (tapping it only worked sometimes).</td>
    </tr>


    <tr>
        <td align=center>clearAllStatusBarNotifs</td>
        <td align=left>p_silent=False</td>
        <td align=left>Opens the statusbar, presses "Clear all", then closes the status bar.<br>  <b>p_silent</b> will supress any pass/fail (useful if this isn't relevant  to the test, or if you're just using it for a bit of housekeeping).</td>
    </tr>


    <tr>
        <td align=center>openSettingFromStatusbar</td>
        <td align=left></td>
        <td align=left>As it says on the tin - opens the settings  app via the statusbar.</td>
    </tr>


    <tr>
        <td align=center>waitForStatusBarNew</td>
        <td align=left>p_dom=DOM.Statusbar.status_bar_new<br>p_displayed=True<br>p_timeOut=20</td>
        <td align=left>Waits for a new notification in the status bar (20s timeout by default).</td>
    </tr>


    <tr>
        <td align=center>toggleViaStatusBar</td>
        <td align=left>p_type</td>
        <td align=left>Uses the statusbar to toggle items on or off.<br>  <b>NOTE:</b> Doesn't care if it's toggling items ON or OFF. It just toggles!  <br><br>  Accepted 'types' are:<br>  <b>data</b><br>  <b>wifi</b><br>  <b>airplane</b><br>  <b>bluetooth</b></td>
    </tr>


    <tr>
        <td align=center>waitForNetworkItemDisabled</td>
        <td align=left>p_type<br>p_timeOut=60</td>
        <td align=left>Waits for network 'item' to be disabled.  <br><br>  Accepted 'types' are:<br>  <b>data</b><br>  <b>wifi</b><br>  <b>airplane</b><br>  <b>bluetooth</b></td>
    </tr>


    <tr>
        <td align=center>getNetworkConnection</td>
        <td align=left></td>
        <td align=left>Tries several methods to get ANY network connection  (either wifi or dataConn).</td>
    </tr>


    <tr>
        <td align=center>waitForNetworkItemEnabled</td>
        <td align=left>p_type<br>p_timeOut=60</td>
        <td align=left>Waits for network 'item' to be enabled.  <br><br>  Accepted 'types' are:<br>  <b>data</b><br>  <b>wifi</b><br>  <b>airplane</b><br>  <b>bluetooth</b></td>
    </tr>


    <tr>
        <td align=center>disableAllNetworkSettings</td>
        <td align=left></td>
        <td align=left>Turns off all network settings (wifi, dataconn, bluetooth and airplane mode).</td>
    </tr>


    <tr>
        <td align=center>isNetworkTypeEnabled</td>
        <td align=left>p_type</td>
        <td align=left>Returns True or False.<br><br>  Accepted 'types' are:<br>  <b>data</b><br>  <b>wifi</b><br>  <b>airplane</b><br>  <i>bluetooth (**NOT WORKING CURRENTLY!!**)</i></td>
    </tr>


    <tr>
        <td align=center>waitForNotElements</td>
        <td align=left>p_element<br>p_msg<br>p_displayed=True<br>p_timeout=False<br>p_stop=True</td>
        <td align=left>Waits for an element to be displayed and captures the error if not.<br>  p_timeout defaults to _DEFAULT_ELEMENT_TIMEOUT (set in the utils.py file).</td>
    </tr>


    <tr>
        <td align=center>moveScroller</td>
        <td align=left>p_scroller<br>p_forward=True</td>
        <td align=left>Move the scroller back one item.</td>
    </tr>


    <tr>
        <td align=center>getElements</td>
        <td align=left>p_element<br>p_msg<br>p_displayed=True<br>p_timeout=False<br>p_stop=True</td>
        <td align=left>Returns a list of matching elements, or False if none are found.<br>  p_timeout defaults to _DEFAULT_ELEMENT_TIMEOUT (set in the utils.py file).</td>
    </tr>


    <tr>
        <td align=center>getElement</td>
        <td align=left>p_element<br>p_msg<br>p_displayed=True<br>p_timeout=False<br>p_stop=True</td>
        <td align=left>Returns an element, or False it it's not found.<br>  p_timeout defaults to _DEFAULT_ELEMENT_TIMEOUT (set in the utils.py file).</td>
    </tr>


    <tr>
        <td align=center>setScrollerVal</td>
        <td align=left>p_scrollerElement<br>p_number</td>
        <td align=left>Set the numeric value of a scroller (only works with numbers just now).</td>
    </tr>


    <tr>
        <td align=center>headerCheck</td>
        <td align=left>p_str</td>
        <td align=left>Returns the header that matches a string.  NOTE: ALL headers in this iframe return true for ".is_displayed()"!</td>
    </tr>


    <tr>
        <td align=center>waitForElements</td>
        <td align=left>p_element<br>p_msg<br>p_displayed=True<br>p_timeout=False<br>p_stop=True</td>
        <td align=left>Waits for an element to be displayed and captures the error if not.<br>  p_timeout defaults to _DEFAULT_ELEMENT_TIMEOUT (set in the utils.py file).</td>
    </tr>


    <tr>
        <td align=center>screenShot</td>
        <td align=left>p_fileSuffix</td>
        <td align=left>Take a screenshot.</td>
    </tr>


    <tr>
        <td align=center>screenShotOnErr</td>
        <td align=left></td>
        <td align=left>Take a screenshot on error (increments the file number).</td>
    </tr>


    <tr>
        <td align=center>savePageHTML</td>
        <td align=left>p_outfile</td>
        <td align=left>Save the HTML of the current page to the specified file.</td>
    </tr>


    <tr>
        <td align=center>typeThis</td>
        <td align=left>p_element_array<br>p_desc<br>p_str<br>p_no_keyboard=False<br>p_clear=True<br>p_enter=True<br>p_validate=True<br>p_remove_keyboard=True</td>
        <td align=left>Types this string into this element.  If p_no_keyboard = True then it doesn't use the keyboard.  <b>NOTE:</b> If os variable "NO_KEYBOARD" is set (to anything),  then regardless of what you send to this method, it will never  use the keyboard.</td>
    </tr>


    <tr>
        <td align=center>setDeviceDefaults</td>
        <td align=left></td>
        <td align=left>Set the device defaults before testing.</td>
    </tr>


    <tr>
        <td align=center>setupDataConn</td>
        <td align=left></td>
        <td align=left>Set the phone's details for data conn (APN etc...).</td>
    </tr>


    <tr>
        <td align=center>setTimeToNow</td>
        <td align=left>p_continent=False<br>p_city=False</td>
        <td align=left>Set the phone's time (using gaia data_layer instead of the UI).</td>
    </tr>


    <tr>
        <td align=center>get_os_variable</td>
        <td align=left>p_name<br>p_validate=True</td>
        <td align=left>Get a variable from the OS.</td>
    </tr>


    <tr>
        <td align=center>clearGeolocPermission</td>
        <td align=left>p_allow=False</td>
        <td align=left>Since this appers all over the place I've added this  as a common method in UTILS.<br>  This method clears the Geolocation permission dialog  (if necessary) with p_allow.</td>
    </tr>


    <tr>
        <td align=center>setSetting</td>
        <td align=left>p_item<br>p_val<br>p_silent=False</td>
        <td align=left>Just a container function to catch any issues when using gaiatest's  'set_setting()' function.</td>
    </tr>


    <tr>
        <td align=center>addFileToDevice</td>
        <td align=left>p_file<br>count=1<br>destination=''</td>
        <td align=left>Put a file onto the device (path is relative to the dir  you are physically in when running the tests).</td>
    </tr>


    <tr>
        <td align=center>selectFromSystemDialog</td>
        <td align=left>p_str</td>
        <td align=left>Selects an item from a system select box (such as country / timezone etc...).</td>
    </tr>


    <tr>
        <td align=center>switch_24_12</td>
        <td align=left>p_hour</td>
        <td align=left>Switches a 24-hour number to 12-hour format.  Returns array: ["hour" (12 hour format), "ampm"] based on a 24hour "p_hour".</td>
    </tr>


    <tr>
        <td align=center>logComment</td>
        <td align=left>p_str</td>
        <td align=left>Add a comment to the comment array.</td>
    </tr>


    <tr>
        <td align=center>reportResults</td>
        <td align=left></td>
        <td align=left>Clear out 'things' left by previous tests, then  Create the final result file from the result and comment arrays  (run only once, at the end of each test case).</td>
    </tr>


    <tr>
        <td align=center>logResult</td>
        <td align=left>p_result<br>p_msg<br>p_fnam=False</td>
        <td align=left>Add a test result to the result array.  Everything after the first "</td>
    </tr>

</table>
