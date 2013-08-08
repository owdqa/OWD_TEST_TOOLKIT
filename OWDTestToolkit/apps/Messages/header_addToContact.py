from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def header_addToContact(self):
        #
		# Taps the header and tries to tap the 'Add to an existsing contact' button.
        # - Assumes we are looking at a message thread already.
        # - Leaves you in the correct iframe to continue (contacts).
        #
        x = self.UTILS.getElement(DOM.Messages.message_header, "Thread header")
        x.tap()
        
        x = self.UTILS.getElement(DOM.Messages.header_add_to_contact_btn, "'Add to an existing contact' button")
        x.tap()
        
        #
        # Switch to correct iframe.
        #
        self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)

