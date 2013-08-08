from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def deleteContact(self, p_fullName):
        #
        # Deletes a contact.<br>
        # p_fullName must match the name displayed
        # in the 'view all contacts' screen (including spaces).
        #
        
        #
        # Make sure we are in the contacts app.
        #
        try:
            self.wait_for_element_displayed("xpath", "//h1[text() = 'Contacts']", timeout=1)
        except:
            self.launch()
        
        #
        # View our contact.
        #
        self.viewContact(p_fullName)
           
        #
        # Edit our contact.
        #
        self.pressEditContactButton()
         
        #
        # Delete our contact.
        #
        self.pressDeleteContactButton()
         
        #
        # Confirm deletion.
        #
        x = self.UTILS.getElement(DOM.Contacts.confirm_delete_btn, "Confirm deletion button")
        x.tap()
         
        #
        # Now verify that this contact is no longer present (or no search field if
        # this was the only contact).
        #
        contact_el = x = ("xpath", DOM.Contacts.view_all_contact_xpath % p_fullName.replace(" ",""))
        self.UTILS.waitForNotElements(contact_el, "Contact name in 'all contacts' screen")
