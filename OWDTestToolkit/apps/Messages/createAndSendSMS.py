from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def createAndSendSMS(self, p_nums, p_msg):
        #
        # Create and send a new SMS.<br>
        # <b>Note:</b> The p_nums field must be an array of numbers
        # or contact names.
        #

        self.startNewSMS()
        
        #
        # Enter the number.
        #
        for p_num in p_nums:
            self.addNumberInToField(p_num)
            
        #
        # The header should now say how many receipients.
        #
        num_recs = len(p_nums)
        search_str = " recipient" if num_recs == 1 else " recipients"
        self.UTILS.headerCheck(str(num_recs) + search_str)
        
        #
        # Enter the message.
        #
        self.enterSMSMsg(p_msg)
         
        #
        # Send the message.
        #
        self.sendSMS()
