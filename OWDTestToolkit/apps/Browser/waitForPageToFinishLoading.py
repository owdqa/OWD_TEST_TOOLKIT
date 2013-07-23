from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def waitForPageToFinishLoading(self):
        #
        # Waits for the current url to finish loading.
        #
        time.sleep(3)
        try:
        	self.wait_for_element_displayed(*DOM.Browser.throbber)
    	except:
    		pass
        self.UTILS.waitForNotElements(DOM.Browser.throbber, "Animated 'wait' icon", True, 90, False)
        
     	time.sleep(2)
