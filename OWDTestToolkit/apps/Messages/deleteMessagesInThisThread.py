from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def deleteMessagesInThisThread(self, p_msg_array=False):
        #
        # Enters edit mode, selects the required messages and
        # deletes them.<br>
        # p_msg_array is an array of numbers. 
        # If it's not specified then all messages in this 
        # thread will be deleted.
        #
        if p_msg_array:
            self.editAndSelectMessages(p_msg_array)
        else:
            x= self.UTILS.getElement(DOM.Messages.edit_messages_icon, "Edit button" )
            x.tap()
            
            x = self.UTILS.getElement(DOM.Messages.check_all_messages_btn, "'Select all' button")
            x.tap()
            
        self.deleteSelectedMessages()
        
