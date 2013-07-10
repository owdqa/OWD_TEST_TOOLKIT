from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def createContactFromThisNum(self):
        #
        # Creates a new contact from the number currently in the dialler 
        # (doesn't fill in the contact details).
        #
        self.UTILS.switchToFrame(*DOM.Phone.frame_locator)
        
        x = self.UTILS.getElement(DOM.Phone.add_to_contacts_button, "Add to contacts button")
        x.tap()

        x = self.UTILS.getElement(DOM.Phone.create_new_contact_btn, "Create new contact button")
        x.tap()
        
        #
        # Switch to the contacts frame.
        #
        self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)
        
