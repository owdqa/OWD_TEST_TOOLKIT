from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def editAndSelectThreads(self, p_target_array):
        #
        # Puts this thread into Edit mode and selects
        # the messages listed in p_msg_array.<br>
        # p_target_array is an array of target numbers 
        # or contacts which identify the threads to be selected.
        #
        
        #
        # Go into edit mode..
        #
        x= self.threadEditModeON()
        
        #
        # Check the messages (for some reason, just doing x[i].click() doesn't
        # work for element zero, so I had to do this 'longhanded' version!).
        #
        for i in p_target_array:
            x = self.UTILS.getElement(("xpath", 
                                       DOM.Messages.thread_selector_xpath % i),
                                      "Thread checkbox for '" + i + "'")
            x.click()
        
