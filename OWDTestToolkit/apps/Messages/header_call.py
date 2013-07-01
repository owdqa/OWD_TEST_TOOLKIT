from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def header_call(self):
        #
		# Taps the header and tries to tap the 'send message' button.
        # - Assumes we are looking at a message thread already.
        # - Leaves you in the correct iframe to continue.
        #
        x = self.UTILS.getElement(DOM.Messages.message_header, "Thread header")
        x.tap()
        
        x = self.UTILS.getElement(DOM.Messages.header_call_btn, "'Call' button")
        x.tap()
        
		#
		# Switch to correct iframe.
		#
        self.marionette.switch_to_frame()
        self.UTILS.switchToFrame(*DOM.Phone.frame_locator_from_sms)

