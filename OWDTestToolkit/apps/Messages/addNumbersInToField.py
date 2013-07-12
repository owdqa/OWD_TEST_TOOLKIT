from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def addNumbersInToField(self, p_nums):
        #
        # Add the numbers (or contact name) in the 'To'
        # field of this sms message.
        # Assumes you are in 'create sms' screen.
        # <br>
        # <b>p_nums</b> must be an array.
        #
        for i in p_nums:
            self.UTILS.typeThis(DOM.Messages.target_numbers_empty, 
	                            "Target number field", 
	                            i, 
	                            p_no_keyboard=True,
	                            p_validate=False,
	                            p_clear=False,
	                            p_enter=True)
        
        for i in p_nums:
            self.checkIsInToField(i)
        
