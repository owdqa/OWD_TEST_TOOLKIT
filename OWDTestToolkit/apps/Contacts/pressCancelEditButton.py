from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def pressCancelEditButton(self):
        #
        # Presses the Edit contact button when vieweing a contact.
        #
        editCnclBTN = self.UTILS.getElement(DOM.Contacts.edit_cancel_button, "Cancel edit button")
        editCnclBTN.tap()
        self.UTILS.waitForElements(DOM.Contacts.view_details_title, "'View contact details' title")

