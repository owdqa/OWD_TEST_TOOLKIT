from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def addNumberInToField(self, p_num):
        #
        # Add the number (or contact name) in the 'To'
        # field of this sms message.
        # Assums you are in 'create sms' screen.
        #
        self.UTILS.typeThis(DOM.Messages.target_numbers, 
                            "Target number field", 
                            p_num, 
                            p_no_keyboard=True,
                            p_validate=False,
                            p_clear=False,
                            p_enter=True)
        
        self.checkIsInToField(p_num)
        
