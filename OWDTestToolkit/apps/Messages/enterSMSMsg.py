from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def enterSMSMsg(self, p_msg, p_not_keyboard=True):
        #
        # Create and send a message (assumes we are in a new 'create new message'
        # screen with the destination number filled in already).
        #
        self.UTILS.typeThis(DOM.Messages.input_message_area, 
                            "Input message area",
                            p_msg,
                            p_no_keyboard=p_not_keyboard,
                            p_clear=False,
                            p_enter=False,
                            p_validate=False) # it's the text() of this field, not the value.
        
        #
        # Validate the field.
        #
        x = self.UTILS.getElement(DOM.Messages.input_message_area, "Input message area (for validation)")
        self.UTILS.TEST(x.text == p_msg, 
                        "The text in the message area is as expected." + \
                        "|EXPECTED: '" + p_msg + "'" + \
                        "|ACTUAL  : '" + x.text + "'")
    
