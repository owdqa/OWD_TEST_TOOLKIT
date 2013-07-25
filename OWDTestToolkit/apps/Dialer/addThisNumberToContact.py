from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def addThisNumberToContact(self):
        #
        # Adds the current number to existing contact.
        #
        x = self.UTILS.getElement(DOM.Dialer.add_to_contacts_button, "Add to contacts button")
        x.tap()
        
        x = self.UTILS.getElement(DOM.Dialer.add_to_existing_contact_btn, "Add to existing contact button")
        x.tap()
        
