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
		
		#
		# If we tapped this from a contact header then we will already be in the
		# dialer so this won't be necessary.
		#
        if x.get_attribute("data-is-contact") != "true":
        	#
        	# Select dialer option.
        	#
            x = self.UTILS.getElement(DOM.Messages.header_call_btn, "'Call' button")
            x.tap()
	        
		#
		# Switch to correct iframe.
		#
        self.UTILS.switchToFrame(*DOM.Dialer.frame_locator)

