from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def deleteSelectedMessages(self):
        #
        # Delete the currently selected messages in this thread.
        #
        x= self.UTILS.getElement(DOM.Messages.edit_msgs_delete_btn, "Delete message" )
        x.tap()

        #
        # Press OK button to confirm. OK button is displayed on top_level frame.
        #
        self.marionette.switch_to_frame()
        x = self.UTILS.getElement(DOM.Messages.delete_messages_ok_btn, "OK button in question dialog")
        x.tap()

        #self.UTILS.switchToFrame(*DOM.Messages.frame_locator)
        time.sleep(2)
        
    
