from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def callLog_createContact(self, p_num, p_openCallLog=True):
        #
        # Creates a new contact from the call log (only
        # as far as the contacts app opening).
        # If p_openCallLog is set to False it will assume you are
        # already in the call log.
        #
		if p_openCallLog:
			self.openCallLog()
			   
		x = self.UTILS.getElement( ("xpath", DOM.Dialer.call_log_number_xpath % p_num),
								   "The call log for number %s" % p_num)
		x.tap()
		
		x = self.UTILS.getElement( DOM.Dialer.call_log_numtap_create_new, "Create new contact button", True, 20)
		x.tap()
		
		self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)
		self.UTILS.waitForElements(DOM.Contacts.add_contact_header, "'Add contact' header")