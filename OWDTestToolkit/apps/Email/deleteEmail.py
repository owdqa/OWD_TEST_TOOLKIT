from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def deleteEmail(self, p_subject):
        #
        # Deletes the first message in this folder with this subject line.
        #
        
        #
        # Open the message.
        #
        self.openMsg(p_subject)

        #
        # Press the delete button and confirm deletion.
        #
        x = self.UTILS.getElement(DOM.Email.delete_this_email_btn, "Delete button")
        x.tap()
        
        #
        # Horrific, but there's > 1 button with this id and > 1 button with this text.
        # For some reason, I can't wait_for_displayed() here either, so I have to wait for the buttons
        # to be 'present' (not 'displayed'), then look through them until I find the one I want.
        #
        x = self.UTILS.getElements(DOM.Email.delete_confirm_buttons, "Confirmation buttons", False, 2, False)
        for i in x:
            if i.is_displayed() and i.text == "Delete":
                self.UTILS.logResult("info", "Clicking confirmation button.")
                # (click, not tap!)
                i.click()
                break
            
        #
        # "1 message deleted" displayed.
        #
        x = self.UTILS.getElement(DOM.Email.deleted_email_notif, "Email deletion notifier")
        
        #
        # Refresh and check that the message is no longer in the inbox.
        #
        x = self.marionette.find_element(*DOM.Email.folder_refresh_button)
        x.tap()
        time.sleep(5)
        x = self.UTILS.getElements(DOM.Email.folder_subject_list, "Email messages in this folder")

        self.UTILS.TEST(x[0].text != p_subject,
                        "Email '" + p_subject + "' no longer found in this folder.", False)
