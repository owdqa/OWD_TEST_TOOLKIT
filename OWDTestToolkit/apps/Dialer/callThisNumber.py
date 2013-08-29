from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def callThisNumber(self):
        #
        # Calls the current number.
        #
        x = self.UTILS.getElement(DOM.Dialer.call_number_button, "Call number button")
        x.tap()
        
        self.UTILS.checkMarionetteOK()
        
        self.UTILS.switchToFrame(*DOM.Dialer.frame_locator_calling)
        self.UTILS.waitForElements(DOM.Dialer.outgoing_call_locator, "Outgoing call element")
     	
        
