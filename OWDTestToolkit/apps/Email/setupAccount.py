from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def setupAccount(self, p_user, p_email, p_pass):
        #
        # Set up a new email account in the email app and login.
        #

        #
        # If we've just started out, email will open directly to "New Account").
        #
        x = self.UTILS.getElement(DOM.GLOBAL.app_head, "Application header")
        if x.text.lower() != "new account":
            #
            # We have at least one emali account setup,
            # check to see if we can just switch to ours.
            #
            if self.switchAccount(p_email):
                return

            #
            # It's not setup already, so prepare to set it up!
            #
            x = self.UTILS.getElement(DOM.Email.settings_set_btn, "Settings set button")
            x.tap()

            x = self.UTILS.getElement(DOM.Email.settings_add_account_btn, "Add account button")
            x.tap()

        #
        # (At this point we are now in the 'New account' screen by one path or
        # another.)
        #
        self.UTILS.typeThis(DOM.Email.username  , "Username field", p_user , True, True)
        self.UTILS.typeThis(DOM.Email.email_addr, "Address field" , p_email, True, True)
        self.UTILS.typeThis(DOM.Email.password  , "Password field", p_pass , True, True)

        self.parent.lockscreen.unlock()
        self.marionette.switch_to_frame()
        self.UTILS.switchToFrame(*DOM.Email.frame_locator)

        #
        # (doesn't always appear when using hotmail)
        #
        try:
            self.wait_for_element_displayed(*DOM.Email.login_next_btn, timeout=5)
            btn = self.marionette.find_element(*DOM.Email.login_next_btn)
            btn.tap()
        except:
            pass

        time.sleep(1)
        x = self.UTILS.getElement(DOM.Email.login_next_btn, "'Next' button", True, 60)
        x.tap()

        time.sleep(1)
        x = self.UTILS.getElement(DOM.Email.login_next_btn, "'Next' button", True, 60)
        x.tap()

        #
        # Click the 'continue to mail' button.
        #
        time.sleep(1)
        x = self.UTILS.getElement(DOM.Email.login_cont_to_email_btn, "'Continue to mail' button", True, 60)
        x.tap()

        self.UTILS.waitForNotElements(DOM.Email.login_cont_to_email_btn, "'Continue to mail' button")

        self.UTILS.waitForElements(("xpath", "/html/body/div/div/div/div/div/a[7]/span"), "Inbox")
        time.sleep(2)