from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def checkThreadHeader(self, p_header):
        #
        # Verifies if a string is contained in the header
        #
        x = self.UTILS.getElement(DOM.Messages.message_header, "Header")
        
        boolOK = False
        if x.get_attribute("data-number") == p_header:
                boolOK = True
        
        self.UTILS.TEST(boolOK, "\"" + str(p_header) + "\" is the header in the SMS conversation.")
        return boolOK
        
