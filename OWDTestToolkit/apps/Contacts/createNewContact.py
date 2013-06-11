from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def createNewContact(self, p_contact_json_obj, p_imgSource=False):
        #
        # Create a new contact with a image (if specified).
        # p_imgSource is either "gallery" or "camera" (or left undefined).
        # <br><br>
        # <b>p_contact_json_obj</b> must be an object in the same format as the
        # one in ./example/tests/mock_data/contacts.py.
        #
        self.startCreateNewContact()
        
        if p_imgSource == "gallery":
            self.addGalleryImageToContact(0)
            
        self.populateContactFields(p_contact_json_obj)

