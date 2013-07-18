from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def removeContactFromToField(self, p_target):
        #
        # Removes p_target from the "To" field of this SMS.<br>
        # Returns True if it found the target, or False if not.<br><br>
        #
        # <b>NOTE:</b> This will <i>only</i> work if the contact was added
        # using the 'add contact' icon like this:<br><br>
        # <pre>
		# 	self.messages.selectAddContactButton()
		# 	self.contacts.selectContactFromAll(self.contact_1["familyName"])
		# 	self.UTILS.switchToFrame(*DOM.Messages.frame_locator)
		# </pre>
        #
        x = self.UTILS.getElements(DOM.Messages.target_numbers, "'To:' field contents")
         
        for i in x:
            if i.text.lower() == p_target.lower():
                self.UTILS.logResult("info", "Tapping contact '" + p_target + "' ...")
                i.tap()
                
                x = self.UTILS.getElement( ("xpath", "//button[text()='Remove']"), "Remove button")
                x.tap()
                return True
        
        return False
        
