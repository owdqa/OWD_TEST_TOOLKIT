from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def selectContactFromAll(self, p_contactName):
        #
        # Select the result of a search 
        #
        y = self.UTILS.getElements(DOM.Contacts.view_all_contact_list, "All contacts list")
        for i in y:
            if p_contactName in i.text:
                i.tap()
                break
                

