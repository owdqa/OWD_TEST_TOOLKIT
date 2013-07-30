from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def importFromGmail_login(self, p_name, p_pass):
        #
        # Presses the Settings button, then Gmail, then logs in using
        # p_name and p_pass (to begin the process of importing contacts).
        #
        x = self.UTILS.getElement(DOM.Contacts.settings_button, "Settings button")
        x.tap()
        
        #
        # Press the Gmail button.
        #
        x = self.UTILS.getElement(DOM.Contacts.gmail_button, "Gmail button")
        x.tap()
        
        #
        # Switch to the gmail login frame.
        #
        self.UTILS.switchToFrame(*DOM.Contacts.gmail_frame)
        time.sleep(2)
        self.UTILS.waitForNotElements(DOM.Contacts.gmail_throbber, "Animated 'loading' indicator")        

        #
        # Send the login information.
        #        
        x = self.UTILS.getElement(DOM.Contacts.gmail_username, "Email field")
        x.send_keys(p_name)
        x = self.UTILS.getElement(DOM.Contacts.gmail_password, "Password field")
        x.send_keys(p_pass)
        x = self.UTILS.getElement(DOM.Contacts.gmail_signIn_button, "Sign In button")
        x.tap()
        
        
        