from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def deleteSelectedThreads(self):
        #
        # Delete the currently selected message threads.
        #
        self.UTILS.logResult(False, "Deleting threads is blocked by bug 879816 (and takes too long to fail!).")
        return
       
       
       
       
       
        orig_iframe = self.UTILS.currentIframe()
        x = self.UTILS.getElement(DOM.Messages.delete_threads_button, "Delete threads button")
        x.tap()
        self.UTILS.quitTest()
        
        time.sleep(1)
        self.marionette.switch_to_frame()
        x = self.UTILS.getElement(DOM.GLOBAL.modal_ok_button, "OK button in question dialog")
        x.tap()
        
        #
        # For some reason after you do this, you can't enter a 'to' number anymore.
        # After a lot of headscratching, it was just easier to re-launch the app.
        #
        time.sleep(5)
        self.launch()
        
