from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def callLog_call(self, p_num):
        #
        # Calls a number from the call log.
        #
		self.openCallLog()

		x = self.UTILS.getElement( ("xpath", DOM.Dialer.call_log_number_xpath % p_num),
								   "The call log for number %s" % p_num)
		x.tap()
		
		x = self.UTILS.getElement( DOM.Dialer.call_log_numtap_call, "Call button")
		x.tap()
		
		self.UTILS.switchToFrame(*DOM.Dialer.frame_locator_calling)
		
		x = self.UTILS.getElement(DOM.Dialer.outgoing_call_number, "Number being called")
		self.UTILS.logResult("info", "X: %s, %s" % (x.get_attribute("value"), x.text))
