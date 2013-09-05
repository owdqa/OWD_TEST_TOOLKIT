# Notes about using app classes

To implement these, put this in the import section of your code:

<pre>
from OWDTestToolkit import *
</pre>

Then in the 'setUp() method of your code, put:

<pre>
self.browser   = Browser(self)
</pre>

(... or whatever app you want to use.)

Then you can use these methods in your code like this:

<pre>
self.browser.check_page_loaded("http://www.this_api_works_for_me.com")
</pre>

<!--api-->
#Browser
<table>
  <tr>
    <th>Method</th><th>Parameters and defaults</th><th>Description</th>
  </tr>

    <tr>
        <td align=center>check_page_loaded</td>
        <td align=left>p_url</td>
        <td align=left>Check the page didn't have a problem.</td>
    </tr>


    <tr>
        <td align=center>open_url</td>
        <td align=left>p_url</td>
        <td align=left>Open url.</td>
    </tr>


    <tr>
        <td align=center>waitForPageToFinishLoading</td>
        <td align=left></td>
        <td align=left>Waits for the current url to finish loading.</td>
    </tr>

</table>
#Calculator
<table>
  <tr>
    <th>Method</th><th>Parameters and defaults</th><th>Description</th>
  </tr>

    <tr>
        <td align=center></td>
        <td align=left></td>
        <td align=left></td>
    </tr>

</table>
#Calendar
<table>
  <tr>
    <th>Method</th><th>Parameters and defaults</th><th>Description</th>
  </tr>

    <tr>
        <td align=center>moveMonthViewBy</td>
        <td align=left>p_num</td>
        <td align=left>Switches to month view, then moves 'p_num' months in the future or past (if the p_num is  positive or negative) relative to today.</td>
    </tr>


    <tr>
        <td align=center>changeDay</td>
        <td align=left>p_numDays<br>p_viewType</td>
        <td align=left>Changes the calendar day to a different day relative to 'today' - <b>uses the  month view to do this, then switches back to whichever  view you want (month, week, day)</b>.<br>  <b>p_numDays</b> is a number (can be negative to go back, i.e. -5,-2,1,3,5 etc...).<br>  <b>p_viewType</b> is the calendar view to return to (today / day / week / month)<br>  Returns a modified DateTime object from <i>UTILS.getDateTimeFromEpochSecs()</i>.</td>
    </tr>


    <tr>
        <td align=center>getEventPreview</td>
        <td align=left>p_view<br>p_hour24<br>p_title<br>p_location=False</td>
        <td align=left>Return object for an event in month / week or day view.</td>
    </tr>


    <tr>
        <td align=center>moveDayViewBy</td>
        <td align=left>p_num</td>
        <td align=left>Switches to week view, then moves 'p_num' weeks in the future or past (if the p_num is  positive or negative) relative to today.</td>
    </tr>


    <tr>
        <td align=center>createEvent</td>
        <td align=left></td>
        <td align=left>Create a new event - use 'False' in the following fields if you want to leave them at default:   start date,  end date,  location,  notes</td>
    </tr>


    <tr>
        <td align=center>setView</td>
        <td align=left>p_type</td>
        <td align=left>Set to view type (today / day / week / month).</td>
    </tr>


    <tr>
        <td align=center>moveWeekViewBy</td>
        <td align=left>p_num</td>
        <td align=left>Switches to week view, then moves 'p_num' weeks in the future or past (if the p_num is  positive or negative) relative to today.</td>
    </tr>

</table>
#Camera
<table>
  <tr>
    <th>Method</th><th>Parameters and defaults</th><th>Description</th>
  </tr>

    <tr>
        <td align=center>takePicture</td>
        <td align=left></td>
        <td align=left>Take a picture.</td>
    </tr>


    <tr>
        <td align=center>goToGallery</td>
        <td align=left></td>
        <td align=left>Clicks the Gallery button to switch to the Gallery application  (warning: this will land you in the gallery iframe).</td>
    </tr>


    <tr>
        <td align=center>checkVideoLength</td>
        <td align=left>p_vid_num<br>p_from_SS<br>p_to_SS</td>
        <td align=left>Check the length of a video.</td>
    </tr>


    <tr>
        <td align=center>switchSource</td>
        <td align=left></td>
        <td align=left>Switch between still shot and video.</td>
    </tr>


    <tr>
        <td align=center>clickThumbnail</td>
        <td align=left>p_num</td>
        <td align=left>Click thumbnail.</td>
    </tr>


    <tr>
        <td align=center>recordVideo</td>
        <td align=left>p_length</td>
        <td align=left>Record a video.  p_length is the number of seconds to record for.</td>
    </tr>

</table>
#Clock
<table>
  <tr>
    <th>Method</th><th>Parameters and defaults</th><th>Description</th>
  </tr>

    <tr>
        <td align=center>createAlarm</td>
        <td align=left>p_hour<br>p_min<br>p_label<br>p_repeat="Never"<br>p_sound="Classic Buzz"<br>p_snooze="5 minutes"</td>
        <td align=left>Create a new alarm.</td>
    </tr>


    <tr>
        <td align=center>deleteAllAlarms</td>
        <td align=left></td>
        <td align=left>Deletes all current alarms.</td>
    </tr>


    <tr>
        <td align=center>checkAlarmRingDetails</td>
        <td align=left>p_hour<br>p_min<br>p_label</td>
        <td align=left>Check details of alarm when it rings.   NOTE: the status bar alarm is always 'visible', so you have to manually  wait until the alarm is expected to have started before calling this!</td>
    </tr>


    <tr>
        <td align=center>checkStatusbarIcon</td>
        <td align=left></td>
        <td align=left>Check for the little alarm bell icon in the statusbar of the  homescreen.</td>
    </tr>


    <tr>
        <td align=center>checkAlarmPreview</td>
        <td align=left>p_hour<br>p_min<br>p_ampm<br>p_label<br>p_repeat</td>
        <td align=left>Verify the alarm details in the clock screen.</td>
    </tr>

</table>
#Contacts
<table>
  <tr>
    <th>Method</th><th>Parameters and defaults</th><th>Description</th>
  </tr>

    <tr>
        <td align=center>addAnotherEmailAddress</td>
        <td align=left>p_email_address</td>
        <td align=left>Add a new email address to the contact currnetly being viewed in Edit mode.</td>
    </tr>


    <tr>
        <td align=center>import_ImportAll</td>
        <td align=left></td>
        <td align=left>Assumes you're already in the gmail import screen (after logging in etc...).</td>
    </tr>


    <tr>
        <td align=center>tapSettingsButton</td>
        <td align=left></td>
        <td align=left>Tap the settings button.</td>
    </tr>


    <tr>
        <td align=center>getContactFields</td>
        <td align=left>p_view=False</td>
        <td align=left>Return 3-d array of contact details.  if p_view is set, it will use the DOM specs for the view screen. Otherwise  it will assume you are in the edit screen.</td>
    </tr>


    <tr>
        <td align=center>replaceStr</td>
        <td align=left>p_field<br>p_str</td>
        <td align=left>Replace text in a field (as opposed to just appending to it).</td>
    </tr>


    <tr>
        <td align=center>pressEditContactButton</td>
        <td align=left></td>
        <td align=left>Presses the Edit contact button when vieweing a contact.</td>
    </tr>


    <tr>
        <td align=center>selectSearchResult</td>
        <td align=left>p_contactName</td>
        <td align=left>Select the result of a search</td>
    </tr>


    <tr>
        <td align=center>populateContactFields</td>
        <td align=left>p_contact_json_obj</td>
        <td align=left>Put the contact details into each of the fields.  <br><br>  <b>p_contact_json_obj</b> must be an object in the same format as the  one in ./example/tests/mock_data/contacts.py.</td>
    </tr>


    <tr>
        <td align=center>pressCancelEditButton</td>
        <td align=left></td>
        <td align=left>Presses the Edit contact button when vieweing a contact.</td>
    </tr>


    <tr>
        <td align=center>import_GmailLogin</td>
        <td align=left>p_name<br>p_pass<br>p_clickSignIn=True</td>
        <td align=left>Presses the Settings button, then Gmail, then logs in using  p_name and p_pass (to begin the process of importing contacts).  <br>  If p_clickSignIn is set to True then this method will also click  the Sign in button (defaults to true).  <br>  Returns False if the login failed, else True.</td>
    </tr>


    <tr>
        <td align=center>selectSearchResultSeveralPhones</td>
        <td align=left>p_contactName<br>p_num</td>
        <td align=left>Select the result of a search</td>
    </tr>


    <tr>
        <td align=center>editContact</td>
        <td align=left>p_contact_name<br>p_contact_new_json_obj</td>
        <td align=left>Replace the details of one contact with another via the edit screen.  <br><br>  <b>p_contact_curr_json_obj</b> and <b>p_contact_new_json_obj</b> must  be objects in the same format as the one in  ./example/tests/mock_data/contacts.py (however, only needs the  'name' component is used from the p_contact_curr_json_obj).</td>
    </tr>


    <tr>
        <td align=center>verifyLinked</td>
        <td align=left>p_contact_name<br>p_fb_email</td>
        <td align=left>Verifies that this contact is linked  (assumes we're in the 'all contacts' screen).</td>
    </tr>


    <tr>
        <td align=center>tapLinkContact</td>
        <td align=left></td>
        <td align=left>Press the 'Link contact' button in the view contact details screen.</td>
    </tr>


    <tr>
        <td align=center>deleteContact</td>
        <td align=left>p_fullName</td>
        <td align=left>Deletes a contact.<br>  p_fullName must match the name displayed  in the 'view all contacts' screen (including spaces).</td>
    </tr>


    <tr>
        <td align=center>search</td>
        <td align=left>p_val</td>
        <td align=left>Searches the 'all contacts' screen for p_val  (assumes we're currently in the 'all contacts' screen).</td>
    </tr>


    <tr>
        <td align=center>verifyFieldContents</td>
        <td align=left>p_contact_json_obj<br>p_view=False</td>
        <td align=left>Verify the contents of the contact fields in this screen (assumes  you are in the correct screen since this could be view or edit).  <br><br>  <b>p_contact_json_obj</b> must be an object in the same format as the  one in ./example/tests/mock_data/contacts.py.<br>  <b>p_view</b> selects whether this is the 'view contact' screen or not (defaults to False -> edit screen).</td>
    </tr>


    <tr>
        <td align=center>viewContact</td>
        <td align=left>p_contactName<br>p_HeaderCheck=True</td>
        <td align=left>Navigate to the 'view details' screen for a contact (assumes we are in the  'view all contacts' screen, either from Contacts app, or Dialer app).  <br>  In some cases you don't want this to check the header (if the contact has no name,  or you're just using the given name etc..). In that case, set p_HeaderCheck=False.</td>
    </tr>


    <tr>
        <td align=center>import_HotmailLogin</td>
        <td align=left>p_name<br>p_pass<br>p_clickSignIn=True</td>
        <td align=left>Presses the Settings button in the contacts app, then Hotmail, then logs in using  p_name and p_pass (to begin the process of importing contacts).  <br>  If p_clickSignIn is set to True then this method will also click  the Sign in button (defaults to true).  <br>  Returns False if the login failed, "ALLIMPORTED" if all your contacts are already imported else True.</td>
    </tr>


    <tr>
        <td align=center>startCreateNewContact</td>
        <td align=left></td>
        <td align=left>Open the screen to add a contact.</td>
    </tr>


    <tr>
        <td align=center>addGalleryImageToContact</td>
        <td align=left>p_num</td>
        <td align=left>Adds an image for this contact from the gallery  (assumes we're already in the 'new contact' or  'edit conact' screen, and also that we have already  added an image to the gallery).   self.UTILS.addFileToDevice(p_file, destination='DCIM/100MZLLA')  AppGallery(self).launch()</td>
    </tr>


    <tr>
        <td align=center>populateFields</td>
        <td align=left>p_contact_json_obj</td>
        <td align=left>Put the contact details into the fields (assumes you are in the correct  screen already since this could be create or edit).  <br><br>  <b>p_contact_json_obj</b> must be an object in the same format as the  one in ./example/tests/mock_data/contacts.py.</td>
    </tr>


    <tr>
        <td align=center>checkViewContactDetails</td>
        <td align=left>p_contact_json_obj<br>p_imageCheck = False</td>
        <td align=left>Validate the details of a contact in the 'view contact' screen.  <br><br>  <b>p_contact_json_obj</b> must be an object in the same format as the  one in ./example/tests/mock_data/contacts.py.</td>
    </tr>


    <tr>
        <td align=center>import_toggleSelectContact</td>
        <td align=left>p_num</td>
        <td align=left>Toggles select / de-select a gmail contact( marionette doesn't work here yet, so use JS).  p_num is the actualt contact number (1 -> x).</td>
    </tr>


    <tr>
        <td align=center>enableFBImport</td>
        <td align=left></td>
        <td align=left>Enable fb import.</td>
    </tr>


    <tr>
        <td align=center>countEmailAddressesWhileEditing</td>
        <td align=left></td>
        <td align=left>Count the emails and return the number - assumes you  are currently EDITING the contact (not viewing).</td>
    </tr>


    <tr>
        <td align=center>checkEditContactDetails</td>
        <td align=left>p_contact_json_obj</td>
        <td align=left>Validate the details of a contact in the 'view contact' screen.   p_contact_json_obj must be an object in the same format as the  one in ./example/tests/mock_data/contacts.py.</td>
    </tr>


    <tr>
        <td align=center>changeVal</td>
        <td align=left>p_contact_name<br>p_field<br>p_newVal</td>
        <td align=left>Change a value for a contact (assumes we're looking at the 'all contacts' screen  currently).</td>
    </tr>


    <tr>
        <td align=center>switchToFacebook</td>
        <td align=left></td>
        <td align=left><i>Private</i> function to handle the iframe hop-scotch involved in  finding the facebook app launched via contacts app.</td>
    </tr>


    <tr>
        <td align=center>checkMatch</td>
        <td align=left>p_el<br>p_val<br>p_name</td>
        <td align=left>Test for a match between an element and a string  (found I was doing this rather a lot so it's better in a function).</td>
    </tr>


    <tr>
        <td align=center>pressDeleteContactButton</td>
        <td align=left></td>
        <td align=left>In it's own function just to save time figuring out  that you have to get the button into view before you  can press it, then re-align the screen again.</td>
    </tr>


    <tr>
        <td align=center>verifyImageInAllContacts</td>
        <td align=left>p_contact_name</td>
        <td align=left>Verify that the contact's image is displayed.</td>
    </tr>


    <tr>
        <td align=center>createNewContact</td>
        <td align=left>p_contact_json_obj<br>p_imgSource=False</td>
        <td align=left>Create a new contact with a image (if specified).  p_imgSource is either "gallery" or "camera" (or left undefined).  <br><br>  <b>p_contact_json_obj</b> must be an object in the same format as the  one in ./example/tests/mock_data/contacts.py.</td>
    </tr>


    <tr>
        <td align=center>checkSearchResults</td>
        <td align=left>p_contactName<br>p_present=True</td>
        <td align=left>Checks the results of a search() to see  if the contact is present or not (depending  on the 'p_present' setting).</td>
    </tr>

</table>
#Dialer
<table>
  <tr>
    <th>Method</th><th>Parameters and defaults</th><th>Description</th>
  </tr>

    <tr>
        <td align=center>hangUp</td>
        <td align=left></td>
        <td align=left>Hangs up (assuming we're in the 'calling' frame).</td>
    </tr>


    <tr>
        <td align=center>callLog_call</td>
        <td align=left>p_num</td>
        <td align=left>Calls a number from the call log.</td>
    </tr>


    <tr>
        <td align=center>callLog_createContact</td>
        <td align=left>p_num<br>p_openCallLog=True</td>
        <td align=left>Creates a new contact from the call log (only  as far as the contacts app opening).  If p_openCallLog is set to False it will assume you are  already in the call log.</td>
    </tr>


    <tr>
        <td align=center>callLog_clearAll</td>
        <td align=left></td>
        <td align=left>Wipes all entries from the csll log.</td>
    </tr>


    <tr>
        <td align=center>openCallLog</td>
        <td align=left></td>
        <td align=left>Opens the call log.</td>
    </tr>


    <tr>
        <td align=center>callThisNumber</td>
        <td align=left></td>
        <td align=left>Calls the current number.</td>
    </tr>


    <tr>
        <td align=center>addThisNumberToContact</td>
        <td align=left>p_name</td>
        <td align=left>Adds the current number to existing contact.</td>
    </tr>


    <tr>
        <td align=center>enterNumber</td>
        <td align=left>p_num</td>
        <td align=left>Enters a number into the dialler using the keypad.</td>
    </tr>


    <tr>
        <td align=center>createContactFromThisNum</td>
        <td align=left></td>
        <td align=left>Creates a new contact from the number currently in the dialler  (doesn't fill in the contact details).</td>
    </tr>


    <tr>
        <td align=center>callLog_addToContact</td>
        <td align=left>p_num<br>p_name<br>p_openCallLog=True</td>
        <td align=left>Adds this number in the call log to an existing contact  (and returns you to the call log).  If p_openCallLog is set to False it will assume you are  already in the call log.</td>
    </tr>


    <tr>
        <td align=center>createMultipleCallLogEntries</td>
        <td align=left>p_num<br>p_amount</td>
        <td align=left>Put a number in the call log multiple times  (done by manipulating the device time).  Leaves you in the call log.</td>
    </tr>


    <tr>
        <td align=center>callLog_clearSome</td>
        <td align=left>p_entryNumbers</td>
        <td align=left>Wipes entries from the call log, using p_entryNumbers as an array of  numbers. For example: callLog_clearSome([1,2,3]) will remove the first 3.  <br><b>NOTE:</b> the first item is 1, <i>not</i> 0.</td>
    </tr>

</table>
#Email
<table>
  <tr>
    <th>Method</th><th>Parameters and defaults</th><th>Description</th>
  </tr>

    <tr>
        <td align=center>deleteEmail</td>
        <td align=left>p_subject</td>
        <td align=left>Deletes the first message in this folder with this subject line.</td>
    </tr>


    <tr>
        <td align=center>emailIsInFolder</td>
        <td align=left>p_subject</td>
        <td align=left>Verify an email is in this folder with the expected subject.</td>
    </tr>


    <tr>
        <td align=center>goto_folder_from_list</td>
        <td align=left>p_name</td>
        <td align=left>Goto a specific folder in the folder list screen.</td>
    </tr>


    <tr>
        <td align=center>sendTheMessage</td>
        <td align=left></td>
        <td align=left>Hits the 'Send' button to send the message (handles  waiting for the correct elements etc...).</td>
    </tr>


    <tr>
        <td align=center>remove_accounts_and_restart</td>
        <td align=left></td>
        <td align=left>Remove current email accounts via the UI and restart the application.  <br><br>  <b>NOTE:</b> Currently broken due to https://bugzilla.mozilla.org/show_bug.cgi?id=849183  so it's been set to do nothing!</td>
    </tr>


    <tr>
        <td align=center>openMailFolder</td>
        <td align=left>p_folderName</td>
        <td align=left>Open a specific mail folder (must be called from "Inbox").</td>
    </tr>


    <tr>
        <td align=center>switchAccount</td>
        <td align=left>p_address</td>
        <td align=left>Add a new account.</td>
    </tr>


    <tr>
        <td align=center>waitForDone</td>
        <td align=left></td>
        <td align=left>Wait until any progress icon goes away.</td>
    </tr>


    <tr>
        <td align=center>setupAccount</td>
        <td align=left>p_user<br>p_email<br>p_pass</td>
        <td align=left>Set up a new email account in the email app and login.</td>
    </tr>


    <tr>
        <td align=center>openMsg</td>
        <td align=left>p_subject</td>
        <td align=left>Opens a specific email in the current folder  (assumes we're already in the folder we want).</td>
    </tr>


    <tr>
        <td align=center>send_new_email</td>
        <td align=left>p_target<br>p_subject<br>p_message</td>
        <td align=left>Compose and send a new email.</td>
    </tr>

</table>
#EverythingMe
<table>
  <tr>
    <th>Method</th><th>Parameters and defaults</th><th>Description</th>
  </tr>

    <tr>
        <td align=center>searchForApp</td>
        <td align=left>p_name</td>
        <td align=left>Uses the search field to find the app (waits for the  result to appear etc...).<br>  Returns the element for the icon (or False if it's not found).</td>
    </tr>


    <tr>
        <td align=center>removeGroup</td>
        <td align=left>p_group</td>
        <td align=left>Removes a group from the EME group page.</td>
    </tr>


    <tr>
        <td align=center>pickGroup</td>
        <td align=left>p_name</td>
        <td align=left>Pick a group from the main icons.</td>
    </tr>


    <tr>
        <td align=center>addGroup</td>
        <td align=left>p_group</td>
        <td align=left>Adds a group to EME (assumes you're already in the EME group screen).</td>
    </tr>


    <tr>
        <td align=center>addAppToHomescreen</td>
        <td align=left>p_name</td>
        <td align=left>Pick an app from the apps listed in this group.</td>
    </tr>

</table>
#Facebook
<table>
  <tr>
    <th>Method</th><th>Parameters and defaults</th><th>Description</th>
  </tr>

    <tr>
        <td align=center>login</td>
        <td align=left>p_user<br>p_pass</td>
        <td align=left>Log into facebook (and navigate to the facebook login frame ... sometimes!!).</td>
    </tr>


    <tr>
        <td align=center>importAll</td>
        <td align=left></td>
        <td align=left>Import all contacts after enabling fb via Contacts Settings.</td>
    </tr>


    <tr>
        <td align=center>LinkContact</td>
        <td align=left>p_contactEmail</td>
        <td align=left>After clicking the link contact button, use this to click on a contact.</td>
    </tr>

</table>
#Ftu
<table>
  <tr>
    <th>Method</th><th>Parameters and defaults</th><th>Description</th>
  </tr>

    <tr>
        <td align=center>skipTour</td>
        <td align=left></td>
        <td align=left>Click to skip the Tour.</td>
    </tr>


    <tr>
        <td align=center>setTimezone</td>
        <td align=left>p_continent<br>p_city</td>
        <td align=left>Set the timezone.</td>
    </tr>


    <tr>
        <td align=center>setNetwork</td>
        <td align=left>p_wifiName<br>p_userName<br>p_password</td>
        <td align=left>Join a wifi network.</td>
    </tr>


    <tr>
        <td align=center>endTour</td>
        <td align=left></td>
        <td align=left>Click to end the Tour.</td>
    </tr>


    <tr>
        <td align=center>nextScreen</td>
        <td align=left></td>
        <td align=left>Click to the next screen (works until you get to the tour).</td>
    </tr>


    <tr>
        <td align=center>setDataConnEnabled</td>
        <td align=left></td>
        <td align=left>Enable data.</td>
    </tr>


    <tr>
        <td align=center>setLanguage</td>
        <td align=left>p_lang</td>
        <td align=left>Set the language (assume we're in the language screen).</td>
    </tr>


    <tr>
        <td align=center>nextTourScreen</td>
        <td align=left></td>
        <td align=left>Click to next page of the Tour.</td>
    </tr>


    <tr>
        <td align=center>startTour</td>
        <td align=left></td>
        <td align=left>Click to start the Tour.</td>
    </tr>

</table>
#Gallery
<table>
  <tr>
    <th>Method</th><th>Parameters and defaults</th><th>Description</th>
  </tr>

    <tr>
        <td align=center>thumbCount</td>
        <td align=left></td>
        <td align=left>Returns the number of thumbnails.</td>
    </tr>


    <tr>
        <td align=center>checkVideoLength</td>
        <td align=left>p_from_SS<br>p_to_SS</td>
        <td align=left>Check the length of a video.</td>
    </tr>


    <tr>
        <td align=center>playCurrentVideo</td>
        <td align=left></td>
        <td align=left>Plays the video we've loaded (in gallery you have to click the thumbnail first,  THEN press a play button - it doesn't play automatically).</td>
    </tr>


    <tr>
        <td align=center>deleteThumbnails</td>
        <td align=left>p_num_array</td>
        <td align=left>Deletes the thumbnails listed in p_num_array  (following an index starting at number 0).<br>  The list must be numeric, i.e "deleteThumbnails( (0,1,2) )".</td>
    </tr>


    <tr>
        <td align=center>clickThumb</td>
        <td align=left>p_num</td>
        <td align=left>Clicks a thumbnail from the gallery.</td>
    </tr>


    <tr>
        <td align=center>getGalleryItems</td>
        <td align=left></td>
        <td align=left>Returns a list of gallery item objects.</td>
    </tr>


    <tr>
        <td align=center>waitForThumbnails</td>
        <td align=left>p_count<br>p_failOnErr=False</td>
        <td align=left>Waits until p_count thumbnails are present  (because it can take a few seconds).  Since there could be a bug in the Gallery app  which prevents this, there is a 10s timeout.</td>
    </tr>

</table>
#Marketplace
<table>
  <tr>
    <th>Method</th><th>Parameters and defaults</th><th>Description</th>
  </tr>

    <tr>
        <td align=center>searchForApp</td>
        <td align=left>p_app</td>
        <td align=left>Search for an app in the market.</td>
    </tr>


    <tr>
        <td align=center>installApp</td>
        <td align=left>p_app<br>p_author</td>
        <td align=left>Install an app.</td>
    </tr>


    <tr>
        <td align=center>selectSearchResultApp</td>
        <td align=left>p_app<br>p_author</td>
        <td align=left>Select the application we want from the list returned by  searchForApp().</td>
    </tr>

</table>
#Messages
<table>
  <tr>
    <th>Method</th><th>Parameters and defaults</th><th>Description</th>
  </tr>

    <tr>
        <td align=center>clickSMSNotifier</td>
        <td align=left>p_num</td>
        <td align=left>Click new sms in the home page status bar notificaiton.</td>
    </tr>


    <tr>
        <td align=center>timeOfThread</td>
        <td align=left>p_num</td>
        <td align=left>Returns the time of a thread.</td>
    </tr>


    <tr>
        <td align=center>deleteSelectedMessages</td>
        <td align=left></td>
        <td align=left>Delete the currently selected messages in this thread.</td>
    </tr>


    <tr>
        <td align=center>threadEditModeON</td>
        <td align=left></td>
        <td align=left>Turns on Edit mode while in the SMS threads screen.</td>
    </tr>


    <tr>
        <td align=center>readNewSMS</td>
        <td align=left>p_FromNum</td>
        <td align=left>Read and return the value of the new message received from number.</td>
    </tr>


    <tr>
        <td align=center>checkAirplaneModeWarning</td>
        <td align=left></td>
        <td align=left>Checks for the presence of the popup  warning message if you just sent a message  while in 'airplane mode' (also removes  the message so you can continue).</td>
    </tr>


    <tr>
        <td align=center>lastMessageInThisThread</td>
        <td align=left></td>
        <td align=left>Returns an object of the last message in the current thread.</td>
    </tr>


    <tr>
        <td align=center>header_addToContact</td>
        <td align=left></td>
        <td align=left>Taps the header and tries to tap the 'Add to an existsing contact' button.  - Assumes we are looking at a message thread already.  - Leaves you in the correct iframe to continue (contacts).</td>
    </tr>


    <tr>
        <td align=center>threadEditModeOFF</td>
        <td align=left></td>
        <td align=left>Turns off Edit mode while in the SMS threads screen.</td>
    </tr>


    <tr>
        <td align=center>threadExists</td>
        <td align=left>p_num</td>
        <td align=left>Verifies that a thread exists for this number (returns True or False).</td>
    </tr>


    <tr>
        <td align=center>startNewSMS</td>
        <td align=left></td>
        <td align=left>Starts a new sms (doesn't fill anything in).  Assumes the Messaging app is already launched.</td>
    </tr>


    <tr>
        <td align=center>threadCarrier</td>
        <td align=left></td>
        <td align=left>Returns the 'carrier' being used by this thread.</td>
    </tr>


    <tr>
        <td align=center>sendSMS</td>
        <td align=left></td>
        <td align=left>Just presses the 'send' button (assumes everything else is done).</td>
    </tr>


    <tr>
        <td align=center>deleteSelectedThreads</td>
        <td align=left></td>
        <td align=left>Delete the currently selected message threads.</td>
    </tr>


    <tr>
        <td align=center>checkThreadHeader</td>
        <td align=left>p_header</td>
        <td align=left>Verifies if a string is contained in the header</td>
    </tr>


    <tr>
        <td align=center>checkIsInToField</td>
        <td align=left>p_target<br>p_targetIsPresent=True</td>
        <td align=left>Verifies if a number (or contact name) is  displayed in the "To: " field of a compose message.<br>  (Uses 'caseless' search for this.)</td>
    </tr>


    <tr>
        <td align=center>threadType</td>
        <td align=left></td>
        <td align=left>Returns the 'type' being used by this thread.</td>
    </tr>


    <tr>
        <td align=center>createAndSendSMS</td>
        <td align=left>p_nums<br>p_msg</td>
        <td align=left>Create and send a new SMS.<br>  <b>Note:</b> The p_nums field must be an array of numbers  or contact names.</td>
    </tr>


    <tr>
        <td align=center>waitForNewSMSPopup_by_number</td>
        <td align=left>p_num</td>
        <td align=left>Waits for a new SMS popup notification which  is from this 'p_num' number.</td>
    </tr>


    <tr>
        <td align=center>checkNumberIsInToField</td>
        <td align=left>p_target</td>
        <td align=left>Verifies if a number is contained in the  "To: " field of a compose message (even if it's  not displayed - i.e. a contact name is displayed,  but this validates the <i>number</i> for that  contact).</td>
    </tr>


    <tr>
        <td align=center>readLastSMSInThread</td>
        <td align=left></td>
        <td align=left>Read last message in the current thread.</td>
    </tr>


    <tr>
        <td align=center>enterSMSMsg</td>
        <td align=left>p_msg<br>p_not_keyboard=True</td>
        <td align=left>Create and send a message (assumes we are in a new 'create new message'  screen with the destination number filled in already).</td>
    </tr>


    <tr>
        <td align=center>header_call</td>
        <td align=left></td>
        <td align=left>Taps the header and tries to tap the 'send message' button.  - Assumes we are looking at a message thread already.  - Leaves you in the correct iframe to continue.</td>
    </tr>


    <tr>
        <td align=center>waitForReceivedMsgInThisThread</td>
        <td align=left>p_timeOut=30</td>
        <td align=left>Waits for the last message in this thread to be a 'received' message  and returns the element for this message.</td>
    </tr>


    <tr>
        <td align=center>header_createContact</td>
        <td align=left></td>
        <td align=left>Taps the header and tries to tap the 'send message' button.  - Assumes we are looking at a message thread already.  - Leaves you in the correct iframe to continue.</td>
    </tr>


    <tr>
        <td align=center>closeThread</td>
        <td align=left></td>
        <td align=left>Closes the current thread (returns you to the  'thread list' SMS screen).</td>
    </tr>


    <tr>
        <td align=center>removeContactFromToField</td>
        <td align=left>p_target</td>
        <td align=left>Removes p_target from the "To" field of this SMS.<br>  Returns True if it found the target, or False if not.</td>
    </tr>


    <tr>
        <td align=center>waitForNewSMSPopup_by_msg</td>
        <td align=left>p_msg</td>
        <td align=left>Waits for a new SMS popup notification which  matches this 'p_msg' string.</td>
    </tr>


    <tr>
        <td align=center>waitForSMSNotifier</td>
        <td align=left>p_num<br>p_timeout=40</td>
        <td align=left>Get the element of the new SMS from the status bar notification.</td>
    </tr>


    <tr>
        <td align=center>deleteMessagesInThisThread</td>
        <td align=left>p_msg_array=False</td>
        <td align=left>Enters edit mode, selects the required messages and  deletes them.<br>  p_msg_array is an array of numbers.  If it's not specified then all messages in this  thread will be deleted.</td>
    </tr>


    <tr>
        <td align=center>addNumbersInToField</td>
        <td align=left>p_nums</td>
        <td align=left>Add the numbers (or contact name) in the 'To'  field of this sms message.  Assumes you are in 'create sms' screen.  <br>  <b>p_nums</b> must be an array.</td>
    </tr>


    <tr>
        <td align=center>getThreadText</td>
        <td align=left>p_num</td>
        <td align=left>Returns the preview text for the thread for this number (if it exists),  or False if either the thread doesn't exist or can't be found.</td>
    </tr>


    <tr>
        <td align=center>openThread</td>
        <td align=left>p_num</td>
        <td align=left>Opens the thread for this number (assumes we're looking at the  threads in the messaging screen).</td>
    </tr>


    <tr>
        <td align=center>deleteThreads</td>
        <td align=left>p_target_array=False</td>
        <td align=left>Enters edit mode, selects the required messages and  deletes them.<br>  p_target_array is an array of target numbers  or contacts which identify the threads to be selected.  If it's not specified then all messages in this  thread will be deleted.</td>
    </tr>


    <tr>
        <td align=center>deleteAllThreads</td>
        <td align=left></td>
        <td align=left>Deletes all threads (assumes the messagin app is already open).</td>
    </tr>


    <tr>
        <td align=center>timeOfLastMessageInThread</td>
        <td align=left></td>
        <td align=left>Returns the time of the last message in the current thread.</td>
    </tr>


    <tr>
        <td align=center>selectAddContactButton</td>
        <td align=left></td>
        <td align=left>Taps the 'add contact' button and switches to the  correct 'contacts' frame.<br>  Returns the "src" of the original iframe.</td>
    </tr>


    <tr>
        <td align=center>editAndSelectMessages</td>
        <td align=left>p_msg_array</td>
        <td align=left>Puts this thread into Edit mode and selects  the messages listed in p_msg_array.<br>  p_msg_array is an array of numbers.</td>
    </tr>


    <tr>
        <td align=center>countMessagesInThisThread</td>
        <td align=left></td>
        <td align=left>Returns the number of messages in this thread  (assumes you're already in the thread).</td>
    </tr>


    <tr>
        <td align=center>header_sendMessage</td>
        <td align=left></td>
        <td align=left>Taps the header and tries to tap the 'send message' button.  - Assumes we are looking at a message thread already.  - Leaves you in the correct iframe to continue.</td>
    </tr>


    <tr>
        <td align=center>editAndSelectThreads</td>
        <td align=left>p_target_array</td>
        <td align=left>Puts this thread into Edit mode and selects  the messages listed in p_msg_array.<br>  p_target_array is an array of target numbers  or contacts which identify the threads to be selected.</td>
    </tr>

</table>
#Settings
<table>
  <tr>
    <th>Method</th><th>Parameters and defaults</th><th>Description</th>
  </tr>

    <tr>
        <td align=center>goSound</td>
        <td align=left></td>
        <td align=left>Go to Sound menu.</td>
    </tr>


    <tr>
        <td align=center>setRingerAndNotifsVolume</td>
        <td align=left>p_vol</td>
        <td align=left>Set the volume for ringer and notifications.</td>
    </tr>


    <tr>
        <td align=center>setTimeToNow</td>
        <td align=left></td>
        <td align=left>Set date and time to 'now'.<br>  WARNING: DOES NOT WORK YET!!! ...<br>  1. Marionette.flick() not working here.<br>  2. Cannot figure out how to tell what the current value is (no 'active' setting here),</td>
    </tr>


    <tr>
        <td align=center>wifi</td>
        <td align=left></td>
        <td align=left>Open wifi settings.</td>
    </tr>


    <tr>
        <td align=center>setAlarmVolume</td>
        <td align=left>p_vol</td>
        <td align=left>Set the volume for alarms.</td>
    </tr>


    <tr>
        <td align=center>tap_wifi_network_name</td>
        <td align=left>p_wifi_name<br>p_user<br>p_pass</td>
        <td align=left>Select a network.</td>
    </tr>


    <tr>
        <td align=center>turn_wifi_on</td>
        <td align=left></td>
        <td align=left>Click slider to turn wifi on.</td>
    </tr>


    <tr>
        <td align=center>cellular_and_data</td>
        <td align=left></td>
        <td align=left>Open cellular and data settings.</td>
    </tr>


    <tr>
        <td align=center>checkWifiLisetedAsConnected</td>
        <td align=left>p_name</td>
        <td align=left>Verify the expected network is listed as connected in 'available networks'.</td>
    </tr>


    <tr>
        <td align=center>turn_dataConn_on</td>
        <td align=left>p_wifiOFF=False</td>
        <td align=left>Click slider to turn data connection on.</td>
    </tr>

</table>
#Video
<table>
  <tr>
    <th>Method</th><th>Parameters and defaults</th><th>Description</th>
  </tr>

    <tr>
        <td align=center>checkVideoLength</td>
        <td align=left>p_vid_num<br>p_from_SS<br>p_to_SS</td>
        <td align=left></td>
    </tr>


    <tr>
        <td align=center>startVideo</td>
        <td align=left>p_num</td>
        <td align=left>Clicks the thumbnail to start the video.</td>
    </tr>


    <tr>
        <td align=center>checkThumbDuration</td>
        <td align=left>p_thumb_num<br>p_length_str_MMSS<br>p_errorMargin_SS</td>
        <td align=left>Check the duration of a video thumbnail.</td>
    </tr>

</table>
