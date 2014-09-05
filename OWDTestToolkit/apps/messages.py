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

    @retry(5)
    def launch(self):
        #
        # Launch the app.
        #
        self.app = self.apps.launch(self.__class__.__name__)
        self.UTILS.element.waitForNotElements(DOM.GLOBAL.loading_overlay,
                                              self.__class__.__name__ + " app - loading overlay")
        return self.app

    def addNumbersInToField(self, nums):
        #
        # Add the numbers (or contact name) in the 'To'
        # field of this sms message.
        # Assumes you are in 'create sms' screen.
        # <br>
        # <b>nums</b> must be an array.
        #
        n = 0

        for i in nums:
            x = self.UTILS.debug.screenShotOnErr()

            #
            # Even though we don't use the keyboard for putting the number in,
            # we need it for the ENTER button (which allows us to put more than
            # one number in).
            #
            # So check that the keyboard appears when we tap the "TO" field if we have
            # more than one number.
            #
            if len(nums) > 1:
                self.UTILS.reporting.logResult("info", "Checking the keyboard appears when I tap the 'To' field ...")
                x = self.UTILS.element.getElement(DOM.Messages.target_numbers_empty, "Target number field")
                x.tap()

                boolKBD = False
                self.marionette.switch_to_frame()

                if n < 1:

                    try:
                        #
                        # A 'silent' check to see if the keyboard iframe appears.
                        elDef = ("xpath", "//iframe[contains(@{}, '{}')]".\
                                 format(DOM.Keyboard.frame_locator[0], DOM.Keyboard.frame_locator[1]))
                        self.parent.wait_for_element_displayed(*elDef, timeout=2)
                        boolKBD = True
                    except:
                        boolKBD = False

                    self.UTILS.test.TEST(boolKBD, "Keyboard is displayed when 'To' field is clicked.")

                self.UTILS.iframe.switchToFrame(*DOM.Messages.frame_locator)

            #
            # Seems okay, so proceed ...
            #
            if n == 0:

                self.UTILS.general.typeThis(DOM.Messages.target_numbers_empty,
                                    "Target number field",
                                    i,
                                    p_no_keyboard=True,
                                    p_validate=False,
                                    p_clear=False,
                                    p_enter=True)

            else:
                self.UTILS.general.typeThis(DOM.Messages.target_numbers_empty,
                                    "Target number field",
                                    i,
                                    p_no_keyboard=True,
                                    p_validate=False,
                                    p_clear=False,
                                    p_enter=False)
                x = self.UTILS.element.getElement(DOM.Messages.input_message_area, "Target number field")
                x.tap()

            n += 1

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

    def check_last_message_contents(self, expected):
        """Get the last message text and check it against the expected value.
        """
        returnedSMS = self.lastMessageInThisThread()
        returnedSMS_text = self.marionette.find_element(*DOM.Messages.last_message_text,
                                                                      id=returnedSMS.id)
        self.UTILS.test.TEST((returnedSMS_text and returnedSMS_text.text == expected),
                             "Expected SMS text = '{}' (got '{}').".format(expected, returnedSMS_text.text))

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
        self.UTILS.test.TEST(boolOK == targetIsPresent, testMsg)
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
            self.UTILS.test.TEST(icon is not None, "MMS icon detected for thread [{}]".format(thread_name))

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

        self.UTILS.test.TEST(boolOK,
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

        self.UTILS.test.TEST(boolOK, "\"" + str(header) + "\" is the header in the SMS conversation.")
        return boolOK

    def checkThreadHeaderWithNameSurname(self, header):
        #
        # Verifies if a string is contained in the header
        #
        x = self.UTILS.element.getElement(DOM.Messages.message_header, "Header")

        boolOK = False

        if x.text == header:
                boolOK = True

        self.UTILS.test.TEST(boolOK, "\"" + header + "\" is the header in the SMS conversation.")
        return boolOK

    def clickSMSNotifier(self, num):
        #
        # Click new sms in the home page status bar notificaiton.
        #
        self.UTILS.reporting.logResult("info",
            "Clicking statusbar notification of new SMS from " + num + " ...")

        #
        # Switch to the 'home' frame to click the notifier.
        #
        self.marionette.switch_to_frame()
        self.UTILS.statusbar.displayStatusBar()

        x = (DOM.Messages.statusbar_new_sms[0],
            DOM.Messages.statusbar_new_sms[1].format(num))
        x = self.UTILS.element.getElement(x, "Statusbar notification for " + num)
        x.tap()

        #
        # Switch back to the messaging app.
        #
        self.UTILS.iframe.switchToFrame(*DOM.Messages.frame_locator)

        #
        # Wait for the message thread to finish loading.
        #
        self.UTILS.element.waitForElements(("xpath", "//h1[text()='" + num + "']"),
                                   "SMS thread header for " + str(num), True, 20)
        self.waitForReceivedMsgInThisThread()

    def click_wap_push_notifier(self, num):
        #
        # Click new WAP push in the home page status bar notification.
        #
        self.UTILS.reporting.logResult("info", "Clicking status bar notification of new WAPPush from " + num + " ...")

        #
        # Switch to the 'home' frame to click the notifier.
        #
        self.marionette.switch_to_frame()
        self.UTILS.statusbar.displayStatusBar()
        notif = (DOM.Messages.statusbar_new_sms[0], DOM.Messages.statusbar_new_sms[1].format(num))
        elem = self.UTILS.element.getElement(notif, "Status bar notification for " + num)
        elem.tap()

        #
        # Switch back to the messaging app.
        #
        time.sleep(5)
        self.marionette.switch_to_frame(self.apps.displayed_app.frame_id)

    def closeThread(self):
        #
        # Closes the current thread (returns you to the
        # 'thread list' SMS screen).
        #
        x = self.UTILS.element.getElement(DOM.Messages.header_back_button, "Back button")
        x.tap()
        self.UTILS.element.waitForElements(("xpath", "//h1[text()='{}']".format(_("Messages"))),
                                           "Messages main header")

    def countMessagesInThisThread(self):
        #
        # Returns the number of messages in this thread
        # (assumes you're already in the thread).
        #
        try:
            len(self.UTILS.element.getElements(DOM.Messages.message_list, "Messages"))
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

    def createAndSendMMS(self, attached_type, nums, m_text):

        self.gallery = Gallery(self)
        self.video = Video(self)
        self.music = Music(self)

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
        # self.addNumbersInToField([self.UTILS.general.get_os_variable("GLOBAL_TARGET_SMS_NUM")])
        self.addNumbersInToField(nums)

        #
        # Create MMS.
        #
        self.enterSMSMsg(m_text)

        if attached_type == "image":
            #
            # Add an image file
            #
            self.UTILS.general.addFileToDevice('./tests/_resources/80x60.jpg', destination='DCIM/100MZLLA')

            self.createMMSImage()
            self.gallery.clickThumbMMS(0)

            self.sendSMS()
        elif attached_type == "cameraImage":
            #
            # Add an image file from camera
            #
            self.createMMSCameraImage()
            time.sleep(3)
            self.sendSMS()
        elif attached_type == "video":
            #
            # Load an video file into the device.
            #
            self.UTILS.general.addFileToDevice('./tests/_resources/mpeg4.mp4', destination='/SD/mus')

            self.createMMSVideo()
            self.video.clickOnVideoMMS(0)
            self.sendSMS()
        elif attached_type == "audio":
            #
            # Load an video file into the device.
            #
            self.UTILS.general.addFileToDevice('./tests/_resources/AMR.amr', destination='/SD/mus')

            self.createMMSMusic()
            self.music.click_on_song_mms()

            self.sendSMS()
        else:
            # self.UTILS.reporting.logResult("info", "incorrect value received")
            msg = "FAILED: Incorrect parameter received in createAndSendMMS()"\
                ". attached_type must being image, video or audio."
            self.UTILS.test.quitTest(msg)

    def createAndSendSMS(self, nums, msg):
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
        self.sendSMS()

    def createMMSImage(self):

        attach = self.UTILS.element.getElement(DOM.Messages.attach_button, "Attach button")
        attach.tap()

        self.marionette.switch_to_frame()

        gallery = self.UTILS.element.getElement(DOM.Messages.mms_from_gallery, "From gallery")
        gallery.tap()

        self.UTILS.iframe.switchToFrame(*DOM.Gallery.frame_locator)

    def createMMSCameraImage(self):
        self.camera = Camera(self)

        attach = self.UTILS.element.getElement(DOM.Messages.attach_button, "Attach button")
        attach.tap()

        self.marionette.switch_to_frame()

        camera = self.UTILS.element.getElement(DOM.Messages.mms_from_camera, "From Camera")
        camera.tap()

        self.UTILS.iframe.switchToFrame(*DOM.Camera.frame_locator)

        #
        # Take a picture.
        #
        self.camera.takeAndSelectPicture()

        self.UTILS.iframe.switchToFrame(*DOM.Messages.frame_locator)

    def createMMSMusic(self):

        attach = self.UTILS.element.getElement(DOM.Messages.attach_button, "Attach button")
        attach.tap()

        self.marionette.switch_to_frame()

        music = self.UTILS.element.getElement(DOM.Messages.mms_from_music, "From music")
        music.tap()

        self.UTILS.iframe.switchToFrame(*DOM.Music.frame_locator)

    def createMMSVideo(self):

        attach = self.UTILS.element.getElement(DOM.Messages.attach_button, "Attach button")
        attach.tap()

        self.marionette.switch_to_frame()

        video = self.UTILS.element.getElement(DOM.Messages.mms_from_video, "From video")
        video.tap()

        self.UTILS.iframe.switchToFrame(*DOM.Video.frame_locator)

    def deleteAllThreads(self):
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
                self.deleteAllThreads()

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
        self.UTILS.test.TEST(expected_title in header, "Check that all desired threads have been selected")

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
        self.UTILS.test.TEST(x.text == msg,
                        "The text in the message area is as expected." + \
                        "|EXPECTED: '" + msg + "'" + \
                        "|ACTUAL  : '" + x.text + "'")

    def forwardMessage(self, msg_type, target_telNum):
        self.actions = Actions(self.marionette)

        #
        # Establish which phone number to use.
        #

        if msg_type == "sms":

            self.UTILS.reporting.logResult("info", "is a sms")
            #
            # Open sms option with longtap on it
            #
            self.UTILS.reporting.logResult("info", "Open sms option with longtap on it")
            sms = self.lastMessageInThisThread()
            body = self.marionette.find_element(*DOM.Messages.last_message_body, id=sms.id)
            self.actions.long_press(body, 2).perform()

            #
            # Press forward button
            #
            self.UTILS.reporting.logResult("info", "Clicking on forward button")
            x = self.UTILS.element.getElement(DOM.Messages.forward_btn_msg_opt, "Forward button is displayed")
            x.tap()

            #
            # Add a phone number.
            #
            self.addNumbersInToField([target_telNum])

            #
            # Send the sms.
            #
            self.UTILS.reporting.logResult("info", "Clicking on Send button")
            self.sendSMS()
        elif msg_type == "mms":

            self.UTILS.reporting.logResult("info", "is a mms")
            #
            # Open mms option with longtap on it
            #
            self.UTILS.reporting.logResult("info", "Open mms option with longtap on it")
            sms = self.lastMessageInThisThread()
            body = self.marionette.find_element(*DOM.Messages.last_message_body, id=sms.id)
            self.actions.long_press(body, 2).perform()

            #
            # Press forward button
            #
            self.UTILS.reporting.logResult("info", "Clicking on forward button")
            x = self.UTILS.element.getElement(DOM.Messages.forward_btn_msg_opt, "Forward button is displayed")
            x.tap()

            #
            # Add a phone number.
            #
            self.addNumbersInToField([target_telNum])

            #
            # Send the mms.
            #
            self.UTILS.reporting.logResult("info", "Clicking on Send button")

            #
            # Click send and wait for the message to be received
            #
            self.sendSMS()
        elif msg_type == "mmssub":

            self.UTILS.reporting.logResult("info", "is a mms with subject")

            #
            # Open mms option with longtap on it
            #
            self.UTILS.reporting.logResult("info", "Open mms with subject options with longtap on it")
            x = self.UTILS.element.getElement(DOM.Messages.received_mms_subject, "Target MMS field")
            self.actions.long_press(x, 2).perform()

            #
            # Press forward button
            #
            self.UTILS.reporting.logResult("info", "Clicking on forward button")
            x = self.UTILS.element.getElement(DOM.Messages.forward_btn_msg_opt, "Forward button is displayed")
            x.tap()

            #
            # Add a phone number.
            #
            self.addNumbersInToField([target_telNum])

            #
            # Send the mms.
            #
            self.UTILS.reporting.logResult("info", "Clicking on Send button")
            self.sendSMS()
        else:
            self.UTILS.reporting.logResult("info", "incorrect value received")
            self.UTILS.test.quitTest()

    def forwardMessageToContact(self, msg_type, contact_name):
        self.actions = Actions(self.marionette)
        self.contacts = Contacts(self)

        #
        # Establish which phone number to use.
        #

        if msg_type == "sms":

            self.UTILS.reporting.logResult("info", "is a sms")
            #
            # Open sms option with longtap on it
            #
            self.UTILS.reporting.logResult("info", "Open sms option with longtap on it")
            sms = self.lastMessageInThisThread()
            body = self.marionette.find_element(*DOM.Messages.last_message_body, id=sms.id)
            self.actions.long_press(body, 2).perform()

            #
            # Press forward button
            #
            self.UTILS.reporting.logResult("info", "Clicking on forward button")
            x = self.UTILS.element.getElement(DOM.Messages.forward_btn_msg_opt, "Forward button is displayed")
            x.tap()

            #
            # Add a phone number.
            #

            #
            # Search for our contact.
            #
            orig_iframe = self.selectAddContactButton()
            self.contacts.search(contact_name)
            self.contacts.check_search_results(contact_name)

            x = self.UTILS.element.getElements(DOM.Contacts.search_results_list, "Contacts search results")
            for i in x:
                if i.text == contact_name:
                    i.tap()
                    break

            #
            # Switch back to the sms iframe.
            #
            self.marionette.switch_to_frame()
            self.UTILS.iframe.switchToFrame("src", orig_iframe)

            #
            # Now check the correct name is in the 'To' list.
            #
            self.checkIsInToField(contact_name)

            #
            # Send the sms.
            #
            self.UTILS.reporting.logResult("info", "Clicking on Send button")
            self.sendSMS()
        elif msg_type == "mms":

            self.UTILS.reporting.logResult("info", "is a mms")
            #
            # Open mms option with longtap on it
            #
            self.UTILS.reporting.logResult("info", "Open mms option with longtap on it")
            sms = self.lastMessageInThisThread()
            body = self.marionette.find_element(*DOM.Messages.last_message_body, id=sms.id)
            self.actions.long_press(body, 2).perform()

            #
            # Press forward button
            #
            self.UTILS.reporting.logResult("info", "Clicking on forward button")
            x = self.UTILS.element.getElement(DOM.Messages.forward_btn_msg_opt, "Forward button is displayed")
            x.tap()

            #
            # Add a phone number.
            #

            #
            # Search for our contact.
            #
            orig_iframe = self.selectAddContactButton()
            self.contacts.search(contact_name)
            self.contacts.check_search_results(contact_name)

            x = self.UTILS.element.getElements(DOM.Contacts.search_results_list, "Contacts search results")
            for i in x:
                if i.text == contact_name:
                    i.tap()
                    break

            #
            # Switch back to the sms iframe.
            #
            self.marionette.switch_to_frame()
            self.UTILS.iframe.switchToFrame("src", orig_iframe)

            #
            # Now check the correct name is in the 'To' list.
            #
            self.checkIsInToField(contact_name)

            #
            # Send the mms.
            #
            self.UTILS.reporting.logResult("info", "Clicking on Send button")
            self.sendSMS()
        elif msg_type == "mmssub":

            self.UTILS.reporting.logResult("info", "is a mms with subject")

            #
            # Open mms option with longtap on it
            #
            self.UTILS.reporting.logResult("info",
                                    "Open mms with subject options with longtap on it")
            x = self.UTILS.element.getElement(DOM.Messages.received_mms_subject,
                                    "Target MMS field")
            self.actions.long_press(x, 2).perform()

            #
            # Press forward button
            #
            self.UTILS.reporting.logResult("info", "Clicking on forward button")
            x = self.UTILS.element.getElement(DOM.Messages.forward_btn_msg_opt,
                                          "Forward button is displayed")
            x.tap()

            #
            # Add a phone number.
            #

            #
            # Search for our contact.
            #
            orig_iframe = self.selectAddContactButton()
            self.contacts.search(contact_name)
            self.contacts.check_search_results(contact_name)

            x = self.UTILS.element.getElements(DOM.Contacts.search_results_list, "Contacts search results")
            for i in x:
                if i.text == contact_name:
                    i.tap()
                    break

            #
            # Switch back to the sms iframe.
            #
            self.marionette.switch_to_frame()
            self.UTILS.iframe.switchToFrame("src", orig_iframe)

            #
            # Now check the correct name is in the 'To' list.
            #
            self.checkIsInToField(contact_name)

            #
            # Send the mms.
            #
            self.UTILS.reporting.logResult("info", "Clicking on Send button")
            self.sendSMS()
        else:
            self.UTILS.reporting.logResult("info", "incorrect value received")
            self.UTILS.test.quitTest()

    def addContactToField(self, contact_name):
        self.actions = Actions(self.marionette)
        self.contacts = Contacts(self)

        self.UTILS.reporting.logResult("info", "is a sms")
        #
        # Create and send a new SMS.<br>
        # <b>Note:</b> The nums field must be an array of numbers
        # or contact names.
        #

        # self.startNewSMS()

        #
        # Search for our contact.
        #
        orig_iframe = self.selectAddContactButton()
        self.contacts.search(contact_name)
        self.contacts.check_search_results(contact_name)

        x = self.UTILS.element.getElements(DOM.Contacts.search_results_list, "Contacts search results")
        for i in x:
            if i.text == contact_name:
                i.tap()
                break

        #
        # Switch back to the sms iframe.
        #
        self.marionette.switch_to_frame()
        self.UTILS.iframe.switchToFrame("src", orig_iframe)

        #
        # Now check the correct name is in the 'To' list.
        #
        self.checkIsInToField(contact_name)

    def forwardMessageToMultipleRecipients(self, msg_type, target_telNum, contact_name):
        self.actions = Actions(self.marionette)
        self.contacts = Contacts(self)

        self.UTILS.iframe.switchToFrame(*DOM.Messages.frame_locator)
        if msg_type == "sms":

            self.UTILS.reporting.logResult("info", "is a sms")
            #
            # Open sms option with longtap on it
            #
            self.UTILS.reporting.logResult("info", "Open sms option with longtap on it")
            sms = self.lastMessageInThisThread()
            body = self.marionette.find_element(*DOM.Messages.last_message_body, id=sms.id)
            self.actions.long_press(body, 2).perform()

            #
            # Press forward button
            #
            self.UTILS.reporting.logResult("info", "Clicking on forward button")
            x = self.UTILS.element.getElement(DOM.Messages.forward_btn_msg_opt, "Forward button is displayed")
            x.tap()

            #
            # Add a phone number.
            #
            self.addNumbersInToField([target_telNum])

            #
            # Search for our contact.
            #
            orig_iframe = self.selectAddContactButton()
            self.contacts.search(contact_name)
            self.contacts.check_search_results(contact_name)

            x = self.UTILS.element.getElements(DOM.Contacts.search_results_list, "Contacts search results")
            for i in x:
                if i.text == contact_name:
                    i.tap()
                    break

            #
            # Switch back to the sms iframe.
            #
            self.marionette.switch_to_frame()
            self.UTILS.iframe.switchToFrame("src", orig_iframe)

            #
            # Now check the correct name is in the 'To' list.
            #
            self.checkIsInToField(contact_name)

            #
            # Send the sms.
            #
            self.UTILS.reporting.logResult("info", "Clicking on Send button")
            self.sendSMS()
        elif msg_type == "mms":

            self.UTILS.reporting.logResult("info", "is a mms")
            #
            # Open mms option with longtap on it
            #
            self.UTILS.reporting.logResult("info", "Open mms option with longtap on it")
            sms = self.lastMessageInThisThread()
            body = self.marionette.find_element(*DOM.Messages.last_message_body, id=sms.id)
            self.actions.long_press(body, 2).perform()

            #
            # Press forward button
            #
            self.UTILS.reporting.logResult("info", "Clicking on forward button")
            x = self.UTILS.element.getElement(DOM.Messages.forward_btn_msg_opt, "Forward button is displayed")
            x.tap()

            #
            # Add a phone number.
            #
            self.addNumbersInToField([target_telNum])

            #
            # Search for our contact.
            #
            orig_iframe = self.selectAddContactButton()
            self.contacts.search(contact_name)
            self.contacts.check_search_results(contact_name)

            x = self.UTILS.element.getElements(DOM.Contacts.search_results_list, "Contacts search results")
            for i in x:
                if i.text == contact_name:
                    i.tap()
                    break

            #
            # Switch back to the sms iframe.
            #
            self.marionette.switch_to_frame()
            self.UTILS.iframe.switchToFrame("src", orig_iframe)

            #
            # Now check the correct name is in the 'To' list.
            #
            self.checkIsInToField(contact_name)

            #
            # Send the mms.
            #
            self.UTILS.reporting.logResult("info", "Clicking on Send button")
            self.sendSMS()
        elif msg_type == "mmssub":

            self.UTILS.reporting.logResult("info", "is a mms with subject")

            #
            # Open mms option with longtap on it
            #
            self.UTILS.reporting.logResult("info",
                                    "Open mms with subject options with longtap on it")
            x = self.UTILS.element.getElement(DOM.Messages.received_mms_subject,
                                    "Target MMS field")
            self.actions.long_press(x, 2).perform()

            #
            # Press forward button
            #
            self.UTILS.reporting.logResult("info", "Clicking on forward button")
            x = self.UTILS.element.getElement(DOM.Messages.forward_btn_msg_opt,
                                          "Forward button is displayed")
            x.tap()

            #
            # Add a phone number.
            #
            self.addNumbersInToField([target_telNum])

            #
            # Search for our contact.
            #
            orig_iframe = self.selectAddContactButton()
            self.contacts.search(contact_name)
            self.contacts.check_search_results(contact_name)

            x = self.UTILS.element.getElements(DOM.Contacts.search_results_list, "Contacts search results")
            for i in x:
                if i.text == contact_name:
                    i.tap()
                    break

            #
            # Switch back to the sms iframe.
            #
            self.marionette.switch_to_frame()
            self.UTILS.iframe.switchToFrame("src", orig_iframe)

            #
            # Now check the correct name is in the 'To' list.
            #
            self.checkIsInToField(contact_name)

            #
            # Send the mms.
            #
            self.UTILS.reporting.logResult("info", "Clicking on Send button")
            self.sendSMS()
        else:
            self.UTILS.reporting.logResult("info", "incorrect value received")
            self.UTILS.test.quitTest()

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

    def lastMessageInThisThread(self):
        #
        # Returns an object of the last message in the current thread.
        #
        self.parent.wait_for_element_present(*DOM.Messages.last_message, timeout=20)
        return self.marionette.find_element(*DOM.Messages.last_message)

    def last_sent_message_timestamp(self):
        """Returns the timestamp of the last sent message
        """
        send_time = self.marionette.find_element(*DOM.Messages.last_sent_message).get_attribute("data-timestamp")
        return float(send_time) / 1000

    def openThread(self, num):
        #
        # Opens the thread for this number (assumes we're looking at the
        # threads in the messaging screen).
        #
        try:
            thread_el = ("xpath", DOM.Messages.thread_selector_xpath.format(num))
            x = self.UTILS.element.getElement(thread_el, "Message thread for " + num)
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
                    self.parent.wait_for_element_displayed("xpath", "//button[text()='{}']".format(_("Remove")),
                                                    timeout=2)
                    y = self.marionette.find_element("xpath", "//button[text()='{}']".format(_("Remove")))
                    self.UTILS.reporting.logResult("info", "Tapping 'Remove' button.")
                    y.tap()
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
        # Taps the 'add contact' button and switches to the
        # correct 'contacts' frame.<br>
        # Returns the "src" of the original iframe.
        #
        x = self.UTILS.element.getElement(DOM.Messages.add_contact_button, "Add contact button")
        x.tap()

        time.sleep(2)

        #
        # Switch to the contacts frame.
        #
        orig_iframe = self.UTILS.iframe.currentIframe()
        self.UTILS.iframe.switchToFrame(*DOM.Contacts.frame_locator)

        time.sleep(2)
        return orig_iframe

    def sendSMS(self):
        #
        # Just presses the 'send' button (assumes everything else is done).
        #
        sendBtn = self.UTILS.element.getElement(DOM.Messages.send_message_button, "Send sms button")
        sendBtn.tap()

        # (Give the spinner time to appear.)
        time.sleep(2)
        self.UTILS.element.waitForNotElements(DOM.Messages.message_sending_spinner, "'Sending' icon", True, 240)

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

    def timeOfLastMessageInThread(self):
        #
        # Returns the time of the last message in the current thread.
        #
        t = self.UTILS.element.getElement(DOM.Messages.last_message_time, "Last message time")
        return t.text

    def timeOfThread(self, num):
        #
        # Returns the time of a thread.
        #
        x = self.UTILS.element.getElement(("xpath", DOM.Messages.thread_timestamp_xpath.format(num)),
                                    "Thread time", True, 5, False)
        return x.text

    def thread_timestamp(self, num):
        #
        # Returns the timestamp of a thread
        #
        x = self.marionette.find_element(*DOM.Messages.last_message).get_attribute("data-timestamp")
        return float(x)

    def verifyMMSReceived(self, attached_type, sender_number):

        self.UTILS.iframe.switchToFrame(*DOM.Messages.frame_locator)
        self.openThread(sender_number)
        message = self.lastMessageInThisThread()
        self.UTILS.test.TEST(message, "A received message appeared in the thread.", True)

        self.UTILS.reporting.debug("*** attached type: {}".format(attached_type))
        if attached_type == "img":
            elem = DOM.Messages.last_message_attachment_img
        elif attached_type == "video":
            elem = DOM.Messages.last_message_attachment_av
        elif attached_type == "audio":
            elem = DOM.Messages.last_message_attachment_av
        else:
            # self.UTILS.reporting.logResult("info", "incorrect value received")
            msg = "FAILED: Incorrect parameter received in verifyMMSReceived()"\
                ". Attached_type must be image, video or audio."
            self.UTILS.test.quitTest(msg)

        self.UTILS.reporting.debug("*** searching for attachment type")
        last = self.UTILS.element.getElement(elem, "Last message")
        self.UTILS.element.scroll_into_view(last)
        typ = last.get_attribute("data-attachment-type")
        self.UTILS.reporting.debug("*** searching for attachment type Result: {}".format(typ))
        if typ != attached_type:
            msg = "Incorrect file type. The file must be {}, but is {} instead".format(attached_type, typ)
            self.UTILS.test.quitTest(msg)

    def waitForReceivedMsgInThisThread(self, send_time=None, timeOut=30):
        #
        # Waits for the last message in this thread to be a 'received' message
        # and returns the element for this message.
        #
        pollTime = 2
        pollReps = (timeOut / pollTime)
        lastEl = False

        for i in range(pollReps):
            # Get last message in this thread.
            x = self.lastMessageInThisThread()

            if not x:
                time.sleep(pollTime)
                continue

            # If the send_time timestamp is greater than this message's timestamp,it means the message
            # we expect has not arrived yet, so we have to wait a bit more.
            if send_time:
                message_data_time = float(x.get_attribute("data-timestamp")) / 1000
                fmt = "data-timestamp of last message in thread: {:.3f} send_time: {:.3f} --> {}"
                self.UTILS.reporting.debug(fmt.format(message_data_time, send_time, send_time > message_data_time))
                if send_time > message_data_time:
                    continue

            # Is this a received message?
            if "incoming" in x.get_attribute("class"):
                lastEl = x
                break

            # Nope - sleep then try again.
            time.sleep(pollTime)

        self.UTILS.test.TEST(lastEl,
                        "Last message in thread is a 'received' message within " + str(timeOut) + " seconds.")
        return lastEl
