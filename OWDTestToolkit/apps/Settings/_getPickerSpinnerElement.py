from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def _getPickerSpinnerElement(self, p_DOM, p_msg):
        #
        # Returns the element for the spinner in a picker.
        # 
        
        # Get the elements that match this one.
        els = self.UTILS.getElements(p_DOM, p_msg, False, 20, True)
        
        # Get the one that's not hidden (the 'hidden'
        # attribute here has no 'value', so we need to just
        # check if it's been set to "".
        boolOK = False
        el     = False
        for i in els:
            if str(i.get_attribute("hidden")) == "false":
                boolOK = True
                el = i
                break
        
        self.UTILS.TEST(boolOK, "... one of them is visible|('hidden' attribute is not set)", True)
        return el

