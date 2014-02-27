from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def deleteSelectedThreads(self):
        #
        # Delete the currently selected message threads.
        #
        orig_iframe = self.UTILS.currentIframe()
        x = self.UTILS.getElement(DOM.Messages.delete_threads_button, "Delete threads button")
        x.tap()
#         self.marionette.execute_script("document.getElementById('threads-delete-button').click();")
        
        time.sleep(2)
        self.marionette.switch_to_frame()
        x = self.UTILS.getElement(DOM.Messages.delete_messages_ok_btn, "OK button in question dialog")
        x.tap()
#         self.marionette.execute_script("document.getElementById('modal-dialog-confirm-ok').click();")

        
        #
        # For some reason after you do this, you can't enter a 'to' number anymore.
        # After a lot of headscratching, it was just easier to re-launch the app.
        #
        time.sleep(5)
        self.launch()
        
