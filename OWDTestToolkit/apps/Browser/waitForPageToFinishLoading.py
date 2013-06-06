from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def waitForPageToFinishLoading(self):
        #
        # Waits for the current url to finish loading.
        #
        self.UTILS.waitForElements(   DOM.Browser.throbber, "Animated 'wait' icon", True, 5, False)
        self.UTILS.waitForNotElements(DOM.Browser.throbber, "Animated 'wait' icon", True, 90, False)
        
    
