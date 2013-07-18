from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def removeContactFromToField(self, p_target):
        #
        # Removes p_target from the "To" field of this SMS.<br>
        # Returns True if it found the target, or False if not.
        #
        x = self.UTILS.getElements(DOM.Messages.target_numbers, "'To:' field contents")
        
        x_pos = 0
        for i in range(0,len(x)):
            self.UTILS.logResult("info", "Checking target '%s' to '%s' ..." % (x[i].text, p_target))
            if x[i].text.lower() == p_target.lower():
                self.UTILS.logResult("info", "Tapping contact '" + p_target + "' ...")
                x[i].tap()
                
                try:
                	#
                	# This contact was added via 'add contact' icon.
                	#
                 	y = self.marionette.find_element("xpath", "//button[text()='Remove']")
                	self.UTILS.logResult("info", "Tapping 'Remove' button.")
                	y.tap()
                	return True
                except:
                	#
                	# This contact was manually entered.
                	#
                	z = self.UTILS.getElements(DOM.Messages.target_numbers, "Target to be removed")[i]
                	z.clear()
                	return True
        return False
        
