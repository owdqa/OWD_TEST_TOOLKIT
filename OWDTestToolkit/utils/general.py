import json
import time
import datetime
from gaiatest.apps.keyboard.app import Keyboard
from gaiatest import GaiaData
from gaiatest import GaiaApps
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.decorators import retry
from OWDTestToolkit.utils.contacts import MockContact


class general(object):

    def __init__(self, parent):
        self.parent = parent
        self.marionette = parent.marionette
        self.keyboard = Keyboard(self.marionette)

    def add_file_to_device(self, file_name, count=1):
        """
        Put a file onto the device (path is relative to the dir
        you are physically in when running the tests).
        """
        self.parent.device.file_manager.push_file(
            local_path=file_name, remote_path=self.parent.device.storage_path, count=count)

    def checkMarionetteOK(self):
        """
        Sometimes marionette session 'vanishes', so this makes sure we have one still.
        <b>NOTE: </b>This leaves you in the 'top -level' iframe, so you'll need to navigate back
        to your frame after running this.
        """
        try:
            self.marionette.start_session()
            self.parent.reporting.logResult("debug", "<i>(*** The Marionette session was "
                                            "restarted due to a possible crash. ***)</i>")
        except:
            self.parent.reporting.logResult('debug', "Marionette session still running")
            pass
        self.parent.parent.apps.switch_to_displayed_app()

    def clearGeolocPermission(self, allow_geoloc=False):
        """
        This method clears the Geolocation permission dialog
        (if necessary) with allow_geoloc.
        """
        permission_yes = ("id", "permission-yes")
        permission_no = ("id", "permission-no")
        orig_frame = self.parent.iframe.currentIframe()
        self.marionette.switch_to_frame()
        try:
            if allow_geoloc:
                self.parent.parent.wait_for_element_displayed(*permission_yes, timeout=2)
                x = self.marionette.find_element(*permission_yes)
            else:
                self.parent.parent.wait_for_element_displayed(*permission_no, timeout=2)
                x = self.marionette.find_element(*permission_no)
            x.tap()
        except:
            pass

        self.parent.iframe.switchToFrame("src", orig_frame)

    def get_current_date_string(self):
        """Return the current date as a formatted string, to include it in logs, SMS bodies, etc.
        """
        now = datetime.datetime.now()
        return now.strftime("%Y/%m/%d %H:%M:%S.%f")

    def get_config_variable(self, name, group=None):
        """Get a configuration variable.
        """
        try:
            if group:
                return self.parent.data_layer.testvars[group][name]
            else:
                return self.parent.data_layer.testvars[name]
        except:
            return False

    def insertContact(self, contact):
        self.marionette.switch_to_frame()
        mozcontact = contact.create_mozcontact()
        result = self.marionette.execute_async_script('return GaiaDataLayer.insertContact({});'.
                                                      format(json.dumps(mozcontact)), special_powers=True)
        assert result, 'Unable to insert contact {}'.format(contact)

    def is_device_dual_sim(self):
        import os
        try:
            with open(os.devnull, 'w') as DEVNULL:
                prop = subprocess32.check_output(
                    'adb shell cat /system/build.prop | grep multisim', shell=True, stderr=DEVNULL).strip().split("=")[-1]
            self.parent.reporting.logResult("info", "Value of property: {}".format(prop))
            return prop == "dsds"
        except:
            self.parent.reporting.logResult("info", "That property was not found")
            return False

    def selectFromSystemDialog(self, p_str):
        """
        Selects an item from a system select box (such as country / timezone etc...).
        """

        # Remember the current frame then switch to the system level one.
        orig_iframe = self.parent.iframe.currentIframe()
        self.marionette.switch_to_frame()
        """
        Find and click the list item (it may be off the screen, so 'displayed' would be false, but
        Marionette will scroll it into view automatically so it can be clicked just as it
        would it real life).
        """
        xpath_val = "//section[@id='value-selector-container']//li[label[span[text()='{}']]]".format(p_str)
        list_item = self.parent.element.getElement(("xpath", xpath_val), "'{}' in the selector".format(p_str), False)
        list_item.click()
        """
        A bug in Marionette just now moves the entire screen up, so the statusbar
        dissappears off the top of the display. This hack corrects it.
        """
        self.marionette.execute_script("document.getElementById('statusbar').scrollIntoView();")

        # Find and click OK.
        close_button = self.parent.element.getElement(DOM.GLOBAL.modal_valueSel_ok, "OK button", True, 30)
        close_button.click()

        # Return to the orginal frame.
        self.parent.iframe.switchToFrame("src", orig_iframe)

    def setSetting(self, item, value, silent=False):
        """
        Just a container function to catch any issues when using gaiatest's
        'set_setting()' function.
        """
        try:
            self.parent.data_layer.set_setting(item, value)
            if not silent:
                self.parent.reporting.logResult("info", "Setting '{}' to '{}' returned no issues.".format(item, value))
            return True
        except:
            if not silent:
                self.parent.reporting.logResult("info", "WARNING: Unable to set '{}' to '{}'!".format(item, value))
            return False

    def setupDataConn(self):
        """
        Set the phone's details for data conn (apn etc...).
        """
        apn = "telefonica.es"
        conn_id = "telefonica"
        passwd = "telefonica"
        host = "10.138.255.133"
        port = "8080"

        self.parent.reporting.logResult("info", "Ensuring dataconn settings (APN, etc...) are correct.")

        self.set_item("ril.data.apn", apn)
        self.set_item("ril.data.user", conn_id)
        self.set_item("ril.data.passwd", passwd)
        self.set_item("ril.data.httpProxyHost", host)
        self.set_item("ril.data.httpProxyPort", port)

        self.parent.reporting.logResult("info", "Done.")

    def set_item(self, item, value):
        """
        Just a quick function to report issues setting this.
        """
        try:
            self.parent.data_layer.set_setting(item, value)
        except:
            self.parent.reporting.logResult(False, "Unable to set '{}' to '{}'.".format(item, value))

    def typeThis(self, p_element_array, p_desc, p_str, p_no_keyboard=False,
                 p_clear=True, p_enter=True, p_validate=True, p_remove_keyboard=True):
        """
        Types this string into this element.
        If p_no_keyboard = True then it doesn't use the keyboard.
        <b>NOTE:</b> If os variable "NO_KEYBOARD" is set (to anything),
        then regardless of what you send to this method, it will never
        use the keyboard.
        """
        no_keyboard = self.parent.general.get_config_variable("NO_KEYBOARD")

        # Remember the current frame.
        orig_frame = self.parent.iframe.currentIframe()
        self.parent.reporting.debug("Original frame filtered name: {}".format(orig_frame))

        input_elem = self.parent.element.getElement(p_element_array, p_desc)

        # Need to click in the bottom right corner, or the cursor may not be properly located to append.
        input_elem.tap(x=input_elem.size["width"] - 1, y=input_elem.size["height"] - 1)

        if p_clear:
            input_elem.clear()

        if no_keyboard or p_no_keyboard:

            # Don't use the keyboard.
            self.parent.reporting.logResult("info", u"(Sending '{}' to this field without using the keyboard.)".
                                            format(p_str))

            input_elem.send_keys(p_str)

        else:

            # Tap the element to get the keyboard to popup.
            self.parent.reporting.logResult("info", u"(Sending '{}' to this field using the keyboard.)".
                                            format(p_str))

            # Type the string.
            self.keyboard.send(p_str)
        """
        Tap ENTER on the keyboard (helps to remove the keyboard even if
        you didn't use it to type)?
        """
        if p_enter:
            self.keyboard.tap_enter()

        # Switch back to the frame we were in and get the element again.
        self.parent.reporting.debug("Switching back to original frame {}".format(orig_frame))
        self.parent.iframe.switchToFrame("src", orig_frame)

        # Validate that the field now has the value we sent it.
        if p_validate:
            elem = self.marionette.find_element(*p_element_array)
            value = elem.get_attribute("value")
            self.parent.reporting.debug("*** VALUE of cmp-body-text: [{}]".format(value))
            if value is None:
                value = elem.text
                self.parent.reporting.debug("*** No value found. Using TEXT of cmp-body-text: [{}]".format(value))

            if p_clear:
                fieldText = value
            else:
                fieldText = value[-(len(p_str)):]

            self.parent.test.test(p_str == fieldText,
                                  "The field contains the correct string ...|{}|- vs. -|{}".format(fieldText, p_str))

        if p_remove_keyboard:

            # Try to tap the header to remove the keyboard now that we've finished.
            try:
                self.parent.parent.wait_for_element_displayed(*DOM.GLOBAL.app_head, timeout=1)
                app_header = self.marionette.find_element(*DOM.GLOBAL.app_head)
                app_header.tap()
                time.sleep(0.5)
            except:
                pass

    def remove_files(self):
        """
        Removes all files from the sdcard
        """
        self.parent.device.file_manager.remove(self.parent.device.storage_path)

    def restart(self):
        self.parent.reporting.logResult('info', 'Restarting the device...')
        # Lockscreen does not get on very well with restarts
        lock_enabled = self.parent.data_layer.get_setting("lockscreen.enabled")
        if lock_enabled:
            self.parent.data_layer.set_setting("lockscreen.enabled", False)

        # After restarting we need to re-instantiate javascript objects
        self.parent.device.restart_b2g()
        self.apps = GaiaApps(self.marionette)
        self.parent.data_layer = GaiaData(self.marionette, self.parent.parent.testvars)
        # Restore lockscreen status
        self.parent.data_layer.set_setting("lockscreen.enabled", lock_enabled)

    @retry(5, 5)
    def connect_to_cell_data(self):
        self.parent.reporting.debug(">>> Trying to connect to cell data...")
        self.parent.data_layer.connect_to_cell_data()
        self.parent.reporting.debug("    Connected: {}".format(self.parent.data_layer.is_cell_data_connected))

    def insert_some_mock_contacts(self, number_of_contacts):
        """Insert the given number of contacts in the device."""
        contact_given = "Test"
        contact_family = map(str, range(1, number_of_contacts + 1))
        contact_name = ["{} {}".format(contact_given, contact_family[i])
                        for i in range(number_of_contacts)]

        contact_numbers = [str(i) * 12 for i in range(1, number_of_contacts + 1)]

        test_contacts = [MockContact(name=contact_name[i], givenName=contact_given,
                                     familyName=contact_family[i],
                                     tel={'type': 'Mobile', 'value': contact_numbers[i]})
                         for i in range(number_of_contacts)]
        map(self.insertContact, test_contacts)

    def show_all_settings(self):
        self.parent.reporting.debug("** Device current settings: {}".format(self.parent.data_layer.all_settings))
