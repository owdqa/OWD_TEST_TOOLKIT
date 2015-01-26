import time
from marionette import Actions
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.decorators import retry

from OWDTestToolkit.utils.i18nsetup import I18nSetup
_ = I18nSetup(I18nSetup).setup()


class Settings(object):

    def __init__(self, parent):
        self.apps = parent.apps
        self.data_layer = parent.data_layer
        self.parent = parent
        self.marionette = parent.marionette
        self.UTILS = parent.UTILS
        self.actions = Actions(self.marionette)

    def launch(self):
        self.app = self.apps.launch(self.__class__.__name__)
        self.UTILS.element.waitForNotElements(DOM.GLOBAL.loading_overlay,
                                              self.__class__.__name__ + " app - loading overlay")
        return self.app

    def go_back(self, elem_id=None):
        """
        Tap the back icon.
        """
        # TODO: remove tap with coordinates after Bug 1061698 is fixed
        if elem_id is not None:
            self.UTILS.reporting.info("Tapping element: {}".format(elem_id))
            header = self.UTILS.element.getElement(('css selector', 'gaia-header#{}[action=back]'.format(elem_id)),
                                                   "Back button")
            time.sleep(5)
            header.tap(25, 25)
            self.UTILS.reporting.info("Tapped {}".format(elem_id))
        else:
            self.UTILS.reporting.info("Tapping unknown element")
            headers = self.marionette.find_elements('css selector', 'gaia-header[action=back]')
            for header in headers:
                if header.is_displayed():
                    header.tap(25, 25)
                    break
        time.sleep(2)

    def go_sound(self):
        """
        Go to Sound menu.
        """
        self.launch()
        sound_menu = self.UTILS.element.getElement(DOM.Settings.sound, "Sound setting link")
        sound_menu.tap()

    def wait_for_option_to_be_enabled(self, locator):
        self.parent.wait_for_condition(lambda m: m.find_element(*locator).get_attribute("aria-disabled") is None,
                                       timeout=30, message="Option to be enabled")

    def call_settings(self, sim_card_number=1):
        """
        Open call settings
        """
        self.wait_for_option_to_be_enabled(DOM.Settings.call_settings_option)

        call_settings_btn = self.UTILS.element.getElement(DOM.Settings.call_settings, "Call settings button")
        self.UTILS.element.simulateClick(call_settings_btn)
        """
        In case the device supports dual sim, we have to select one before
        entering the call_settings menu.
        """
        try:
            elem = (DOM.Settings.call_settings_sim_card_number[0],
                    DOM.Settings.call_settings_sim_card_number[1].format(sim_card_number))

            self.parent.wait_for_element_displayed(elem[0], elem[1], 20)
            sim_card_option = self.marionette.find_element(*elem)
            sim_card_option.tap()
        except:
            self.UTILS.reporting.logResult("info", "No double SIM detected. Keep working...")

        self.UTILS.element.waitForElements(('xpath', DOM.GLOBAL.app_head_specific.
                                            format(_("Call Settings").encode("utf8"))), "Call settings header")

    def cellular_and_data(self):
        """
        Open cellular and data settings.
        """
        self.wait_for_option_to_be_enabled(DOM.Settings.data_connectivity)

        # Once it is enabled, click on it
        self.parent.wait_for_element_displayed(*DOM.Settings.cellData)
        link = self.marionette.find_element(*DOM.Settings.cellData)
        link.tap()

        self.UTILS.element.waitForElements(DOM.Settings.celldata_header, "Celldata header", True, 20, False)

    def open_sim_settings(self, sim_card_number=1):
        """
        Open cellular and data settings.
        """
        # In case the device supports dual sim, we have to select one before entering the call_settings menu.
        sim_card_option = self.get_multi_sim(sim_card_number)
        if sim_card_option:
            sim_card_option.tap()

    def open_apn_settings(self):
        apn_settings_option = self.UTILS.element.getElement(
            DOM.Settings.cellData_apn_settings, "Network Operator option")
        apn_settings_option.tap()
        self.parent.wait_for_element_displayed(*DOM.Settings.apn_settings_header)

    def open_network_operator_menu(self):
        network_operator_option = self.UTILS.element.getElement(
            DOM.Settings.networkOperator_button, "Network Operator option")
        network_operator_option.tap()
        self.parent.wait_for_element_displayed(*DOM.Settings.networkOperator_header)

    def open_data_settings(self, sim_card_number=1):
        self.open_apn_settings()
        data_menu = self.UTILS.element.getElement(DOM.Settings.celldata_DataSettings, "Data settings link")
        data_menu.tap()

    def open_msg_settings(self, sim_card_number=1):
        self.open_apn_settings()
        msg_menu = self.UTILS.element.getElement(DOM.Settings.celldata_MsgSettings, "Message settings link")
        msg_menu.tap()

    def select_default_apn(self, apn):
        """
        Makes a certain apn default
        """
        # Tap on the added APN
        dom_elem = (DOM.Settings.apn_item_by_name[0], DOM.Settings.apn_item_by_name[1].format(apn))
        apn_elem = self.UTILS.element.getElement(dom_elem, "APN to make default")

        radio_button = self.get_radio_button_for_label(apn_elem)
        self.UTILS.element.simulateClick(radio_button)

    def get_label_for_radio_button(self, da_input):
        return self.UTILS.element.getParent(self.UTILS.element.getParent(da_input)).find_element(*('css selector', 'label.name span'))

    def get_radio_button_for_label(self, label_elem):
        return self.UTILS.element.getParent(self.UTILS.element.getParent(label_elem)).find_element(*('css selector', 'input[type=radio]'))

    def is_apn_selected(self, apn):
        # Tap on the added APN
        dom_elem = (DOM.Settings.apn_item_by_name[0], DOM.Settings.apn_item_by_name[1].format(apn))
        apn_elem = self.UTILS.element.getElement(dom_elem, "APN to make default")

        radio_button = self.get_radio_button_for_label(apn_elem)
        return radio_button.is_selected()

    def check_apn_content(self, apn_name, apn_user, apn_pwd):
        def _test_apn_data(locator, info):
            self.parent.wait_for_element_displayed(*locator)
            input_value = self.marionette.find_element(*locator).get_attribute("value")
            self.UTILS.test.test(input_value == info, "'Info' field contains expected value: {}".format(input_value))

        locators = [DOM.Settings.celldata_data_apn, DOM.Settings.celldata_apn_user, DOM.Settings.celldata_apn_passwd]
        expected_data = [apn_name, apn_user, apn_pwd]
        map(_test_apn_data, locators, expected_data)

    def tap_on_apn(self, apn_name):
        apn = (DOM.Settings.apn_item_by_name[0], DOM.Settings.apn_item_by_name[1].format(apn_name))
        apn_elem = self.UTILS.element.getElement(apn, "Got the apn to tap on")
        apn_elem.tap()
        self.UTILS.element.waitForElements(DOM.Settings.apn_editor_header, "APN Editor header")

    def get_apn_data(self):
        """
        Gets the data (so far, name, user and passwd) of the already selected APN
        """
        def _get_value(locator):
            return self.marionette.find_element(*locator).get_attribute("value")

        locators = [DOM.Settings.celldata_data_apn, DOM.Settings.celldata_apn_user, DOM.Settings.celldata_apn_passwd]
        return map(_get_value, locators)

    def set_network_operator(self, network_type):
        self.open_network_operator_menu()

        time.sleep(2)
        network_type_select = self.UTILS.element.getElement(
            DOM.Settings.networkOperator_types, "Network Operator type")
        network_type_select.tap()

        self.marionette.switch_to_frame()

        network_type_locator = (DOM.Settings.networkOperator_select_type[0],
                                DOM.Settings.networkOperator_select_type[1].format(network_type))

        option = self.UTILS.element.getElement(
            network_type_locator, "Network Operator. Select: {}".format(network_type))
        option.tap()

        select_ok_btns = self.marionette.find_elements(*DOM.Settings.networkOperator_OK_btn)
        for btn in select_ok_btns:
            if btn.is_displayed():
                btn.tap()
        self.UTILS.iframe.switchToFrame(*DOM.Settings.frame_locator)

    def confirm_data_conn(self):
        self.UTILS.iframe.switchToFrame(*DOM.Settings.frame_locator)
        try:
            self.UTILS.reporting.logResult("info", "Waiting for data switch-on confirmation")
            self.parent.wait_for_element_displayed(*DOM.Settings.celldata_DataConn_ON)
            data_on_btn = self.marionette.find_element(*DOM.Settings.celldata_DataConn_ON)
            data_on_btn.tap()
            self.UTILS.reporting.logResult("info", "Data connection: confirmed")
            self.UTILS.reporting.log_to_file("*** Data connection confirmed")
        except Exception as e:
            self.UTILS.reporting.log_to_file("*** Exception: {}".format(e))
            self.UTILS.reporting.logResult("info", "No data connection confirmation")

    def get_multi_sim(self, sim_card_number=1):
        """
        Try to find the element for selecting between multiple SIMs.
        Return the element for the selected SIM number, if found. None otherwise.
        """
        try:
            elem = (DOM.Settings.cellData_sim_card_number[0],
                    DOM.Settings.cellData_sim_card_number[1].format(sim_card_number))

            self.parent.wait_for_element_displayed(elem[0], elem[1], 20)
            return self.marionette.find_element(*elem)
        except:
            self.UTILS.reporting.logResult("info", "No double SIM detected. Keep working...")
        return None

    def skip_multisim(self):
        """Detect if we are in a multisim selection menu and skip it using the Back button.
        """
        time.sleep(2)
        sim_card_option = self.get_multi_sim()
        if sim_card_option:
            self.go_back()

    def configure_mms_auto_retrieve(self, value):
        # Tap on Messaging Settings button
        time.sleep(2)
        settings_btn = self.UTILS.element.getElement(DOM.Settings.msg_settings, "Messaging Settings button")
        self.UTILS.element.simulateClick(settings_btn)

        time.sleep(2)
        # Tap on Auto Retrieve Select
        auto_retr_btn = self.UTILS.element.getElement(DOM.Settings.auto_retrieve_select_btn, "Auto Retrieve Select")
        auto_retr_btn.tap()

        # Changing to top level frame
        time.sleep(2)
        self.marionette.switch_to_frame()

        # Selecting the specific option using the received parameter
        auto_retrieve_option = None
        if value == "off":
            auto_retrieve_option = _("Off")
        elif value == "on_with_r":
            auto_retrieve_option = _("On with roaming")
        elif value == "on_without_r":
            auto_retrieve_option = _("On without roaming")
        else:
            self.UTILS.test.test(False, "FAILED: Incorrect parameter received in configure_mms_auto_retrieve()")

        self.UTILS.reporting.debug("Auto retrieve option selected: {}".format(auto_retrieve_option))
        dom = (DOM.Settings.auto_retrieve_select[0], DOM.Settings.auto_retrieve_select[1].format(auto_retrieve_option))
        select_btn = self.UTILS.element.getElement(dom, "Auto retrieve option")
        select_btn.tap()

        # Tapping on OK button in auto Retrieve select
        ok_btn = self.UTILS.element.getElement(DOM.Settings.auto_retrieve_ok_btn,
                                               "Tapping on OK button in auto Retrieve select")
        ok_btn.tap()

        self.UTILS.iframe.switchToFrame(*DOM.Settings.frame_locator)
        self.marionette.find_element('css selector', 'gaia-header[action=back]').tap(25, 25)

    def create_custom_apn(self, apn, identifier, pwd, sim_card_number=1):
        # We do not want suggestions or auto-correction for the APN values, so, just disable them
        self.data_layer.set_setting('keyboard.wordsuggestion', False)
        self.data_layer.set_setting('keyboard.autocorrect', False)

        def _fill_apn_data(locator, info):
            self.parent.wait_for_element_displayed(*locator)
            input_field = self.marionette.find_element(*locator)
            input_field.send_keys(info)

        # Select custom settings
        add_new_apn = self.UTILS.element.getElement(DOM.Settings.add_new_apn, "Add new APN button")
        add_new_apn.tap()

        locators = [DOM.Settings.celldata_data_apn, DOM.Settings.celldata_apn_user, DOM.Settings.celldata_apn_passwd]
        data = [apn, identifier, pwd]
        map(_fill_apn_data, locators, data)

        # Tap the ok button to save the changes
        ok_btn = self.UTILS.element.getElement(DOM.Settings.apn_ok_button, "Ok button")
        time.sleep(1)
        ok_btn.tap()

    def initial_check_fdn(self, pin2, puk2):
        """This method ensure FDN is disabled, and, if during that process it finds out that
            the SIM card is locked because of PUK2 is required, it unlocks the SIM and then,
            disables FDN

            This method should be called as soon as possible inside the setUp method of each
            test that deals somehow with FDN
        """
        self.call_settings()
        self.open_fdn()

        status = self.UTILS.element.getElement(DOM.Settings.fdn_status, "FDN status").text
        if (status == _("Disabled")):
            self.UTILS.reporting.logResult('info', '[initial_check_fdn] FDN disabled')
            return

        switch = self.UTILS.element.getElement(DOM.Settings.fdn_enable, "Disable FDN")
        switch.tap()

        header = ('xpath', DOM.GLOBAL.app_head_specific.format(_("Disable FDN")))
        self.UTILS.element.waitForElements(header, "Disable FDN header")
        self.fdn_type_pin2(pin2)

        try:
            self.parent.wait_for_element_displayed(
                *('xpath', DOM.GLOBAL.app_head_specific.format(_("Fixed dialing numbers").encode("utf8"))))
        except:
            self.restore_pin2(pin2, puk2)

            switch = self.UTILS.element.getElement(DOM.Settings.fdn_enable, "Disable FDN")
            time.sleep(1)
            switch.tap()

            header = ('xpath', DOM.GLOBAL.app_head_specific.format(_("Disable FDN")))
            self.UTILS.element.waitForElements(header, "Disable FDN header")
            self.fdn_type_pin2(pin2)
            status = self.UTILS.element.getElement(DOM.Settings.fdn_status, "FDN status").text
            self.UTILS.test.test(status == _("Disabled"), "FDN is DISABLED on way or another")


    def open_fdn(self):
        fdn = self.UTILS.element.getElement(DOM.Settings.call_fdn, "Fixed dialing numbers")
        fdn.tap()
        self.UTILS.element.waitForElements(('xpath', DOM.GLOBAL.app_head_specific.format(_("Fixed dialing numbers").
                                                                                         encode("utf8"))), "FDN header")

    def go_enable_fdn(self, enable):
        status = self.UTILS.element.getElement(DOM.Settings.fdn_status, "FDN status").text

        do_return = (enable and status == _("Enabled")) or (not enable and status == _("Disabled"))
        """
        If it is already enabled/disabled, then return False, so that we can
        know outside this method that there is no need in typing the PIN2
        """
        if do_return:
            self.UTILS.reporting.logResult('info', 'FDN already {}!'.format("Enabled" if enable else "Disabled"))
            return False

        switch = self.UTILS.element.getElement(DOM.Settings.fdn_enable, "{} FDN".
                                               format("Enable" if enable else "Disable"))
        switch.tap()
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

    def reset_pin2(self, old_pin2, new_pin2):
        self.call_settings()
        self.open_fdn()
        changed = self.go_enable_fdn(True)
        if changed:
            self.fdn_type_pin2(old_pin2)

        reset_btn = self.UTILS.element.getElement(DOM.Settings.fdn_reset_pin2_btn, "Reset PIN2 button")
        time.sleep(1)
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

        self.parent.wait_for_condition(
            lambda m: self._is_auth_numbers_menu_tapped(), timeout=30, message="'Authorized numbers' menu tapped")

    def _is_auth_numbers_menu_tapped(self):

        header = ('xpath', DOM.GLOBAL.app_head_specific.format(_("Authorized numbers").encode("utf8")))
        try:
            self.parent.wait_for_element_displayed(*header)
            return True
        except:
            self.UTILS.reporting.logResult("info", "Looks like 'Authorized numbers' has not been tapped")
            auth_list = self.UTILS.element.getElement(DOM.Settings.fdn_auth_numbers, "Authorized numbers")
            auth_list.tap()
            return False

    def fdn_add_auth_number(self, name, number, pin2):
        """
        Add a contact to the list of authorized numbers
        """
        add_btn = self.UTILS.element.getElement(DOM.Settings.fdn_add_auth_number, "Add button")
        add_btn.tap()
        self.UTILS.element.waitForElements(('xpath', DOM.GLOBAL.app_head_specific.format(_("Add contact"))),
                                           "Add contact header")

        # Fill contact data
        name_input = self.UTILS.element.getElement(DOM.Settings.fdn_add_auth_number_name, "Auth contact name")
        name_input.send_keys(name)

        number_input = self.UTILS.element.getElement(DOM.Settings.fdn_add_auth_number_number, "Auth contact number")
        number_input.send_keys(number)

        done_btn = self.UTILS.element.getElement(DOM.Settings.fdn_add_auth_number_done, "Auth contact Done button")
        done_btn.tap()

        # PIN2 Confirmation
        self.UTILS.element.waitForElements(('xpath', DOM.GLOBAL.app_head_specific.format(_("Enter SIM PIN2"))),
                                           "Confirm SIM PIN2 header")

        pin2_input = self.UTILS.element.getElement(DOM.Settings.fdn_pin2_input, "PIN2 input")
        pin2_input.send_keys(pin2)

        done_btn = self.UTILS.element.getElement(DOM.Settings.fdn_pin2_done, "Done button")
        done_btn.tap()

        # Check the number has been added to the list
        elem = (DOM.Settings.fdn_auth_numbers_list_elem[0],
                DOM.Settings.fdn_auth_numbers_list_elem[1].format(number))
        self.UTILS.element.waitForElements(elem, "Waiting for contact to be in the list", True, 30)

    def fdn_delete_auth_number(self, number, pin2):
        """
        This method deletes a contact from the authorized numbers list
        It must be called once the list has been displayed
        """

        # Tap over the contact
        elem = (DOM.Settings.fdn_auth_numbers_list_elem[0],
                DOM.Settings.fdn_auth_numbers_list_elem[1].format(number))

        try:
            self.parent.wait_for_element_displayed(*elem)
            contact = self.marionette.find_element(*elem)
            contact.tap()
            time.sleep(1)
        except:
            self.UTILS.reporting.logResult("info", "Something went wrong deleting the contact from FDN list")
            return

        # Choose delete option
        delete_option = self.UTILS.element.getElement(
            DOM.Settings.fdn_auth_number_action_delete, "Delete option", is_displayed=True, timeout=20)
        delete_option.tap()

        # PIN2 Confirmation
        self.UTILS.element.waitForElements(('xpath', DOM.GLOBAL.app_head_specific.format(_("Enter SIM PIN2"))),
                                           "Confirm SIM PIN2 header", True, 10)

        pin2_input = self.UTILS.element.getElement(DOM.Settings.fdn_pin2_input, "PIN2 input", True, 10)
        pin2_input.send_keys(pin2)

        done_btn = self.UTILS.element.getElement(DOM.Settings.fdn_pin2_done, "Done button", True, 10)
        done_btn.tap()

        time.sleep(2)

        # Check the number is no longer present in the list
        elem = (DOM.Settings.fdn_auth_numbers_list_elem[0],
                DOM.Settings.fdn_auth_numbers_list_elem[1].format(number))
        self.UTILS.element.waitForNotElements(elem, "Waiting for contact NOT to be in the list", True, 30)

    def fdn_delete_all_auth_numbers(self, pin2):
        contacts = self.UTILS.element.getElements(DOM.Settings.fdn_auth_numbers_list, "Contact list")
        self.UTILS.reporting.debug("*** DELETING FDN CONTACTS: [{}]".format(contacts))

        # We have to do it this way to avoid StaleElementException to be raised
        for i in range(len(contacts)):
            contact = self.UTILS.element.getElement(DOM.Settings.fdn_auth_numbers_list, "contact")
            self.UTILS.reporting.debug("*** Contact found: [{}]".format(contact))
            number = self.marionette.find_element('css selector', 'small', contact.id).text
            self.UTILS.reporting.logResult("info", "Number of contact to be deleted: {}".format(number))
            self.fdn_delete_auth_number(number, pin2)
            time.sleep(2)

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

    def downloads(self):
        """
        Open downloads.
        sometimes after checking the notification, downloads list is already opened
        """
        try:
            self.parent.wait_for_element_displayed(DOM.Settings.downloads[0], DOM.Settings.downloads[1], timeout=10)
        except:
            self.UTILS.element.waitForElements(DOM.Settings.downloads_header,
                                               "Downloads header appears.", True, 10, True)
            return

        downloads_link = self.marionette.find_element(*DOM.Settings.downloads)

        self.UTILS.element.scroll_into_view(downloads_link)
        time.sleep(2)
        downloads_link.tap()
        self.UTILS.element.waitForElements(DOM.Settings.downloads_header,
                                           "Downloads header appears.", True, 20, True)

        # Code commented due to Bug 1042404 - in the meantime, we just wait some time to make
        # sure everything is loaded
        # try:
        #     self.parent.wait_for_element_displayed(*DOM.DownloadManager.download_empty_list_content)
        # except:
        #     self.parent.wait_for_element_displayed(*DOM.DownloadManager.download_list_elems)
        time.sleep(5)

    def hotspot(self):
        """
        Open 'Internet sharing' settings (also known as 'hotspot').
        """
        self.UTILS.reporting.info("*** Looking for hotspot: {}".format(DOM.Settings.hotspot))
        self.parent.wait_for_element_displayed(*DOM.Settings.hotspot, timeout=30)
        hotspot_elem = self.marionette.find_element(*DOM.Settings.hotspot)
        self.UTILS.reporting.info("*** Found hotspot menu: {}".format(hotspot_elem))
        time.sleep(1)
        self.UTILS.element.scroll_into_view(hotspot_elem)
        time.sleep(1)
        hotspot_elem.tap()
        time.sleep(1)

    def disable_hotspot(self):
        """
        Disable hotspot (internet sharing) - assumes Settings app is already open.
        """
        self.UTILS.reporting.logResult("info", "<u>Disabling hotspot ...</u>")

        # Is it already disabled?
        hotspot_settings = self.UTILS.element.getElement(DOM.Settings.hotspot_settings, "Hotspot settings")
        if not hotspot_settings.is_enabled():
            self.UTILS.reporting.logResult("info", "Hotspot is already disabled.")
            return True

        switch = self.UTILS.element.getElement(DOM.Settings.hotspot_switch, "Hotspot switch")
        switch.tap()
        time.sleep(1)

        self.parent.wait_for_condition(lambda m: not m.find_element(*DOM.Settings.hotspot_settings).is_enabled())
        is_disabled = not self.marionette.find_element(*DOM.Settings.hotspot_settings).is_enabled()

        is_status_icon = self.parent.wait_for_element_not_present(*DOM.Statusbar.hotspot)

        self.UTILS.test.test(is_disabled, "Hotspot settings are disabled (because 'hotspot' is not running).")
        self.UTILS.test.test(not is_status_icon, "Hotspot icon is not present in the status bar.")

    def enable_hotspot(self):
        """
        Enable hotspot (internet sharing) - assumes Settings app is already open.
        """
        self.UTILS.reporting.logResult("info", "<u>Enabling hotspot ...</u>")

        # Is it already enabled?
        hotspot_settings = self.UTILS.element.getElement(DOM.Settings.hotspot_settings, "Hotspot settings")
        # FJCS: disabled == "true" to enable?
        if hotspot_settings.is_enabled():
            self.UTILS.reporting.logResult("info", "Hotspot is already enabled.")
            return True

        switch = self.UTILS.element.getElement(DOM.Settings.hotspot_switch, "Hotspot switch")
        time.sleep(1)
        switch.tap()
        time.sleep(1)

        self.parent.wait_for_condition(lambda m: m.find_element(*DOM.Settings.hotspot_settings).is_enabled())
        is_enabled = self.marionette.find_element(*DOM.Settings.hotspot_settings).is_enabled()

        self.marionette.switch_to_frame()
        is_status_icon = self.marionette.find_element(*DOM.Statusbar.hotspot)
        self.UTILS.iframe.switchToFrame(*DOM.Settings.frame_locator)

        self.UTILS.test.test(is_enabled, "Hotspot settings are disabled (because 'hotspot' is now running).")
        self.UTILS.test.test(is_status_icon, "Hotspot icon is present in the status bar.")

    def fxa(self):
        self.parent.wait_for_element_displayed(DOM.Settings.fxa[0], DOM.Settings.fxa[1], timeout=20)
        fxa_link = self.marionette.find_element(*DOM.Settings.fxa)
        self.UTILS.element.scroll_into_view(fxa_link)
        time.sleep(2)
        fxa_link.tap()

    def is_fxa_logged_in(self):
        try:
            self.parent.wait_for_element_displayed(*DOM.Settings.fxa_logged_in_screen)
            return True
        except:
            return False

    def fxa_log_out(self):
        if not self.is_fxa_logged_in():
            return

        log_out_btn = self.marionette.find_element(*DOM.Settings.fxa_log_out_btn)
        log_out_btn.tap()
        self.parent.wait_for_element_displayed(*DOM.Settings.fxa_logged_out_screen)

    def fxa_log_in(self, email, password, is_wrong=False):
        if self.is_fxa_logged_in():
            return

        log_in_btn = self.marionette.find_element(*DOM.Settings.fxa_log_in_btn)
        log_in_btn.tap()
        time.sleep(2)

        self.UTILS.iframe.switchToFrame(*DOM.Loop.ffox_account_frame_locator)
        self._fill_fxa_field(DOM.Loop.ffox_account_login_mail, email)
        self._fill_fxa_field(DOM.Loop.ffox_account_login_pass, password)

        if not is_wrong:
            done_btn = self.marionette.find_element(*DOM.Loop.ffox_account_login_done)
            done_btn.tap()

        self.apps.switch_to_displayed_app()
        self.parent.wait_for_condition(lambda m: email in m.find_element(
            *DOM.Settings.fxa_logged_in_text).text, timeout=10, message="Fxa login succesfully done.")

    def _fill_fxa_field(self, field_locator, text):
        """ Auxiliary method to fill "Firefox account login" fields
        """
        self.UTILS.reporting.logResult('info', '[firefox_login] Filling fxa field with text: {}'.format(text))
        self.parent.wait_for_element_displayed(*field_locator)
        fxa_input = self.marionette.find_element(*field_locator)
        fxa_input.send_keys(text)
        time.sleep(2)

        self.parent.wait_for_condition(
            lambda m: m.find_element(*DOM.Loop.ffox_account_login_next).get_attribute("disabled") != "disabled")
        next_btn = self.marionette.find_element(*DOM.Loop.ffox_account_login_next)
        next_btn.tap()
        self.parent.wait_for_element_not_displayed(*DOM.Loop.ffox_account_login_overlay)

    def set_alarm_volume(self, volume):
        """
        Set the volume for alarms.
        """
        self.parent.data_layer.set_setting('audio.volume.alarm', volume)

    def set_ringer_and_notifs_volume(self, volume):
        """
        Set the volume for ringer and notifications.
        """
        self.parent.data_layer.set_setting('audio.volume.notification', volume)

    def set_time_to_now(self):
        """
        Set date and time to 'now'.<br>
        TODO: Verify this
        WARNING: DOES NOT WORK YET!!! ...<br>
           1. Marionette.flick() not working here.<br>
           2. Cannot figure out how to tell what the current value is (no 'active' setting here),
        """
        return
        self.launch()

        date_and_time_link = ("id", "menuItem-dateAndTime")
        el = self.UTILS.element.getElement(date_and_time_link, "Date & Time setting")
        el.tap()

        clock_date = ("id", "clock-date")
        el = self.UTILS.element.getElement(clock_date, "Date setting")
        el.tap()

        time.sleep(2)
        self.marionette.switch_to_frame()

    def enable_sim_security(self, enable, pin, puk=None):
        """Enable SIM PIN security, if required"""

        sim_manager = self.UTILS.element.getElement(DOM.Settings.sim_manager, "SIM Manager menu")
        time.sleep(3)
        self.UTILS.element.simulateClick(sim_manager)

        sim_security = self.UTILS.element.getElement(DOM.Settings.sim_manager_sim_security, "SIM Security menu")
        sim_security.tap()

        switcher = self.UTILS.element.getElement(DOM.Settings.dual_sim_switch_pin_sim1, "SIM PIN switch")
        switch_input = self.marionette.find_element('css selector', 'input', switcher.id)
        enabled = switch_input.get_attribute("checked") is not None
        self.UTILS.reporting.info("PIN enabled: {}".format(enabled is not None))

        # If PIN is already in the correct state, just return
        if enabled and not enable or (not enabled and enable):
            self.UTILS.reporting.info("Pin not in correct state. Current: {} Requested: {}. Changing.".
                                      format(enabled, enable))
            # First of all, verify if the SIM is locked, and, in that case, unlock using PUK
            switcher.tap()
            time.sleep(1)
            unlocked = self.unlock_sim(puk, pin)
            if unlocked:
                self.check_security_menu()
                switcher.tap()
            pin_input = self.UTILS.element.getElement(DOM.Settings.sim_security_enter_pin_input, "Enter PIN input")
            pin_input.tap()
            time.sleep(1)
            pin_input.send_keys(pin)
            time.sleep(1)
            done_btn = self.marionette.find_element(*DOM.Settings.sim_security_enter_pin_done)
            done_btn.tap()

        self.check_security_menu()
        self.go_back("simpin-header")
        time.sleep(1)
        self.go_back()

    def check_security_status(self, expected):
        sim_manager = self.UTILS.element.getElement(DOM.Settings.sim_manager, "SIM Manager menu")
        time.sleep(3)
        self.UTILS.element.simulateClick(sim_manager)

        sim_security = self.UTILS.element.getElement(DOM.Settings.sim_manager_sim_security, "SIM Security menu")
        sim_security.tap()

        switcher = self.UTILS.element.getElement(DOM.Settings.dual_sim_switch_pin_sim1, "SIM PIN switch")
        switch_input = self.marionette.find_element('css selector', 'input', switcher.id)
        enabled = switch_input.get_attribute("checked") is not None
        self.UTILS.reporting.info("PIN enabled: {}".format(enabled is not None))
        self.UTILS.test.test(enabled == expected, "Security enabled: {}  Expected: {}".format(enabled, expected))

    def check_security_menu(self):
        try:
            self.UTILS.reporting.logResult("info", "SIM Security header")
            self.parent.wait_for_element_displayed(*DOM.Settings.sim_security_header)
        except:
            sim_security = self.UTILS.element.getElement(DOM.Settings.sim_manager_sim_security,
                                                         "SIM manager -> SIM security")
            sim_security.tap()
        time.sleep(1)

    def unlock_sim(self, puk, pin):
        time.sleep(2)
        self.UTILS.reporting.info("Checking if SIM is locked to unlock with PUK {} and PIN {}".format(puk, pin))
        try:
            self.marionette.find_element('css selector', 'h1[data-l10n-id=pukTitle]')
        except:
            # SIM is not locked, so simply return
            return False

        # Enter PUK and PIN twice to unlock the SIM
        puk_input = self.UTILS.element.getElement(DOM.Settings.puk_code_input, "PUK code input")
        puk_input.send_keys(puk)

        pin_input = self.UTILS.element.getElement(DOM.Settings.unlock_new_pin_input, "New PIN input")
        pin_input.send_keys(pin)

        confirm_pin_input = self.UTILS.element.getElement(DOM.Settings.unlock_confirm_new_pin_input,
                                                          "Confirm PIN input")
        confirm_pin_input.send_keys(pin)
        done_btn = self.UTILS.element.getElement(DOM.Settings.unlock_done_btn, "Done button")
        done_btn.tap()
        return True

    def change_sim_pin(self, old_pin, new_pin, confirm_pin):
        """
        This method changes the current PIN code to a new one
        """
        self.enable_sim_security(True, old_pin)
        time.sleep(1)

        sim_manager = self.UTILS.element.getElement(DOM.Settings.sim_manager, "SIM Manager menu")
        time.sleep(3)
        self.UTILS.element.simulateClick(sim_manager)

        sim_security = self.UTILS.element.getElement(DOM.Settings.sim_manager_sim_security, "SIM Security menu")
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

    def enable_sim_security2(self, enable, pin, is_dual_sim=None):
        """
        This method sets the SIM security configuration.
        """
        self.UTILS.reporting.logResult("info", "Enabling SIM security" if enable else "Disabling SIM Security")

        if is_dual_sim is None:
            is_dual_sim = self.UTILS.general.is_device_dual_sim()

        if is_dual_sim:
            self.UTILS.reporting.logResult("info", "Is dual SIM")

            self.wait_for_option_to_be_enabled(DOM.Settings.sim_manager_option)
            sim_manager = self.UTILS.element.getElement(DOM.Settings.sim_manager_option, "SIM manager")
            sim_manager.tap()

            self.UTILS.reporting.logResult("info", "Time to select SIM security option")

            sim_security = self.UTILS.element.getElement(DOM.Settings.sim_manager_sim_security,
                                                         "SIM manager -> SIM security")
            sim_security.tap()

            self.UTILS.reporting.logResult("info", "Try to switch ON the SIM 1 PIN switch")
            try:
                self.UTILS.reporting.logResult("info", "First we have to check if there's a button to change the PIN")
                self.parent.wait_for_element_displayed(*DOM.Settings.dual_sim_change_pin_sim1)
                if enable:
                    self.UTILS.reporting.logResult("info", "Trying to enable, but it was already done!! Exiting...")
                    return
                else:
                    sim_security_pin = self.UTILS.element.getElement(DOM.Settings.dual_sim_switch_pin_sim1,
                                                                     "Enable PIN 1 switch")
                    sim_security_pin.tap()
            except:
                if not enable:
                    self.UTILS.reporting.logResult("info", "Trying to disable, but it was already done!! Exiting...")
                    return

                self.UTILS.reporting.logResult("info", "The button was not there, so let's enable security")
                sim_security_pin = self.UTILS.element.getElement(DOM.Settings.dual_sim_switch_pin_sim1,
                                                                 "Enable PIN 1 switch")
                sim_security_pin.tap()

        else:
            self.UTILS.reporting.logResult("info", "Is single SIM")
            self.wait_for_option_to_be_enabled(DOM.Settings.sim_security_option)
            sim_security = self.UTILS.element.getElement(DOM.Settings.sim_security, "SIM Security")
            self.UTILS.element.scroll_into_view(sim_security)
            sim_security_tag = self.UTILS.element.getElement(DOM.Settings.sim_security_tag, "SIM security status")
            time.sleep(4)

            # If the attribute is already in the desired state, return
            self.UTILS.reporting.logResult("info", "Value of enable: {}".format(enable))
            self.UTILS.reporting.logResult("info", "Value of sim security tag: {}".format(sim_security_tag.text))
            current = sim_security_tag.text == _("Enabled")
            self.UTILS.reporting.logResult("info", "Value of current: {}".format(current))
            if enable == current:
                # click anyway so that we can later check whether the button to change the PIN
                sim_security.tap()
                return

            sim_security.tap()
            sim_security_pin = self.UTILS.element.getElement(DOM.Settings.sim_security_pin, "SIM security switch")
            sim_security_pin.tap()

        self.UTILS.reporting.logResult("info", "Now it should appear a 'Enter PIN' header")
        self.UTILS.element.waitForElements(DOM.Settings.sim_security_enter_pin_header, "Enter PIN header")

        # Type the PIN in
        pin_input = self.UTILS.element.getElement(DOM.Settings.sim_security_enter_pin_input, "Enter PIN input")
        pin_input.send_keys(pin)

        done_btn = self.UTILS.element.getElement(DOM.Settings.sim_security_enter_pin_done, "Done button")
        done_btn.tap()

        """
        Check that we're in SIM security menu.
        NOTE: There's a glitch (automation presumed) in which after hitting the "Done button" (see above)
        we come back to the SIM manager menu instead of the SIM security.
        """

        # I haven't been able to reproduce it manually, so the following patch had to be applied.
        try:
            self.UTILS.reporting.logResult("info", "SIM Security header")
            self.parent.wait_for_element_displayed(*DOM.Settings.sim_security_header)
        except:
            sim_security = self.UTILS.element.getElement(DOM.Settings.sim_manager_sim_security,
                                                         "SIM manager -> SIM security")
            sim_security.tap()

        # Check that SIM security was actually enabled/disabled
        if is_dual_sim:
            if enable:
                """
                Now the PIN has been set up, we should be able to see the "Change PIN" button
                If not, something went wrong
                """
                try:
                    self.UTILS.element.getElement(DOM.Settings.dual_sim_change_pin_sim1,
                                                  "Change PIN button <b> is there </b>")
                except:
                    self.UTILS.test.test(False, "Something went wrong while activating the PIN", True)
            else:
                self.UTILS.element.waitForNotElements(DOM.Settings.dual_sim_change_pin_sim1,
                                                      "Change PIN button <b> is not there </b>")
        else:
            if enable:
                """
                Now the PIN has been set up, we should be able to see the "Change PIN" button
                If not, something went wrong
                """
                try:
                    self.UTILS.element.getElement(DOM.Settings.sim_security_change_pin,
                                                  "Change PIN button <b> is there </b>")
                except:
                    self.UTILS.test.test(False, "Something went wrong while activating the PIN", True)
            else:
                self.UTILS.element.waitForNotElements(DOM.Settings.sim_security_change_pin,
                                                      "Change PIN button <b> is not there </b>")

    def enter_lockscreen_menu(self):
        """Open the Lock Screen menu"""

        # Enter the screen lock menu
        scr_lock_menu = self.UTILS.element.getElement(DOM.Settings.screen_lock_menu, "Screen lock menu")
        self.UTILS.element.scroll_into_view(scr_lock_menu)
        time.sleep(1)
        self.UTILS.element.simulateClick(scr_lock_menu)
        time.sleep(1)

    def set_lockscreen(self, enable):
        """Enable or disable the lock screen"""

        # Get lockscreen input status and enable if required
        lockscreen_elem = self.marionette.find_element(*DOM.Settings.lockscreen_input)
        enabled = lockscreen_elem.get_attribute("checked")
        self.UTILS.reporting.info("LOCKSCREEN ENABLED: {}".format(enabled))
        if (not enabled and enable) or (enabled and not enable):
            self.marionette.find_element(*DOM.Settings.lockscreen_label).tap()

    def set_passcode_lock(self, enable=False, code=None):
        """Configure the passcode lock option.

        Enable or disable the passcode lock option.
        enable: if True, it will enable passcode lock.
        code: the code used for locking/unlocking.
        """

        # Move the passcode lock slider to the desired position, if required
        passcode_element = self.UTILS.element.getElement(DOM.Settings.passcode_lock, "Passcode lock")
        passcode_lock = self.marionette.find_element(*DOM.Settings.passcode_enable)
        checked = passcode_lock.get_attribute("checked")
        passcode_enabled = checked is not None and checked == "true"
        self.UTILS.reporting.debug(
            "Checked: {} ({})     Passcode enabled: {}".format(checked, type(checked), passcode_enabled))
        if passcode_enabled == enable:
            return

        passcode_element.tap()
        # Give some time for the keyboard to appear
        time.sleep(1)
        passcode_input = self.UTILS.element.getElement(DOM.Settings.passcode_input, "Passcode input")
        self.UTILS.reporting.debug("* Sending code {} to passcode input".format(code))
        passcode_input.send_keys(code)

        # If enable is True, we must confirm the code
        if enable:
            passcode_confirm = self.UTILS.element.getElement(DOM.Settings.passcode_confirm, "Passcode confirm")
            self.UTILS.reporting.debug("* Sending code {} to passcode confirm".format(code))
            passcode_confirm.send_keys(code)
            passcode_btn_create = self.UTILS.element.getElement(DOM.Settings.passcode_btn_create, "Button Create")
            passcode_btn_create.tap()
        # Return to the main settings menu
        self.go_back()

    def enter_unlock_code(self, code):
        """Enter the unlock code via the keyboard.
        """
        for c in code:
            btn = self.marionette.find_element(DOM.Settings.passcode_keyb_btn[0],
                                               DOM.Settings.passcode_keyb_btn[1].format(c))
            btn.tap()

    def wifi(self):
        """Open wifi settings menu
        """
        time.sleep(1)
        settings_menu = self.UTILS.element.getElement(DOM.Settings.wifi, "Wifi settings link")
        time.sleep(1)
        settings_menu.tap()

        self.UTILS.element.waitForElements(DOM.Settings.wifi_header, "Wifi header appears.", True, 20, False)

    def wifi_forget(self, quiet=True):
        """
        Forget the wifi (assumes you have clicked the wifi name).<br>
        If quiet is True, then it will not assert if this wifi is already known.<br>
        If quiet is True, then it will assert (and expect) that this wifi is already known.<br>
        Either way, it will return True for forgotten, or False for 'not known'.
        """
        try:
            self.parent.wait_for_element_displayed(*DOM.Settings.wifi_details_header, timeout=2)
        except:
            return False

        wlan = self.UTILS.element.getElement(DOM.Settings.wifi_details_header, "Header").text
        self.UTILS.reporting.logResult("info", "Forgetting wifi '{}' ...".format(wlan))
        is_connected = False
        try:
            """
            Already connected to this wifi (or connected automatically).
            'Forget' it (so we can reconnect as-per test) and tap the wifi name again.
            """
            self.parent.wait_for_element_displayed(*DOM.Settings.wifi_details_forget_btn, timeout=3)
            wifi_forget_btn = self.marionette.find_element(*DOM.Settings.wifi_details_forget_btn)
            wifi_forget_btn.tap()
            is_connected = True

            # Takes a few seconds to disconnect, so check a few times.
            is_forgotten = False
            network = {'ssid': wlan}
            self.parent.wait_for_condition(lambda m: not self.parent.data_layer.is_wifi_connected(network), timeout=30)
        except:
            pass

        if not quiet:
            _msg_1 = "was" if is_connected else "was not"
            _msg_2 = "and has been succesfully" if is_forgotten else "but could not be"

            self.UTILS.test.test(is_connected and is_forgotten,
                                 "Wifi network '{}' {} connected {} forgotten.".format(wlan, _msg_1, _msg_2))

        return is_connected

    def _check_disconnected(self, wlan):
        """
        Private function to wait until this wifi network is no longer marked as "Connected".
        """
        available_networks = self.marionette.find_elements(*DOM.Settings.wifi_available_networks)
        for network in available_networks:
            if network.find_element("tag name", "a").text == wlan:
                if network.find_element("tag name", "small").text != "Connected":
                    return True
                else:
                    return False

    def wifi_list_is_connected(self, wlan_name, timeout=30):
        """
        Verify the expected network is listed as connected in 'available networks'.
        """
        try:
            self.parent.wait_for_element_present("xpath", DOM.Settings.wifi_list_connected_xp.format(wlan_name),
                                                 timeout=timeout)
            return True
        except:
            return False

    def wifi_list_is_not_connected(self, wlan_name, timeout=30):
        """
        Verify the expected network is listed as connected in 'available networks'.
        """
        try:
            self.parent.wait_for_element_not_present("xpath", DOM.Settings.wifi_list_connected_xp.format(wlan_name),
                                                     timeout=timeout)
            return True
        except:
            return False

    def wifi_list_tap_name(self, wlan_name):
        """
        Tap the network name in the list.
        """
        screenshot = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult('info', "Screenshot", screenshot)

        _wifi_name_element = ("xpath", DOM.Settings.wifi_name_xpath.format(wlan_name))
        wifi = self.UTILS.element.getElement(_wifi_name_element, "Wifi name", timeout=10)

        wifi.tap()
        time.sleep(2)

    def wifi_switch_on(self):
        """
        Click slider to turn wifi on.
        """
        if not self.parent.data_layer.get_setting("wifi.enabled"):
            wifi_switch = self.UTILS.element.getElement(DOM.Settings.wifi_enabled, "Enable wifi switch")
            wifi_switch.tap()
        """
        Nothing to check for yet, because the network may require login etc...,
        so just wait a little while before proceeding ...
        """
        time.sleep(3)

    def wifi_switch_off(self):
        """
        Click slider to turn wifi on.
        """
        if self.parent.data_layer.get_setting("wifi.enabled"):
            wifi_switch = self.UTILS.element.getElement(DOM.Settings.wifi_enabled, "Disable wifi switch")
            wifi_switch.tap()
        """
        Nothing to check for yet, because the network may require login etc...,
        so just wait a little while before proceeding ...
        """
        time.sleep(3)

    @retry(10)
    def connect_to_wifi(self, wifi_name, wifi_pass):
        """
        Connect to the wifi.
        """
        self.wifi_switch_on()
        time.sleep(2)
        self.wifi_list_tap_name(wifi_name)
        self.UTILS.general.typeThis(DOM.Settings.wifi_login_pass, "Password for the WLAN", wifi_pass,
                                    p_no_keyboard=True)
        ok_btn = self.marionette.find_element(*DOM.Settings.wifi_login_ok_btn)
        ok_btn.tap()

    def select_language(self, lang="English (US)"):
        """Enter the language menu and select the given language from the selectable.
        """
        lang_item = self.UTILS.element.getElement(DOM.Settings.language_item, "Language menu")
        lang_item.tap()

        selector = self.UTILS.element.getElement(DOM.Settings.language_selector, "Language selector")
        selector.tap()

        # switch to the root frame, since the selectable menu appears on top, not under Settings
        self.marionette.switch_to_frame()
        option = self.UTILS.element.getElement(DOM.Settings.language_option_xpath.format(lang))
        option.tap()
        ok_btn = self.UTILS.element.getElement(DOM.Settings.language_option_ok_btn)
        ok_btn.tap()
        # switch back to the Settings application
        self.UTILS.iframe.switch_to_frame(*DOM.Settings.frame_locator)
        self.go_back()

    def reset_phone(self):
        """Open the Information menu and reset the device.
        """
        device_item = self.UTILS.element.getElement(DOM.Settings.device_info_item, "Device information menu")
        device_item.tap()

        more_info = self.UTILS.element.getElement(DOM.Settings.device_more_info, "More information menu")
        more_info.tap()

        reset_btn = self.UTILS.element.getElement(DOM.Settings.reset_phone_button, "Reset phone button")
        reset_btn.tap()
