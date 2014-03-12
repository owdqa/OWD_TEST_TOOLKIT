from OWDTestToolkit import DOM
from OWDTestToolkit.apps.video import Video
from OWDTestToolkit.apps.gallery import Gallery
from OWDTestToolkit.apps.music import Music

from marionette import Actions
import time

class Messages(object):
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
        self.UTILS.waitForNotElements(DOM.GLOBAL.loading_overlay, self.__class__.__name__ + " app - loading overlay")
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
            x = self.UTILS.screenShotOnErr()
            
            #
            # Even though we don't use the keyboard for putting the number in, 
            # we need it for the ENTER button (which allows us to put more than
            # one number in).
            #
            # So check that the keyboard appears when we tap the "TO" field if we have
            # more than one number.
            #
            if len(nums) > 1:
                self.UTILS.logResult("info", "Checking the keyboard appears when I tap the 'To' field ...")
                x = self.UTILS.getElement(DOM.Messages.target_numbers_empty, "Target number field")
                x.tap()
    
                boolKBD=False
                self.marionette.switch_to_frame()

                if n < 1:

                    try:
                        #
                        # A 'silent' check to see if the keyboard iframe appears.
                        elDef = ("xpath", 
                                "//iframe[contains(@{}, '{}')]".format(DOM.Keyboard.frame_locator[0],DOM.Keyboard.frame_locator[1]))
                        self.parent.wait_for_element_displayed(*elDef, timeout=2)
                        boolKBD = True
                    except:
                        boolKBD=False
                    
                    self.UTILS.TEST(boolKBD, "Keyboard is displayed when 'To' field is clicked.")
    
                self.UTILS.switchToFrame(*DOM.Messages.frame_locator)
            
            #
            # Seems okay, so proceed ...
            #
            if n == 0:

                self.UTILS.typeThis(DOM.Messages.target_numbers_empty,
                                    "Target number field",
                                    i,
                                    p_no_keyboard=True,
                                    p_validate=False,
                                    p_clear=False,
                                    p_enter=True)

            else:
                self.UTILS.typeThis(DOM.Messages.target_numbers_empty,
                                    "Target number field",
                                    i,
                                    p_no_keyboard=True,
                                    p_validate=False,
                                    p_clear=False,
                                    p_enter=False)
                x = self.UTILS.getElement(DOM.Messages.input_message_area, "Target number field")
                x.tap()

            n += 1

    def addSubject(self, subject):

        #
        # Press options button
        #
        self.UTILS.logResult("info", "Cliking on messages options button")
        x = self.UTILS.getElement(DOM.Messages.messages_options_btn, 
            "Messages option button is displayed")
        x.tap()

        #
        # Press add subject button
        #
        self.UTILS.logResult("info", "Cliking on add subject button")
        x = self.UTILS.getElement(DOM.Messages.addsubject_btn_msg_opt, 
            "add subject option button is displayed")
        x.tap()


        self.UTILS.typeThis(DOM.Messages.target_subject,
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
        x = self.UTILS.getElement(DOM.Messages.airplane_warning_message, 
                                    "Airplane mode warning message",
                                    True, 5, False)
        if x:
            self.UTILS.logResult("info", 
                                 "Warning message title detected = '" + x.text + "'.")
            
            x = self.UTILS.getElement(DOM.Messages.airplane_warning_ok, "OK button")
            x.tap()

    def checkIsInToField(self, target, targetIsPresent=True):
        #
        # Verifies if a number (or contact name) is
        # displayed in the "To: " field of a compose message.<br>
        # (Uses 'caseless' search for this.)
        #
        time.sleep(1)
        x = self.UTILS.getElements(DOM.Messages.target_numbers, "'To:' field contents", False)
        
        boolOK = False
        for i in x:
            if i.text.lower() == str(target).lower():
                boolOK = True
                break
        
        testMsg = "is" if targetIsPresent else "is not"
        testMsg = "\"" + str(target) + "\" " + testMsg + " in the 'To:' field."
        self.UTILS.TEST(boolOK == targetIsPresent, testMsg)
        return boolOK

    def checkMMSIcon(self):
        #
        # Checks for the presence of the MMS icon
        #
        x = self.UTILS.getElement(DOM.Messages.mms_icon, "MMS Icon", True, 5, False)
        if x:
            self.UTILS.logResult("info", "MMS icon detected")

    def checkNumberIsInToField(self, target):
        #
        # Verifies if a number is contained in the
        # "To: " field of a compose message (even if it's
        # not displayed - i.e. a contact name is displayed,
        # but this validates the <i>number</i> for that
        # contact).
        #
        x = self.UTILS.getElements(DOM.Messages.target_numbers, "'To:' field contents")
        
        boolOK = False
        for i in x:
            if i.get_attribute("data-number") == target:
                boolOK = True
                break
        
        self.UTILS.TEST(boolOK, 
            "\"" + str(target) + "\" is the number in one of the 'To:' field targets.")
        return boolOK
        
    def checkThreadHeader(self, header):
        #
        # Verifies if a string is contained in the header
        #
        x = self.UTILS.getElement(DOM.Messages.message_header, "Header")
        
        boolOK = False
        if x.get_attribute("data-number") == header:
                boolOK = True
        
        self.UTILS.TEST(boolOK, "\"" + str(header) + "\" is the header in the SMS conversation.")
        return boolOK

    def clickSMSNotifier(self, num):
        #
        # Click new sms in the home page status bar notificaiton.
        #
        self.UTILS.logResult("info", 
            "Clicking statusbar notification of new SMS from " + num + " ...")

        #
        # Switch to the 'home' frame to click the notifier.
        #
        self.marionette.switch_to_frame()
        self.UTILS.displayStatusBar()

        x = (DOM.Messages.statusbar_new_sms[0],
            DOM.Messages.statusbar_new_sms[1].format(num))
        x = self.UTILS.getElement(x, "Statusbar notification for " + num)
        x.tap()

        #
        # Switch back to the messaging app.
        #
        self.UTILS.switchToFrame(*DOM.Messages.frame_locator)
        
        #
        # Wait for the message thread to finish loading.
        #
        self.UTILS.waitForElements(("xpath", "//h1[text()='" + num + "']"), 
                                   "SMS thread header for " + str(num), True, 20)
        self.waitForReceivedMsgInThisThread()

    def closeThread(self):
        #
        # Closes the current thread (returns you to the
        # 'thread list' SMS screen).
        #
        x = self.UTILS.getElement(DOM.Messages.header_back_button, "Back button")
        x.tap()
        
        self.UTILS.waitForElements(("xpath", "//h1[text()='Messages']"), "Messages main header")

    def countMessagesInThisThread(self):
        #
        # Returns the number of messages in this thread
        # (assumes you're already in the thread).
        #
        return len(self.UTILS.getElements(DOM.Messages.message_list, "Messages"))

    def createAndSendMMS(self, attached_type, m_text):

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
        self.addNumbersInToField([self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM")])

        #
        # Create MMS.
        #
        self.enterSMSMsg(m_text)

        if attached_type == "image":
            #
            # Add an image file
            #
            self.UTILS.addFileToDevice('./tests/_resources/80x60.jpg', destination='DCIM/100MZLLA')

            self.createMMSImage()
            self.gallery.clickThumbMMS(0)

            #
            # Click send and wait for the message to be received
            #
            self.sendSMS()
            time.sleep(5)

            #
            # Obtaining file attached type
            #
            x = self.UTILS.getElement(DOM.Messages.attach_preview_img_type, "preview type")
            type = x.get_attribute("data-attachment-type")


            if type != "img":
                self.UTILS.quitTest("Incorrect file type. The file must be img ")

        elif attached_type == "video":
            #
            # Load an video file into the device.
            #
            self.UTILS.addFileToDevice('./tests/_resources/mpeg4.mp4', destination='/SD/mus')

            self.createMMSVideo()
            self.video.clickOnVideoMMS(0)
            self.sendSMS()


            #
            # Obtaining file attached type
            #
            x = self.UTILS.getElement(DOM.Messages.attach_preview_video_audio_type, "preview type")
            type = x.get_attribute("data-attachment-type")

            if type != "video":
                self.UTILS.quitTest("Incorrect file type. The file must be video")

        elif attached_type == "audio":
            #
            # Load an video file into the device.
            #
            self.UTILS.addFileToDevice('./tests/_resources/AMR.amr', destination='/SD/mus')

            self.createMMSMusic()
            self.music.click_on_song_mms()

            #
            # Click send and wait for the message to be received
            #
            self.sendSMS()
            time.sleep(5)


            #
            # Obtaining file attached type
            #
            x = self.UTILS.getElement(DOM.Messages.attach_preview_video_audio_type, "preview type")
            type = x.get_attribute("data-attachment-type")

            if type != "audio":
                self.UTILS.quitTest("Incorrect file type. The file must be audio ")

        else:
            # self.UTILS.logResult("info", "incorrect value received")
            msg = "FAILED: Incorrect parameter received in createAndSendMMS()"\
                ". attached_type must being image, video or audio."
            self.UTILS.quitTest(msg)

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
        # The header should now say how many receipients.
        #
        time.sleep(2) # give the header time to change.
        
        num_recs = len(nums)
        search_str = " recipient" if num_recs == 1 else " recipients"
        self.UTILS.headerCheck(str(num_recs) + search_str)

        #
        # Send the message.
        #
        self.sendSMS()

    def createMMSImage(self):

        attach = self.UTILS.getElement(DOM.Messages.attach_button, "Attach button")
        attach.tap()

        self.marionette.switch_to_frame()

        gallery = self.UTILS.getElement(DOM.Messages.mms_from_gallery, "From gallery")
        gallery.tap()

        self.UTILS.switchToFrame(*DOM.Gallery.frame_locator)

    def createMMSMusic(self):

        attach = self.UTILS.getElement(DOM.Messages.attach_button, "Attach button")
        attach.tap()

        self.marionette.switch_to_frame()

        music = self.UTILS.getElement(DOM.Messages.mms_from_music, "From music")
        music.tap()

        self.UTILS.switchToFrame(*DOM.Music.frame_locator)

    def createMMSVideo(self):

        attach = self.UTILS.getElement(DOM.Messages.attach_button, "Attach button")
        attach.tap()

        self.marionette.switch_to_frame()

        video = self.UTILS.getElement(DOM.Messages.mms_from_video, "From video")
        video.tap()

        self.UTILS.switchToFrame(*DOM.Video.frame_locator)

    def deleteAllThreads(self):
        #
        # Deletes all threads (assumes the messagin app is already open).
        #
        try:
            self.parent.wait_for_element_displayed(*DOM.Messages.no_threads_message, timeout=2)
            x = self.marionette.find_element(*DOM.Messages.no_threads_message)
            if x.is_displayed():
                self.UTILS.logResult("info", "(No message threads to delete.)")
        except:
            self.UTILS.logResult("info", "Deleting message threads ...")
 
            x = self.threadEditModeON()
            x = self.UTILS.getElement(DOM.Messages.check_all_threads_btn, 
                                        "Select all button")
            x.tap()
             
            self.deleteSelectedThreads()
            self.UTILS.waitForElements(DOM.Messages.no_threads_message, 
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
            x= self.UTILS.getElement(DOM.Messages.edit_messages_icon, "Edit button")
            x.tap()

            #
            # Go into message edit mode..
            #
            x= self.UTILS.getElement(DOM.Messages.delete_messages_btn, "Edit button")
            x.tap()

            #
            # Press select all button.
            #
            x = self.UTILS.getElement(DOM.Messages.check_all_messages_btn, 
                                        "'Select all' button")
            x.tap()
            
        self.deleteSelectedMessages()

    def deleteSelectedMessages(self):
        #
        # Delete the currently selected messages in this thread.
        #
        x= self.UTILS.getElement(DOM.Messages.edit_msgs_delete_btn, 
                                    "Delete message" )
        x.tap()

        #
        # Press OK button to confirm. OK button is displayed on top_level frame.
        #
        self.marionette.switch_to_frame()
        x = self.UTILS.getElement(DOM.Messages.delete_messages_ok_btn, 
                                    "OK button in question dialog")
        x.tap()

        #self.UTILS.switchToFrame(*DOM.Messages.frame_locator)
        time.sleep(2)

    def deleteSelectedThreads(self):
        #
        # Delete the currently selected message threads.
        #
        orig_iframe = self.UTILS.currentIframe()
        x = self.UTILS.getElement(DOM.Messages.delete_threads_button, 
                                    "Delete threads button")
        x.tap()
        
        time.sleep(2)
        self.marionette.switch_to_frame()
        x = self.UTILS.getElement(DOM.Messages.delete_messages_ok_btn, 
                                    "OK button in question dialog")
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
                self.UTILS.logResult("info", "(No message threads to delete.)")
                
                #
                # Without this 'return' the code actually tries to do the 'else:' part
                # too!!
                #
                return
        except:
            self.UTILS.logResult("info", "Deleting message threads ...")
            if target_array:
                self.editAndSelectThreads(target_array)
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
        x= self.UTILS.getElement(DOM.Messages.edit_messages_icon, "Edit button" )
        x.tap()

        #
        # Go into message edit mode..
        #
        x= self.UTILS.getElement(DOM.Messages.delete_messages_btn, "Edit button")
        x.tap()
        
        #
        # Check the messages (for some reason, just doing x[i].click() doesn't
        # work for element zero, so I had to do this 'longhanded' version!).
        #
        x = self.UTILS.getElements(DOM.Messages.message_list, "Messages")
        y = 0
        for i in x:
            if y in msg_array:
                self.UTILS.logResult("info", "Selecting message " + str(y) + " ...")
                i.click()
            y += 1

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
        x= self.threadEditModeON()
        
        #
        # Check the messages (for some reason, just doing x[i].click() doesn't
        # work for element zero, so I had to do this 'longhanded' version!).
        #
        for i in target_array:
            x = self.UTILS.getElement(("xpath", 
                                       DOM.Messages.thread_selector_xpath.format(i)),
                                      "Thread checkbox for '" + i + "'")
            x.click()

    def enterSMSMsg(self, msg, not_keyboard=True):
        #
        # Create and send a message (assumes we are in a new 'create new message'
        # screen with the destination number filled in already).
        #
        time.sleep(1) # Trying to remove an intermittent issue.
        self.UTILS.typeThis(DOM.Messages.input_message_area, 
                            "Input message area",
                            msg,
                            p_no_keyboard=not_keyboard,
                            p_clear=False,
                            p_enter=False,
                            p_validate=False) # it's the text() of this field, not the value.
        
        #
        # Validate the field.
        #
        x = self.UTILS.getElement(DOM.Messages.input_message_area, 
                                    "Input message area (for validation)")
        self.UTILS.TEST(x.text == msg, 
                        "The text in the message area is as expected." + \
                        "|EXPECTED: '" + msg + "'" + \
                        "|ACTUAL  : '" + x.text + "'")

    def fordwardMessage(self, msg_type, target_telNum):
        self.actions = Actions(self.marionette)

        #
        # Establish which phone number to use.
        #

        if msg_type == "sms":

            self.UTILS.logResult("info", "is a sms")
            #
            # Open sms option with longtap on it
            #
            self.UTILS.logResult("info", "Open sms option with longtap on it")
            x = self.UTILS.getElement(DOM.Messages.received_sms, "Target sms field")
            self.actions.long_press(x, 2).perform()

            #
            # Press fordward button
            #
            self.UTILS.logResult("info", "Cliking on fordward button")
            x = self.UTILS.getElement(DOM.Messages.fordward_btn_msg_opt, 
                                          "Fordward button is displayed")
            x.tap()

            #
            # Add a phone number.
            #
            self.addNumbersInToField([target_telNum])

            #
            # Send the sms.
            #
            self.UTILS.logResult("info", "Cliking on Send button")
            x = self.UTILS.getElement(DOM.Messages.send_message_button, 
                                          "Send button is displayed")
            x.tap()

            #
            # Wait for the last message in this thread to be a 'recieved' one.
            #
            returnedSMS = self.waitForReceivedMsgInThisThread()
            self.UTILS.TEST(returnedSMS, 
                              "A receieved message appeared in the thread.", True)


        elif msg_type == "mms":

            self.UTILS.logResult("info", "is a mms")
            #
            # Open mms option with longtap on it
            #
            self.UTILS.logResult("info", "Open mms option with longtap on it")
            x = self.UTILS.getElement(DOM.Messages.received_mms, "Target mms field")
            self.actions.long_press(x, 2).perform()

            #
            # Press fordward button
            #
            self.UTILS.logResult("info", "Cliking on fordward button")
            x = self.UTILS.getElement(DOM.Messages.fordward_btn_msg_opt, 
                                          "Fordward button is displayed")
            x.tap()

            #
            # Add a phone number.
            #
            self.addNumbersInToField([target_telNum])

            #
            # Send the mms.
            #
            self.UTILS.logResult("info", "Cliking on Send button")
            x = self.UTILS.getElement(DOM.Messages.send_message_button, 
                                          "Send button is displayed")
            x.tap()


            #
            # Click send and wait for the message to be received
            #
            self.sendSMS()

            #
            # This step is necessary because our sim cards receive mms with +XXX
            #
            x = self.UTILS.getElement(DOM.Messages.header_back_button, "Back button")
            x.tap()

            self.openThread("+" + self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM"))

            #
            # Wait for the last message in this thread to be a 'recieved' one.
            #
            returnedSMS = self.waitForReceivedMsgInThisThread()
            self.UTILS.TEST(returnedSMS, 
                              "A receieved message appeared in the thread.", True)

        elif msg_type == "mmssub":

            self.UTILS.logResult("info", "is a mms with subject")

            #
            # Open mms option with longtap on it
            #
            self.UTILS.logResult("info", 
                                    "Open mms with subject options with longtap on it")
            x = self.UTILS.getElement(DOM.Messages.received_mms_subject, 
                                    "Target MMS field")
            self.actions.long_press(x, 2).perform()


            #
            # Press fordward button
            #
            self.UTILS.logResult("info", "Cliking on fordaward button")
            x = self.UTILS.getElement(DOM.Messages.fordward_btn_msg_opt, 
                                          "Fordward button is displayed")
            x.tap()


            #
            # Add a phone number.
            #
            self.addNumbersInToField([target_telNum])

            #
            # Send the mms.
            #
            self.UTILS.logResult("info", "Cliking on Send button")
            x = self.UTILS.getElement(DOM.Messages.send_message_button, 
                                          "Send button is displayed")
            x.tap()


            #
            # Click send and wait for the message to be received
            #
            self.sendSMS()

            #
            # This step is necessary because our sim cards receive mms with +XXX
            #
            x = self.UTILS.getElement(DOM.Messages.header_back_button, "Back button")
            x.tap()

            self.openThread("+" + self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM"))

            #
            # Wait for the last message in this thread to be a 'recieved' one.
            #
            returnedSMS = self.waitForReceivedMsgInThisThread()
            self.UTILS.TEST(returnedSMS, 
                              "A receieved message appeared in the thread.", True)

        else:
            self.UTILS.logResult("info", "incorrect value received")
            self.UTILS.quitTest()

    def getThreadText(self, num):
        #
        # Returns the preview text for the thread for this number (if it exists),
        # or False if either the thread doesn't exist or can't be found.
        #
        if self.threadExists(num):
            x = self.UTILS.getElements(DOM.Messages.threads_list, "Threads")
            
            for thread in x:
                try:
                    y = thread.find_element("xpath", ".//p[text()='{}']".format(num))
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
        x = self.UTILS.getElement(DOM.Messages.message_header, "Thread header")
        x.tap()
        
        x = self.UTILS.getElement(DOM.Messages.header_add_to_contact_btn, 
                                    "'Add to an existing contact' button")
        x.tap()
        
        #
        # Switch to correct iframe.
        #
        self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)

    def header_call(self):
        #
        # Taps the header and tries to tap the 'send message' button.
        # - Assumes we are looking at a message thread already.
        # - Leaves you in the correct iframe to continue.
        #
        x = self.UTILS.getElement(DOM.Messages.message_header, "Thread header")
        x.tap()

        #
        # If we tapped this from a contact header then we will already be in the
        # dialer so this won't be necessary.
        #

        #
        # Select dialer option.
        #
        x = self.UTILS.getElement(DOM.Messages.header_call_btn, "'Call' button")
        x.tap()

        #
        # Switch to correct iframe.
        #
        self.UTILS.switchToFrame(*DOM.Dialer.frame_locator)

    def header_createContact(self):
        #
        # Taps the header and tries to tap the 'send message' button.
        # - Assumes we are looking at a message thread already.
        # - Leaves you in the correct iframe to continue.
        #
        x = self.UTILS.getElement(DOM.Messages.message_header, "Thread header")
        x.tap()
        
        x = self.UTILS.getElement(DOM.Messages.header_create_new_contact_btn, 
                                    "'Create new contact' button")
        x.tap()
        
        #
        # Switch to correct iframe.
        #
        self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)

    def header_sendMessage(self):
        #
        # Taps the header and tries to tap the 'send message' button.
        # - Assumes we are looking at a message thread already.
        # - Leaves you in the correct iframe to continue.
        #
        x = self.UTILS.getElement(DOM.Messages.message_header, "Thread header")
        x.tap()
        
        x = self.UTILS.getElement(DOM.Messages.header_send_message_btn, "'Send message' button")
        x.tap()

    def lastMessageInThisThread(self):
        #
        # Returns an object of the last message in the current thread.
        #
        time.sleep(5)
        # try:
        self.parent.wait_for_element_present(*DOM.Messages.message_list, timeout=20)
        x = self.marionette.find_elements(*DOM.Messages.message_list)
        
        if len(x) > 1:
            return x[-1]
        else:
            return x[0]
        # except:
            # return False

    def openThread(self, num):
        #
        # Opens the thread for this number (assumes we're looking at the
        # threads in the messaging screen).
        #
        try:
            thread_el = ("xpath", DOM.Messages.thread_selector_xpath.format(num))
            x = self.UTILS.getElement(thread_el,"Message thread for " + num)
            
            x.tap()
            
            self.UTILS.waitForElements(DOM.Messages.send_message_button, "'Send' button")
        except:
            x = self.UTILS.screenShotOnErr()
            msg = "<b>NOTE:</b> The thread <i>may</i> have failed to open."
            self.UTILS.logResult("info", msg, x)

    def readLastSMSInThread(self):
        #
        # Read last message in the current thread.
        #
        received_message = self.UTILS.getElements(DOM.Messages.received_messages,
                                                     "Received messages")[-1]
        return str(received_message.text)

    def readNewSMS(self, fromNum):
        #
        # Read and return the value of the new message received from number.
        #
        x = self.UTILS.getElement(("xpath", DOM.Messages.messages_from_num.format(fromNum)),
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
        x = self.UTILS.getElements(DOM.Messages.target_numbers, "'To:' field contents")
        
        x_pos = 0
        for i in range(0, len(x)):
            self.UTILS.logResult("info", 
                                "Checking target '{}' to '{}' ...".format(x[i].text, target))

            if x[i].text.lower() == target.lower():
                self.UTILS.logResult("info", "Tapping contact '" + target + "' ...")
                x[i].tap()
                
                try:
                    #
                    # This contact was added via 'add contact' icon.
                    #
                    self.parent.wait_for_element_displayed("xpath", "//button[text()='Remove']",
                                                    timeout=2)
                    y = self.marionette.find_element("xpath", "//button[text()='Remove']")
                    self.UTILS.logResult("info", "Tapping 'Remove' button.")
                    y.tap()
                    return True
                except:
                    #
                    # This contact was manually entered.
                    #
                    z = self.UTILS.getElements(DOM.Messages.target_numbers, 
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
        x = self.UTILS.getElement(DOM.Messages.add_contact_button, "Add contact button")
        x.tap()
        
        time.sleep(2)
        
        #
        # Switch to the contacts frame.
        #
        orig_iframe = self.UTILS.currentIframe()
        self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)
        
        time.sleep(2)
        return orig_iframe

    def sendSMS(self):
        #
        # Just presses the 'send' button (assumes everything else is done).
        #
        sendBtn = self.UTILS.getElement(DOM.Messages.send_message_button, 
                                        "Send sms button")
        sendBtn.tap()

        time.sleep(2) # (Give the spinner time to appear.)
        self.UTILS.waitForNotElements(DOM.Messages.message_sending_spinner, 
                                        "'Sending' icon", True, 120)

        #
        # Check if we received the 'service unavailable' message.
        #
        try:
            self.parent.wait_for_element_displayed(*DOM.Messages.service_unavailable_msg,
                                            timeout=2)
            x = self.UTILS.screenShotOnErr()
            msg = "'Service unavailable' message detected - unable to send sms!"
            self.UTILS.logResult("info", msg, x)
            return False
        except:
            pass

        return True

    def startNewSMS(self):
        #
        # Starts a new sms (doesn't fill anything in).
        # Assumes the Messaging app is already launched.
        #
        newMsgBtn = self.UTILS.getElement(DOM.Messages.create_new_message_btn,
                                             "Create new message button")
        newMsgBtn.tap()

    def threadCarrier(self):
        #
        # Returns the 'carrier' being used by this thread.
        #
        x = self.UTILS.getElement(DOM.Messages.type_and_carrier_field,
                                     "Type and carrier information")
        return x.text.split("|")[1].strip()

    def threadEditModeOFF(self):
        #
        # Turns off Edit mode while in the SMS threads screen.
        #
        x = self.UTILS.getElement(DOM.Messages.cancel_edit_threads, "Cancel button")
        x.tap()
        self.UTILS.waitForElements(DOM.Messages.edit_threads_button, "Edit button")

    def threadEditModeON(self):
        #
        # Turns on Edit mode while in the SMS threads screen.
        #
        x= self.UTILS.getElement(DOM.Messages.edit_threads_button, "Edit button")
        x.tap()
        self.UTILS.waitForElements(DOM.Messages.cancel_edit_threads, "Cancel button")

    def threadExists(self, num):
        #
        # Verifies that a thread exists for this number (returns True or False).
        #
        boolOK=False
        try:
            self.parent.wait_for_element_present("xpath", 
                                    DOM.Messages.thread_selector_xpath.format(num), 1)
            boolOK=True
        except:
            boolOK=False
            
        return boolOK

    def threadType(self):
        #
        # Returns the 'type' being used by this thread.
        #
        x = self.UTILS.getElement(DOM.Messages.type_and_carrier_field,
                                    "Type and carrier information")
        return x.text.split("|")[0].strip()

    def timeOfLastMessageInThread(self):
        #
        # Returns the time of the last message in the current thread.
        #
        time.sleep(2)
        x = self.UTILS.getElements(DOM.Messages.message_timestamps, "Message timestamps")
        return x[-1].text

    def timeOfThread(self, num):
        #
        # Returns the time of a thread.
        #
        x = self.UTILS.getElement(("xpath", 
                                    DOM.Messages.thread_timestamp_xpath.format(num)), 
                                    "Thread timestamp",
                                    True, 5, False)
        return x.text

    def verifyMMSReceived(self, attached_type):

        if attached_type == "image":
            self._verify(DOM.Messages.attach_preview_img_type, "img")

        elif attached_type == "video":
            self._verify(DOM.Messages.attach_preview_video_audio_type, attached_type)

        elif attached_type == "audio":
            self._verify(DOM.Messages.attach_preview_video_audio_type, attached_type)

        else:
            #self.UTILS.logResult("info", "incorrect value received")
            msg = "FAILED: Incorrect parameter received in verifyMMSReceived()"\
                ". attached_type must being image, video or audio."
            self.UTILS.quitTest(msg)

    def _verify(self, DOM_elem, attached_type):
        #
        # This step is necessary because our sim cards receive mms with +XXX
        #
        x = self.UTILS.getElement(DOM.Messages.header_back_button, "Back button")
        x.tap()

        self.openThread("+" + self.UTILS.get_os_variable("GLOBAL_TARGET_SMS_NUM"))

        #
        # Wait for the last message in this thread to be a 'recieved' one.
        #
        returnedSMS = self.waitForReceivedMsgInThisThread()
        self.UTILS.TEST(returnedSMS, "A received message appeared in the thread.", True)

        #
        # Obtaining file attached type
        #
        x = self.UTILS.getElement(DOM_elem, "preview type")
        type = x.get_attribute("data-attachment-type")

        if type != attached_type:
            msg = "Incorrect file type. The file must be {}".format(attached_type)
            self.UTILS.quitTest(msg)

    def waitForNewSMSPopup_by_msg(self, msg):
        #
        # Waits for a new SMS popup notification which
        # matches this 'msg' string.
        #
        myIframe = self.UTILS.currentIframe()

        self.marionette.switch_to_frame()
        x = (DOM.Messages.new_sms_popumsg[0], DOM.Messages.new_sms_popumsg[1].format(msg))
        self.UTILS.waitForElements(x,
                                    "Popup message saying we have a new sms containing '" + msg + "'",
                                    True,
                                    30)

        self.UTILS.switchToFrame("src", myIframe)

    def waitForNewSMSPopup_by_number(self, num):
        #
        # Waits for a new SMS popup notification which
        # is from this 'num' number.
        #
        myIframe = self.UTILS.currentIframe()
        
        self.marionette.switch_to_frame()
        x = (DOM.Messages.new_sms_popunum[0], DOM.Messages.new_sms_popunum[1].format(str(num)))
        self.UTILS.waitForElements(x,
                                    "Popup message saying we have a new sms from " + str(num),
                                    True,
                                    30)

        self.UTILS.switchToFrame("src", myIframe)

    def waitForReceivedMsgInThisThread(self, timeOut=30):
        #
        # Waits for the last message in this thread to be a 'received' message
        # and returns the element for this message.
        #
        pollTime = 2
        pollReps = (timeOut / pollTime)
        lastEl = False

        for i in range(1, pollReps):
            # Get last message in this thread.
            x = self.lastMessageInThisThread()

            if not x:
                time.sleep(pollTime)
                continue
            
            # Is this a received message?
            if "incoming" in x.get_attribute("class"):
                lastEl = x
                break
            
            # Nope - sleep then try again.
            time.sleep(pollTime)
        
        self.UTILS.TEST(lastEl,
                        "Last message in thread is a 'received' message within " + str(timeOut) + " seconds.")
        return lastEl

    def waitForSMSNotifier(self, num, p_timeout=40):
        #
        # Get the element of the new SMS from the status bar notification.
        #
        self.UTILS.logResult("info",
                    "Waiting for statusbar notification of new SMS from " + num + " ...")

        #
        # Create the string to wait for.
        #
        x=(DOM.Messages.statusbar_new_sms[0],
            DOM.Messages.statusbar_new_sms[1].format(num))
        
        #
        # Wait for the notification to be present for this number 
        # in the popup messages (this way we make sure it's coming from our number,
        # as opposed to just containing our number in the notification).
        #
        time.sleep(5)
        x = self.UTILS.waitForStatusBarNew(x, p_displayed=False, p_timeOut=p_timeout)

        self.UTILS.logResult(x, "SMS notifier from " + num + " found in status bar.")
        return x