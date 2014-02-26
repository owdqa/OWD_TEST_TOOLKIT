from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def populateContactFields(self,p_contact_json_obj):
        #
        # Put the contact details into each of the fields.
        # <br><br>
        # <b>p_contact_json_obj</b> must be an object in the same format as the
        # one in ./example/tests/mock_data/contacts.py.
        #
        self.populateFields(p_contact_json_obj)
        
        # Press the 'done' button and wait for the 'all contacts' page to load.
        done_button = self.UTILS.getElement(DOM.Contacts.done_button, "'Done' button")
        done_button.tap()
        
        # Wait for the 'view all contacts' header to be displayed.
        self.UTILS.waitForElements(DOM.Contacts.view_all_header, "View all contacts header")
        
        # Now check the contact's name is displayed here too.
        x = ("xpath", 
            DOM.Contacts.view_all_contact_xpath.format(p_contact_json_obj['name'].replace(" ","")))

        self.UTILS.waitForElements(x, "Contact '" + p_contact_json_obj['name'] + "'")
