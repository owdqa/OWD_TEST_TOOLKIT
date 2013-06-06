from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def startNewSMS(self):
        #
        # Starts a new sms (doesn't fill anything in).
        # Assumes the Messaging app is already launched.
        #
        newMsgBtn = self.UTILS.getElement(DOM.Messages.create_new_message_btn, "Create new message button")
        newMsgBtn.tap()
        
