import time
from OWDTestToolkit import DOM

from OWDTestToolkit.utils.i18nsetup import I18nSetup
_ = I18nSetup(I18nSetup).setup()

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

    def wait_for_option_to_be_enabled(self, locator):
         #
        # Wait for option to be enabled
        #
        self.parent.wait_for_element_displayed(*locator)
        option = self.marionette.find_element(*locator)

        while option.get_attribute("aria-disabled"):
            option = self.marionette.find_element(*locator)
            continue

        
    def call_settings(self):

        self.wait_for_option_to_be_enabled(DOM.Settings.call_settings_option)

        x = self.UTILS.element.getElement(DOM.Settings.call_settings, "Call settings button")
        self.UTILS.element.simulateClick(x)
        self.UTILS.element.waitForElements(('xpath',
            DOM.GLOBAL.app_head_specific.format(_("Call Settings").encode("utf8"))), "Call settings header")

    def callID_verify(self):
        self.call_settings()

        self.UTILS.reporting.logResult("info", "Call number presses")

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

    def three_times_bad_pin2(self, wrong_pin2):
        """Change the PIN2.

        Enter a wrong PIN2 three consecutive times. After that, the PUK2 is requested,
        and also a new PIN2 value is entered twice.
        """
        for i in range(3):
            self.fdn_type_pin2(wrong_pin2)

    def restore_pin2(self, good_pin2, puk2):
        """Restore PIN2 using PUK2.

        After PIN2 has been entered wrongly three times, the PUK2 is required to unlock the SIM.
        """
        # SIM locked, enter PUK2 and new PIN2 twice
        puk2_input = self.UTILS.element.getElement(DOM.Settings.fdn_enter_puk2_input, "PUK2 input")
        puk2_input.send_keys(puk2)

        new_pin2_input = self.UTILS.element.getElement(DOM.Settings.fdn_puk2_pin2_input, "New PIN2 input")
        new_pin2_input.send_keys(good_pin2)

        confirm_pin2_input = self.UTILS.element.getElement(DOM.Settings.fdn_confirm_pin2_input, "Confirm PIN2 input")
        confirm_pin2_input.send_keys(good_pin2)

        ok_btn = self.UTILS.element.getElement(DOM.Settings.fdn_pin2_done, "OK button")
        ok_btn.tap()

    def cellular_and_data(self):
        #
        # Open cellular and data settings.
        #
        
        self.wait_for_option_to_be_enabled(DOM.Settings.data_connectivity)

        #
        # Once it is enabled, click on it
        #

        link = self.marionette.find_element(*DOM.Settings.cellData)
        link.tap()
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

        # We do not want suggestions or auto-correction for the APN values, so, just disable them
        self.data_layer.set_setting('keyboard.wordsuggestion', False)
        self.data_layer.set_setting('keyboard.autocorrect', False)

        #
        # Enter the data
        #
        
        #
        # This has to commented since there's a bug in Keyboard application from gaitestcase
        # Instead, we have to use the primitive methods from marionette.
        #

        # self.UTILS.general.typeThis(DOM.Settings.celldata_data_apn, "APN", apn,
        #                             p_no_keyboard=False, p_validate=False, p_clear=True, p_enter=True)

        # self.UTILS.general.typeThis(DOM.Settings.celldata_apn_user, "APN", identifier,
        #                             p_no_keyboard=False, p_validate=False, p_clear=True, p_enter=True)

        # self.UTILS.general.typeThis(DOM.Settings.celldata_apn_passwd, "APN", pwd,
        #                             p_no_keyboard=False, p_validate=False, p_clear=True, p_enter=True)

        apn_field = self.UTILS.element.getElement(DOM.Settings.celldata_data_apn, "APN name")
        apn_field.clear()
        apn_field.send_keys(apn)

        identifier_field = self.UTILS.element.getElement(DOM.Settings.celldata_apn_user, "APN identifier")
        identifier_field.clear()
        identifier_field.send_keys(identifier)

        pwd_field = self.UTILS.element.getElement(DOM.Settings.celldata_apn_passwd, "APN pass")
        pwd_field.clear()
        pwd_field.send_keys(pwd)

        #
        # Tap the ok button to save the changes
        #
        x = self.UTILS.element.getElement(DOM.Settings.celldata_ok_button, "Ok button")
        x.tap()

    def open_fdn(self):
        fdn = self.UTILS.element.getElement(DOM.Settings.call_fdn, "Fixed dialing numbers")
        fdn.tap()
        self.UTILS.element.waitForElements(('xpath',
            DOM.GLOBAL.app_head_specific.format(_("Fixed dialing numbers").encode("utf8"))), "FDN header")

    def go_enable_fdn(self, enable):
        status = self.UTILS.element.getElement(DOM.Settings.fdn_status, "FDN status").text

        do_return = (enable and status == _("Enabled")) or (not enable and status == _("Disabled"))

        #
        # If it is already enabled/disabled, then return False, so that we can
        # know outside this method that there is no need in typing the PIN2
        #
        if do_return:
            return False

        time.sleep(3)
        switch = self.UTILS.element.getElement(DOM.Settings.fdn_enable, "{} FDN".\
                                               format("Enable" if enable else "Disable"))
        switch.tap()
        # self.UTILS.element.simulateClick(switch)

        header = ('xpath', DOM.GLOBAL.app_head_specific.format(_("Enable FDN") if enable else _("Disable FDN")))
        self.UTILS.element.waitForElements(header, "{} FDN header".format("Enable" if enable else "Disable"))
        return True

    def fdn_type_pin2(self, pin2):
        pin2_input = self.UTILS.element.getElement(DOM.Settings.fdn_pin2_input, "PIN2 input", timeout=20)
        pin2_input.send_keys(pin2)

        done_btn = self.UTILS.element.getElement(DOM.Settings.fdn_pin2_done, "Done button")
        done_btn.tap()

    def change_pin2_full_process(self, wrong_pin2, good_pin2, puk2):
        self.call_settings()
        self.open_fdn()
        result = self.go_enable_fdn(True)

        if result:
            self.three_times_bad_pin2(wrong_pin2)
            self.restore_pin2(good_pin2, puk2)

    def confirm_data_conn(self):
        self.UTILS.iframe.switchToFrame(*DOM.Settings.frame_locator)
        try:
            self.UTILS.reporting.logResult("info", "Waiting for data switch-on confirmation")
            self.parent.wait_for_element_displayed(*DOM.Settings.celldata_DataConn_ON)
            x = self.marionette.find_element(*DOM.Settings.celldata_DataConn_ON)
            x.tap()
            self.UTILS.reporting.logResult("info", "Data connection: confirmed")
            self.UTILS.reporting.log_to_file("*** Data connection confirmed")
        except Exception as e:
            self.UTILS.reporting.log_to_file("*** Exception: {}".format(e))
            self.UTILS.reporting.logResult("info", "No data connection confirmation")

    def reset_pin2(self, old_pin2, new_pin2):
        self.call_settings()
        self.open_fdn()
        changed = self.go_enable_fdn(True)
        if changed:
            self.fdn_type_pin2(old_pin2)

        reset_btn = self.UTILS.element.getElement(DOM.Settings.fdn_reset_pin2_btn, "Reset PIN2 button")
        reset_btn.tap()

        pin2_input = self.UTILS.element.getElement(DOM.Settings.fdn_pin2_input, "Old PIN2 input")
        pin2_input.send_keys(old_pin2)

        pin2_new_input = self.UTILS.element.getElement(DOM.Settings.fdn_puk2_pin2_input, "New PIN2 input")
        pin2_new_input.send_keys(new_pin2)

        pin2_confirm_input = self.UTILS.element.getElement(DOM.Settings.fdn_confirm_pin2_input, "Confirm new PIN2")
        pin2_confirm_input.send_keys(new_pin2)

        done_btn = self.UTILS.element.getElement(DOM.Settings.fdn_pin2_done, "Done Reset PIN2 button")
        done_btn.tap()

    def fdn_open_auth_numbers(self):
        auth_list = self.UTILS.element.getElement(DOM.Settings.fdn_auth_numbers, "Authorized numbers")
        auth_list.tap()
        header = ('xpath', DOM.GLOBAL.app_head_specific.format(_("Authorized numbers").encode("utf8")))
        self.UTILS.element.waitForElements(header, "Authorized numbers header")

    def fdn_add_auth_number(self, name, number, pin2):
        #
        # Add a contact to the list of authorized numbers
        #
        add_btn = self.UTILS.element.getElement(DOM.Settings.fdn_add_auth_number, "Add button")
        add_btn.tap()
        self.UTILS.element.waitForElements(('xpath',
            DOM.GLOBAL.app_head_specific.format(_("Add contact"))), "Add contact header")

        #
        # Fill contact data
        #
        name_input = self.UTILS.element.getElement(DOM.Settings.fdn_add_auth_number_name, "Auth contact name")
        name_input.send_keys(name)

        number_input = self.UTILS.element.getElement(DOM.Settings.fdn_add_auth_number_number, "Auth contact number")
        number_input.send_keys(number)

        done_btn = self.UTILS.element.getElement(DOM.Settings.fdn_add_auth_number_done, "Auth contact Done button")
        done_btn.tap()

        #
        # PIN2 Confirmation
        #
        self.UTILS.element.waitForElements(('xpath',
            DOM.GLOBAL.app_head_specific.format(_("Enter SIM PIN2"))), "Confirm SIM PIN2 header")

        pin2_input = self.UTILS.element.getElement(DOM.Settings.fdn_pin2_input, "PIN2 input")
        pin2_input.send_keys(pin2)

        done_btn = self.UTILS.element.getElement(DOM.Settings.fdn_pin2_done, "Done button")
        done_btn.tap()

        #
        # Check the number has been added to the list
        #
        elem = (DOM.Settings.fdn_auth_numbers_list_elem[0], 
            DOM.Settings.fdn_auth_numbers_list_elem[1].format(number))
        self.UTILS.element.waitForElements(elem, "Waiting for contact to be in the list", True, 30)

    def fdn_delete_auth_number(self, name, number, pin2):
        #
        # This method deletes a contact from the authorized numbers list
        # It must be called once the list has been displayed
        #

        # Tap over the contact
        #
        elem = (DOM.Settings.fdn_auth_numbers_list_elem[0],
            DOM.Settings.fdn_auth_numbers_list_elem[1].format(number))

        contact = self.UTILS.element.getElement(elem, "Contact to be deleted")
        contact.tap()
        time.sleep(1)

        #
        # Choose delete option
        #
        delete_option = self.UTILS.element.getElement(DOM.Settings.fdn_auth_number_action_delete, "Delete option", is_displayed=True, timeout=20)
        delete_option.tap()

        #
        # PIN2 Confirmation
        #
        self.UTILS.element.waitForElements(('xpath',
            DOM.GLOBAL.app_head_specific.format(_("Enter SIM PIN2"))), "Confirm SIM PIN2 header")

        pin2_input = self.UTILS.element.getElement(DOM.Settings.fdn_pin2_input, "PIN2 input")
        pin2_input.send_keys(pin2)

        done_btn = self.UTILS.element.getElement(DOM.Settings.fdn_pin2_done, "Done button")
        done_btn.tap()

        #
        # Check the number is no longer present in the list
        #
        elem = (DOM.Settings.fdn_auth_numbers_list_elem[0],
            DOM.Settings.fdn_auth_numbers_list_elem[1].format(number))
        self.UTILS.element.waitForNotElements(elem, "Waiting for contact NOT to be in the list", True, 30)

    def fdn_delete_all_auth_numbers(self, pin2):
        contacts = self.UTILS.element.getElements(DOM.Settings.fdn_auth_numbers_list, "Contact list")
        self.UTILS.reporting.debug("*** DELETING FDN CONTACTS: [{}]".format(contacts))
        #
        # We have to do it this way to avoid StaleElementException to be raised
        #
        for i in range(len(contacts)):
            contact = self.UTILS.element.getElement(DOM.Settings.fdn_auth_numbers_list, "contact")
            self.UTILS.reporting.debug("*** Contact found: [{}]".format(contact))
            number = self.marionette.find_element('css selector', 'small', contact.id).text
            contact = self.UTILS.element.getElement(DOM.Settings.fdn_auth_numbers_list, "contact")
            name = self.marionette.find_element('css selector', 'span', contact.id).text
            self.fdn_delete_auth_number(name, number, pin2)
            time.sleep(2)

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
        x = self.UTILS.element.getElement(DOM.Settings.celldata_DataSettings, "Data settings link")
        self.UTILS.element.scroll_into_view(x)
        x.tap()

    def open_msg_settings(self):
        #
        # Open cellular and data settings.
        #
        self.cellular_and_data()
        x = self.UTILS.element.getElement(DOM.Settings.celldata_MsgSettings, "Message settings link")
        self.UTILS.element.scroll_into_view(x)
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
        self.goBack()

    def setAlarmVolume(self, volume):
        #
        # Set the volume for alarms.
        #
        self.parent.data_layer.set_setting('audio.volume.alarm', volume)

    def setNetworkOperator(self):
        #
        # Open cellular and data settings.
        #
        x = self.UTILS.element.getElement(DOM.Settings.cellData, "Cellular and Data settings link")
        self.UTILS.element.simulateClick(x)

        self.UTILS.element.waitForElements(DOM.Settings.celldata_header, "Celldata header", True, 20, False)

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

    def change_sim_pin(self, old_pin, new_pin, confirm_pin):
        #
        # This method changes the current PIN code to a new one
        #
        sim_security = self.UTILS.element.getElement(DOM.Settings.sim_security, "SIM Security")
        self.UTILS.element.scroll_into_view(sim_security)
        sim_security_tag = self.UTILS.element.getElement(DOM.Settings.sim_security_tag, "SIM security status")

        # If no SIM security enabled, enable it
        if sim_security_tag.text == _("Disabled"):
            self.enable_sim_security(True, old_pin)
            self.goBack()

        sim_security.tap()
        change_btn = self.UTILS.element.getElement(DOM.Settings.sim_security_change_pin, "Change PIN button")
        change_btn.tap()

        old = self.UTILS.element.getElement(DOM.Settings.change_pin_old_input, "getting OLD PIN input")
        old.send_keys(old_pin)

        new = self.UTILS.element.getElement(DOM.Settings.change_pin_new_input, "getting new PIN input")
        new.send_keys(new_pin)

        confirm = self.UTILS.element.getElement(DOM.Settings.change_pin_confirm_input, "getting CONFIRM PIN input")
        confirm.send_keys(confirm_pin)

        done_btn = self.UTILS.element.getElement(DOM.Settings.change_pin_done_btn, "Change PIN Done button")
        done_btn.tap()

    def enable_sim_security(self, enable, pin):
        #
        # This method sets the SIM security configuration.
        #
        sim_security = self.UTILS.element.getElement(DOM.Settings.sim_security, "SIM Security")
        self.UTILS.element.scroll_into_view(sim_security)
        sim_security_tag = self.UTILS.element.getElement(DOM.Settings.sim_security_tag, "SIM security status")
        time.sleep(4)

        # If the attribute is already in the desired state, return
        current = sim_security_tag.text == _("Enabled")
        if enable == current:
            #click anyway so that we can later check whether the button to change the PIN
            sim_security.tap()
            return

        sim_security.tap()
        sim_security_pin = self.UTILS.element.getElement(DOM.Settings.sim_security_pin, "SIM security switch")
        sim_security_pin.tap()

        self.UTILS.element.waitForElements(DOM.Settings.sim_security_enter_pin_header, "Enter PIN header")

        #
        # Type the PIN in
        #
        pin_input = self.UTILS.element.getElement(DOM.Settings.sim_security_enter_pin_input, "Enter PIN input")
        pin_input.send_keys(pin)

        done_btn = self.UTILS.element.getElement(DOM.Settings.sim_security_enter_pin_done, "Done button")
        done_btn.tap()

        self.UTILS.element.waitForElements(DOM.Settings.sim_security_header, "SIM Security header")

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
                                      False, 15, False)
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

        self.apps.kill_all()

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
