from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

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
        self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)
        
        return orig_iframe
        
