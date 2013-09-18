from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def searchForApp(self, p_name):
        #
        # Uses the search field to find the app (waits for the
        # result to appear etc...).<br>
        # Returns the element for the icon (or False if it's not found).
        #
        x = self.UTILS.getElement(DOM.EME.search_field, "Search field")
        x.clear()
        x.send_keys(p_name)
        x.click()
        time.sleep(0.5)
        
        x = self.UTILS.getElements(DOM.EME.search_suggestions, "Search suggestions")
        boolOK = False
        for i in x:
            if i.get_attribute("data-suggestion") == p_name:
                i.tap()
                boolOK = True
                break
        
        self.UTILS.TEST(boolOK, "Found '%s' in suggestions." % p_name)
                
        boolOK = True
        try:
            self.wait_for_element_displayed("xpath", 
                                            DOM.EME.search_result_icon_xpath % p_name,
                                            timeout=60)
        except:
            boolOK = False
            
        return boolOK

