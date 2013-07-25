from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def addThisNumberToContact(self, p_name):
        #
        # Adds the current number to existing contact.
        #
		x = self.UTILS.getElement(DOM.Dialer.phone_number, "Phone number field", False)
		dialer_num = x.get_attribute("value")
		
		x = self.UTILS.getElement(DOM.Dialer.add_to_contacts_button, "Add to contacts button")
		x.tap()
        
		x = self.UTILS.getElement(DOM.Dialer.add_to_existing_contact_btn, "Add to existing contact button")
		x.tap()
        
		self._complete_addNumberToContact(dialer_num, p_name)