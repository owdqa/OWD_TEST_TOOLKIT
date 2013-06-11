from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def getElement(self, p_element, p_msg, p_displayed=True, p_timeout=False, p_stop=True):
        #
        # Returns an element, or False it it's not found.<br>
        # p_timeout defaults to _DEFAULT_ELEMENT_TIMEOUT (set in the utils.py file).
        #
        p_timeout = self._DEFAULT_ELEMENT_TIMEOUT if not p_timeout else p_timeout

        x = self.getElements(p_element, p_msg, p_displayed, p_timeout, p_stop)
        
        if x:
            # We're expecting ONE element back (it has different methods if it's one).
            return x[0]
        else:
            return False
    
