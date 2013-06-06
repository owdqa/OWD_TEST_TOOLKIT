from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def deleteAllThreads(self):
        #
        # Deletes all threads.
        #
        x = self.marionette.find_element(*DOM.Messages.no_threads_message)
        if x.is_displayed():
            self.UTILS.logResult("info", "(No message threads to delete.)")
        else:
            self.UTILS.logResult("info", "Deleting message threads ...")
 
            x = self.threadEditModeON()
            x = self.UTILS.getElement(DOM.Messages.check_all_threads_btn, "Select all button")
            x.tap()
             
            self.deleteSelectedThreads()
            self.UTILS.waitForElements(DOM.Messages.no_threads_message, 
                                       "No message threads notification", True, 60)
    
