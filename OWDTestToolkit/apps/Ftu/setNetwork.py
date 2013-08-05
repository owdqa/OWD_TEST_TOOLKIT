from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def setNetwork(self, p_wifiName, p_userName, p_password):
        #
        # Join a wifi network.
        #
        time.sleep(5)
        x = self.UTILS.getElements(DOM.FTU.wifi_networks_list, "Wifi network list")

        #
        # Pick the one we chose.
        #
        x= self.UTILS.getElement(('id', p_wifiName), "Wifi network '" + p_wifiName + "'")
        x.tap()
            
        #
        # In case we are asked for a username and password ...
        #
        time.sleep(2)
        try:
            self.wait_for_element_displayed(*DOM.FTU.wifi_login_user, timeout=2)
            wifi_login_user = self.marionette.find_element(*DOM.FTU.wifi_login_user)
            wifi_login_pass = self.marionette.find_element(*DOM.FTU.wifi_login_pass)
            wifi_login_join = self.marionette.find_element(*DOM.FTU.wifi_login_join)
            wifi_login_user.send_keys(p_userName)
            wifi_login_pass.send_keys(p_password)
            wifi_login_join.tap()
        except:
        	pass