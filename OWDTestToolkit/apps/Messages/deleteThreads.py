from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def deleteThreads(self, p_target_array=False):
        #
        # Enters edit mode, selects the required messages and
        # deletes them.<br>
        # p_target_array is an array of target numbers 
        # or contacts which identify the threads to be selected.
        # If it's not specified then all messages in this 
        # thread will be deleted.
        #
		x = self.marionette.find_element(*DOM.Messages.no_threads_message)
		if x.is_displayed():
			self.UTILS.logResult("info", "(No message threads to delete.)")
			
			#
			# Without this 'return' the code actually tries to do the 'else:' part
			# too!!
			#
			return
		else:
			self.UTILS.logResult("info", "Deleting message threads ...")
	        if p_target_array:
	            self.editAndSelectThreads(p_target_array)
	            self.deleteSelectedThreads()
	        else:
	            self.deleteAllThreads()
            
