from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def fordwardMessage(self, msg_type, target_telNum):
        self.actions    = Actions(self.marionette)

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
            self.UTILS.logResult("info", "Cliking on fordaward button")
            x = self.UTILS.getElement(DOM.Messages.fordward_btn_msg_opt, "Fordward button is displayed")
            x.tap()

            #
            # Add a phone number.
            #
            self.addNumbersInToField([target_telNum])

            #
            # Send the sms.
            #
            self.UTILS.logResult("info", "Cliking on Send button")
            x = self.UTILS.getElement(DOM.Messages.send_message_button, "Send button is displayed")
            x.tap()

            #
            # Wait for the last message in this thread to be a 'recieved' one.
            #
            returnedSMS = self.waitForReceivedMsgInThisThread()
            self.UTILS.TEST(returnedSMS, "A receieved message appeared in the thread.", True)


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
            self.UTILS.logResult("info", "Cliking on fordaward button")
            x = self.UTILS.getElement(DOM.Messages.fordward_btn_msg_opt, "Fordward button is displayed")
            x.tap()

            #
            # Add a phone number.
            #
            self.addNumbersInToField([target_telNum])

            #
            # Send the mms.
            #
            self.UTILS.logResult("info", "Cliking on Send button")
            x = self.UTILS.getElement(DOM.Messages.send_message_button, "Send button is displayed")
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
            self.UTILS.TEST(returnedSMS, "A receieved message appeared in the thread.", True)

        elif msg_type == "mmssub":
            self.UTILS.logResult("info", "is a mms with subject")

            #
            # Open mms option with longtap on it
            #
            self.UTILS.logResult("info", "Open mms with subject options with longtap on it")
            x = self.UTILS.getElement(DOM.Messages.received_mms_subject, "Target MMS field")
            self.actions.long_press(x, 2).perform()


            #
            # Press fordward button
            #
            self.UTILS.logResult("info", "Cliking on fordaward button")
            x = self.UTILS.getElement(DOM.Messages.fordward_btn_msg_opt, "Fordward button is displayed")
            x.tap()


            #
            # Add a phone number.
            #
            self.addNumbersInToField([target_telNum])

            #
            # Send the mms.
            #
            self.UTILS.logResult("info", "Cliking on Send button")
            x = self.UTILS.getElement(DOM.Messages.send_message_button, "Send button is displayed")
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
            self.UTILS.TEST(returnedSMS, "A receieved message appeared in the thread.", True)

        else:
            self.UTILS.logResult("info", "incorrect value received")
            self.UTILS.quitTest()


