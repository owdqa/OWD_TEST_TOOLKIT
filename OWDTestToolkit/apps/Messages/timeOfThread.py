from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def timeOfThread(self, p_num):
        #
        # Returns the time of a thread.
        #
        x = self.UTILS.getElement( ("xpath", DOM.Messages.thread_timestamp_xpath % p_num), 
                                   "Thread timestamp",
                                   True, 5, False)
        return x.text

