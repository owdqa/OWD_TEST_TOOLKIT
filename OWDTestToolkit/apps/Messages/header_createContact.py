from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def header_createContact(self):
        #
		# Taps the header and tries to tap the 'send message' button.
        # - Assumes we are looking at a message thread already.
        # - Leaves you in the correct iframe to continue.
        #
        x = self.UTILS.getElement(DOM.Messages.message_header, "Thread header")
        x.tap()
        
        x = self.UTILS.getElement(DOM.Messages.header_create_new_contact_btn, "'Create new contact' button")
        x.tap()
        
		#
		# Switch to correct iframe.
		#
        self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)

