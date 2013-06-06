from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def editContact(self, p_contact_curr_json_obj, p_contact_new_json_obj):
        #
        # Replace the details of one contact with another via the edit screen.
        # <br><br>
        # <b>p_contact_curr_json_obj</b> and <b>p_contact_new_json_obj</b> must 
        # be objects in the same format as the one in 
        # ./example/tests/mock_data/contacts.py (however, only needs the 
        # 'name' component is used from the p_contact_curr_json_obj).
        #
        
        #
        # Go to the view details screen for this contact.
        #
        self.viewContact(p_contact_curr_json_obj['name'])
                
        #
        # Tap the Edit button to go to the edit details page.
        #
        editBTN = self.UTILS.getElement(DOM.Contacts.edit_details_button, "Edit details button")
        editBTN.tap()
        self.UTILS.waitForElements(DOM.Contacts.edit_contact_header, "'Edit contacts' screen header")

        #
        # Enter the new contact details.
        #
        self.populateFields(p_contact_new_json_obj)
        
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

