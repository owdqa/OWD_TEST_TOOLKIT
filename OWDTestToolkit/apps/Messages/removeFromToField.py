from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def removeFromToField(self, p_target):
        #
        # Removes p_target from the "To" field of this SMS.<br>
        # Returns True if it found the target, or False if not.
        #
        x = self.UTILS.getElements(DOM.Messages.target_numbers, "'To:' field contents")
         
        for i in x:
            if i.text.lower() == p_target.lower():
                self.UTILS.logResult("info", "Tapping contact '" + p_target + "' ...")
                i.tap()
                
                self.UTILS.logResult(False, "Need to find the confirmation screen!")
                return True
        
        return False
        
