from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def selectSearchResult(self, p_contactName):
        #
        # Select the result of a search 
        #
        y = self.marionette.find_elements(*DOM.Contacts.search_results_list)
        for i in y:
            if p_contactName in i.text:
                i.tap()
                

