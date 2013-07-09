from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def selectSearchResultSeveralPhones(self, p_contactName, p_num):
        #
        # Select the result of a search 
        #
        y = self.UTILS.getElements(DOM.Contacts.search_results_list, "Search results list", True, 10)
        for i in y:
            if p_contactName in i.text:
                i.tap()
                break
        
        #
        # Then select the phone p_num, nothing if p_num is 0 
        #
        self.marionette.switch_to_frame()        
        OK = self.UTILS.getElement(DOM.GLOBAL.conf_screen_ok_button, "OK button")
        if p_num == 0:
            OK.tap()
        else:
            xpath=('xpath','//span[contains(text(),"'+ str(p_num) +'")]')
            self.UTILS.logComment("Using xpath " + str(xpath))
            num = self.UTILS.getElement(xpath,"Number to select")
            num.tap()

