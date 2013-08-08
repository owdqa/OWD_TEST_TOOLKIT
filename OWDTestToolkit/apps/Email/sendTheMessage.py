from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def sendTheMessage(self):        
        #
        # Hits the 'Send' button to send the message (handles
        # waiting for the correct elements etc...).
        #
        x = self.UTILS.getElement(DOM.Email.compose_send_btn, "Send button")
        x.tap()
        self.UTILS.waitForElements(DOM.Email.compose_sending_spinner, "Sending email spinner")
		
        #
        # Wait for inbox to re-appear (give it a BIG wait time because sometimes
        # it just needs it).
        #
        self.UTILS.waitForNotElements(DOM.Email.compose_sending_spinner, "Sending email spinner", True, 60, False)

        x = ('xpath', DOM.GLOBAL.app_head_specific % "Inbox")
        y = self.UTILS.waitForElements(x, "Inbox", True, 120)
		
        return True