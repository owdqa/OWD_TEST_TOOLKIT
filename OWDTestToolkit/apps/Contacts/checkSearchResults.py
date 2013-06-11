from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def checkSearchResults(self, p_contactName, p_present=True):
        #
        # Checks the results of a search() to see
        # if the contact is present or not (depending
        # on the 'p_present' setting).
        #
        
        #
        # Verify our contact is all that's displayed in the result list.
        #
        y = self.marionette.find_elements(*DOM.Contacts.search_results_list)
        boolContact=False
        for i in y:
            if p_contactName in i.text:
                boolContact = True
                
        if p_present:
            comment = " is "
        else:
            comment = " is not "
        
        comment2 = comment + "displayed in the result list."
                 
        self.UTILS.TEST(p_present == boolContact, 
                        "Contact '" + p_contactName + "'" + comment2)

