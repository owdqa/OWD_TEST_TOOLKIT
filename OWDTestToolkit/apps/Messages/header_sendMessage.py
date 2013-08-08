from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

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
        
        #
        # Already in the correct iframe for messages, so just finish here.
        #

