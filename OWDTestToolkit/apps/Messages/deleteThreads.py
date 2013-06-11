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
        if p_target_array:
            self.editAndSelectThreads(p_target_array)
            self.deleteSelectedThreads()
        else:
            self.deleteAllThreads()
            
