from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def startCreateNewContact(self):
        #
        # Open the screen to add a contact.
        #
        
        #
        # First make sure we're in the right place.
        #
        viewAllHeader = self.UTILS.getElement(DOM.Contacts.view_all_header, "'View all contacts' header", False)
        if not viewAllHeader.is_displayed():
            #
            # Header isn't present, so we're not running yet.
            #
            self.launch()
            
        #
        # Click Create new contact from the view all screen.
        #
        self.UTILS.waitForElements(DOM.Contacts.view_all_header, "View all contacts header")
        add_new_contact = self.UTILS.getElement(DOM.Contacts.add_contact_button, "'Add new contact' button")
        
        add_new_contact.tap()
        
        #
        # Enter details for new contact.
        #
        self.UTILS.waitForElements(DOM.Contacts.add_contact_header, "Add contact header")
