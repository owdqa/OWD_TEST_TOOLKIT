from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def openCallLog(self):
        #
        # Opens the call log.
        #
        x = self.UTILS.getElement(DOM.Dialer.option_bar_call_log, "Call log button")
        x.tap()
        
        self.UTILS.waitForElements(DOM.Dialer.call_log_filter, "Call log filter")
        
        time.sleep(2)