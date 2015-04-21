from OWDTestToolkit import DOM
from OWDTestToolkit.apps.video import Video
from OWDTestToolkit.apps.gallery import Gallery
from OWDTestToolkit.apps.music import Music
from OWDTestToolkit.apps.contacts import Contacts
from OWDTestToolkit.apps.camera import Camera
from OWDTestToolkit.utils.decorators import retry

from marionette import Actions
import time

from OWDTestToolkit.utils.i18nsetup import I18nSetup
_ = I18nSetup(I18nSetup).setup()


class Messages(object):

    def __init__(self, parent):
        self.apps = parent.apps
        self.data_layer = parent.data_layer
        self.parent = parent
        self.marionette = parent.marionette
        self.UTILS = parent.UTILS
        self.actions = Actions(self.marionette)

    @retry(5)
    def launch(self):
        #
        # Launch the app.
        #
        self.app = self.apps.launch(self.__class__.__name__)
        self.UTILS.element.waitForNotElements(DOM.GLOBAL.loading_overlay,
                                              self.__class__.__name__ + " app - loading overlay")
        return self.app

    def cancelSettings(self):

        #
        # Press options button
        #
        self.UTILS.reporting.logResult("info", "Cliking on messages options button")
        x = self.UTILS.element.getElement(DOM.Messages.messages_options_btn,
                                          "Messages option button is displayed")
        x.tap()

        #
        # Press cancel button
        #
        cancelBtn = self.UTILS.element.getElement(DOM.Messages.cancel_btn_msg,
                                                  "Press Cancel button")
        cancelBtn.tap()

    def deleteSubject(self, subject):
        #
        # Press options button
        #
        self.UTILS.reporting.logResult("info", "Cliking on messages options button")
        x = self.UTILS.element.getElement(DOM.Messages.messages_options_btn,
                                          "Messages option button is displayed")
        x.tap()

        #
        # Press add subject button
        #
        self.UTILS.reporting.logResult("info", "Cliking on delete subject button")
        x = self.UTILS.element.getElement(DOM.Messages.deletesubject_btn_msg_opt,
                                          "delete subject option button is displayed")
        x.tap()

    def addSubject(self, subject):

        #
        # Press options button
        #
        self.UTILS.reporting.logResult("info", "Cliking on messages options button")
        x = self.UTILS.element.getElement(DOM.Messages.messages_options_btn,
                                          "Messages option button is displayed")
        x.tap()

        #
        # Press add subject button
        #
        screenshot = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult('info', "Screenshot", screenshot)

        self.UTILS.reporting.logResult("info", "Cliking on add subject button")
        x = self.UTILS.element.getElement(DOM.Messages.addsubject_btn_msg_opt,
                                          "add subject option button is displayed")
        x.tap()

        self.UTILS.general.typeThis(DOM.Messages.target_subject,
                                    "Target Subject  field",
                                    subject,
                                    p_no_keyboard=True,
                                    p_validate=False,
                                    p_clear=False,
                                    p_enter=False)

    def checkAirplaneModeWarning(self):
        #
        # Checks for the presence of the popup
        # warning message if you just sent a message
        # while in 'airplane mode' (also removes
        # the message so you can continue).
        #
        x = self.UTILS.element.getElement(DOM.Messages.airplane_warning_message,
                                          "Airplane mode warning message",
                                          True, 5, False)
        if x:
            self.UTILS.reporting.logResult("info",
                                           "Warning message title detected = '" + x.text + "'.")

            x = self.UTILS.element.getElement(DOM.Messages.airplane_warning_ok, "OK button")
            x.tap()

    def check_last_message_contents(self, expected, mms=False):
        """Get the last message text and check it against the expected value.
        """
        msg = self.last_message_in_this_thread()
        dom = DOM.Messages.last_message_mms_text if mms else DOM.Messages.last_message_text
        msg_text = self.marionette.find_element(*dom, id=msg.id)
        self.UTILS.test.test((msg_text and msg_text.text == expected),
                             u"Expected message text = '{}' ({}) (got '{}' ({})).".
                             format(expected, len(expected), msg_text.text, len(msg_text.text)))

    def checkIsInToField(self, target, targetIsPresent=True):
        #
        # Verifies if a number (or contact name) is
        # displayed in the "To: " field of a compose message.<br>
        # (Uses 'caseless' search for this.)
        #
        time.sleep(1)
        x = self.UTILS.element.getElements(DOM.Messages.target_numbers, "'To:' field contents", False)

        boolOK = False
        for i in x:
            if i.text.lower() == str(target).lower():
                boolOK = True
                break

        testMsg = "is" if targetIsPresent else "is not"
        testMsg = "\"" + str(target) + "\" " + testMsg + " in the 'To:' field."
        self.UTILS.test.test(boolOK == targetIsPresent, testMsg)
        return boolOK

    def checkMMSIcon(self, thread_name):

        #
        # Get the thread for which we want to check the icon existence
        #
        selector = ("xpath", DOM.Messages.thread_selector_xpath.format(thread_name))
        elem = self.UTILS.element.getElement(selector, "Message thread for " + thread_name)

        #
        # But, in order to make sure we're getting the specific frame, what we trully
        # got above is an inner child of the thread element. So, we gotta get the father
        #
        thread = self.marionette.execute_script("""
            return arguments[0].parentNode;
        """, script_args=[elem])

        #
        # Checks for the presence of the MMS icon
        #
        icon = thread.find_element(*DOM.Messages.mms_icon)
        if icon:
            self.UTILS.test.test(icon is not None, "MMS icon detected for thread [{}]".format(thread_name))

    def checkNumberIsInToField(self, target):
        #
        # Verifies if a number is contained in the
        # "To: " field of a compose message (even if it's
        # not displayed - i.e. a contact name is displayed,
        # but this validates the <i>number</i> for that
        # contact).
        #
        x = self.UTILS.element.getElements(DOM.Messages.target_numbers, "'To:' field contents")

        boolOK = False
        for i in x:
            if i.get_attribute("data-number") == target:
                boolOK = True
                break

        self.UTILS.test.test(boolOK,
            "\"" + str(target) + "\" is the number in one of the 'To:' field targets.")
        return boolOK

    def checkThreadHeader(self, header):
        #
        # Verifies if a string is contained in the header
        #
        x = self.UTILS.element.getElement(DOM.Messages.message_header, "Header")

        boolOK = False
        if x.get_attribute("data-number") == header:
            boolOK = True

        self.UTILS.test.test(boolOK, "\"" + str(header) + "\" is the header in the SMS conversation.")
        return boolOK

    def checkThreadHeaderWithNameSurname(self, header):
        #
        # Verifies if a string is contained in the header
        #
        x = self.UTILS.element.getElement(DOM.Messages.message_header, "Header")

        boolOK = False

        if x.text == header:
            boolOK = True

        self.UTILS.test.test(boolOK, "\"" + header + "\" is the header in the SMS conversation.")
        return boolOK

    def closeThread(self):
        #
        # Closes the current thread (returns you to the
        # 'thread list' SMS screen).
        #
        x = self.UTILS.element.getElement(DOM.Messages.header_back_button, "Back button")
        x.tap()
        self.UTILS.element.waitForElements(DOM.Messages.main_header, "Messages main header")

    def countMessagesInThisThread(self):
        #
        # Returns the number of messages in this thread
        # (assumes you're already in the thread).
        #
        try:
            return len(self.UTILS.element.getElements(DOM.Messages.message_list, "Messages"))
        except:
            return 0

    def countNumberOfThreads(self):
        #
        # Count all threads (assumes the messagin app is already open).
        #
        try:
            return len(self.UTILS.element.getElements(DOM.Messages.threads_list, "Threads"))
        except:
            return 0

    def create_and_send_mms(self, attached_type, nums, m_text):

        self.gallery = Gallery(self.parent)
        self.video = Video(self.parent)
        self.music = Music(self.parent)

        #
        # Launch messages app.
        #
        self.launch()

        #
        # Create a new SMS
        #
        self.startNewSMS()

        #
        # Insert the phone number in the To field
        #
        self.addNumbersInToField(nums)

        #
        # Create MMS.
        #
        self.enterSMSMsg(m_text)

        if attached_type == "image":
            #
            # Add an image file
            #
            self.UTILS.general.add_file_to_device('./tests/_resources/80x60.jpg', destination='DCIM/100MZLLA')

            self.create_mms_image()
            self.gallery.click_on_thumbnail_at_position_mms(0)
        elif attached_type == "cameraImage":
            #
            # Add an image file from camera
            #
            self.create_mms_camera_image()
            time.sleep(3)
        elif attached_type == "video":
            #
            # Load an video file into the device.
            #
            self.UTILS.general.add_file_to_device('./tests/_resources/mpeg4.mp4', destination='DCIM/100MZLLA')

            self.create_mms_video()
            self.video.click_on_video_at_position_mms(0)
        elif attached_type == "audio":
            #
            # Load an video file into the device.
            #
            self.UTILS.general.add_file_to_device('./tests/_resources/AMR.amr', destination='/SD/mus')

            self.create_mms_music()
            self.music.click_on_song_mms()
        else:
            # self.UTILS.reporting.logResult("info", "incorrect value received")
            msg = "FAILED: Incorrect parameter received in create_and_send_mms()"\
                ". attached_type must being image, video or audio."
            self.UTILS.test.test(False, msg)

        self.sendSMS()
        return self.last_sent_message_timestamp()

    def create_and_send_sms(self, nums, msg, sending_check=True):
        #
        # Create and send a new SMS.<br>
        # <b>Note:</b> The nums field must be an array of numbers
        # or contact names.
        #

        self.startNewSMS()

        #
        # Enter the numbers.
        #
        self.addNumbersInToField(nums)

        #
        # Enter the message.
        #
        self.enterSMSMsg(msg)

        #
        # The header should now say how many recipients.
        #
        time.sleep(2)  # give the header time to change.

        num_recs = len(nums)
        search_str = _(" recipient") if num_recs == 1 else _(" recipients")
        self.UTILS.element.headerCheck(str(num_recs) + search_str)

        #
        # Send the message.
        #
        self.sendSMS(sending_check)

    def create_mms_image(self):

        attach = self.UTILS.element.getElement(DOM.Messages.attach_button, "Attach button")
        attach.tap()

        self.marionette.switch_to_frame()

        gallery = self.UTILS.element.getElement(DOM.Messages.mms_from_gallery, "From gallery")
        gallery.tap()

        self.UTILS.iframe.switchToFrame(*DOM.Gallery.frame_locator)

    def create_mms_camera_image(self):
        self.camera = Camera(self.parent)

        attach = self.UTILS.element.getElement(DOM.Messages.attach_button, "Attach button")
        attach.tap()

        self.marionette.switch_to_frame()

        camera = self.UTILS.element.getElement(DOM.Messages.mms_from_camera, "From Camera")
        camera.tap()

        self.UTILS.iframe.switchToFrame(*DOM.Camera.frame_locator)

        #
        # Take a picture.
        #
        self.camera.take_and_select_picture()

        self.UTILS.iframe.switchToFrame(*DOM.Messages.frame_locator)

    def create_mms_music(self):

        attach = self.UTILS.element.getElement(DOM.Messages.attach_button, "Attach button")
        attach.tap()

        self.marionette.switch_to_frame()

        music = self.UTILS.element.getElement(DOM.Messages.mms_from_music, "From music")
        music.tap()

        self.UTILS.iframe.switchToFrame(*DOM.Music.frame_locator)

    def create_mms_video(self):

        attach = self.UTILS.element.getElement(DOM.Messages.attach_button, "Attach button")
        attach.tap()

        self.marionette.switch_to_frame()

        video = self.UTILS.element.getElement(DOM.Messages.mms_from_video, "From video")
        video.tap()

        self.UTILS.iframe.switchToFrame(*DOM.Video.frame_locator)

    def delete_all_threads(self):
        #
        # Deletes all threads (assumes the messagin app is already open).
        #
        try:
            self.parent.wait_for_element_displayed(*DOM.Messages.no_threads_message, timeout=2)
            x = self.marionette.find_element(*DOM.Messages.no_threads_message)
            if x.is_displayed():
                self.UTILS.reporting.logResult("info", "(No message threads to delete.)")
        except:
            self.UTILS.reporting.logResult("info", "Deleting message threads ...")

            x = self.threadEditModeON()
            x = self.UTILS.element.getElement(DOM.Messages.delete_threads_button, "Delete threads button")
            x.tap()
            x = self.UTILS.element.getElement(DOM.Messages.check_all_threads_btn,
                                              "Select all button")
            x.tap()

            self.deleteSelectedThreads()
            self.UTILS.element.waitForElements(DOM.Messages.no_threads_message,
                                               "No message threads notification", True, 60)

    def deleteMessagesInThisThread(self, msg_array=False):
        #
        # Enters edit mode, selects the required messages and
        # deletes them.<br>
        # msg_array is an array of numbers.
        # If it's not specified then all messages in this
        # thread will be deleted.
        #
        if msg_array:
            self.editAndSelectMessages(msg_array)
        else:
            #
            # Go into messages Settings..
            #
            x = self.UTILS.element.getElement(DOM.Messages.edit_messages_icon, "Edit button")
            x.tap()

            #
            # Go into message edit mode..
            #
            x = self.UTILS.element.getElement(DOM.Messages.delete_messages_btn, "Edit button")
            x.tap()

            #
            # Press select all button.
            #
            x = self.UTILS.element.getElement(DOM.Messages.check_all_messages_btn, "'Select all' button")
            x.tap()

        self.deleteSelectedMessages()

    def deleteSelectedMessages(self):
        self.UTILS.reporting.debug("*** Tapping top Delete button")
        x = self.UTILS.element.getElement(DOM.Messages.delete_messages_ok_btn, "Delete button")
        x.tap()
        time.sleep(2)

        self.UTILS.reporting.debug("*** Tap Delete messages confirmation button")
        x = self.UTILS.element.getElement(DOM.Messages.delete_threads_ok_btn, "Delete messages confirmation button")
        x.tap()
        time.sleep(2)

    def deleteSelectedThreads(self):
        delete_btn = self.UTILS.element.getElement(DOM.Messages.threads_delete_button, "Delete threads button")
        delete_btn.tap()

        time.sleep(2)
        x = self.UTILS.element.getElement(DOM.Messages.delete_threads_ok_btn, "Delete threads confirmation button")
        x.tap()

        #
        # For some reason after you do this, you can't enter a 'to' number anymore.
        # After a lot of headscratching, it was just easier to re-launch the app.
        #
        time.sleep(5)
        self.launch()

    def deleteThreads(self, target_array=False):
        #
        # Enters edit mode, selects the required messages and
        # deletes them.<br>
        # target_array is an array of target numbers
        # or contacts which identify the threads to be selected.
        # If it's not specified then all messages in this
        # thread will be deleted.
        #
        try:
            self.parent.wait_for_element_displayed(*DOM.Messages.no_threads_message, timeout=2)
            x = self.marionette.find_element(*DOM.Messages.no_threads_message)
            if x.is_displayed():
                self.UTILS.reporting.logResult("info", "(No message threads to delete.)")
        except:
            self.UTILS.reporting.logResult("info", "Deleting message threads ...")
            if target_array:
                self.UTILS.reporting.debug("*** Selecting threads for deletion [{}]".format(target_array))
                self.editAndSelectThreads(target_array)
                self.UTILS.reporting.debug("*** Threads selected")
                self.deleteSelectedThreads()
            else:
                self.delete_all_threads()

    def editAndSelectMessages(self, msg_array):
        #
        # Puts this thread into Edit mode and selects
        # the messages listed in msg_array.<br>
        # msg_array is an array of numbers.
        #

        #
        # Go into messages Settings..
        #
        self.UTILS.reporting.debug("*** Tap Edit button")
        x = self.UTILS.element.getElement(DOM.Messages.edit_messages_icon, "Edit button")
        x.tap()
        time.sleep(2)

        #
        # Go into message edit mode..
        #
        self.UTILS.reporting.debug("*** Tap Delete messages button")
        x = self.UTILS.element.getElement(DOM.Messages.delete_messages_btn, "Delete messages button")
        x.tap()
        time.sleep(2)

        #
        # Check the messages (for some reason, just doing x[i].click() doesn't
        # work for element zero, so I had to do this 'longhanded' version!).
        #
        messages = self.UTILS.element.getElements(DOM.Messages.message_list, "Messages")
        selected = 0
        for msg in messages:
            if selected in msg_array:
                self.UTILS.reporting.debug("Selecting message {} ...".format(selected))
                msg.tap()
                time.sleep(2)
            selected += 1

    def editAndSelectThreads(self, target_array):
        #
        # Puts this thread into Edit mode and selects
        # the messages listed in p_msg_array.<br>
        # target_array is an array of target numbers
        # or contacts which identify the threads to be selected.
        #

        #
        # Go into edit mode..
        #
        self.threadEditModeON()

        x = self.UTILS.element.getElement(DOM.Messages.delete_threads_button, "Delete threads button")
        x.tap()

        for i in target_array:
            self.UTILS.reporting.debug("selecting thread for [{}]".format(i))
            x = self.UTILS.element.getElement(("xpath", DOM.Messages.thread_selector_xpath.format(i)),
                                              "Thread checkbox for '{}'".format(i))
            self.UTILS.reporting.debug("Trying to tap in element {}".format(x))
            x.tap()

        #
        # Finally check that all desired threads have been selected
        #
        header = self.UTILS.element.getElement(DOM.Messages.edit_threads_header, "Edit threads header").text
        expected_title = str(len(target_array)) if len(target_array) else _("Delete messages")
        self.UTILS.test.test(expected_title in header, "Check that all desired threads have been selected")

    def enterSMSMsg(self, msg, not_keyboard=True):
        #
        # Create and send a message (assumes we are in a new 'create new message'
        # screen with the destination number filled in already).
        #
        time.sleep(1)  # Trying to remove an intermittent issue.
        self.UTILS.general.typeThis(DOM.Messages.input_message_area,
                                    "Input message area",
                                    msg,
                                    p_no_keyboard=not_keyboard,
                                    p_clear=False,
                                    p_enter=False,
                                    p_validate=False)  # it's the text() of this field, not the value.

        #
        # Validate the field.
        #
        x = self.UTILS.element.getElement(DOM.Messages.input_message_area,
                                    "Input message area (for validation)")
        self.UTILS.test.test(x.text == msg,
                        "The text in the message area is as expected." + \
                        "|EXPECTED: '" + msg + "'" + \
                        "|ACTUAL  : '" + x.text + "'")

    def addNumbersInToField(self, nums):
        """
        Add the phone numbers in the 'To' field of this sms message.
        Assumes you are in 'create sms' screen.
        """

        # This variable is used to keep track of the appearance of the keyboard frame
        n = 0

        for num in nums:
            # Even though we don't use the keyboard for putting the number in,
            # we need it for the ENTER button (which allows us to put more than
            # one number in).
            #
            # So check that the keyboard appears when we tap the "TO" field if we have
            # more than one number.
            if len(nums) > 1:
                self.UTILS.reporting.logResult("info", "Checking the keyboard appears when I tap the 'To' field ...")
                to_field = self.UTILS.element.getElement(DOM.Messages.target_numbers_empty, "Target number field")
                to_field.tap()

                boolKBD = False
                self.marionette.switch_to_frame()

                if n < 1:

                    try:
                        # A 'silent' check to see if the keyboard iframe appears.
                        elDef = ("xpath", "//iframe[contains(@{}, '{}')]".
                                 format(DOM.Keyboard.frame_locator[0], DOM.Keyboard.frame_locator[1]))
                        self.parent.wait_for_element_displayed(*elDef, timeout=2)
                        boolKBD = True
                    except:
                        boolKBD = False

                    self.UTILS.test.test(
                        boolKBD, "Keyboard is displayed when 'To' field is clicked for the first time")

                self.UTILS.iframe.switchToFrame(*DOM.Messages.frame_locator)

            if n == 0:

                self.UTILS.general.typeThis(DOM.Messages.target_numbers_empty,
                                            "Target number field",
                                            num,
                                            p_no_keyboard=True,
                                            p_validate=False,
                                            p_clear=False,
                                            p_enter=True)

            else:
                self.UTILS.general.typeThis(DOM.Messages.target_numbers_empty,
                                            "Target number field",
                                            num,
                                            p_no_keyboard=True,
                                            p_validate=False,
                                            p_clear=False,
                                            p_enter=False)
                input_area = self.UTILS.element.getElement(DOM.Messages.input_message_area, "Target number field")
                input_area.tap()

            n += 1

    def addContactToField(self, contact_name):
        self._search_for_contact(contact_name)
        # Now check the correct name is in the 'To' list.
        self.checkIsInToField(contact_name)

    def _select_forward_option_for(self, element):
        self.actions.long_press(element, 2).perform()
        self.UTILS.reporting.logResult("info", "Clicking on forward button")
        forward_option = self.UTILS.element.getElement(DOM.Messages.forward_btn_msg_opt, "Forward button is displayed")
        forward_option.tap()

    def _search_for_contact(self, contact_name):
        self.contacts = Contacts(self.parent)
        self.selectAddContactButton()
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)

        self.contacts.search(contact_name)
        self.contacts.check_search_results(contact_name)

        results = self.UTILS.element.getElements(DOM.Contacts.search_results_list, "Contacts search results")
        for result in results:
            if result.text == contact_name:
                result.tap()
                break

        # Switch back to the sms iframe.
        self.apps.switch_to_displayed_app()

    def forwardMessage(self, msg_type, target_telNum):
        """
        Forwards the last message of the thread to a number
        """

        self.UTILS.reporting.logResult('info', "The message type to forward is: {}".format(msg_type))

        if msg_type == "sms" or msg_type == "mms":
            self.UTILS.reporting.logResult("info", "Open {} option with longtap on it".format(msg_type))
            last = self.last_message_in_this_thread()
            body = self.marionette.find_element(*DOM.Messages.last_message_body, id=last.id)
            self._select_forward_option_for(body)

        elif msg_type == "mmssub":
            self.UTILS.reporting.logResult("info", "Open mms with subject options with longtap on it")
            mms_subject = self.UTILS.element.getElement(DOM.Messages.received_mms_subject, "Target MMS field")
            self._select_forward_option_for(mms_subject)

        else:
            self.UTILS.reporting.logResult("info", "incorrect value received")
            self.UTILS.test.test(False, "Incorrect value received")

        self.addNumbersInToField([target_telNum])

        self.UTILS.reporting.logResult("info", "Clicking on Send button")
        self.sendSMS()

    def forwardMessageToContact(self, msg_type, contact_name):
        """
        Forwards the last message of the thread to a contact, searching for it
        """
        self.UTILS.reporting.logResult('info', "The message type to forward is: {}".format(msg_type))

        if msg_type == "sms" or msg_type == "mms":
            # Open sms option with longtap on it
            self.UTILS.reporting.logResult("info", "Open sms option with longtap on it")
            sms = self.last_message_in_this_thread()
            body = self.marionette.find_element(*DOM.Messages.last_message_body, id=sms.id)
            self._select_forward_option_for(body)

        elif msg_type == "mmssub":
            # Open mms option with longtap on it
            self.UTILS.reporting.logResult("info", "Open mms with subject options with longtap on it")
            mms_subject = self.UTILS.element.getElement(DOM.Messages.received_mms_subject,
                                                        "Target MMS field")
            self._select_forward_option_for(mms_subject)

        else:
            self.UTILS.reporting.logResult("info", "incorrect value received")
            self.UTILS.test.test(False, "Incorrect value received")

        # Search for the contact and check it's been added
        self.addContactToField(contact_name)

        # Send the mms.
        self.UTILS.reporting.logResult("info", "Clicking on Send button")
        self.sendSMS()

    def forwardMessageToMultipleRecipients(self, msg_type, target_telNum, contact_name):
        self.UTILS.reporting.logResult('info', "The message type to forward is: {}".format(msg_type))

        if msg_type == "sms" or msg_type == "mms":
            # Open sms option with longtap on it
            self.UTILS.reporting.logResult("info", "Open sms option with longtap on it")
            sms = self.last_message_in_this_thread()
            body = self.marionette.find_element(*DOM.Messages.last_message_body, id=sms.id)
            self._select_forward_option_for(body)

        elif msg_type == "mmssub":
            # Open mms option with longtap on it
            self.UTILS.reporting.logResult("info", "Open mms with subject options with longtap on it")
            mms_subject = self.UTILS.element.getElement(DOM.Messages.received_mms_subject,
                                                        "Target MMS field")
            self._select_forward_option_for(mms_subject)

        else:
            self.UTILS.reporting.logResult("info", "incorrect value received")
            self.UTILS.test.test(False, "Incorrect value received")

        # Add phone numbers
        self.addNumbersInToField([target_telNum])
        # Search for the contact and check it's been added
        self.addContactToField(contact_name)

        # Send the mms.
        self.UTILS.reporting.logResult("info", "Clicking on Send button")
        self.sendSMS()

    def get_mms_attachments_info(self, mms):
        """Give name and file size for all attachments in an MMS.

        Given an MMS, return a list containing a dictionary for every attachment,
        with two keys, name and size.
        """
        attachment_names = self.marionette.find_elements(*DOM.Messages.mms_attachment_names, id=mms.id)
        attachment_sizes = self.marionette.find_elements(*DOM.Messages.mms_attachment_sizes, id=mms.id)
        result = []
        for (i, name) in enumerate(attachment_names):
            inner_text = self.marionette.execute_script("""return arguments[0].innerHTML;""", script_args=[name])
            att = {}
            att["name"] = inner_text
            size_elem = attachment_sizes[i].get_attribute("data-l10n-args")
            size = size_elem[size_elem.index(":") + 2:size_elem.rfind("\"")]
            i = i + 1
            att["size"] = size
            result.append(att)
        return result

    def getThreadText(self, num):
        #
        # Returns the preview text for the thread for this number (if it exists),
        # or False if either the thread doesn't exist or can't be found.
        #
        if self.threadExists(num):
            x = self.UTILS.element.getElements(DOM.Messages.threads_list, "Threads")

            for thread in x:
                try:
                    thread.find_element("xpath", ".//p[text()='{}']".format(num))
                    z = thread.find_element("xpath", ".//span[@class='body-text']")
                    return z.text
                except:
                    pass
        return False

    def header_addToContact(self):
        #
        # Taps the header and tries to tap the 'Add to an existsing contact' button.
        # - Assumes we are looking at a message thread already.
        # - Leaves you in the correct iframe to continue (contacts).
        #
        x = self.UTILS.element.getElement(DOM.Messages.message_header, "Thread header")
        x.tap()

        x = self.UTILS.element.getElement(DOM.Messages.header_add_to_contact_btn,
                                          "'Add to an existing contact' button")
        x.tap()

        #
        # Switch to correct iframe.
        #
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)

    def header_call(self):
        """Tap on the header of a messages thread and dial the number
        """
        x = self.UTILS.element.getElement(DOM.Messages.message_header, "Thread header")
        x.tap()

        #
        # Select dialer option.
        #
        x = self.UTILS.element.getElement(DOM.Messages.header_call_btn, "'Call' button")
        x.tap()

        #
        # Switch to correct iframe.
        #
        self.UTILS.iframe.switchToFrame(*DOM.Dialer.frame_locator)

    def header_createContact(self):
        #
        # Taps the header and tries to tap the 'send message' button.
        # - Assumes we are looking at a message thread already.
        # - Leaves you in the correct iframe to continue.
        #
        x = self.UTILS.element.getElement(DOM.Messages.message_header, "Thread header")
        x.tap()

        x = self.UTILS.element.getElement(DOM.Messages.header_create_new_contact_btn,
                                          "'Create new contact' button")
        x.tap()

        #
        # Switch to correct iframe.
        #
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)

    def header_sendMessage(self):
        #
        # Taps the header and tries to tap the 'send message' button.
        # - Assumes we are looking at a message thread already.
        # - Leaves you in the correct iframe to continue.
        #
        x = self.UTILS.element.getElement(DOM.Messages.message_header, "Thread header")
        x.tap()

        x = self.UTILS.element.getElement(DOM.Messages.header_send_message_btn, "'Send message' button")
        x.tap()

    def last_message_in_this_thread(self):
        #
        # Returns an object of the last message in the current thread.
        #
        self.parent.wait_for_element_present(*DOM.Messages.last_message, timeout=20)
        message = self.marionette.find_element(*DOM.Messages.last_message)
        self.UTILS.element.scroll_into_view(message)
        return message

    def last_sent_message_timestamp(self):
        """Returns the timestamp of the last sent message
        """
        send_time = self.marionette.find_element(*DOM.Messages.last_sent_message).get_attribute("data-timestamp")
        return float(send_time) / 1000

    def last_sent_message(self):
        """Returns the last sent message
        """
        return self.marionette.find_element(*DOM.Messages.last_sent_message)

    def open_attached_file(self, frame_to_change):
        elem = DOM.Messages.last_message_attachment_av
        last = self.UTILS.element.getElement(elem, "Last message attachment")
        self.UTILS.element.scroll_into_view(last)

        # Now get the thumbnail in order to open it
        thumb = last.find_element(*DOM.Messages.last_message_thumbnail)
        thumb.tap()
        self.UTILS.iframe.switchToFrame(*frame_to_change)

    def openThread(self, num):
        #
        # Opens the thread for this number (assumes we're looking at the
        # threads in the messaging screen).
        #
        self.UTILS.reporting.logResult('info', 'Trying to open thread for: {}'.format(num))
        try:
            thread_el = ("xpath", DOM.Messages.thread_selector_xpath.format(num))
            self.parent.wait_for_element_displayed(*thread_el)
            x = self.marionette.find_element(*thread_el)
            x.tap()

            self.UTILS.element.waitForElements(DOM.Messages.send_message_button, "'Send' button")
        except Exception as e:
            x = self.UTILS.debug.screenShotOnErr()
            msg = "<b>NOTE:</b> The thread <i>may</i> have failed to open due to [{}].".format(e)
            self.UTILS.reporting.logResult("info", msg, x)

    def readLastSMSInThread(self):
        #
        # Read last message in the current thread.
        #
        received_message = self.UTILS.element.getElements(DOM.Messages.received_messages,
                                                          "Received messages")[-1]
        return str(received_message.text)

    def readNewSMS(self, fromNum):
        #
        # Read and return the value of the new message received from number.
        #
        x = self.UTILS.element.getElement(("xpath", DOM.Messages.messages_from_num.format(fromNum)),
                                          "Message from '" + fromNum + "'")
        x.tap()

        # (From gaiatest: "TODO Due to displayed bugs I cannot find a good wait
        # for switch btw views")
        time.sleep(5)

        #
        # Return the last comment in this thread.
        #
        return self.readLastSMSInThread()

    def removeContactFromToField(self, target):
        #
        # Removes target from the "To" field of this SMS.<br>
        # Returns True if it found the target, or False if not.
        #
        x = self.UTILS.element.getElements(DOM.Messages.target_numbers, "'To:' field contents")

        for i in range(len(x)):
            self.UTILS.reporting.logResult("info",
                                           "Checking target '{}' to '{}' ...".format(x[i].text, target))

            if x[i].text.lower() == target.lower():
                self.UTILS.reporting.logResult("info", "Tapping contact '" + target + "' ...")
                x[i].tap()

                try:
                    #
                    # This contact was added via 'add contact' icon.
                    #
                    self.parent.wait_for_element_displayed(*DOM.Messages.remove_contact_from_to_field)
                    confirm_remove = self.marionette.find_element(*DOM.Messages.remove_contact_from_to_field)
                    self.UTILS.reporting.logResult("info", "Tapping 'Remove' button.")
                    confirm_remove.tap()
                    return True
                except:
                    #
                    # This contact was manually entered.
                    #
                    z = self.UTILS.element.getElements(DOM.Messages.target_numbers,
                                                       "Target to be removed")[i]
                    z.clear()
                    return True
        return False

    def selectAddContactButton(self):
        #
        # Taps the 'add contact' button
        #
        add_btn = self.UTILS.element.getElement(DOM.Messages.add_contact_button, "Add contact button")
        add_btn.tap()

    def sendSMS(self, check=True):
        #
        # Just presses the 'send' button (assumes everything else is done).
        #
        sendBtn = self.UTILS.element.getElement(DOM.Messages.send_message_button, "Send sms button")
        time.sleep(1)
        sendBtn.tap()

        if check:
            self.UTILS.element.waitForElements(DOM.Messages.last_message_sending_spinner, "'Sending' icon", True, 20)
            # (Give the spinner time to appear.)
            time.sleep(2)
            self.UTILS.element.waitForNotElements(DOM.Messages.last_message_sending_spinner, "'Sending' icon", True, 180)

        #
        # Check if we received the 'service unavailable' message.
        #
        try:
            self.parent.wait_for_element_displayed(*DOM.Messages.service_unavailable_msg, timeout=2)
            x = self.UTILS.debug.screenShotOnErr()
            msg = "'Service unavailable' message detected - unable to send sms!"
            self.UTILS.reporting.logResult("info", msg, x)
            return False
        except:
            pass

        return True


    def startNewSMS(self):
        #
        # Starts a new sms (doesn't fill anything in).
        # Assumes the Messaging app is already launched.
        #
        newMsgBtn = self.UTILS.element.getElement(DOM.Messages.create_new_message_btn, "Create new message button")
        newMsgBtn.tap()

    def threadCarrier(self):
        #
        # Returns the 'carrier' being used by this thread.
        #
        x = self.UTILS.element.getElement(DOM.Messages.type_and_carrier_field, "Type and carrier information")
        parts = x.text.split("|")
        if len(parts) > 1:
            return parts[1].strip()
        return parts[0].strip()

    def threadEditModeOFF(self):
        #
        # Turns off Edit mode while in the SMS threads screen.
        #
        x = self.UTILS.element.getElement(DOM.Messages.cancel_edit_threads, "Cancel button")
        x.tap()
        self.UTILS.element.waitForElements(DOM.Messages.edit_threads_button, "Edit button")

    def threadEditModeON(self):
        #
        # Turns on Edit mode while in the SMS threads screen.
        #
        x = self.UTILS.element.getElement(DOM.Messages.edit_threads_button, "Edit button")
        self.UTILS.element.simulateClick(x)
        self.UTILS.element.waitForElements(DOM.Messages.cancel_edit_threads, "Cancel button")

    def threadExists(self, num):
        #
        # Verifies that a thread exists for this number (returns True or False).
        #
        boolOK = False
        try:
            self.parent.wait_for_element_present("xpath", DOM.Messages.thread_selector_xpath.format(num), 1)
            boolOK = True
        except:
            boolOK = False

        return boolOK

    def threadType(self):
        #
        # Returns the 'type' being used by this thread.
        #
        x = self.UTILS.element.getElement(DOM.Messages.type_and_carrier_field, "Type and carrier information")
        parts = x.text.split("|")
        typ = parts[0].strip()
        return typ if len(parts) > 1 else ''

    def time_of_last_message_in_thread(self):
        #
        # Returns the time of the last message in the current thread.
        #
        t = self.UTILS.element.getElement(DOM.Messages.last_message_time, "Last message time")
        return t.text

    def time_of_thread(self, num):
        #
        # Returns the time of a thread.
        #
        x = self.UTILS.element.getElement(("xpath", DOM.Messages.thread_timestamp_xpath.format(num)),
                                          "Thread time", True, 10, False)
        return x.text

    def thread_timestamp(self, num):
        #
        # Returns the timestamp of a thread
        #
        x = self.marionette.find_element(*DOM.Messages.last_message).get_attribute("data-timestamp")
        return float(x)

    def verify_mms_received(self, attached_type, sender_number):

        self.UTILS.iframe.switchToFrame(*DOM.Messages.frame_locator)
        self.openThread(sender_number)
        message = self.last_message_in_this_thread()
        self.UTILS.test.test(message, "A received message appeared in the thread.", True)

        self.UTILS.reporting.debug("*** attached type: {}".format(attached_type))
        if attached_type == "img":
            elem = DOM.Messages.last_message_attachment_img
        elif attached_type == "video":
            elem = DOM.Messages.last_message_attachment_av
        elif attached_type == "audio":
            elem = DOM.Messages.last_message_attachment_av
        else:
            # self.UTILS.reporting.logResult("info", "incorrect value received")
            msg = "FAILED: Incorrect parameter received in verify_mms_received()"\
                ". Attached_type must be image, video or audio."
            self.UTILS.test.test(False, msg)

        self.UTILS.reporting.debug("*** searching for attachment type")
        # Look for all the attachments, since there can be more than one
        atts = self.UTILS.element.getElements(elem, "Last message attachments")
        self.UTILS.element.scroll_into_view(atts[0])
        found = False
        for att in atts:
            typ = att.get_attribute("data-attachment-type")
            self.UTILS.reporting.debug("*** searching for attachment type Result: {}".format(typ))
            if typ == attached_type:
                found = True
        if not found:
            msg = "No attachment with type {} was found in the message".format(attached_type)
            self.UTILS.test.test(False, msg)

    def wait_for_message(self, send_time=None, timeout=120):
        """Wait for a received message in the current thread and return it.
        """
        if not send_time:
            send_time = self.last_sent_message_timestamp()

        poll_time = 2
        poll_reps = (timeout / poll_time)
        result = False

        for i in range(poll_reps):
            # Get last message in this thread.
            last_msg = self.last_message_in_this_thread()

            if not last_msg:
                time.sleep(poll_time)
                continue

            # If the send_time timestamp is greater than this message's timestamp,it means the message
            # we expect has not arrived yet, so we have to wait a bit more.
            message_data_time = float(last_msg.get_attribute("data-timestamp")) / 1000
            fmt = "data-timestamp of last message in thread: {:.3f} send_time: {:.3f} --> {}"
            self.UTILS.reporting.debug(fmt.format(message_data_time, send_time, send_time > message_data_time))
            if send_time > message_data_time:
                continue

            # Is this a received message?
            if "incoming" in last_msg.get_attribute("class"):
                result = last_msg
                break

            # Nope - sleep then try again.
            time.sleep(poll_time)

        self.UTILS.test.test(result, "Last message in thread 'received' within {} seconds.".\
                             format(timeout))
        return result
