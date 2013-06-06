from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def checkIsInToField(self, p_target, p_targetIsPresent=True):
        #
        # Verifies if a number (or contact name) is
        # displayed in the "To: " field of a compose message.<br>
        # (Uses 'caseless' search for this.)
        #
        x = self.UTILS.getElements(DOM.Messages.target_numbers, "'To:' field contents")
        
        boolOK = False
        for i in x:
            if i.text.lower() == str(p_target).lower():
                boolOK = True
                break
        
        testMsg = "is" if p_targetIsPresent else "is not"
        testMsg = "\"" + str(p_target) + "\" " + testMsg + " in the 'To:' field."
        self.UTILS.TEST(boolOK == p_targetIsPresent, testMsg)
        return boolOK

