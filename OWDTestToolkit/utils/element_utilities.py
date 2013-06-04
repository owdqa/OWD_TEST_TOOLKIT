from global_imports import *
from gaiatest import GaiaTestCase

class main(GaiaTestCase):
    
    _TIMEOUT = 5
        
    def waitForNotElements(self, p_element, p_msg, p_displayed=True, p_timeout=_TIMEOUT, p_stop=True):
        #
        # Waits for an element to be displayed and captures the error if not.
        #
        boolOK = True
        try:
            if p_displayed:
                p_msg = p_msg + " no longer displayed within " + str(p_timeout) + " seconds.|" + str(p_element)
                self.wait_for_element_not_displayed(*p_element, timeout=p_timeout)
            else:
                p_msg = p_msg + " no longer present within " + str(p_timeout) + " seconds.|" + str(p_element)
                self.wait_for_element_not_present(*p_element, timeout=p_timeout)
        except:
            boolOK = False
            
        self.TEST(boolOK, p_msg, p_stop)
        
        return boolOK
    
    def waitForElements(self, p_element, p_msg, p_displayed=True, p_timeout=_TIMEOUT, p_stop=True):
        #
        # Waits for an element to be displayed and captures the error if not.
        #
        boolOK = True
        try:
            if p_displayed:
                p_msg = p_msg + " displayed within " + str(p_timeout) + " seconds.|" + str(p_element)
                self.wait_for_element_displayed(*p_element, timeout=p_timeout)
            else:
                p_msg = p_msg + " present within " + str(p_timeout) + " seconds.|" + str(p_element)
                self.wait_for_element_present(*p_element, timeout=p_timeout)
        except:
            boolOK = False
            
        self.TEST(boolOK, p_msg, p_stop)
        
        return boolOK
        
    def getElements(self, p_element, p_msg, p_displayed=True, p_timeout=_TIMEOUT, p_stop=True):
        #
        # Returns a list of matching elements, or False if none are found.
        #
        boolEl = self.waitForElements(p_element, p_msg, p_displayed, p_timeout, p_stop)
        
        if boolEl:
            el = self.marionette.find_elements(*p_element)
            
            return el
        else:
            return False

    def getElement(self, p_element, p_msg, p_displayed=True, p_timeout=_TIMEOUT, p_stop=True):
        #
        # Returns an element, or False it it's not found.
        #
        x = self.getElements(p_element, p_msg, p_displayed, p_timeout, p_stop)
        
        if x:
            # We're expecting ONE element back (it has different methods if it's one).
            return x[0]
        else:
            return False
    
    def headerCheck(self, p_str):
        #
        # Returns the header that matches a string.
        # NOTE: ALL headers in this iframe return true for ".is_displayed()"!
        #
        boolOK = False
        try:
            self.wait_for_element_present(*DOM.GLOBAL.app_head)
            headerNames = self.marionette.find_elements(*DOM.GLOBAL.app_head)
            for i in headerNames:
                if i.text == p_str:
                    if i.is_displayed():
                        boolOK = True
                        break
        except:
            boolOK = False
                
        self.TEST(boolOK, "Header is \"" + p_str + "\".")
        return boolOK
        
