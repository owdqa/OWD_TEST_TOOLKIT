from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def remove_accounts_and_restart(self):
        #
        # Remove current email accounts via the UI and restart the application.
        # <br><br>
        # <b>NOTE:</b> Currently broken due to https://bugzilla.mozilla.org/show_bug.cgi?id=849183
        # so it's been set to do nothing!
        #
        return

        
        try:
            #
            # Make sure we're starting from the beginning ...
            # (it might not be running, so ignore any errors here).
            #
            self.marionette.kill("Email")
        except:
            pass
        
        self.launch()

        try:
            x = self.UTILS.waitForElements(("xpath", "//h1[text()='Inbox']"), "Inbox header", 10)
        except:
            #
            # We have no accounts set up (or the app would default to
            # the inbox of one of them).
            #
            self.UTILS.logResult("info", "(No email accounts set up yet.)")
            return
                
        x = self.UTILS.getElement(DOM.Email.settings_menu_btn, "Settings button")
        x.tap()
        
        x = self.UTILS.getElement(DOM.Email.settings_set_btn, "Set settings button")
        x.tap()
        
        x=('xpath', DOM.GLOBAL.app_head_specific % "Mail Settings")
        self.UTILS.waitForElements(x, "Mail settings", True, 20, False)
        
        #
        # Remove each email address listed ...
        #
        x = self.UTILS.getElements(DOM.Email.email_accounts_list,
                                   "Email accounts list", False, 20, False)
        for i in x:
            if i.text != "":
                # This isn't a placeholder, so delete it.
                self.UTILS.logComment("i: " + i.text)
                i.tap()
                
                x = ('xpath', DOM.GLOBAL.app_head_specific % i.text)
                self.UTILS.waitForElements(x, i.text + " header", True, 20, False)
                
                # Delete.
                delacc = self.UTILS.getElement(DOM.Email.settings_del_acc_btn, "Delete account button")
                delacc.tap()
                time.sleep(2)
                
                # Confirm.  <<<< PROBLEM (on forums)!
                delconf = self.UTILS.getElement(DOM.Email.settings_del_conf_btn, "Confirm delete button")
                delconf.tap()
                
                # Wait for this dialog to go away, then sleep for 1s.
        
        #
        # Now relaunch the app.
        #
        self.launch()
    
