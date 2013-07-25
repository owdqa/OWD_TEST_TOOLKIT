from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def selectContactFromAll(self, p_contactName):
        #
        # Select the result of a search 
        #
        y = self.UTILS.getElements(DOM.Contacts.view_all_contact_list, "All contacts list", False)
        for i in y:
            if p_contactName in i.text:
                self.UTILS.logResult("info", "Contact '%s' found in all contacts." % p_contactName)
                i.tap()
                return
                
        self.UTILS.logResult("info", "Contact '%s' was <b>not</b> found in the contacts list." % p_contactName)

