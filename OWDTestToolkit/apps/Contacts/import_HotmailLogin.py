from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def import_HotmailLogin(self, p_name, p_pass, p_clickSignIn=True):
        #
        # Presses the Settings button in the contacts app, then Hotmail, then logs in using
        # p_name and p_pass (to begin the process of importing contacts).
        # <br>
        # If p_clickSignIn is set to True then this method will also click
        # the Sign in button (defaults to true).
        # <br>
        # Returns False if the login failed, "ALLIMPORTED" if all your contacts are already imported else True.
        #
        x = self.UTILS.getElement(DOM.Contacts.settings_button, "Settings button")
        x.tap()
        
        #
        # Press the Hotmail button.
        #
        x = self.UTILS.getElement(DOM.Contacts.hotmail_button, "Hotmail button")
        x.tap()

        #
        # Login.
        #
        login_success = self._login(p_name, p_pass, p_clickSignIn)
        if not login_success:
            return False

        if not p_clickSignIn:
            #
            # If we're just entering the login details but not clicking sign in, 
            # then here's where we finish.
            #
            return True
                
        #
        # Go to the hotmail import iframe.
        #
        time.sleep(2)
        self.UTILS.checkMarionetteOK()
        self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)
        self.UTILS.switchToFrame(*DOM.Contacts.hotmail_import_frame, p_viaRootFrame=False)
        
        #
        # Check to see if the 'all friends are imported' message is being
        # displayed.
        #
        all_imported = self._check_all_friends_imported()
    
        if all_imported:
            return "ALLIMPORTED"
        
        #
        # Wait for the hotmail contacts for this p_user to be displayed.
        #
        self.UTILS.waitForElements(DOM.Contacts.import_conts_list, "Contacts list")
    
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Contacts list in the Hotmail / Outlook app:", x)
        
        return True
    
    
    
    def _login(self, p_name, p_pass, p_clickSignIn):
        #
        # Sometimes the device remembers your login from before (even if the device is
        # reset and all data cleared), so check for that.
        #
        self.marionette.switch_to_frame()
        try:
            el_name = "//iframe[contains(@%s, '%s')]" % \
                      (DOM.Contacts.hotmail_frame[0], DOM.Contacts.hotmail_frame[1])
            
            self.wait_for_element_present("xpath", el_name, timeout=5)

            #
            # Switch to the hotmail login frame.
            #
            self.UTILS.switchToFrame(*DOM.Contacts.hotmail_frame)
            time.sleep(2)
            self.UTILS.waitForNotElements(DOM.Contacts.import_throbber, "Animated 'loading' indicator")
        
            #
            # Send the login information (sometimes the username isn't required, just the password).
            # I 'know' that the password field will appear though, so use that element to get the
            # timing right.
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
                # Check to see if sigin failed. If it did then return False.
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
                self._permission_check()
        except:
            pass
        
        return True


    def _permission_check(self):
        #
        # Sometimes hotmail asks for permission - just accept it if it's there.
        #
        try:
            self.wait_for_element_displayed(*DOM.Contacts.hotmail_permission_accept, timeout=2)
    
            x = self.marionette.find_element(*DOM.Contacts.hotmail_permission_accept)
            x.tap()
            x = self.UTILS.getElement(DOM.Contacts.hotmail_password, "Password field")
            x.send_keys(p_pass)
            x = self.UTILS.getElement(DOM.Contacts.hotmail_signIn_button, "Sign In button")
            x.tap()
            self.UTILS.waitForNotElements(DOM.Contacts.import_throbber, "Animated 'loading' indicator")
        except:
            pass



    def _check_all_friends_imported(self):
        #
        # Check to see if the message "All your friends are imported" is being displayed.
        #
        boolYES = False
        try:
            x = self.UTILS.screenShotOnErr() # For some reaosn this is needed before the message can be seen!
            self.wait_for_element_displayed(*DOM.Contacts.import_all_imported_msg, timeout=2)
            boolYES = True
        except:
            pass
        
        if boolYES:
            self.UTILS.logResult("info", 
                                 "<b>NOTE:</b> Apparently all your friends are already imported - " + \
                                 "see the following screenshots for details", x)
            
            self.marionette.execute_script("document.getElementById('%s').click()" % DOM.Contacts.import_close_icon[1])
            time.sleep(1)
#             x = self.UTILS.getElement(DOM.Contacts.import_close_icon, "Close icon")
#             x.tap()
            
            #
            # Switch back to the contacts app frame and wait for the hotmail frame to go away.
            #
            self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)
            time.sleep(1)
            
            #
            # Close the settings screen.
            #
            x = self.UTILS.getElement(DOM.Contacts.settings_done_button, "Contacts app settings 'done' button")
            x.tap()

            #
            # Record the contacts we currently have imported (in case this test fails and this is why).
            #
            self.UTILS.waitForElements(DOM.Contacts.view_all_header, "All contacts main screen", True, 2)
                        
            x = self.UTILS.screenShotOnErr()
            self.UTILS.logResult("info", 
                                 "<b>NOTE:</b> Apparently all your friends are imported from hotmail. " +\
                                 "These are the contacts you have in the Contacts app:", x)
            
            return True
        else:
            return False



        