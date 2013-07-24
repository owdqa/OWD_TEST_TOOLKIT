from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def callLog_addToContact(self, p_num):
        #
        # Creates a new contact from the call log (only
        # as far as the contacts app opening).
        #
		self.openCallLog()

		x = self.UTILS.getElement( ("xpath", DOM.Dialer.call_log_number_xpath % p_num),
								   "The call log for number %s" % p_num)
		x.tap()
		
		x = self.UTILS.getElement( DOM.Dialer.call_log_numtap_add_to_existing, "Add to existing contact button")
		x.tap()
		
		self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)
		self.UTILS.waitForElements(DOM.Contacts.view_all_header, "'Contacts' header")