from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def import_HotmailLogin(self, p_name, p_pass, p_clickSignIn=True):
        #
        # Presses the Settings button, then Hotmail, then logs in using
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
        # Press the Hotmail button.
        #
        x = self.UTILS.getElement(DOM.Contacts.hotmail_button, "Hotmail button")
        x.tap()
        
        #
        # Sometimes the device remembers your login from before (even if the device is
        # reset and all data cleared), so check for that.
        #
        self.marionette.switch_to_frame()
        try:
            el_name = "//iframe[contains(@%s, '%s')]" % \
                      (DOM.Contacts.hotmail_frame[0], DOM.Contacts.hotmail_frame[1])
            
            self.wait_for_element_present("xpath", el_name, timeout=5)
            x = self.marionette.find_element("xpath", el_name)
            if x:
                #
                # Switch to the hotmail login frame.
                #
                self.UTILS.switchToFrame(*DOM.Contacts.hotmail_frame)
                time.sleep(2)
                self.UTILS.waitForNotElements(DOM.Contacts.import_throbber, "Animated 'loading' indicator")
        
                #
                # Send the login information (sometimes the username isn't required, just the password).
                # I 'know' that the password field will appear though, so wait for that before checking
                # to see if the username field has also appeared.
                #
                self.wait_for_element_displayed(*DOM.Contacts.hotmail_password, timeout=30)
                try:
                    self.wait_for_element_displayed(*DOM.Contacts.hotmail_username, timeout=2)
                    x = self.marionette.find_element(*DOM.Contacts.hotmail_username)
                    x.send_keys(p_name)
                except:
                    pass
                
                x = self.UTILS.getElement(DOM.Contacts.hotmail_password, "Password field")
                x.send_keys(p_pass)
            
                if p_clickSignIn:
                    x = self.UTILS.getElement(DOM.Contacts.hotmail_signIn_button, "Sign In button")
                    x.tap()
                    
                    #
                    # Check to see if sigin failed. If it did then stay here.
                    #
                    try:
                        self.wait_for_element_displayed(*DOM.Contacts.hotmail_login_error_msg)
                        
                        x = self.UTILS.screenShotOnErr()
                        self.UTILS.logResult("info", "<b>Login failed!</b> Screenshot and details:", x)
                        return False
                    except:
                        pass

                    #
                    # Sometimes a message about permissions appears.
                    #
                    x=False
                    try:
                        self.wait_for_element_displayed(*DOM.Contacts.hotmail_permission_accept, timeout=2)
                        x = self.marionette.find_element(*DOM.Contacts.hotmail_permission_accept)
                    except:
                        x = False
                            
                    if x:
                        x.tap()
                        x = self.UTILS.getElement(DOM.Contacts.hotmail_password, "Password field")
                        x.send_keys(p_pass)
                        x = self.UTILS.getElement(DOM.Contacts.hotmail_signIn_button, "Sign In button")
                        x.tap()
                        self.UTILS.waitForNotElements(DOM.Contacts.import_throbber, "Animated 'loading' indicator")
            
                else:
                    return
        except:
            pass
                
        #
        # Journey back to the import iframe.
        #
        time.sleep(2)
        self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)
        self.UTILS.switchToFrame(*DOM.Contacts.hotmail_import_frame, p_viaRootFrame=False)
        
        self.UTILS.waitForElements(DOM.Contacts.import_conts_list, "Contacts list")
        
        return True