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
        time.sleep(5)
        
        #
        # Can take a few seconds to appear, so try a few times.
        #
        for _trynum in range(1,6):
            x = self.UTILS.screenShotOnErr()
            self.UTILS.logResult("debug", "Looking for '%s' - attempt %s ..." % (p_name, _trynum), x)

            x = self.UTILS.getElements(DOM.EME.search_suggestions, "Search suggestions")
            boolOK = False
            for i in x:
                i_name  = i.get_attribute("data-suggestion")
                if i_name:
                    i_name = i_name.lower() 
                    i_name = i_name.replace("[", "") 
                    i_name = i_name.replace("]", "") 
                    _boolIN = False
                    for i2 in p_name.lower().split():
                        self.UTILS.logResult("debug", "Is '%s' in '%s'?" % (i2, i_name))
                        if i2 not in i_name:
                            _boolIN = False
                            break
                        else:
                            _boolIN = True
                            
                    if _boolIN:
                        i.tap()
                        boolOK = True
                        break
            
            if boolOK:
                break
            
            time.sleep(3)
    
        self.UTILS.TEST(boolOK, "Found '%s' in suggestions." % p_name)
                
        boolOK = True
        try:
            _el = ("xpath", DOM.EME.search_result_icon_xpath % p_name)
            self.wait_for_element_displayed(*_el, timeout=60)
            x = self.marionette.find_element(*_el)
            return x
        except:
            boolOK = False
            
        return boolOK

