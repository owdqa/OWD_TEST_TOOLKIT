from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def tap_wifi_network_name(self, p_wifi_name, p_user, p_pass):
        #
        # Select a network.
        #
        wifi_name_element = DOM.Settings.wifi_name_xpath % p_wifi_name
        x= self.UTILS.getElement(('xpath', wifi_name_element), "Wifi '" + p_wifi_name + "'", True, 30, True)
        if x:
            x.tap()
        else:
            return False
        
        #
        # In case we are asked for just password, or a username and password ...
        #
        time.sleep(2)
        try:
			try:
				self.wait_for_element_displayed(*DOM.Settings.wifi_login_user, timeout=3)
				wifi_login_user = self.marionette.find_element(*DOM.Settings.wifi_login_user)
				if wifi_login_user.is_displayed():
					wifi_login_user.send_keys(p_user)
			except:
				pass

			wifi_login_pass = self.UTILS.getElement(DOM.Settings.wifi_login_pass, "Wifi password field")
			wifi_login_pass.send_keys(p_pass)
			time.sleep(1)
			wifi_login_ok   = self.UTILS.getElement(DOM.Settings.wifi_login_ok_btn, "Ok button")
			wifi_login_ok.tap()
	        	
        except:
            #
            # We were not asked, so go back to the list.
            #
            try:
	            backBTN = self.marionette.find-element(*DOM.Settings.back_button)
	            backBTN.tap()
            except:
            	pass

            self.UTILS.TEST(self.UTILS.headerCheck("Wi-Fi"), "Header is 'Wi-Fi'.")
        
        #
        # A couple of checks to wait for 'anything' to be Connected (only look for 'present' because it
        # might be off the bottom of the page).
        #
        self.UTILS.waitForElements(DOM.Settings.wifi_connected, "Connected Wifi network", False, 60)
        
        self.UTILS.TEST(self.data_layer.get_setting("wifi.enabled"),
            "Wifi connection to '" + p_wifi_name + "' established.", True)

