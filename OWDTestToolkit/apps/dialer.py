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

    def launch(self):
        #
        # Launch the app (it's called a different name to the everyone knows it as, so hardcode it!).
        #
        self.app = self.apps.launch("Phone")
        self.UTILS.element.waitForNotElements(DOM.GLOBAL.loading_overlay,
                                              self.__class__.__name__ + " app - loading overlay")
        return self.app

    def _complete_addNumberToContact(self, p_num, p_name):
        #
        # PRIVATE function - finishes the process of adding a number to an existing contact
        # (used bu addThisNumberToContact() etc...).<br>
        # Handles switching frames etc... and finishes with you back in the dialer.
        #
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)
        self.UTILS.element.waitForElements(("xpath", "//h1[text()='{}']".format(_("Select contact"))), "'Select contact' header")

        y = self.UTILS.element.getElements(DOM.Contacts.view_all_contact_list, "All contacts list")
        boolOK = False
        for i in y:
            if p_name in i.text:
                self.UTILS.reporting.logResult("info", "Contact '{}' found in all contacts.".format(p_num))
                i.tap()
                boolOK = True
                break

        self.UTILS.test.TEST(boolOK, "Succesfully selected contact from list.")
        self.UTILS.element.waitForElements(DOM.Contacts.edit_contact_header, "'Edit contact' header")

        # Test for an input field for number_<x> contaiing our number.
        self.UTILS.element.waitForElements(("xpath", DOM.Contacts.phone_field_xpath.format(p_num)),
                                    "Phone field containing {}".format(p_num))

        #
        # Hit 'update' to save the changes to this contact.
        #
        done_button = self.UTILS.element.getElement(DOM.Contacts.edit_update_button, "'Update' button")
        done_button.tap()

        #
        # Verify that the contacts app is closed and we are returned to the call log.
        #
        self.marionette.switch_to_frame()
        self.UTILS.element.waitForNotElements(("xpath", "//iframe[contains(@{}, '{}')]".\
                                                format(DOM.Contacts.frame_locator[0], DOM.Contacts.frame_locator[1])),
                                        "COntacts frame")
        self.UTILS.iframe.switchToFrame(*DOM.Dialer.frame_locator)

    def addThisNumberToContact(self, p_name):
        #
        # Adds the current number to existing contact.
        #
        x = self.UTILS.element.getElement(DOM.Dialer.phone_number, "Phone number field", False)
        dialer_num = x.get_attribute("value")

        x = self.UTILS.element.getElement(DOM.Dialer.add_to_contacts_button, "Add to contacts button")
        x.tap()

        x = self.UTILS.element.getElement(DOM.Dialer.add_to_existing_contact_btn, "Add to existing contact button")
        x.tap()

        self._complete_addNumberToContact(dialer_num, p_name)

    def callLog_addToContact(self, p_num, p_name, p_openCallLog=True):
    #
    # Adds this number in the call log to an existing contact
    # (and returns you to the call log).
        # If p_openCallLog is set to False it will assume you are
        # already in the call log.
        #
        if p_openCallLog:
            self.openCallLog()

        time.sleep(1)

        x = self.UTILS.element.getElement(("xpath", DOM.Dialer.call_log_number_xpath.format(p_num)),
                               "The call log for number {}".format(p_num))
        x.tap()

        x = self.UTILS.element.getElement(DOM.Dialer.call_log_numtap_add_to_existing, "Add to existing contact button")
        x.tap()

        self._complete_addNumberToContact(p_num, p_name)

    def callLog_call(self, p_num):
        #
        # Get own number.
        #
        own_num = self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")

        #
        # Calls a number from the call log.
        #
        try:
            self.parent.wait_for_element_displayed(*DOM.Dialer.call_log_filter, timeout=1)
        except:
            self.openCallLog()

        x = self.UTILS.element.getElement(("xpath", DOM.Dialer.call_log_number_xpath.format(p_num)),
                                   "The call log for number {}".format(p_num))
        x.tap()

        x = self.UTILS.element.getElement(DOM.Dialer.call_log_numtap_call, "Call button")
        x.tap()
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
    #
    # Wipes all entries from the csll log.
    #
        try:
            self.parent.wait_for_element_displayed(*DOM.Dialer.call_log_filter, timeout=1)
        except:
            self.openCallLog()

        boolLIST = True
        try:
            self.parent.wait_for_element_displayed(*DOM.Dialer.call_log_no_calls_msg, timeout=1)
            boolLIST = False
        except:
            pass

        if boolLIST:
            #
            # At the moment, the 'edit' div looks like it's not displayed, so Marionette can't tap it.
            # For this reason I'm using JS to click() instead.
            #
            self.UTILS.reporting.logResult("info", "Some numbers are in the call log here - removing them ...")
            x = self.UTILS.element.getElement(DOM.Dialer.call_log_edit_btn, "Edit button")
            x.tap()
            time.sleep(2)
            self.parent.wait_for_element_present(*DOM.Dialer.call_log_edit_selAll, timeout=2)
            self.marionette.execute_script("document.getElementById('{}').click();".\
                                           format(DOM.Dialer.call_log_edit_selAll[1]))
            time.sleep(1)
            self.parent.wait_for_element_present(*DOM.Dialer.call_log_edit_delete, timeout=2)
            self.marionette.execute_script("document.getElementById('{}').click();".\
                                           format(DOM.Dialer.call_log_edit_delete[1]))

            self.marionette.execute_script("""
            var getElementByXpath = function (path) {
                return document.evaluate(path, document, null, 9, null).singleNodeValue;
            };
            getElementByXpath("/html/body/form[3]/menu/button[2]").click();
            """)

        self.UTILS.element.waitForElements(DOM.Dialer.call_log_no_calls_msg, "'No calls ...' message")

    def callLog_clearSome(self, p_entryNumbers):
        #
        # Wipes entries from the call log, using p_entryNumbers as an array of
        # numbers. For example: callLog_clearSome([1,2,3]) will remove the first 3.
        # <br><b>NOTE:</b> the first item is 1, <i>not</i> 0.
        #
        try:
            self.parent.wait_for_element_displayed(*DOM.Dialer.call_log_filter, timeout=1)
        except:
            self.openCallLog()

        boolLIST = True
        try:
            self.parent.wait_for_element_displayed(*DOM.Dialer.call_log_no_calls_msg, timeout=1)
            boolLIST = False
        except:
            pass

        if boolLIST:
            #
            # At the moment, the 'edit' div looks like it's not displayed, so Marionette can't tap it.
            # For this reason I'm using JS to click() instead.
            #
            self.UTILS.reporting.logResult("info", "Some numbers are in the call log here - removing them ...")
            x = self.UTILS.element.getElement(DOM.Dialer.call_log_edit_btn, "Edit button")
            x.tap()

            #
            # The edit mode doens't seem to be 'displayed', so we have to work around
            # that at the moment.
            #
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
            self.marionette.execute_script("document.getElementById('{}').click();".\
                                           format(DOM.Dialer.call_log_edit_delete[1]))
            self.marionette.execute_script("""
            var getElementByXpath = function (path) {
                return document.evaluate(path, document, null, 9, null).singleNodeValue;
            };
            getElementByXpath("/html/body/form[3]/menu/button[2]").click();
            """)

            try:
                _postcount = self.UTILS.element.getElements(_els, "Call log items", False)
                _postcount = len(_postcount)
            except:
                _postcount = 0

            self.UTILS.test.TEST(_postcount == _precount,
                        "{} numbers are left after deletion (there are {}).".format(_precount, _postcount))

    def callLog_createContact(self, p_num, p_openCallLog=True):
    #
    # Creates a new contact from the call log (only
    # as far as the contacts app opening).
    # If p_openCallLog is set to False it will assume you are
    # already in the call log.
    #
        if p_openCallLog:
            self.openCallLog()

        x = self.UTILS.element.getElement(("xpath", DOM.Dialer.call_log_number_xpath.format(p_num)),
                                   "The call log for number {}".format(p_num))
        x.tap()

        x = self.UTILS.element.getElement(DOM.Dialer.call_log_numtap_create_new, "Create new contact button", True, 20)
        x.tap()

        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)
        self.UTILS.element.waitForElements(DOM.Contacts.add_contact_header, "'Add contact' header")

    def callThisNumber(self):
        #
        # Calls the current number.
        #
        x = self.UTILS.element.getElement(DOM.Dialer.call_number_button, "Call number button")
        x.tap()

        self.UTILS.general.checkMarionetteOK()
        self.UTILS.iframe.switchToFrame(*DOM.Dialer.frame_locator_calling)
        self.UTILS.element.waitForElements(DOM.Dialer.outgoing_call_locator, "Outgoing call element", True, 5)

    def call_this_number_and_hangup(self, delay):
        self.callThisNumber()
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

    def createContactFromThisNum(self):
        #
        # Creates a new contact from the number currently in the dialler
        # (doesn't fill in the contact details).
        #
        self.UTILS.iframe.switchToFrame(*DOM.Dialer.frame_locator)

        x = self.UTILS.element.getElement(DOM.Dialer.add_to_contacts_button, "Add to contacts button")
        x.tap()

        x = self.UTILS.element.getElement(DOM.Dialer.create_new_contact_btn, "Create new contact button")
        x.tap()

        #
        # Switch to the contacts frame.
        #
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)

    def createMultipleCallLogEntries(self, p_num, p_amount):
        #
        # Put a number in the call log multiple times
        # (done by manipulating the device time).
        # Leaves you in the call log.
        #
        #x = self.UTILS.date_and_time.getDateTimeFromEpochSecs(time.time())

        today = datetime.datetime.today()
        for i in range(p_amount):
            delta = datetime.timedelta(days=i)
            new_date = today - delta

            self.UTILS.date_and_time.setTimeToSpecific(p_day=new_date.day, p_month=new_date.month)

            self.enterNumber(p_num)
            self.callThisNumber()
            time.sleep(2)
            self.hangUp()

        #
        # Open the call log to finish.
        #
        self.UTILS.general.checkMarionetteOK()
        self.launch()
        self.openCallLog()

    def enterNumber(self, p_num, validate=True):
        #
        # Enters a number into the dialer using the keypad.
        #
        try:
            self.parent.wait_for_element_displayed(*DOM.Dialer.phone_number, timeout=1)
        except:
            x = self.UTILS.element.getElement(DOM.Dialer.option_bar_keypad, "Keypad option selector")
            x.tap()
            self.UTILS.element.waitForElements(DOM.Dialer.phone_number, "Phone number area")

        for i in str(p_num):

            if i == "+":
                x = self.UTILS.element.getElement(("xpath", DOM.Dialer.dialler_button_xpath.format(0)),
                                           "keypad symbol '+'")
                self.actions = Actions(self.marionette)
                self.actions.long_press(x, 2).perform()
            else:
                x = self.UTILS.element.getElement(("xpath", DOM.Dialer.dialler_button_xpath.format(i)),
                                           "keypad number {}".format(i))
                x.tap()

        #
        # Verify that the number field contains the expected number.
        #
        if validate:
            x = self.UTILS.element.getElement(DOM.Dialer.phone_number, "Phone number field", False)
            dialer_num = x.get_attribute("value")
            self.UTILS.test.TEST(str(p_num) in dialer_num, "After entering '{}', phone number field contains '{}'.".\
                                                      format(dialer_num, p_num))

            x = self.UTILS.debug.screenShotOnErr()
            self.UTILS.reporting.logResult("info", "Screenshot:", x)

    def clear_dialer(self):
        #
        # Deletes a single number from the dialer
        #
        delete = self.UTILS.element.getElement(DOM.Dialer.keypad_delete, "Delete keypad")
        delete.tap()

    def clear_dialer_all(self):
        #
        # Clears all dialer input area
        #
        delete = self.UTILS.element.getElement(DOM.Dialer.keypad_delete, "Delete keypad")
        self.actions = Actions(self.marionette)
        self.actions.long_press(delete, 3).perform()

    def answer(self):
        self.marionette.switch_to_frame()
        elDef = ("xpath", "//iframe[contains(@{}, '{}')]".\
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
        #
        # Hangs up (assuming we're in the 'calling' frame).
        #

        # The call may already be terminated, so don't throw an error if
        # the hangup bar isn't there.
        try:
            self.UTILS.iframe.switchToFrame(*DOM.Dialer.frame_locator)

            try:
                self.parent.wait_for_element_displayed(*DOM.Dialer.call_busy_button_ok, timeout=5)
                ok_btn = self.marionette.find_element(*DOM.Dialer.call_busy_button_ok)
                # If the call destination is the same as the origin, it's very likely to get an error
                # message. If this is the case, tap the OK button. Otherwise (i.e. using twilio), hang up the call
                if ok_btn:
                    self.UTILS.test.TEST(True, "Button text: {}".format(ok_btn.text))
                    ok_btn.tap()
                    return
            except: # non-busy call

                self.marionette.switch_to_frame()
                elDef = ("xpath", "//iframe[contains(@{}, '{}')]".\
                                    format(DOM.Dialer.frame_locator_calling[0],
                                    DOM.Dialer.frame_locator_calling[1]))

                self.parent.wait_for_element_displayed(*elDef, timeout=60)
                frame_calling = self.marionette.find_element(*elDef)
                if frame_calling:
                    self.UTILS.iframe.switchToFrame(*DOM.Dialer.frame_locator_calling)
                    self.parent.wait_for_element_displayed(*DOM.Dialer.hangup_bar_locator, timeout=1)
                    hangup = self.marionette.find_element(*DOM.Dialer.hangup_bar_locator)
                    if hangup:
                        hangup.tap()
        except:
            pass

        #
        # Just to be sure!
        #
        try:
            self.parent.data_layer.kill_active_call()
        except:
            pass

        self.UTILS.iframe.switchToFrame(*DOM.Dialer.frame_locator)

    def openCallLog(self):
        #
        # Opens the call log.
        #
        x = self.UTILS.element.getElement(DOM.Dialer.option_bar_call_log, "Call log button")
        x.tap()

        time.sleep(2)
