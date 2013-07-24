from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def openCallLog(self):
        #
        # Opens the call log.
        #
        x = self.UTILS.getElement(DOM.Dialer.call_log_btn, "Call number button")
        x.tap()
        
        self.UTILS.waitForElements(DOM.Dialer.call_log_filter, "Call log filter")