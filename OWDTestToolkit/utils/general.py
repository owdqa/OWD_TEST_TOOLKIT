import sys
import os
import json
import time
from twilio.rest import TwilioRestClient
from OWDTestToolkit import DOM


class general(object):

    def addFileToDevice(self, file_name, count=1, destination=''):
        #
        # Put a file onto the device (path is relative to the dir
        # you are physically in when running the tests).
        #
        self.parent.device.push_file(file_name, count, '/'.join(['sdcard', destination]))

    def checkMarionetteOK(self):
        #
        # Sometimes marionette session 'vanishes', so this makes sure we have one still.
        # <b>NOTE: </b>This leaves you in the 'top -level' iframe, so you'll need to navigate back
        # to your frame after running this.
        #
        try:
            self.marionette.start_session()
            self.logResult("debug", "<i>(*** The Marionette session was restarted due to a possible crash. ***)</i>")
        except:
            pass

    def clearGeolocPermission(self, allow_geoloc=False):
        #
        # This method clears the Geolocation permission dialog
        # (if necessary) with allow_geoloc.
        #
        permission_yes = ("id", "permission-yes")
        permission_no = ("id", "permission-no")
        orig_frame = self.currentIframe()
        self.marionette.switch_to_frame()
        try:
            if allow_geoloc:
                self.wait_for_element_displayed(*permission_yes, timeout=2)
                x = self.marionette.find_element(*permission_yes)
            else:
                self.wait_for_element_displayed(*permission_no, timeout=2)
                x = self.marionette.find_element(*permission_no)
            x.tap()
        except:
            pass

        self.switchToFrame("src", orig_frame)

    def createIncomingCall(self, num):
        """
        Create an incoming call using Twilio API
        """

        account_sid = "ACd3d2699e42974fd163129ff8a7530e56"
        auth_token = "0ac68cfbf12aa7e0725da1750da609b7"
        client = TwilioRestClient(account_sid, auth_token)

        client.calls.create(url="http://demo.twilio.com/docs/voice.xml", to=num, from_="+34518880854")

    def get_os_variable(self, name, validate=True):
        #
        # Get a variable from the OS.
        #
        if name == "ENTER":
            return ""
        else:
            x = False
            try:
                x = os.environ[name]
            except:
                self.logResult("info", "NOTE: OS variable '{}' was not set.".format(name))
                if validate:
                    self.reportResults()
                    sys.exit(1)
                return False
            return x

    def insertContact(self, contact):
        self.marionette.switch_to_frame()
        mozcontact = contact.create_mozcontact()
        result = self.marionette.execute_async_script('return GaiaDataLayer.insertContact({});'.\
                                                      format(json.dumps(mozcontact)), special_powers=True)
        assert result, 'Unable to insert contact {}'.format(contact)

    def selectFromSystemDialog(self, p_str):
        #
        # Selects an item from a system select box (such as country / timezone etc...).
        #

        #
        # Remember the current frame then switch to the system level one.
        #
        orig_iframe = self.currentIframe()
        self.marionette.switch_to_frame()

        #
        # Find and click the list item (it may be off the screen, so 'displayed' would be false, but
        # Marionette will scroll it into view automatically so it can be clicked just as it
        # would it real life).
        #
        xpath_val = "//section[@id='value-selector-container']//li[label[span[text()='{}']]]".format(p_str)
        list_item = self.getElement(("xpath", xpath_val), "'{}' in the selector".format(p_str), False)
        list_item.click()

        #
        # A bug in Marionette just now moves the entire screen up, so the statusbar
        # dissappears off the top of the display. This hack corrects it.
        #
        self.marionette.execute_script("document.getElementById('statusbar').scrollIntoView();")

        #
        # Find and click OK.
        #
        close_button = self.getElement(DOM.GLOBAL.modal_valueSel_ok, "OK button", True, 30)
        close_button.click()

        #
        # Return to the orginal frame.
        #
        self.switchToFrame("src", orig_iframe)

    def setSetting(self, item, value, silent=False):
        #
        # Just a container function to catch any issues when using gaiatest's
        # 'set_setting()' function.
        #
        try:
            self.data_layer.set_setting(item, value)
            if not silent:
                self.logResult("info", "Setting '{}' to '{}' returned no issues.".format(item, value))
            return True
        except:
            if not silent:
                self.logresult("info", "WARNING: Unable to set '{}' to '{}'!".format(item, value))
            return False

    def setupDataConn(self):
        #
        # Set the phone's details for data conn (apn etc...).
        #
        apn = "telefonica.es"
        conn_id = "telefonica"
        passwd = "telefonica"
        host = "10.138.255.133"
        port = "8080"

        self.logResult("info", "Ensuring dataconn settings (APN, etc...) are correct.")

        self.set_item("ril.data.apn", apn)
        self.set_item("ril.data.user", conn_id)
        self.set_item("ril.data.passwd", passwd)
        self.set_item("ril.data.httpProxyHost", host)
        self.set_item("ril.data.httpProxyPort", port)

        self.logResult("info", "Done.")

    def set_item(self, item, value):
        #
        # Just a quick function to report issues setting this.
        #
        try:
            self.data_layer.set_setting(item, value)
        except:
            self.logResult(False, "Unable to set '{}' to '{}'.".format(item, value))

    def typeThis(self, p_element_array, p_desc, p_str, p_no_keyboard=False,
                 p_clear=True, p_enter=True, p_validate=True, p_remove_keyboard=True):
        #
        # Types this string into this element.
        # If p_no_keyboard = True then it doesn't use the keyboard.
        # <b>NOTE:</b> If os variable "NO_KEYBOARD" is set (to anything),
        # then regardless of what you send to this method, it will never
        # use the keyboard.
        #
        no_keyboard = self.get_os_variable("NO_KEYBOARD", False)

        #
        # Make sure the string is a string!
        #
        p_str = str(str(p_str))

        #
        # Remember the current frame.
        #
        orig_frame = self.currentIframe()

        x = self.getElement(p_element_array, p_desc)

        #
        # Need to click in a lot of these or the field isn't located correctly (esp. SMS).
        #
        x.click()

        if p_clear:
            x.clear()

        if no_keyboard or p_no_keyboard:
            #
            # Don't use the keyboard.
            #
            self.logResult("info", "(Sending '{}' to this field without using the keyboard.)".format(p_str))
            x.send_keys(p_str)

            #
            # There's a weird 'quirk' in Marionette just now:
            # if you send_keys() an underscore ("_") then the
            # screen is locked. No idea who thought that was a
            # good idea, but it seems it's here to stay, so unlock()
            # if necessary.
            #
            if "_" in p_str:
                self.parent.lockscreen.unlock()
                self.marionette.switch_to_frame()
                self.switchToFrame("src", orig_frame)

        else:
            #
            # Tap the element to get the keyboard to popup.
            #
            self.logResult("info", "(Sending '{}' to this field using the keyboard.)".format(p_str))
            x.tap()

            #
            # Type the string.
            #
            self.parent.keyboard.send(p_str)

        #
        # Tap ENTER on the keyboard (helps to remove the keyboard even if
        # you didn't use it to type)?
        #
        if p_enter:
            self.parent.keyboard.tap_enter()

        #
        # Switch back to the frame we were in and get the element again.
        #
        self.switchToFrame("src", orig_frame)

        #
        # Validate that the field now has the value we sent it.
        #
        if p_validate:
            x = self.marionette.find_element(*p_element_array)
            y = x.get_attribute("value")

            if p_clear:
                fieldText = y
            else:
                fieldText = y[-(len(p_str)):]

            self.TEST(p_str == fieldText,
                      "The field contains the correct string ...|{}|- vs. -|{}".format(fieldText, p_str))

        if p_remove_keyboard:
            #
            # Try to tap the header to remove the keyboard now that we've finished.
            #
            try:
                self.wait_for_element_displayed(*DOM.GLOBAL.app_head, timeout=1)
                x = self.marionette.find_element(*DOM.GLOBAL.app_head)
                x.tap()
                time.sleep(0.5)
            except:
                pass
