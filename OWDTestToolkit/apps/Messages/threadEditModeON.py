from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def threadEditModeON(self):
        #
        # Turns on Edit mode while in the SMS threads screen.
        #
        x= self.UTILS.getElement(DOM.Messages.edit_threads_button, "Edit button" )
        x.tap()
        self.UTILS.waitForElements(DOM.Messages.cancel_edit_threads, "Cancel button")
        
