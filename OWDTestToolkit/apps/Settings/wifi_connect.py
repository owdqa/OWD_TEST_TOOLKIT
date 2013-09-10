from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):
    
    def wifi_connect(self, p_wifi_name, p_user, p_pass):
        #
        # Connects to the wifi specified in the parameters using the Settings app.
        # Launches Settings if it's not already running.
        #
        
        #
        # Are we in the settings app?
        #
        if self.UTILS.framePresent(*DOM.Settings.frame_locator):
            self.UTILS.switchToFrame(*DOM.Settings.frame_locator)
            try:
                self.wait_for_element_displayed(*DOM.Settings.wifi)
                self.wifi()
            except:
                pass
        else:
            self.launch()
            self.wifi()
            
        self.wifi_switchOn() 
                        
        self.wifi_list_tapName(p_wifi_name)        
        
        if self.wifi_forget():
            self.wifi_list_tapName(p_wifi_name)
        
        try:
        	#
        	# Asked for username.
        	#
            self.wait_for_element_displayed(*DOM.Settings.wifi_login_user, timeout=3)
            wifi_login_user = self.marionette.find_element(*DOM.Settings.wifi_login_user)
            if wifi_login_user.is_displayed():
                wifi_login_user.send_keys(p_user)
                self.UTILS.logResult("info", 
                                     "Username '%s' supplied to connect to '%s' wifi." % \
                                     (p_user, p_wifi_name))
        except:
            pass
        
        try:
            #
            # Asked for password.
            #
            wifi_login_pass = self.marionette.find_element(*DOM.Settings.wifi_login_pass)
            wifi_login_pass.send_keys(p_pass)
            time.sleep(1)
            self.UTILS.logResult("info", 
                                 "Password '%s' supplied to connect to '%s' wifi." % \
                                 (p_pass, p_wifi_name))
        except:
            pass
        
        try:
            wifi_login_ok = self.marionette.find_element(*DOM.Settings.wifi_login_ok_btn)
            wifi_login_ok.tap()
            self.UTILS.logResult("info", "Ok button pressed.")
        except:
            pass

        #
        # A couple of checks to wait for 'anything' to be Connected (only look for 'present' because it
        # might be off the bottom of the page).
        #
        self.UTILS.TEST(
                self.wifi_list_isConnected(p_wifi_name, p_timeOut=60),
                "Wifi '" + p_wifi_name + "' is listed as 'connected' in wifi settings.", False)

        self.UTILS.TEST(self.data_layer.get_setting("wifi.enabled"),
            "Wifi connection to '" + p_wifi_name + "' established.", True)



