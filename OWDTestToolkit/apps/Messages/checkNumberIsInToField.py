from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def checkNumberIsInToField(self, p_target):
        #
        # Verifies if a number is contained in the
        # "To: " field of a compose message (even if it's
        # not displayed - i.e. a contact name is displayed,
        # but this validates the <i>number</i> for that
        # contact).
        #
        x = self.UTILS.getElements(DOM.Messages.target_numbers, "'To:' field contents")
        
        boolOK = False
        for i in x:
            if i.get_attribute("data-number") == p_target:
                boolOK = True
                break
        
        self.UTILS.TEST(boolOK, "\"" + str(p_target) + "\" is the number in one of the 'To:' field targets.")
        return boolOK
        
