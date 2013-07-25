from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def callLog_addToContact(self, p_num, p_name):
        #
        # Adds this number in the call log to an existing contact
        # (and returns you to the call log).
        #
		self.openCallLog()

		x = self.UTILS.getElement( ("xpath", DOM.Dialer.call_log_number_xpath % p_num),
								   "The call log for number %s" % p_num)
		x.tap()
		
		x = self.UTILS.getElement( DOM.Dialer.call_log_numtap_add_to_existing, "Add to existing contact button")
		x.tap()
		
		#
		# Switch to the Contacts frame, select our contacts and verify that this number
		# is automatically in the telephone number fields.
		#
		self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)
		self.UTILS.waitForElements( ("xpath", "//h1[text()='Select contact']"), "'Select contact' header")
		
		y = self.UTILS.getElements(DOM.Contacts.view_all_contact_list, "All contacts list")
		boolOK = False
		for i in y:
			if p_name in i.text:
				self.UTILS.logResult("info", "Contact '%s' found in all contacts." % p_num)
				i.tap()
				boolOK = True
				break
			
		self.UTILS.TEST(boolOK, "Succesfully selected contact from list.")
		self.UTILS.waitForElements(DOM.Contacts.edit_contact_header, "'Edit contact' header")

		# Test for an input field for number_<x> contaiing our number.
		self.UTILS.waitForElements( ("xpath", DOM.Contacts.phone_field_xpath % p_num),
									"Phone field contaiing %s" % p_num)
		
		#
		# Hit 'update' to save the changes to this contact.
		#
		done_button = self.UTILS.getElement(DOM.Contacts.edit_update_button, "'Update' button")
		done_button.tap()
 
		#
		# Verify that the contacts app is closed and we are returned to the call log.
		#
		self.marionette.switch_to_frame()
		self.UTILS.waitForNotElements( ("xpath", "//iframe[contains(@%s, '%s')]" % \
												(DOM.Contacts.frame_locator[0], DOM.Contacts.frame_locator[1])),
										"COntacts frame")
		self.UTILS.switchToFrame(*DOM.Dialer.frame_locator)
		 
		self.UTILS.waitForElements( ("xpath", "//h1[text()='Call log']"), "Call log header")
		
