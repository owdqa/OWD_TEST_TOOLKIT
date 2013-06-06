from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def checkEditContactDetails(self, p_contact_json_obj):
        #
        # Validate the details of a contact in the 'view contact' screen.
        #
        # p_contact_json_obj must be an object in the same format as the
        # one in ./example/tests/mock_data/contacts.py.
        #
        self.pressEditContactButton()

        #
        # Correct details are in the contact fields.
        #
        self.verifyFieldContents(p_contact_json_obj)
