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
        self.UTILS.logResult("info", 
							"Currently using email account '%s' (looking to be in account '%s')." % \
							(x.text, p_address))
        if x.text == p_address:
			self.UTILS.logResult("info", "Already in the account we want - switch back to inbox.")
			self.goto_folder_from_list("Inbox")
			return True
		
        self.UTILS.logResult("info", "Need to switch from account '%s' to account '%s' ..." % \
							 		(x.text, p_address))
        
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
        try:
        	self.wait_for_element_present(*DOM.Email.accounts_list_names, timeout=2)
        	time.sleep(1)
	        x = self.marionette.find_elements(*DOM.Email.accounts_list_names)
	        for i in x:
	            if i.text != "":
	                if i.text == p_address:
	                    i.tap()
	                    
	                    self.goto_folder_from_list("Inbox")
	                    return True
        except:
        	pass
        
        #
        # It's not setup yet, so we couldn't switch.
        #
        return False


