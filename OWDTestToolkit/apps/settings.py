from OWDTestToolkit import DOM
import time

class Settings(object):

    def __init__(self, parent):
        self.apps = parent.apps
        self.data_layer = parent.data_layer
        self.parent = parent
        self.marionette = parent.marionette
        self.UTILS = parent.UTILS

    def launch(self):
        #
        # Launch the app.
        #
        self.app = self.apps.launch(self.__class__.__name__)
        self.UTILS.element.waitForNotElements(DOM.GLOBAL.loading_overlay,
                                              self.__class__.__name__ + " app - loading overlay")
        return self.app

    def callID_verify(self):
        x = self.UTILS.element.getElement(DOM.Settings.call_settings, "Call number button")
        x.tap()
        self.UTILS.reporting.logResult("info", "Call number presses")
        time.sleep(20)

        x = self.UTILS.element.getElement(DOM.Settings.call_button, "Call ID button")
        x.tap()
        self.UTILS.reporting.logResult("info", "Call ID button presses")

        #Change Frame
        self.marionette.switch_to_frame()

        #Get option selected
        x = self.UTILS.element.getElement(DOM.Settings.call_show_number, "Call Option value")
        y = x.get_attribute("aria-selected")

        self.UTILS.reporting.logResult("info", "Screen shot of the result of tapping call button", y)
        self.UTILS.test.TEST(y == "true", "Checking Call ID value")

    def cellular_and_data(self):
        #
        # Open cellular and data settings.
        #
        x = self.UTILS.element.getElement(DOM.Settings.cellData, "Cellular and Data settings link")
        x.tap()

        self.UTILS.element.waitForElements(DOM.Settings.celldata_header, "Celldata header", True, 20, False)

    def configureMMSAutoRetrieve(self, value):
        #
        # Launch messages app.
        #
        self.launch()

        #
        # Tap on Messaging Settings button
        #
        x = self.UTILS.element.getElement(DOM.Settings.msg_settings, "Messaging Settings button")
        x.tap()

        #
        # Tap on Auto Retireve Select
        #
        x = self.UTILS.element.getElement(DOM.Settings.auto_retrieve_select_btn, "Auto Retrieve Select")
        x.tap()

        #
        # Changing to top level frame
        #
        time.sleep(2)
        self.marionette.switch_to_frame()

        #
        # Selecting the specific option using que received parameter
        #
        if value == "off":
            x = self.UTILS.element.getElement(DOM.Settings.auto_retrieve_select_off,
                                              "Off option in Auto Retrieve Select")
            x.tap()
        elif value == "on_with_r":
            x = self.UTILS.element.getElement(DOM.Settings.auto_retrieve_select_roaming,
                                      "On with roaming option in Auto Retrieve Select")
            x.tap()
        elif value == "on_without_r":
            x = self.UTILS.element.getElement(DOM.Settings.auto_retrieve_select_no_roaming,
                                      "On without roaming option in Auto Retrieve Select")
            x.tap()
        else:
            self.UTILS.test.quitTest("FAILED: Incorrect parameter received in configureMMSAutoRetrieve()")

        #
        #Tapping on OK button in auto Retrieve select
        #
        x = self.UTILS.element.getElement(DOM.Settings.ok_btn, "Tapping on OK button in auto Retrieve select")
        x.tap()

        #
        #Verifying if the option value has been selected
        #
        self.verify_autoRetrieve_SelectedItem(value)

    def createCustomAPN(self, apn, identifier, pwd):
        #
        # Open Data Settings
        #
        self.open_data_settings()

        #
        # Select custom settings
        #
        x = self.UTILS.element.getElement(DOM.Settings.custom_settings_apn, "Custom settings button")
        x.tap()

        #
        # Enter the data
        #
        self.UTILS.general.typeThis(DOM.Settings.celldata_data_apn, "APN", apn,
                                    p_no_keyboard=True, p_validate=False, p_clear=True, p_enter=False)

        self.UTILS.general.typeThis(DOM.Settings.celldata_apn_user, "APN", identifier,
                                    p_no_keyboard=True, p_validate=False, p_clear=True, p_enter=False)

        self.UTILS.general.typeThis(DOM.Settings.celldata_apn_passwd, "APN", pwd,
                                    p_no_keyboard=True, p_validate=False, p_clear=True, p_enter=True)

        #
        # Tap the ok button to save the changes
        #
        x = self.UTILS.element.getElement(DOM.Settings.celldata_ok_button, "Ok button")
        x.tap()

    def disable_hotSpot(self):
        #
        # Disable hotspot (internet sharing) - assumes Settings app is already open.
        #
        self.UTILS.reporting.logResult("info", "<u>Disabling hotspot ...</u>")

        #
        # Is it already disabled?
        #
        x = self.UTILS.element.getElement(DOM.Settings.hotspot_settings, "Hotspot settings")
        if x.get_attribute("disabled") == "false":
            self.UTILS.reporting.logResult("info", "Hotspot is already disabled.")
            return True

        x = self.UTILS.element.getElement(DOM.Settings.hotspot_switch, "Hotspot switch")
        x.tap()
        time.sleep(1)

        #
        # Wait for the hotspot to begin.
        #
        is_disabled = False
        retry = 10
        for i in range(retry):
            x = self.marionette.find_element(*DOM.Settings.hotspot_settings)
            # FJCS: disabled == "false" to disable?
            if x.get_attribute("disabled") == "false":
                # It's done.
                is_disabled = True
                break
            time.sleep(0.5)

        is_status_icon = self.UTILS.statusbar.isIconInStatusBar(DOM.Statusbar.hotspot)

        self.UTILS.test.TEST(is_disabled, "Hotspot settings are disabled (because 'hotspot' is not running).")
        self.UTILS.test.TEST(not is_status_icon, "Hotspot icon is not present in the status bar.")

    def downloads(self):
        #
        # Open wifi settings.
        #
        x = self.UTILS.element.getElement(DOM.Settings.downloads, "Downloads settings link")
        x.tap()

        self.UTILS.element.waitForElements(DOM.Settings.downloads_header,
                                    "Downloads header appears.", True, 20, False)

    def enable_hotSpot(self):
        #
        # Enable hotspot (internet sharing) - assumes Settings app is already open.
        #
        self.UTILS.reporting.logResult("info", "<u>Enabling hotspot ...</u>")

        #
        # Is it already enabled?
        #
        x = self.UTILS.element.getElement(DOM.Settings.hotspot_settings, "Hotspot settings")
        # FJCS: disabled == "true" to enable?
        if x.get_attribute("disabled") == "true":
            self.UTILS.reporting.logResult("info", "Hotspot is already enabled.")
            return True

        x = self.UTILS.element.getElement(DOM.Settings.hotspot_switch, "Hotspot switch")
        x.tap()
        time.sleep(1)

        #
        # Wait for the hotspot to begin.
        #
        is_enabled = False
        retry = 10
        for i in range(retry):
            x = self.marionette.find_element(*DOM.Settings.hotspot_settings)
            if x.get_attribute("disabled") == "true":
                # It's done.
                is_enabled = True
                break
            time.sleep(0.5)

        is_status_icon = self.UTILS.statusbar.isIconInStatusBar(DOM.Statusbar.hotspot)

        self.UTILS.test.TEST(is_enabled, "Hotspot settings are disabled (because 'hotspot' is now running).")
        self.UTILS.test.TEST(is_status_icon, "Hotspot icon is present in the status bar.")

    def goBack(self):
        #
        # Tap the back icon (gets a bit complicated sometimes, because
        # there's sometimes more than one match for this icon DOM reference).
        #
        time.sleep(0.5)
        x = self.UTILS.element.getElements(DOM.Settings.back_button, "Back buttons", False)
        ok = False
        for i in x:
            try:
                i.tap()
                ok = True
                break
            except:
                pass

        if not ok:
            self.UTILS.reporting.logResult(False, "Tap the 'back' icon to return to the parent screen.")
            return False

        time.sleep(1)
        return True

    def goSound(self):
        #
        # Go to Sound menu.
        #
        self.launch()
        x = self.UTILS.element.getElement(DOM.Settings.sound, "Sound setting link")
        x.tap()

    def hotSpot(self):
        #
        # Open 'Internet sharing' settings (also known as 'hotspot').
        #
        self.UTILS.test.TEST(True, "Executing script to scroll hotspot")
        self.marionette.execute_script("document.getElementById('{}').scrollIntoView();".\
                                       format(DOM.Settings.hotspot[1]))

        self.UTILS.test.TEST(True, "Get element hotspot")
        x = self.UTILS.element.getElement(DOM.Settings.hotspot, "'Internet sharing' (hotspot) link")
        x.tap()

        self.UTILS.test.TEST(True, "Get element hotspot")
        self.UTILS.element.waitForElements(DOM.Settings.hotspot_header, "Hotspot header appears.", True, 20, False)

    def open_data_settings(self):
        #
        # Open cellular and data settings.
        #
        self.cellular_and_data()
        self.marionette.execute_script("""
        var getElementByXpath = function (path) {
            return document.evaluate(path, document, null, 9, null).singleNodeValue;
        };
        getElementByXpath('/html/body/section[29]/div/ul[3]/li[2]/label/button').scrollIntoView();
        """)
        x = self.UTILS.element.getElement(DOM.Settings.celldata_DataSettings, "Data settings link")
        x.tap()

    def open_msg_settings(self):
        #
        # Open cellular and data settings.
        #
        self.cellular_and_data()
        self.marionette.execute_script("""
        var getElementByXpath = function (path) {
            return document.evaluate(path, document, null, 9, null).singleNodeValue;
        };
        getElementByXpath('/html/body/section[29]/div/ul[3]/li[3]/label/button').scrollIntoView();
        """)
        x = self.UTILS.element.getElement(DOM.Settings.celldata_MsgSettings, "Message settings link")
        x.tap()

    def selectDefaultAPN(self, apn, open_settings=True):

        #
        # Open Data Settings
        #
        if open_settings:
            self.open_data_settings()

        #
        # Tap on the added APN
        #
        dom_elem = (DOM.Settings.default_apn[0], DOM.Settings.default_apn[1].format(apn))
        x = self.UTILS.element.getElement(dom_elem, "Added APN")
        self.UTILS.test.TEST(True, "APN {} element: {}".format(apn, x))
        x.tap()

        #
        # Tap the ok button to save the changes
        #
        x = self.UTILS.element.getElement(DOM.Settings.celldata_ok_button, "Ok button")
        x.tap()

    def setAlarmVolume(self, volume):
        #
        # Set the volume for alarms.
        #
        self.parent.data_layer.set_setting('audio.volume.alarm', volume)

    def setRingerAndNotifsVolume(self, volume):
        #
        # Set the volume for ringer and notifications.
        #
        self.parent.data_layer.set_setting('audio.volume.notification', volume)

    def setTimeToNow(self):
        #
        # Set date and time to 'now'.<br>
        # TODO: Verify this
        # WARNING: DOES NOT WORK YET!!! ...<br>
        #   1. Marionette.flick() not working here.<br>
        #   2. Cannot figure out how to tell what the current value is (no 'active' setting here),
        #
        return
        self.launch()

        x = ("id", "menuItem-dateAndTime")
        el = self.UTILS.element.getElement(x, "Date & Time setting")
        el.tap()

        x = ("id", "clock-date")
        el = self.UTILS.element.getElement(x, "Date setting")
        el.tap()

        time.sleep(2)
        self.marionette.switch_to_frame()

    def turn_dataConn_on(self, wireless_off=False):
        #
        # Click slider to turn data connection on.
        #

        #
        # First, make sure we're in "Settings".
        #
        try:
            self.parent.wait_for_element_present(*DOM.Settings.frame_locator, timeout=2)
            x = self.marionette.find_element(*DOM.Settings.frame_locator)
        except:
            #
            # Settings isn't running, so start it.
            #
            self.launch()
            self.cellular_and_data()

        if wireless_off:
            if self.parent.data_layer.get_setting("wifi.enabled"):
                self.parent.data_layer.disable_wifi()

        time.sleep(1)

        if not self.parent.data_layer.get_setting("ril.data.enabled"):
            #
            # If we disabled the wifi we'll be in the wrong frame here, so just make sure ...
            #
            self.marionette.switch_to_frame()
            self.UTILS.iframe.switchToFrame(*DOM.Settings.frame_locator)

            x = self.UTILS.element.getElement(DOM.Settings.celldata_DataConn, "Connect to cellular and data switch",
                                      False, 5, False)
            try:
                x.tap()
            except:
                #
                # The element isn't visible, but we still want to enable dataconn,
                # so try using the 'back door' ...
                #
                self.UTILS.reporting.logResult("info", "(Marionette issue) Unable to start dataconn via U.I. -"\
                                     " trying to force it using gaia data layer instead.")
                try:
                    self.parent.data_layer.connect_to_cell_data()
                    self.UTILS.reporting.logResult("info", "(Marionette issue) Success!")
                except:
                    self.UTILS.reporting.logResult("info", "(Marionette issue) Unsuccessful!")

            self.marionette.switch_to_frame()
            self.UTILS.iframe.switchToFrame(*DOM.Settings.frame_locator)

        #
        # If we get prompted for action, say 'Turn ON'.
        #
        # (Because it's only 'if', we don't verify this element.)
        #
        time.sleep(2)
        try:
            self.parent.wait_for_element_displayed(*DOM.Settings.celldata_DataConn_ON, timeout=2)
            x = self.marionette.find_element(*DOM.Settings.celldata_DataConn_ON)
            if x.is_displayed():
                x.tap()
        except:
            pass

        #
        # Give it time to start up.
        #
        time.sleep(5)

        #
        # Check to see if data conn is now enabled (it may be, even if the icon doesn't appear).
        #
        self.UTILS.test.TEST(
            self.parent.data_layer.get_setting("ril.data.enabled"), "Data connection is enabled", True)

        #
        # Give the statusbar icon time to appear, then check for it.
        #
        # NOTE: 'wireless_off' works here: if it's true then the icon SHOULD be there, else
        #       it shouldn't.
        #
        if not self.parent.data_layer.get_setting("wifi.enabled"):
            x = self.UTILS.statusbar.isIconInStatusBar(DOM.Statusbar.dataConn)
            time.sleep(5)
            self.UTILS.test.TEST(x, "Data connection icon is present in the status bar.", True)

        self.UTILS.home.goHome()

    def verify_autoRetrieve_SelectedItem(self, value):
        #
        # Launch settings app.
        #
        self.launch()

        x = self.UTILS.element.getElement(DOM.Settings.msg_settings, "Messaging Settings button")
        x.tap()

        #
        # Tap on Auto Retireve Select
        #
        x = self.UTILS.element.getElement(DOM.Settings.auto_retrieve_select_btn, "Auto Retrieve Select")
        x.tap()

        #
        # Changing to top level frame
        #
        time.sleep(2)
        self.marionette.switch_to_frame()

        #
        # Selecting the specific option using que received parameter
        #
        if value == "off":
            x = self.UTILS.element.getElement(DOM.Settings.auto_retrieve_select_off,
                                              "Off option in Auto Retrieve Select")
        elif value == "on_with_r":
            x = self.UTILS.element.getElement(DOM.Settings.auto_retrieve_select_roaming,
                                      "On with roaming option in Auto Retrieve Select")
        elif value == "on_without_r":
            x = self.UTILS.element.getElement(DOM.Settings.auto_retrieve_select_no_roaming,
                                      "On without roaming option in Auto Retrieve Select")
        else:
            self.UTILS.reporting.logResult("info", "incorrect value received")
            self.UTILS.test.quitTest("FAILED: Incorrect parameter received in verify_autoRetrieve_SelectedItem()")

        #
        #Get option
        #
        y = x.get_attribute("aria-selected")

        #
        #Verifyin if the option is selected using the value true
        #
        self.UTILS.reporting.logResult("info", "Obtaining Selected option in Auto Retrieve select", y)
        self.UTILS.test.TEST(y == "true", "Checking value")

        #
        #Pressing ok button to leave select option
        #
        x = self.UTILS.element.getElement(DOM.Settings.ok_btn, "Messaging Settings button")
        x.tap()

    def wifi(self):
        #
        # Open wifi settings.
        #
        x = self.UTILS.element.getElement(DOM.Settings.wifi, "Wifi settings link")
        x.tap()

        self.UTILS.element.waitForElements(DOM.Settings.wifi_header, "Wifi header appears.", True, 20, False)

    def wifi_connect(self, wlan_name, username, passwd):
        #
        # Connects to the wifi specified in the parameters using the Settings app.
        # Launches Settings if it's not already running.
        #

        #
        # Are we in the settings app?
        #
        if self.UTILS.iframe.framePresent(*DOM.Settings.frame_locator):
            self.UTILS.iframe.switchToFrame(*DOM.Settings.frame_locator)
            try:
                self.parent.wait_for_element_displayed(*DOM.Settings.wifi)
                self.wifi()
            except:
                pass
        else:
            self.launch()
            self.wifi()

        self.wifi_switchOn()

        self.wifi_list_tapName(wlan_name)

        if self.wifi_forget():
            self.wifi_list_tapName(wlan_name)

        try:
            #
            # Asked for username.
            #
            self.parent.wait_for_element_displayed(*DOM.Settings.wifi_login_user, timeout=3)
            wifi_login_user = self.marionette.find_element(*DOM.Settings.wifi_login_user)
            if wifi_login_user.is_displayed():
                wifi_login_user.send_keys(username)
                self.UTILS.reporting.logResult("info", "Username '{}' supplied to connect to '{}' wifi.".\
                                     format(username, wlan_name))
        except:
            pass

        try:
            #
            # Asked for password.
            #
            wifi_login_pass = self.marionette.find_element(*DOM.Settings.wifi_login_pass)
            wifi_login_pass.send_keys(passwd)
            time.sleep(1)
            self.UTILS.reporting.logResult("info", "Password '{}' supplied to connect to '{}' wifi.".\
                                 format(passwd, wlan_name))
        except:
            pass

        try:
            wifi_login_ok = self.marionette.find_element(*DOM.Settings.wifi_login_ok_btn)
            wifi_login_ok.tap()
            self.UTILS.reporting.logResult("info", "Ok button pressed.")
        except:
            pass

        #
        # A couple of checks to wait for 'anything' to be Connected (only look for 'present' because it
        # might be off the bottom of the page).
        #
        self.UTILS.test.TEST(True, "Connected: {}".format(self.wifi_list_isConnected(wlan_name, timeout=10)))
        self.UTILS.test.TEST(self.wifi_list_isConnected(wlan_name, timeout=60),
                "Wifi '{}' is listed as 'connected' in wifi settings.".format(wlan_name), False)

        self.UTILS.test.TEST(self.parent.data_layer.get_setting("wifi.enabled"),
            "Wifi connection to '{}' established.".format(wlan_name), True)

    def wifi_forget(self, quiet=True):
        #
        # Forget the wifi (assumes you have clicked the wifi name).<br>
        # If quiet is True, then it will not assert if this wifi is already known.<br>
        # If quiet is True, then it will assert (and expect) that this wifi is already known.<br>
        # Either way, it will return True for forgotten, or False for 'not known'.
        #
        try:
            self.parent.wait_for_element_displayed(*DOM.Settings.wifi_details_header, timeout=2)
        except:
            return False

        wlan = self.UTILS.element.getElement(DOM.Settings.wifi_details_header, "Header").text
        self.UTILS.reporting.logResult("info", "Forgetting wifi '{}' ...".format(wlan))
        is_connected = False
        try:
            #
            # Already connected to this wifi (or connected automatically).
            # 'Forget' it (so we can reconnect as-per test) and tap the wifi name again.
            #
            self.parent.wait_for_element_displayed(*DOM.Settings.wifi_details_forget_btn, timeout=3)
            x = self.marionette.find_element(*DOM.Settings.wifi_details_forget_btn)
            x.tap()
            is_connected = True

            #
            # Takes a few seconds to disconnect, so check a few times.
            #
            is_forgotten = False
            for i in range(10):
                if self._checkDisconnected(wlan):
                    is_forgotten = True
                    break
                else:
                    time.sleep(2)
        except:
            pass

        if not quiet:
            _x = "was" if is_connected else "was not"
            _y = "and has been succesfully" if is_forgotten else "but could not be"

            self.UTILS.test.TEST(is_connected and is_forgotten,
                            "Wifi network '{}' {} connected {} forgotten.".format(wlan, _x, _y))

        return is_connected

    def _checkDisconnected(self, wlan):
        #
        # Private function to wait until this wifi network is no longer marked as "Connected".
        #
        x = self.marionette.find_elements(*DOM.Settings.wifi_available_networks)
        for i in x:
            if i.find_element("tag name", "a").text == wlan:
                if i.find_element("tag name", "small").text != "Connected":
                    return True
                else:
                    return False

    def wifi_list_isConnected(self, wlan_name, timeout=30):
        #
        # Verify the expected network is listed as connected in 'available networks'.
        #
        try:
            self.parent.wait_for_element_present("xpath", DOM.Settings.wifi_list_connected_xp.format(wlan_name),
                                          timeout=timeout)
            return True
        except:
            return False

    def wifi_list_isNotConnected(self, wlan_name, timeout=30):
        #
        # Verify the expected network is listed as connected in 'available networks'.
        #
        try:
            self.parent.wait_for_element_not_present("xpath", DOM.Settings.wifi_list_connected_xp.format(wlan_name),
                                              timeout=timeout)
            return True
        except:
            return False

    def wifi_list_tapName(self, wlan_name):
        #
        # Tap the network name in the list.
        #
        _wifi_name_element = ("xpath", DOM.Settings.wifi_name_xpath.format(wlan_name))
        x = self.UTILS.element.getElement(_wifi_name_element, "Wifi '{}'".format(wlan_name), True, 30, True)
        x.tap()
        time.sleep(2)

    def wifi_switchOn(self):
        #
        # Click slider to turn wifi on.
        #
        if not self.parent.data_layer.get_setting("wifi.enabled"):
            x = self.UTILS.element.getElement(DOM.Settings.wifi_enabled, "Enable wifi switch")
            x.tap()

        #
        # Nothing to check for yet, because the network may require login etc...,
        # so just wait a little while before proceeding ...
        #
        time.sleep(3)
