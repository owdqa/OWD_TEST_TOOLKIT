from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def changeVal(self, p_contact_name, p_field, p_newVal):
        #
        # Change a value for a contact (assumes we're looking at the 'all contacts' screen
        # currently).
        #
        
        #
        # View our contact.
        #
        self.viewContact(p_contact_name)
         
        #
        # Press the edit button.
        #
        self.pressEditContactButton()
         
        #
        # Change the name to "aaaaabbbbbccccaaaa"
        #
        contFields = self.getContactFields()
        self.replaceStr(contFields[p_field] , p_newVal)
 
        #
        # Save the changes
        #
        updateBTN = self.UTILS.getElement(DOM.Contacts.edit_update_button, "Edit 'update' button")
        updateBTN.tap()
 
        #
        # Return to the contact list screen.
        #
        backBTN = self.UTILS.getElement(DOM.Contacts.details_back_button, "Details 'back' button")
        backBTN.tap()
         
        self.UTILS.waitForElements(DOM.Contacts.view_all_header, "'View all contacts' screen header")
