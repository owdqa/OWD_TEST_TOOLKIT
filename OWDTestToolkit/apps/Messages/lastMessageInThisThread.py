from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def lastMessageInThisThread(self):
        #
        # Returns an object of the last message in the current thread.
        #
        time.sleep(2)
        try:
        	self.wait_for_element_present(*DOM.Messages.message_list, timeout=2)
	        x = self.marionette.find_elements(*DOM.Messages.message_list)
	        
	        if len(x) > 1:
	            return x[-1]
	        else:
	            return x[0]
    	except:
    		return False
