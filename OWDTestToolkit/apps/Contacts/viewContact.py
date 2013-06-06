from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def viewContact(self, p_contact_name):
        #
        # Navigate to the 'view details' screen for a contact (assumes we are in the
        # 'view all contacts' screen).
        #
        
        x = ("xpath", DOM.Contacts.view_all_contact_xpath % p_contact_name.replace(" ",""))
        contact_found = self.UTILS.getElement(x, "Contact '" + p_contact_name + "'")
        contact_found.tap()
        
        self.UTILS.waitForElements(DOM.Contacts.view_details_title, "'View contact details' title")

        # 
        # TEST: Correct contact name is in the page header.
        #
        self.UTILS.headerCheck(p_contact_name)
            
        time.sleep(2)
