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
        # Enter the numbers.
        #
        self.addNumbersInToField(p_nums)
            
        #
        # Enter the message.
        #
        self.enterSMSMsg(p_msg)
         
		#
		# The header should now say how many receipients.
		#
        time.sleep(2) # give the header time to change.
        num_recs = len(p_nums)
        search_str = " recipient" if num_recs == 1 else " recipients"
        self.UTILS.headerCheck(str(num_recs) + search_str)
		
        #
        # Send the message.
        #
        self.sendSMS()
