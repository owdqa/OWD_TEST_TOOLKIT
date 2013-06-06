from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def searchForApp(self, p_name):
        #
        # Uses the search field to find the app (waits for the
        # result to appear etc...).<br>
        # Returns the element for the icon (or False if it's not found).
        #
        self.UTILS.typeThis(DOM.EME.search_field, "Search field", p_name, p_no_keyboard=True)
        
        boolOK = True
        
        try:
            self.wait_for_element_displayed("xpath", 
                                            DOM.EME.search_result_icon_xpath % p_name,
                                            timeout=60)
        except:
            boolOK = False
            
        return boolOK

