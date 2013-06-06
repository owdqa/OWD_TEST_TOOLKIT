from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def pressEditContactButton(self):
        #
        # Presses the Edit contact button when vieweing a contact.
        #
        editBTN = self.UTILS.getElement(DOM.Contacts.edit_details_button, "Edit details button")
        editBTN.tap()
        self.UTILS.waitForElements(DOM.Contacts.edit_contact_header, "'Edit contact' screen header")
