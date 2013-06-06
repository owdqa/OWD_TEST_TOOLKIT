from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def checkViewContactDetails(self, p_contact_json_obj, p_imageCheck = False):
        #
        # Validate the details of a contact in the 'view contact' screen.
        # <br><br>
        # <b>p_contact_json_obj</b> must be an object in the same format as the
        # one in ./example/tests/mock_data/contacts.py.
        #
        
        #
        # Go to the view details screen for this contact.
        #
        self.viewContact(p_contact_json_obj['name'])
        
        if p_imageCheck:
            #
            # Verify that an image is displayed.
            #
            x = self.marionette.find_element("id", "cover-img")
            x_style = x.get_attribute("style")
            self.UTILS.TEST("blob" in x_style, "Contact's image contains 'something' in contact details screen.")

        #
        # Correct details are in the contact fields.
        #
        self.verifyFieldContents(p_contact_json_obj)
