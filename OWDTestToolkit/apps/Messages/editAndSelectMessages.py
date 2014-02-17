from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def editAndSelectMessages(self, p_msg_array):
        #
        # Puts this thread into Edit mode and selects
        # the messages listed in p_msg_array.<br>
        # p_msg_array is an array of numbers.
        #
        
        #
        # Go into messages Settings..
        #
        x= self.UTILS.getElement(DOM.Messages.edit_messages_icon, "Edit button" )
        x.tap()

        #
        # Go into message edit mode..
        #
        x= self.UTILS.getElement(DOM.Messages.delete_messages_btn, "Edit button")
        x.tap()
        
        #
        # Check the messages (for some reason, just doing x[i].click() doesn't
        # work for element zero, so I had to do this 'longhanded' version!).
        #
        x = self.UTILS.getElements(DOM.Messages.message_list, "Messages")
        y = 0
        for i in x:
            if y in p_msg_array:
                self.UTILS.logResult("info", "Selecting message " + str(y) + " ...")
                i.click()
            
            y = y + 1
        
