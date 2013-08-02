from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def import_GmailLogin(self, p_name, p_pass, p_clickSignIn=True):
        #
        # Presses the Settings button, then Gmail, then logs in using
        # p_name and p_pass (to begin the process of importing contacts).
        # <br>
        # If p_clickSignIn is set to True then this method will also click
        # the Sign in button (defaults to true).
        # <br>
        # Returns False if the login failed, else True.
        #
        x = self.UTILS.getElement(DOM.Contacts.settings_button, "Settings button")
        x.tap()
        
        #
        # Press the Gmail button.
        #
        x = self.UTILS.getElement(DOM.Contacts.gmail_button, "Gmail button")
        x.tap()
        
        #
        # Sometimes the device remembers your login from before (even if the device is
        # reset and all data cleared), so check for that.
        #
        time.sleep(5)
        self.marionette.switch_to_frame()
        try:
            x = self.marionette.find_element("xpath", "//iframe[contains(@%s, '%s')]" % \
                                             (DOM.Contacts.gmail_frame[0], DOM.Contacts.gmail_frame[1]))
            if x:
                #
                # Switch to the gmail login frame.
                #
                self.UTILS.switchToFrame(*DOM.Contacts.gmail_frame)
                time.sleep(2)
                self.UTILS.waitForNotElements(DOM.Contacts.import_throbber, "Animated 'loading' indicator")        
        
                #
                # Sometimes a message about permissions appears (since this is the only place
                # I think I'll need this DOM def, I'm just putting it here).
                # Seems to happen a few times, so loop through 5 just in case ...
                #
                for i in range(1,5):
                    try:
                        x = self.marionette.find_element("id", "submit_approve_access")
                    except:
                        x = False
                        
                    if x:
                        x.tap()
                        time.sleep(2)
                        self.UTILS.waitForNotElements(DOM.Contacts.import_throbber, "Animated 'loading' indicator")
                    else:
                        break
        
                #
                # Send the login information.
                #        
                x = self.UTILS.getElement(DOM.Contacts.gmail_username, "Email field")
                x.send_keys(p_name)
                x = self.UTILS.getElement(DOM.Contacts.gmail_password, "Password field")
                x.send_keys(p_pass)
            
                if p_clickSignIn:
                    x = self.UTILS.getElement(DOM.Contacts.gmail_signIn_button, "Sign In button")
                    x.tap()
                    
                    #
                    # Check to see if sigin failed. If it did then stay here.
                    #
                    try:
                        self.wait_for_element_displayed(*DOM.Contacts.gmail_login_error_msg)
                        
                        x = self.UTILS.screenShotOnErr()
                        self.UTILS.logResult("info", "<b>Login failed!</b> Screenshot and details:", x)
                        return False
                    except:
                        pass

                else:
                    return
        except:
            pass
                
        time.sleep(2)
        
        #
        # Journey back to the import iframe.
        #
        self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)
        self.UTILS.switchToFrame(*DOM.Contacts.gmail_import_frame, p_viaRootFrame=False)
        
        self.UTILS.waitForElements(DOM.Contacts.import_conts_list, "Contacts list")
        
        return True