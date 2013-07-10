from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def callThisNumber(self):
        #
        # Calls the current number.
        #
        x = self.UTILS.getElement(DOM.Phone.call_number_button, "Call number button")
        x.tap()
        
        time.sleep(2)
        
        self.UTILS.switchToFrame(*DOM.Phone.frame_locator_calling)
        self.UTILS.waitForElements(DOM.Phone.outgoing_call_locator, "Outgoing call element")
        
