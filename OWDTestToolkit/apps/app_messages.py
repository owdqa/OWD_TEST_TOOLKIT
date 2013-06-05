import time
from gaiatest   import GaiaTestCase
from marionette import Marionette
from OWDTestToolkit import *

class AppMessages(GaiaTestCase):
    
    #
    # When you create your instance of this class, include the
    # "self" object so we can access the calling class' objects.
    #
    def __init__(self, p_parent):
        self.apps       = p_parent.apps
        self.data_layer = p_parent.data_layer
        self.marionette = p_parent.marionette
        self.UTILS      = p_parent.UTILS



    def launch(self):
        #
        # Launch the app.
        #
        self.apps.kill_all()
        self.app = self.apps.launch('Messages')
        self.UTILS.waitForNotElements(DOM.GLOBAL.loading_overlay, "Messages app - loading overlay", False);
        
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
        self.marionette.switch_to_frame()
        
        self.UTILS.switchToFrame(DOM.Contacts.frame_locator[0],
                                 DOM.Contacts.frame_locator[1] + "?pick")
        
        return orig_iframe
        
    def addContactToThisSMS(self, p_contactName):
        #
        # Uses the 'add contact' button to add a contact to SMS.
        #
        self.UTILS.logResult("info", "Trying to add '" + p_contactName  + "' to the SMS via search button ...")
        
        orig_iframe = self.selectAddContactButton()
        
        #
        # Search the contacts list for our contact.
        #
        x = self.UTILS.getElements(DOM.Contacts.view_all_contact_list, "Contacts list")
        for i in x:
            if i.text.lower() == p_contactName.lower():
                i.tap()
                break
            
        self.marionette.switch_to_frame()
        self.UTILS.switchToFrame("src",orig_iframe)
        
        #
        # Now check the correct name is in the 'To' list.
        #
        return self.checkIsInToField(p_contactName)

    def enterSMSMsg(self, p_msg, p_not_keyboard=True):
        #
        # Create and send a message (assumes we are in a new 'create new message'
        # screen with the destination number filled in already).
        #
        self.UTILS.typeThis(DOM.Messages.input_message_area, 
                            "Input message area",
                            p_msg,
                            p_no_keyboard=p_not_keyboard,
                            p_clear=False,
                            p_enter=False,
                            p_validate=False) # it's the text() of this field, not the value.
        
        #
        # Validate the field.
        #
        x = self.UTILS.getElement(DOM.Messages.input_message_area, "Input message area (for validation)")
        self.UTILS.TEST(x.text == p_msg, 
                        "The text in the message area is as expected." + \
                        "|EXPECTED: '" + p_msg + "'" + \
                        "|ACTUAL  : '" + x.text + "'")
    
    def sendSMS(self):
        #
        # Just presses the 'send' button (assumes everything else is done).
        #
        sendBtn = self.UTILS.getElement(DOM.Messages.send_message_button, "Send sms button")
        sendBtn.click()
        
        time.sleep(2) # (Give the spinner time to appear.)
        self.UTILS.waitForNotElements(DOM.Messages.message_sending_spinner, "'Sending' icon", True, 120)

    def openThread(self, p_receipient):
        #
        # Open a specific message thread.
        #
        x = self.UTILS.getElements(DOM.Messages.threads, "Threads")
        for i in x:
            if i.text == p_receipient:
                i.tap()
                self.UTILS.waitForElements(("xpath", "//h1[text()='" + p_receipient + "']"), "Thread header")
                return True
        
        return False
    
    def closeThread(self):
        #
        # Closes the current thread (returns you to the
        # 'thread list' SMS screen).
        #
        x = self.UTILS.getElement(DOM.Messages.header_back_button, "Back button")
        x.tap()
        
        self.UTILS.waitForElements(("xpath", "//h1[text()='Messages']"), "Messages main header")
    
    def deleteMessagesInThisThread(self, p_msg_array=False):
        #
        # Enters edit mode, selects the required messages and
        # deletes them.<br>
        # p_msg_array is an array of numbers. 
        # If it's not specified then all messages in this 
        # thread will be deleted.
        #
        if p_msg_array:
            self.editAndSelectMessages(p_msg_array)
        else:
            x= self.UTILS.getElement(DOM.Messages.edit_messages_icon, "Edit button" )
            x.tap()
            
            x = self.UTILS.getElement(DOM.Messages.check_all_messages_btn, "'Select all' button")
            x.tap()
            
        self.deleteSelectedMessages()
        
    def threadEditModeON(self):
        #
        # Turns on Edit mode while in the SMS threads screen.
        #
        x= self.UTILS.getElement(DOM.Messages.edit_threads_button, "Edit button" )
        x.tap()
        self.UTILS.waitForElements(DOM.Messages.cancel_edit_threads, "Cancel button")
        
    def threadEditModeOFF(self):
        #
        # Turns off Edit mode while in the SMS threads screen.
        #
        x= self.UTILS.getElement(DOM.Messages.cancel_edit_threads, "Cancel button" )
        x.tap()
        self.UTILS.waitForElements(DOM.Messages.edit_threads_button, "Edit button")
        
    def editAndSelectMessages(self, p_msg_array):
        #
        # Puts this thread into Edit mode and selects
        # the messages listed in p_msg_array.<br>
        # p_msg_array is an array of numbers.
        #
        
        #
        # Go into message edit mode..
        #
        x= self.UTILS.getElement(DOM.Messages.edit_messages_icon, "Edit button" )
        x.tap()
        
        #
        # Check the messages (for some reason, just doing x[i].click() doesn't
        # work for element zero, so I had to do this 'longhanded' version!).
        #
        x = self.UTILS.getElements(DOM.Messages.thread_messages, "Messages")
        y = 0
        for i in x:
            if y in p_msg_array:
                self.UTILS.logResult("info", "Selecting message " + str(y) + " ...")
                i.click()
            
            y = y + 1
        
    def deleteThreads(self, p_target_array=False):
        #
        # Enters edit mode, selects the required messages and
        # deletes them.<br>
        # p_target_array is an array of target numbers 
        # or contacts which identify the threads to be selected.
        # If it's not specified then all messages in this 
        # thread will be deleted.
        #
        if p_target_array:
            self.editAndSelectThreads(p_target_array)
            self.deleteSelectedThreads()
        else:
            self.deleteAllThreads()
            
    def editAndSelectThreads(self, p_target_array):
        #
        # Puts this thread into Edit mode and selects
        # the messages listed in p_msg_array.<br>
        # p_target_array is an array of target numbers 
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
        for i in p_target_array:
            x = self.UTILS.getElement(("xpath", 
                                       DOM.Messages.thread_selector_xpath % i),
                                      "Thread checkbox for '" + i + "'")
            x.click()
        
    def deleteSelectedMessages(self):
        #
        # Delete the currently selected messages in this thread.
        #
        x= self.UTILS.getElement(DOM.Messages.delete_messages_button, "Delete message" )
        x.tap()
        
        self.marionette.switch_to_frame()
        x = self.UTILS.getElement(DOM.GLOBAL.modal_ok_button, "OK button in question dialog")
        x.tap()
        self.UTILS.switchToFrame(*DOM.Messages.frame_locator)
        time.sleep(2)
        
    
    def deleteSelectedThreads(self):
        #
        # Delete the currently selected message threads.
        #
        orig_iframe = self.UTILS.currentIframe()
        x = self.UTILS.getElement(DOM.Messages.delete_threads_button, "Delete threads button")
        x.tap()
        self.UTILS.quitTest()
        
        time.sleep(1)
        self.marionette.switch_to_frame()
        x = self.UTILS.getElement(DOM.GLOBAL.modal_ok_button, "OK button in question dialog")
        x.tap()
        
        #
        # For some reason after you do this, you can't enter a 'to' number anymore.
        # After a lot of headscratching, it was just easier to re-launch the app.
        #
        time.sleep(5)
        self.launch()
        
    def deleteAllThreads(self):
        #
        # Deletes all threads.
        #
        x = self.marionette.find_element(*DOM.Messages.no_threads_message)
        if x.is_displayed():
            self.UTILS.logResult("info", "(No message threads to delete.)")
        else:
            self.UTILS.logResult("info", "Deleting message threads ...")
 
            x = self.threadEditModeON()
            x = self.UTILS.getElement(DOM.Messages.check_all_threads_btn, "Select all button")
            x.tap()
             
            self.deleteSelectedThreads()
            self.UTILS.waitForElements(DOM.Messages.no_threads_message, 
                                       "No message threads notification", True, 60)
    
    def countMessagesInThisThread(self):
        #
        # Returns the number of messages in this thread
        # (assumes you're already in the thread).
        #
        x = self.UTILS.getElements(DOM.Messages.thread_messages,"Messages")
        x = len(x)
        
        return x


    def lastMessageInThisThread(self):
        #
        # Returns an object of the last message in the current thread.
        #
        time.sleep(2)
        x = self.marionette.find_elements(*DOM.Messages.thread_messages)
        
        if len(x) > 1:
            return x[-1]
        else:
            return x[0]
    
    def timeOfThread(self, p_num):
        #
        # Returns the time of a thread.
        #
        x = self.UTILS.getElement( ("xpath", DOM.Messages.thread_timestamp_xpath % p_num), 
                                   "Thread timestamp",
                                   True, 5, False)
        return x.text

    def timeOfLastMessageInThread(self):
        #
        # Returns the time of the last message in the current thread.
        #
        time.sleep(2)
        x = self.UTILS.getElements(DOM.Messages.message_timestamps, "Message timestamps")
        return x[-1].text
        
    def waitForReceivedMsgInThisThread(self, p_timeOut=30):
        #
        # Waits for the last message in this thread to be a 'received' message
        # and returns the element for this message.
        #
        pollTime=2
        pollReps=(p_timeOut / pollTime)
        lastEl  = False
        for i in range(1,pollReps):
            # Get last message in this thread.
            x = self.lastMessageInThisThread()
            
            # Is this a received message?
            if "incoming" in x.get_attribute("class"):
                # Yep.
                lastEl = x
                break
            
            # Nope - sleep then try again.
            time.sleep(pollTime)
            
        self.UTILS.TEST(lastEl,
                        "Last message in thread is a 'received' message within " + str(p_timeOut) + " seconds.")
        return lastEl
            
    
    def waitForSMSNotifier(self, p_num, p_timeout=40):
        #
        # Get the element of the new SMS from the status bar notification.
        #
        self.UTILS.logResult("info", "Waiting for statusbar notification of new SMS from " + p_num + " ...")

        #
        # Create the string to wait for.
        #
        x=( DOM.Messages.statusbar_new_sms[0],
            DOM.Messages.statusbar_new_sms[1] % p_num)
        
        #
        # Wait for the notification to be present for this number 
        # in the popup messages (this way we make sure it's coming from our number,
        # as opposed to just containing our number in the notification).
        #
        time.sleep(5)
        x = self.UTILS.waitForStatusBarNew(x, p_displayed=False, p_timeOut=p_timeout)

        self.UTILS.logResult(x, "SMS notifier from " + p_num + " found in status bar.")
        return x
    
    def clickSMSNotifier(self, p_num):
        #
        # Click new sms in the home page status bar notificaiton.
        #
        self.UTILS.logResult("info", "Clicking statusbar notification of new SMS from " + p_num + " ...")

        #
        # Switch to the 'home' frame to click the notifier.
        #
        self.marionette.switch_to_frame()
        self.UTILS.displayStatusBar()
        x=( DOM.Messages.statusbar_new_sms[0],
            DOM.Messages.statusbar_new_sms[1] % p_num)
        x = self.UTILS.getElement(x, "Statusbar notification for " + p_num)
        x.click()

        #
        # Switch back to the messaging app.
        #
        self.UTILS.switchToFrame(*DOM.Messages.frame_locator)
        
        #
        # Wait for the message thread to finish loading.
        #
        self.UTILS.waitForElements(("xpath", "//h1[text()='" + p_num + "']"), 
                                   "SMS thread header for " + str(p_num), True, 20)
        self.waitForReceivedMsgInThisThread()
        

    def readLastSMSInThread(self):
        #
        # Read last message in the current thread.
        #
        received_message = self.UTILS.getElements(DOM.Messages.received_messages, "Received messages")[-1]
        return str(received_message.text)

    def readNewSMS(self, p_FromNum):
        #
        # Read and return the value of the new message received from number.
        #
        x = self.UTILS.getElement(("xpath", DOM.Messages.messages_from_num % p_FromNum), "Message from '" + p_FromNum + "'")
        x.tap()
        
        # (From gaiatest: "TODO Due to displayed bugs I cannot find a good wait for switch btw views")
        time.sleep(5)
        
        #
        # Return the last comment in this thread.
        #
        return self.readLastSMSInThread()
    
    def openThread(self, p_num):
        #
        # Opens the thread for this number (assumes we're looking at the
        # threads in the messaging screen).
        #
        boolOK = True
        try:
            thread_el = ("xpath", DOM.Messages.thread_selector_xpath % p_num)
            x = self.UTILS.getElement(thread_el,"Message thread for " + p_num)
            
            x.tap()
            
            self.UTILS.waitForElements(DOM.Messages.send_message_button, "'Send' button")
        except:
            boolOK = False
         
        self.UTILS.TEST(boolOK, "Thread '" + p_num + "' opened successfully.")
        
    def checkAirplaneModeWarning(self):
        #
        # Checks for the presence of the popup
        # warning message if you just sent a message
        # while in 'airplane mode' (also removes
        # the message so you can continue).
        #
        x = self.UTILS.getElement(DOM.Messages.airplane_warning_header, "Airplane mode warning message",
                                  True, 5, False)
        if x:
            _popup_title = "Airplane mode activated"
            self.UTILS.TEST(x.text == _popup_title, 
                            "Warning message title = '" + _popup_title + "'.")
            
            x = self.UTILS.getElement(DOM.Messages.airplane_warning_ok, "OK button")
            x.tap()


    def checkIsInToField(self, p_target, p_targetIsPresent=True):
        #
        # Verifies if a number (or contact name) is
        # displayed in the "To: " field of a compose message.<br>
        # (Uses 'caseless' search for this.)
        #
        x = self.UTILS.getElements(DOM.Messages.target_numbers, "'To:' field contents")
        
        boolOK = False
        for i in x:
            if i.text.lower() == str(p_target).lower():
                boolOK = True
                break
        
        testMsg = "is" if p_targetIsPresent else "is not"
        testMsg = "\"" + str(p_target) + "\" " + testMsg + " in the 'To:' field."
        self.UTILS.TEST(boolOK == p_targetIsPresent, testMsg)
        return boolOK

    def removeFromToField(self, p_target):
        #
        # Removes p_target from the "To" field of this SMS.<br>
        # Returns True if it found the target, or False if not.
        #
        x = self.UTILS.getElements(DOM.Messages.target_numbers, "'To:' field contents")
         
        for i in x:
            if i.text.lower() == p_target.lower():
                self.UTILS.logResult("info", "Tapping contact '" + p_target + "' ...")
                i.tap()
                
                self.UTILS.logResult(False, "Need to find the confirmation screen!")
                return True
        
        return False
        
    def checkNumberIsInToField(self, p_target):
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
            if i.get_attribute("data-number") == p_target:
                boolOK = True
                break
        
        self.UTILS.TEST(boolOK, "\"" + str(p_target) + "\" is the number in one of the 'To:' field targets.")
        return boolOK
        
    def addNumberInToField(self, p_num):
        #
        # Add the number (or contact name) in the 'To'
        # field of this sms message.
        # Assums you are in 'create sms' screen.
        #
        self.UTILS.typeThis(DOM.Messages.target_numbers, 
                            "Target number field", 
                            p_num, 
                            p_no_keyboard=True,
                            p_validate=False,
                            p_clear=False,
                            p_enter=True)
        
        self.checkIsInToField(p_num)
        
    def startNewSMS(self):
        #
        # Starts a new sms (doesn't fill anything in).
        # Assumes the Messaging app is already launched.
        #
        newMsgBtn = self.UTILS.getElement(DOM.Messages.create_new_message_btn, "Create new message button")
        newMsgBtn.tap()
        
    def threadCarrier(self):
        #
        # Returns the 'carrier' being used by this thread.
        #
        x = self.UTILS.getElement(DOM.Messages.type_and_carrier_field, "Type and carrier information")
        return x.text.split("|")[1].strip()
        
    def threadType(self):
        #
        # Returns the 'type' being used by this thread.
        #
        x = self.UTILS.getElement(DOM.Messages.type_and_carrier_field, "Type and carrier information")
        return x.text.split("|")[0].strip()
        
    def createAndSendSMS(self, p_nums, p_msg):
        #
        # Create and send a new SMS.<br>
        # <b>Note:</b> The p_nums field must be an array of numbers
        # or contact names.
        #

        self.startNewSMS()
        
        #
        # Enter the number.
        #
        for p_num in p_nums:
            self.addNumberInToField(p_num)
            
        #
        # The header should now say how many receipients.
        #
        num_recs = len(p_nums)
        search_str = " recipient" if num_recs == 1 else " recipients"
        self.UTILS.headerCheck(str(num_recs) + search_str)
        
        #
        # Enter the message.
        #
        self.enterSMSMsg(p_msg)
         
        #
        # Send the message.
        #
        self.sendSMS()
        