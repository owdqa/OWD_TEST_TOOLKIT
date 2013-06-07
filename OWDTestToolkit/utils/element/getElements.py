from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def getElements(self, p_element, p_msg, p_displayed=True, p_timeout=False, p_stop=True):
        #
        # Returns a list of matching elements, or False if none are found.<br>
        # p_timeout defaults to _DEFAULT_ELEMENT_TIMEOUT (set in the utils.py file).
        #
        p_timeout = self._DEFAULT_ELEMENT_TIMEOUT if not p_timeout else p_timeout

        boolEl = self.waitForElements(p_element, p_msg, p_displayed, p_timeout, p_stop)
        
        if boolEl:
            el = self.marionette.find_elements(*p_element)
            
            return el
        else:
            return False

