import time
from OWDTestToolkit import DOM
from marionette import Actions


class Dialer(object):
    """Object representing the Dialer application.
    """

    def __init__(self, p_parent):
        self.apps       = p_parent.apps
        self.data_layer = p_parent.data_layer
        self.parent     = p_parent
        self.marionette = p_parent.marionette
        self.UTILS      = p_parent.UTILS

    def launch(self):
        #
        # Launch the app (it's called a different name to the everyone knows it as, so hardcode it!).
        #
        self.app = self.apps.launch("Phone")
        self.UTILS.waitForNotElements(DOM.GLOBAL.loading_overlay, self.__class__.__name__ + " app - loading overlay")
        return self.app

    def _complete_addNumberToContact(self, p_num, p_name):
        #
        # PRIVATE function - finishes the process of adding a number to an existing contact
        # (used bu addThisNumberToContact() etc...).<br>
        # Handles switching frames etc... and finishes with you back in the dialer.
        #
        self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)
        self.UTILS.waitForElements( ("xpath", "//h1[text()='Select contact']"), "'Select contact' header")

        y = self.UTILS.getElements(DOM.Contacts.view_all_contact_list, "All contacts list")
        boolOK = False
        for i in y:
            if p_name in i.text:
                self.UTILS.logResult("info", "Contact '%s' found in all contacts." % p_num)
                i.tap()
                boolOK = True
                break

        self.UTILS.TEST(boolOK, "Succesfully selected contact from list.")
        self.UTILS.waitForElements(DOM.Contacts.edit_contact_header, "'Edit contact' header")

        # Test for an input field for number_<x> contaiing our number.
        self.UTILS.waitForElements( ("xpath", DOM.Contacts.phone_field_xpath % p_num),
                                    "Phone field contaiing %s" % p_num)

        #
        # Hit 'update' to save the changes to this contact.
        #
        done_button = self.UTILS.getElement(DOM.Contacts.edit_update_button, "'Update' button")
        done_button.tap()

        #
        # Verify that the contacts app is closed and we are returned to the call log.
        #
        self.marionette.switch_to_frame()
        self.UTILS.waitForNotElements( ("xpath", "//iframe[contains(@%s, '%s')]" % \
                                                (DOM.Contacts.frame_locator[0], DOM.Contacts.frame_locator[1])),
                                        "COntacts frame")
        self.UTILS.switchToFrame(*DOM.Dialer.frame_locator)


    def addThisNumberToContact(self, p_name):
        #
        # Adds the current number to existing contact.
        #
        x = self.UTILS.getElement(DOM.Dialer.phone_number, "Phone number field", False)
        dialer_num = x.get_attribute("value")

        x = self.UTILS.getElement(DOM.Dialer.add_to_contacts_button, "Add to contacts button")
        x.tap()

        x = self.UTILS.getElement(DOM.Dialer.add_to_existing_contact_btn, "Add to existing contact button")
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

        x = self.UTILS.getElement( ("xpath", DOM.Dialer.call_log_number_xpath % p_num),
                               "The call log for number %s" % p_num)
        x.tap()

        x = self.UTILS.getElement( DOM.Dialer.call_log_numtap_add_to_existing, "Add to existing contact button")
        x.tap()

        self._complete_addNumberToContact(p_num, p_name)

    def callLog_call(self, p_num):
        #
        # Get own number.
        #
        own_num = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")

        #
        # Calls a number from the call log.
        #
        try:
            self.parent.wait_for_element_displayed(*DOM.Dialer.call_log_filter, timeout=1)
        except:
            self.openCallLog()

        x = self.UTILS.getElement( ("xpath", DOM.Dialer.call_log_number_xpath % p_num),
                                   "The call log for number %s" % p_num)
        x.tap()

        x = self.UTILS.getElement( DOM.Dialer.call_log_numtap_call, "Call button")
        x.tap()
        if own_num == p_num:
            time.sleep(2)
            #self.marionette.switch_to_frame()
            x = self.UTILS.getElement(DOM.Dialer.call_busy_button_ok, "OK button (callLog_call)")
            x.tap()
        else:
            time.sleep(1)
            self.UTILS.switchToFrame(*DOM.Dialer.frame_locator_calling)
            self.UTILS.waitForElements( ("xpath", DOM.Dialer.outgoing_call_numberXP % p_num),
                                    "Outgoing call found with number matching %s" % p_num)


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
            self.UTILS.logResult("info", "Some numbers are in the call log here - removing them ...")
            x = self.UTILS.getElement(DOM.Dialer.call_log_edit_btn, "Edit button")
            x.tap()
            time.sleep(2)
            self.parent.wait_for_element_present(*DOM.Dialer.call_log_edit_selAll, timeout=2)
            self.marionette.execute_script("document.getElementById('%s').click();" % DOM.Dialer.call_log_edit_selAll[1])
            time.sleep(1)
            self.parent.wait_for_element_present(*DOM.Dialer.call_log_edit_delete, timeout=2)
            self.marionette.execute_script("document.getElementById('%s').click();" % DOM.Dialer.call_log_edit_delete[1])

            self.marionette.execute_script("""
            var getElementByXpath = function (path) {
                return document.evaluate(path, document, null, 9, null).singleNodeValue;
            };
            getElementByXpath("/html/body/form[3]/menu/button[2]").click();
            """)

        self.UTILS.waitForElements(DOM.Dialer.call_log_no_calls_msg, "'No calls ...' message")


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
            self.UTILS.logResult("info", "Some numbers are in the call log here - removing them ...")
            x = self.UTILS.getElement(DOM.Dialer.call_log_edit_btn, "Edit button")
            x.tap()

            #
            # The edit mode doens't seem to be 'displayed', so we have to work around
            # that at the moment.
            #
            time.sleep(2)
            self.parent.wait_for_element_present(*DOM.Dialer.call_log_edit_header, timeout=2)
            _els = ("xpath", "//ol[@class='log-group']//li")
            x = self.UTILS.getElements(_els, "Call log items", False)


            _precount = len(x)
            self.UTILS.logResult("info", "%s items found." % _precount)
            for i in p_entryNumbers:
                if i != 0:
                    _precount = _precount - 1
                    x[i-1].tap()

            #prueba
            #time.sleep(0.5)
            self.parent.wait_for_element_present(*DOM.Dialer.call_log_edit_delete, timeout=2)
            self.marionette.execute_script("document.getElementById('%s').click();" % DOM.Dialer.call_log_edit_delete[1])
            #time.sleep(0.5)
            self.marionette.execute_script("""
            var getElementByXpath = function (path) {
                return document.evaluate(path, document, null, 9, null).singleNodeValue;
            };
            getElementByXpath("/html/body/form[3]/menu/button[2]").click();
            """)

            try:
                _postcount = self.UTILS.getElements(_els, "Call log items", False)
                _postcount = len(_postcount)
            except:
                _postcount = 0


            self.UTILS.TEST(_postcount == _precount,
                        "%s numbers are left after deletion (there are %s)." % \
                        (_precount,_postcount))


    def callLog_createContact(self, p_num, p_openCallLog=True):
    #
    # Creates a new contact from the call log (only
    # as far as the contacts app opening).
    # If p_openCallLog is set to False it will assume you are
    # already in the call log.
    #
        if p_openCallLog:
            self.openCallLog()

        x = self.UTILS.getElement( ("xpath", DOM.Dialer.call_log_number_xpath % p_num),
                                   "The call log for number %s" % p_num)
        x.tap()

        x = self.UTILS.getElement( DOM.Dialer.call_log_numtap_create_new, "Create new contact button", True, 20)
        x.tap()

        self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)
        self.UTILS.waitForElements(DOM.Contacts.add_contact_header, "'Add contact' header")


    def callThisNumber(self):
        #
        # Get the current number.
        #
        x = self.UTILS.getElement(DOM.Dialer.phone_number, "Phone number field", False)
        dialer_num = x.get_attribute("value")

        #
        # Get own number.
        #
        own_num = self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")

        #
        # Calls the current number.
        #
        x = self.UTILS.getElement(DOM.Dialer.call_number_button, "Call number button")
        x.tap()

        self.UTILS.checkMarionetteOK()
        self.UTILS.switchToFrame(*DOM.Dialer.frame_locator_calling)
        self.UTILS.waitForElements(DOM.Dialer.outgoing_call_locator, "Outgoing call element", True, 5)


    def createContactFromThisNum(self):
        #
        # Creates a new contact from the number currently in the dialler
        # (doesn't fill in the contact details).
        #
        self.UTILS.switchToFrame(*DOM.Dialer.frame_locator)

        x = self.UTILS.getElement(DOM.Dialer.add_to_contacts_button, "Add to contacts button")
        x.tap()

        x = self.UTILS.getElement(DOM.Dialer.create_new_contact_btn, "Create new contact button")
        x.tap()

        #
        # Switch to the contacts frame.
        #
        self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)


    def createMultipleCallLogEntries(self, p_num, p_amount):
        #
        # Put a number in the call log multiple times
        # (done by manipulating the device time).
        # Leaves you in the call log.
        #
        x = self.UTILS.getDateTimeFromEpochSecs(time.time())

        for i in range(0, p_amount):
            _day = x.mday-i
            _mon = x.mon

            if _day < 1:
                #
                # Jump back a month as well.
                #
                _day = 28 #(just to be sure!)
                _mon = x.mon -1

            self.UTILS.setTimeToSpecific(p_day=_day, p_month=_mon)

            self.enterNumber(p_num)
            self.callThisNumber()
            time.sleep(2)
            self.hangUp()

        #
        # Open the call log to finish.
        #
        self.UTILS.checkMarionetteOK()
        self.launch()
        self.openCallLog()


    def enterNumber(self, p_num):
        #
        # Enters a number into the dialler using the keypad.
        #

        try:
            self.parent.wait_for_element_displayed(*DOM.Dialer.phone_number, timeout=1)
        except:
            x = self.UTILS.getElement(DOM.Dialer.option_bar_keypad, "Keypad option selector")
            x.tap()
            self.UTILS.waitForElements(DOM.Dialer.phone_number, "Phone number area")

        for i in str(p_num):

            if i=="+":
                x = self.UTILS.getElement( ("xpath", DOM.Dialer.dialler_button_xpath % 0),
                                           "keypad symbol '+'")
                self.actions=Actions(self.marionette)
                self.actions.long_press(x,2).perform()
            else:
                x = self.UTILS.getElement( ("xpath", DOM.Dialer.dialler_button_xpath % i),
                                           "keypad number %s" % i)
                x.tap()

        #
        # Verify that the number field contains the expected number.
        #
        x = self.UTILS.getElement(DOM.Dialer.phone_number, "Phone number field", False)
        dialer_num = x.get_attribute("value")
        self.UTILS.TEST(str(p_num) in dialer_num, "After entering '%s', phone number field contains '%s'." % \
                                                  (dialer_num, str(p_num)))

        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot:", x)


    def hangUp(self):
        #
        # Hangs up (assuming we're in the 'calling' frame).
        #

        # The call may already be terminated, so don't throw an error if
        # the hangup bar isn't there.
        try:
            self.maroinette.switch_to_frame()
            elDef = ("xpath", "//iframe[contains(@%s, '%s')]" % \
                                DOM.Dialer.frame_locator_calling[0],
                                DOM.Dialer.frame_locator_calling[1])

            self.parent.wait_for_element_present(*elDef, timeout=2)
            x = self.marionette.find_element(*elDef)
            if x:
                self.marionette.switch_to_frame(x)
                self.parent.wait_for_element_displayed(*DOM.Dialer.hangup_bar_locator, timeout=1)
                x = self.marionette.find_element(*DOM.Dialer.hangup_bar_locator)
                if x: x.tap()
        except:
            pass

        #
        # Just to be sure!
        #
        try:
            self.data_layer.kill_active_call()
        except:
            pass

        self.UTILS.switchToFrame(*DOM.Dialer.frame_locator)


    def openCallLog(self):
        #
        # Opens the call log.
        #
        x = self.UTILS.getElement(DOM.Dialer.option_bar_call_log, "Call log button")
        x.tap()

        #self.UTILS.waitForElements(DOM.Dialer.call_log_filter, "Call log filter")

        time.sleep(2)
