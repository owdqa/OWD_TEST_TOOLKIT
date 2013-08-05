from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def deleteAllThreads(self):
        #
        # Deletes all threads (assumes the messagin app is already open).
        #
        try:
            self.wait_for_element_displayed(*DOM.Messages.no_threads_message, timeout=2)
            x = self.marionette.find_element(*DOM.Messages.no_threads_message)
            if x.is_displayed():
	            self.UTILS.logResult("info", "(No message threads to delete.)")
        except:
            self.UTILS.logResult("info", "Deleting message threads ...")
 
            x = self.threadEditModeON()
            x = self.UTILS.getElement(DOM.Messages.check_all_threads_btn, "Select all button")
            x.tap()
             
            self.deleteSelectedThreads()
            self.UTILS.waitForElements(DOM.Messages.no_threads_message, 
                                       "No message threads notification", True, 60)
    
