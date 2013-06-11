from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def switchAccount(self, p_address):
        #
        # Add a new account.
        #
        x = self.UTILS.getElement(DOM.Email.settings_menu_btn, "Settings menu button")
        x.tap()
        
        #
        # Are we already in this account?
        #
        x = self.UTILS.getElement(DOM.GLOBAL.app_head, "Header")
        if x.text == p_address:
            # Already here - just go to the Inbox.
            self.goto_folder_from_list("Inbox")
            return True
        
        #
        # We're not in this account already, so let's look for it.
        #
        x = self.UTILS.getElement(DOM.Email.goto_accounts_btn, "Accounts button")
        x.tap()
        
        
        x = ('xpath', DOM.GLOBAL.app_head_specific % "Accounts")
        self.UTILS.waitForElements(x, "Accounts header", True, 20, False)
        
        #
        # Check if it's already set up (this may be empty, so don't test for this element).
        #
        x = self.marionette.find_elements(*DOM.Email.accounts_list_names)
        for i in x:
            if i.text != "":
                if i.text == p_address:
                    i.tap()
                    
                    self.goto_folder_from_list("Inbox")
                    return True
        
        #
        # It's not setup yet, so we couldn't switch.
        #
        return False


