from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def headerCheck(self, p_str):
        #
        # Returns the header that matches a string.
        # NOTE: ALL headers in this iframe return true for ".is_displayed()"!
        #
        boolOK = False
        try:
            self.wait_for_element_present(*DOM.GLOBAL.app_head, timeout=1)
            headerNames = self.marionette.find_elements(*DOM.GLOBAL.app_head)
            for i in headerNames:
                self.UTILS.logResult("Header: " + i.text)
                if i.text == p_str:
                    if i.is_displayed():
                        boolOK = True
                        break
        except:
            boolOK = False
                
        self.TEST(boolOK, "Header is \"" + p_str + "\".")
        return boolOK