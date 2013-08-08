from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def sendSMS(self):
        #
        # Just presses the 'send' button (assumes everything else is done).
        #
        sendBtn = self.UTILS.getElement(DOM.Messages.send_message_button, "Send sms button")
        sendBtn.tap()
        
        time.sleep(2) # (Give the spinner time to appear.)
        self.UTILS.waitForNotElements(DOM.Messages.message_sending_spinner, "'Sending' icon", True, 120)

