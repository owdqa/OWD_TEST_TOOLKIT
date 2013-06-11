from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def readNewSMS(self, p_FromNum):
        #
        # Read and return the value of the new message received from number.
        #
        x = self.UTILS.getElement(("xpath", DOM.Messages.messages_from_num % p_FromNum), "Message from '" + p_FromNum + "'")
        x.tap()
        
        # (From gaiatest: "TODO Due to displayed bugs I cannot find a good wait for switch btw views")
        time.sleep(5)
        
        #
        # Return the last comment in this thread.
        #
        return self.readLastSMSInThread()
    
