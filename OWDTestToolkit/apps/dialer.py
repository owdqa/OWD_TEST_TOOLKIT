import time
import datetime
from OWDTestToolkit import DOM
from marionette import Actions

from OWDTestToolkit.utils.i18nsetup import I18nSetup
_ = I18nSetup(I18nSetup).setup()


class Dialer(object):

    """Object representing the Dialer application.
    """

    def __init__(self, p_parent):
        self.apps = p_parent.apps
        self.data_layer = p_parent.data_layer
        self.parent = p_parent
        self.marionette = p_parent.marionette
        self.UTILS = p_parent.UTILS
        self.actions = Actions(self.marionette)

    def launch(self):

        # Launch the app (it's called a different name to the everyone knows it as, so hardcode it!).
        self.app = self.apps.launch("Phone")
        self.UTILS.element.waitForNotElements(DOM.GLOBAL.loading_overlay,
                                              self.__class__.__name__ + " app - loading overlay")
        return self.app

    def _cancel_addNumberToContact(self):
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)
        self.UTILS.element.waitForElements(
            ("xpath", "//h1[text()='{}']".format(_("Contacts"))), "'Select contact' header")

        cancel_icon = self.UTILS.element.getElement(DOM.Dialer.add_to_conts_cancel_btn, "Cancel icon")
        cancel_icon.tap()

    def _complete_addNumberToContact(self, p_num, p_name):
        #
        # PRIVATE function - finishes the process of adding a number to an existing contact
        # (used bu addThisNumberToContact() etc...).<br>
        # Handles switching frames etc... and finishes with you back in the dialer.
        #
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)
        self.UTILS.element.waitForElements(
            ("xpath", "//h1[text()='{}']".format(_("Contacts"))), "'Select contact' header")

        y = self.UTILS.element.getElements(DOM.Contacts.view_all_contact_list, "All contacts list")
        boolOK = False
        for i in y:
            if p_name in i.text:
                self.UTILS.reporting.logResult("info", "Contact '{}' found in all contacts.".format(p_num))
                i.tap()
                boolOK = True
                break

        self.UTILS.test.test(boolOK, "Succesfully selected contact from list.")
        self.UTILS.element.waitForElements(DOM.Contacts.edit_contact_header, "'Edit contact' header")

        # Test for an input field for number_<x> contaiing our number.
        self.UTILS.element.waitForElements(("xpath", DOM.Contacts.phone_field_xpath.format(p_num)),
                                           "Phone field containing {}".format(p_num))

        # Hit 'update' to save the changes to this contact.
        done_button = self.UTILS.element.getElement(DOM.Contacts.edit_update_button, "'Update' button")
        done_button.tap()

        # Verify that the contacts app is closed and we are returned to the call log.
        self.marionette.switch_to_frame()
        self.UTILS.element.waitForNotElements(("xpath", "//iframe[contains(@{}, '{}')]".
                                               format(DOM.Contacts.frame_locator[0], DOM.Contacts.frame_locator[1])),
                                              "COntacts frame")
        self.UTILS.iframe.switchToFrame(*DOM.Dialer.frame_locator)

    def addThisNumberToContact(self, p_name):

        # Adds the current number to existing contact.
        x = self.UTILS.element.getElement(DOM.Dialer.phone_number, "Phone number field", False)
        dialer_num = x.get_attribute("value")

        x = self.UTILS.element.getElement(DOM.Dialer.add_to_contacts_button, "Add to contacts button")
        x.tap()

        x = self.UTILS.element.getElement(DOM.Dialer.add_to_existing_contact_btn, "Add to existing contact button")
        x.tap()

        self._complete_addNumberToContact(dialer_num, p_name)

    def callLog_addToContact(self, phone_number, contact_name, p_open_call_log=True, cancel_process=False):
        """
        Adds this number in the call log to an existing contact
        (and returns you to the call log).
        If p_open_call_log is set to False it will assume you are
        already in the call log.
        """
        
        if p_open_call_log:
            self.open_call_log()

        self.callLog_long_tap(phone_number)
        time.sleep(1)
        self.callLog_long_tap_select_action(
            DOM.Dialer.call_log_numtap_add_to_existing, "Add to existing contact button")

        if cancel_process:
            self._cancel_addNumberToContact()
        else:
            self._complete_addNumberToContact(phone_number, contact_name)

    def callLog_long_tap(self, phone_number):
        entry = self.UTILS.element.getElement(("xpath", DOM.Dialer.call_log_number_xpath.format(phone_number)),
                                              "The call log for number {}".format(phone_number))
        self.actions.long_press(entry, 3).perform()

    def callLog_long_tap_select_action(self, locator, msg="Option chosen"):
        option = self.UTILS.element.getElement(locator, msg, True, 10)
        option.tap()

    def callLog_call(self, p_num):

        # Get own number.
        own_num = self.UTILS.general.get_config_variable("phone_number", "custom")

        # Calls a number from the call log.
        try:
            self.parent.wait_for_element_displayed(*DOM.Dialer.call_log_filter, timeout=1)
        except:
            self.open_call_log()

        entry = self.UTILS.element.getElement(("xpath", DOM.Dialer.call_log_number_xpath.format(p_num)),
                                          "The call log for number {}".format(p_num))
        entry.tap()

        if own_num == p_num:
            time.sleep(2)
            # self.marionette.switch_to_frame()
            x = self.UTILS.element.getElement(DOM.Dialer.call_busy_button_ok, "OK button (callLog_call)")
            x.tap()
        else:
            time.sleep(1)
            self.UTILS.iframe.switchToFrame(*DOM.Dialer.frame_locator_calling)
            self.UTILS.element.waitForElements(("xpath", DOM.Dialer.outgoing_call_numberXP.format(p_num)),
                                               "Outgoing call found with number matching {}".format(p_num))

    def callLog_clearAll(self):

        # Wipes all entries from the call log.
        try:
            self.parent.wait_for_element_displayed(*DOM.Dialer.call_log_filter, timeout=1)
        except:
            self.open_call_log()

        try:
            self.parent.wait_for_element_displayed(*DOM.Dialer.call_log_no_calls_msg, timeout=1)
        except:
            self.UTILS.reporting.logResult("info", "Some numbers are in the call log here - removing them ...")
            edit_btn = self.UTILS.element.getElement(DOM.Dialer.call_log_edit_btn, "Edit button")
            edit_btn.tap()

            """Here something weird is happening, since the form where this button should appear, remains
            hidden. Thus, when we try to get the button, it won't appear. Then, we have have to use
            raw JavaScript in order to obtain the button and click on it."""

            self.parent.wait_for_element_present(*DOM.Dialer.call_log_edit_selAll, timeout=10)
            self.marionette.execute_script("document.getElementById('{}').click();".
                                           format(DOM.Dialer.call_log_edit_selAll[1]))

            self.parent.wait_for_element_present(*DOM.Dialer.call_log_edit_delete, timeout=2)
            self.marionette.execute_script("document.getElementById('{}').click();".
                                           format(DOM.Dialer.call_log_edit_delete[1]))

            confirm_delete = self.UTILS.element.getElement(DOM.Dialer.call_log_confirm_delete, "Confirm button")
            confirm_delete.tap()

            self.UTILS.element.waitForElements(DOM.Dialer.call_log_no_calls_msg, "'No calls ...' message")

    def callLog_clearSome(self, p_entryNumbers):
        """
        Wipes entries from the call log, using p_entryNumbers as an array of
        numbers. For example: callLog_clearSome([1,2,3]) will remove the first 3.
        <br><b>NOTE:</b> the first item is 1, <i>not</i> 0.
        """
        try:
            self.parent.wait_for_element_displayed(*DOM.Dialer.call_log_filter, timeout=1)
        except:
            self.open_call_log()

        boolLIST = True
        try:
            self.parent.wait_for_element_displayed(*DOM.Dialer.call_log_no_calls_msg, timeout=1)
            boolLIST = False
        except:
            pass

        if boolLIST:
            """
            At the moment, the 'edit' div looks like it's not displayed, so Marionette can't tap it.
            For this reason I'm using JS to click() instead.
            """
            self.UTILS.reporting.logResult("info", "Some numbers are in the call log here - removing them ...")
            x = self.UTILS.element.getElement(DOM.Dialer.call_log_edit_btn, "Edit button")
            x.tap()
            """
            The edit mode doens't seem to be 'displayed', so we have to work around
            that at the moment.
            """
            time.sleep(2)
            self.parent.wait_for_element_present(*DOM.Dialer.call_log_edit_header, timeout=2)
            _els = ("xpath", "//ol[@class='log-group']//li")
            x = self.UTILS.element.getElements(_els, "Call log items", False)

            _precount = len(x)
            self.UTILS.reporting.logResult("info", "{} items found.".format(_precount))
            for i in p_entryNumbers:
                if i != 0:
                    _precount = _precount - 1
                    x[i - 1].tap()

            self.parent.wait_for_element_present(*DOM.Dialer.call_log_edit_delete, timeout=2)
            self.marionette.execute_script("document.getElementById('{}').click();".
                                           format(DOM.Dialer.call_log_edit_delete[1]))

            # Click on Delete button
            delete_btn = self.UTILS.element.getElement(DOM.GLOBAL.confirm_form_delete_btn, "Confirm delete")
            delete_btn.tap()

            try:
                _postcount = self.UTILS.element.getElements(_els, "Call log items", False)
                _postcount = len(_postcount)
            except:
                _postcount = 0

            self.UTILS.test.test(_postcount == _precount,
                                 "{} numbers are left after deletion (there are {}).".format(_precount, _postcount))

    def callLog_createContact(self, entry, p_open_call_log=True):
        """
        Creates a new contact from the call log (only
        as far as the contacts app opening).
        If p_open_call_log is set to False it will assume you are
        already in the call log.
        """
        if p_open_call_log:
            self.open_call_log()

        self.callLog_long_tap(entry)
        self.callLog_long_tap_select_action(DOM.Dialer.call_log_numtap_create_new, "Create new contact button")

        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)
        self.UTILS.element.waitForElements(DOM.Contacts.add_contact_header, "'Add contact' header")

    def call_this_number(self):

        # Calls the current number.
        call_number_button = self.UTILS.element.getElement(DOM.Dialer.call_number_button, "Call number button")
        self.UTILS.reporting.debug(
            "*** Call this number button: [{}]   Text: [{}]".format(call_number_button, call_number_button.text))
        self.UTILS.element.simulateClick(call_number_button)

        self.UTILS.iframe.switchToFrame(*DOM.Dialer.frame_locator_calling)
        self.UTILS.element.waitForElements(DOM.Dialer.outgoing_call_locator, "Outgoing call locator", True, 5)

    def call_this_number_and_hangup(self, delay):
        self.call_this_number()
        time.sleep(delay)
        self.hangUp()

    def get_and_accept_fdn_warning(self, phone_number):
        # Check warning message
        self.UTILS.element.waitForElements(DOM.Settings.fdn_warning_header, "Waiting for FDN warning header", True, 10)
        self.UTILS.element.waitForElements(DOM.Settings.fdn_warning_body, "Waiting for FDN warning body")
        body = self.marionette.find_element(*DOM.Settings.fdn_warning_body)
        self.UTILS.reporting.log_to_file("body.text: {}   msg: {}".format(body.text, DOM.Dialer.fdn_warning_msg.\
                                                                          format(phone_number)))
        self.UTILS.test.test(body.text == DOM.Dialer.fdn_warning_msg.format(phone_number),
                             "Correct FDN warning message")

        ok_btn = self.UTILS.element.getElement(DOM.Settings.fdn_warning_ok, "OK button")
        ok_btn.tap()

    def createContactFromThisNum(self):
        """
        Creates a new contact from the number currently in the dialer
        (doesn't fill in the contact details).
        """
        self.UTILS.iframe.switchToFrame(*DOM.Dialer.frame_locator)

        add_btn = self.UTILS.element.getElement(DOM.Dialer.add_to_contacts_button, "Add to contacts button")
        add_btn.tap()

        create_btn = self.UTILS.element.getElement(DOM.Dialer.create_new_contact_btn, "Create new contact button")
        create_btn.tap()

        # Switch to the contacts frame.
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)

    def createMultipleCallLogEntries(self, phone_number, entries_number):
        #
        # Put a number in the call log multiple times
        # (done by manipulating the device time).
        # Leaves you in the call log.
        #
        # x = self.UTILS.date_and_time.getDateTimeFromEpochSecs(time.time())

        today = datetime.datetime.today()
        for i in range(entries_number):
            delta = datetime.timedelta(days=i)
            new_date = today - delta

            self.UTILS.date_and_time.setTimeToSpecific(p_day=new_date.day, p_month=new_date.month)

            self.enterNumber(phone_number)
            self.call_this_number_and_hangup(delay=7)
            # This needs to be done bcs sometimes (50%) the Dialer app crushes after hanging up
            self.apps.kill_all()
            time.sleep(2)
            self.launch()

    def enterNumber(self, p_num, validate=True):

        # Enters a number into the dialer using the keypad.
        try:
            self.parent.wait_for_element_displayed(*DOM.Dialer.phone_number, timeout=1)
        except:
            keypad_selector = self.UTILS.element.getElement(DOM.Dialer.option_bar_keypad, "Keypad option selector")
            keypad_selector.tap()
            self.UTILS.element.waitForElements(DOM.Dialer.phone_number, "Phone number area")

        for i in str(p_num):

            if i == "+":
                plus_symbol = self.UTILS.element.getElement(("xpath", DOM.Dialer.dialer_button_xpath.format(0)),
                                                  "keypad symbol '+'")
                self.actions.long_press(plus_symbol, 2).perform()
            else:
                number_symbol = self.UTILS.element.getElement(("xpath", DOM.Dialer.dialer_button_xpath.format(i)),
                                                  "keypad number {}".format(i))
                number_symbol.tap()

        # Verify that the number field contains the expected number.
        if validate:
            number_field = self.UTILS.element.getElement(DOM.Dialer.phone_number, "Phone number field", False)
            dialer_num = self.marionette.execute_script("return arguments[0].value", script_args=[number_field])
            self.UTILS.reporting.debug(u"** Dialer_num entered: [{}]".format(dialer_num))
            self.UTILS.test.test(str(p_num) in dialer_num, u"After entering '{}', phone number field contains '{}'.".
                                 format(p_num, dialer_num))

            screenshot = self.UTILS.debug.screenShotOnErr()
            self.UTILS.reporting.logResult("info", "Screenshot at enterNumber method [validate]:", screenshot)

    def clear_dialer(self):

        # Deletes a single number from the dialer
        try:
            self.parent.wait_for_element_displayed(*DOM.Dialer.keypad_delete)
            delete = self.marionette.find_element(*DOM.Dialer.keypad_delete)
            delete.tap()
        except:
            return

    def clear_dialer_all(self):

        # Clears all dialer input area
        try:
            self.parent.wait_for_element_displayed(*DOM.Dialer.keypad_delete)
            delete = self.marionette.find_element(*DOM.Dialer.keypad_delete)
            self.actions.long_press(delete, 3).perform()
        except:
            return

    def answer(self):
        self.marionette.switch_to_frame()
        elDef = ("xpath", "//iframe[contains(@{}, '{}')]".
                 format(DOM.Dialer.frame_locator_calling[0],
                        DOM.Dialer.frame_locator_calling[1]))

        self.parent.wait_for_element_displayed(*elDef, timeout=60)
        frame_calling = self.marionette.find_element(*elDef)

        if frame_calling:
            self.UTILS.iframe.switchToFrame(*DOM.Dialer.frame_locator_calling)
            self.parent.wait_for_element_displayed(*DOM.Dialer.answer_callButton, timeout=1)
            answer = self.marionette.find_element(*DOM.Dialer.answer_callButton)
            if answer:
                answer.tap()

    def answer_and_hangup(self, delay=5):
        self.answer()
        time.sleep(delay)

        self.parent.wait_for_element_displayed(*DOM.Dialer.hangup_bar_locator, timeout=1)
        hangup = self.marionette.find_element(*DOM.Dialer.hangup_bar_locator)
        if hangup:
            hangup.tap()
        else:
            try:
                self.parent.data_layer.kill_active_call()
            except:
                self.UTILS.reporting.logResult("info", "Exception when killing active call via data_layer")
                pass

    def hangUp(self):

        # Hangs up (assuming we're in the 'calling' frame).
        try:
            self.parent.wait_for_element_displayed(*DOM.Dialer.hangup_bar_locator, timeout=10)
        except:
            # The call may already be terminated, so don't throw an error if
            # the hangup bar isn't there.
            self.apps.switch_to_displayed_app()  # go back to dialer
            self.parent.wait_for_element_displayed(*DOM.Dialer.call_busy_button_ok, timeout=5)
            ok_btn = self.marionette.find_element(*DOM.Dialer.call_busy_button_ok)
            ok_btn.tap()
            return

        hangup = self.marionette.find_element(*DOM.Dialer.hangup_bar_locator)
        if hangup:
            hangup.tap()
        else:
            try:
                self.parent.data_layer.kill_active_call()
            except:
                self.UTILS.reporting.logResult("info", "Exception when killing active call via data_layer")
                pass

        self.apps.switch_to_displayed_app()

    def open_call_log(self):

        # Opens the call log.
        x = self.UTILS.element.getElement(DOM.Dialer.option_bar_call_log, "Call log button")
        x.tap()

        time.sleep(2)

    def check_incoming_call(self, incoming_number):
        try:
            self.UTILS.iframe.switchToFrame(*DOM.Dialer.frame_locator_calling)
            self.parent.wait_for_element_displayed(
                "xpath", DOM.Dialer.outgoing_call_numberXP.format(incoming_number), timeout=30)
        except:
            self.UTILS.test.test(False, "No incoming call received", True)

    def resume_hidden_call(self):
        self.marionette.switch_to_frame()
        attention = self.marionette.find_element("id", "attention-screen")
        attention.tap()
        self.UTILS.iframe.switchToFrame(*DOM.Dialer.frame_locator_calling)
