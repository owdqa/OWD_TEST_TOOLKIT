from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def createContactFromThisNum(self):
        #
        # Creates a new contact from this number 
        # (doesn't fill in the contact details).
        #
        
        x = self.UTILS.getElement(DOM.Phone.add_to_contacts_button, "Add to contacts button")
        x.tap()

        x = self.UTILS.getElement(DOM.Phone.create_new_contact_btn, "Create new contact button")
        x.tap()
        
        #
        # Switch to the contacts frame.
        #
        self.marionette.switch_to_frame()
        x = (DOM.Contacts.frame_locator[0],
             DOM.Contacts.frame_locator[1] + "?new")
        self.UTILS.switchToFrame(*x)
        
