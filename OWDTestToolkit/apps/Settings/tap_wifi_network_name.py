from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):
    
    def tap_wifi_network_name(self, p_wifi_name, p_user, p_pass):
        #
        # Tap a wifi network name, and log in to it.
        #
        if not self._tapWifi(p_wifi_name):
            return False
        
        #
        # We may already /automatically be connected to this wifi, be asked for just password, 
        # or be asked for a username and password ...
        #
        time.sleep(2)
        try:
        	#
        	# Already connected to this wifi (or connected automatically).
            # 'Forget' it (so we can reconnect as-per test) and tap the wifi name again.
        	#
            self.wait_for_element_displayed(*DOM.Settings.wifi_forget_btn, timeout=3)
            self.UTILS.logResult("info", 
                                 "Device automatically connected to '%s' wifi, so forgetting it to test reconnect ..." % \
                                 p_wifi_name)
            x = self.marionette.find_element(*DOM.Settings.wifi_forget_btn)
            x.tap()
            self._tapWifi(p_wifi_name)
        except:
            pass
        
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
        
        wifi_login_ok   = self.UTILS.getElement(DOM.Settings.wifi_login_ok_btn, "Ok button")
        wifi_login_ok.tap() 

        #
        # A couple of checks to wait for 'anything' to be Connected (only look for 'present' because it
        # might be off the bottom of the page).
        #
        self.UTILS.TEST(
                self.checkWifiConnected(p_wifi_name),
                "Wifi '" + p_wifi_name + "' is listed as 'connected' in wifi settings.", False)

        self.UTILS.TEST(self.data_layer.get_setting("wifi.enabled"),
            "Wifi connection to '" + p_wifi_name + "' established.", True)


    def _tapWifi(self, p_wifi_name):
        #
        # Private method to tap the network.
        #
        _wifi_name_element = ("xpath", DOM.Settings.wifi_name_xpath % p_wifi_name)
        x= self.UTILS.getElement(_wifi_name_element, "Wifi '" + p_wifi_name + "'", True, 30, True)
        if x:
            x.tap()
        else:
            return False
        
        return True


