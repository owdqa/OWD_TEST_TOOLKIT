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
        self.UTILS.logResult("info", "Logging in with '%s'/'%s'." % (p_name, p_pass))

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
        self.marionette.switch_to_frame()
        try:
            self.wait_for_element_present("xpath", "//iframe[contains(@%s, '%s')]" % \
                                             (DOM.Contacts.gmail_frame[0], DOM.Contacts.gmail_frame[1]),
                                             timeout=5)

            #
            # Switch to the gmail login frame.
            #
            self.UTILS.switchToFrame(*DOM.Contacts.gmail_frame)
            
            time.sleep(2)
            self.UTILS.waitForNotElements(DOM.Contacts.import_throbber, "Animated 'loading' indicator")        
    
            #
            # PERMISSIONS (sometimes appears).
            # Seems to happen a few times, so loop through 5 just in case ...
            #
            for i in range(1,5):
                try:
                    self.wait_for_element_displayed(*DOM.Contacts.gmail_permission_accept, timeout=2)
                                
                    x = self.marionette.find_element(*DOM.Contacts.gmail_permission_accept)
                    x.tap()

                    time.sleep(2)
                    self.UTILS.waitForNotElements(DOM.Contacts.import_throbber, "Animated 'loading' indicator")
    
                except:
                    break
        
            #
            # Send the login information (the email field isn't always displayed).
            #
            self.wait_for_element_displayed(*DOM.Contacts.gmail_password, timeout=30)
            try:
                self.wait_for_element_displayed(*DOM.Contacts.gmail_username, timeout=2)
    
                x = self.marionette.find_element(*DOM.Contacts.gmail_username)
                x.send_keys(p_name)
            except:
                pass

            x = self.UTILS.getElement(DOM.Contacts.gmail_password, "Password field")
            x.send_keys(p_pass)
        
            if p_clickSignIn:
                x = self.UTILS.getElement(DOM.Contacts.gmail_signIn_button, "Sign In button")
                x.tap()
                
                #
                # Check to see if sigin failed. If it did then stay here.
                #
                try:
                    self.wait_for_element_displayed(*DOM.Contacts.gmail_login_error_msg, timeout=2)
            
                    x = self.UTILS.screenShotOnErr()
                    self.UTILS.logResult("info", "<b>Login failed!</b> Screenshot and details:", x)
                    return False
                except:
                    pass
            else:
                return True

        except:
            pass
                
        time.sleep(5)
        
        #
        # Journey back to the import iframe.
        #
        self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)
#         self.wait_for_element_present("xpath","//iframe[contains(@%s, '%s')]" % \
#                                       (DOM.Contacts.gmail_import_frame[0],DOM.Contacts.gmail_import_frame[1]),
#                                       timeout=30)

        self.UTILS.switchToFrame(*DOM.Contacts.gmail_import_frame, p_viaRootFrame=False)

        self.UTILS.waitForElements(DOM.Contacts.import_conts_list, "Contacts list", False, 2)

        return True