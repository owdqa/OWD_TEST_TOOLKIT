from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def deleteSelectedMessages(self):
        #
        # Delete the currently selected messages in this thread.
        #
        x= self.UTILS.getElement(DOM.Messages.delete_messages_button, "Delete message" )
        x.tap()
        
        self.marionette.switch_to_frame()
        x = self.UTILS.getElement(DOM.GLOBAL.modal_ok_button, "OK button in question dialog")
        x.tap()
        self.UTILS.switchToFrame(*DOM.Messages.frame_locator)
        time.sleep(2)
        
    
