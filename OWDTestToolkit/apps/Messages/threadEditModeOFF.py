from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def threadEditModeOFF(self):
        #
        # Turns off Edit mode while in the SMS threads screen.
        #
        x= self.UTILS.getElement(DOM.Messages.cancel_edit_threads, "Cancel button" )
        x.tap()
        self.UTILS.waitForElements(DOM.Messages.edit_threads_button, "Edit button")
        
