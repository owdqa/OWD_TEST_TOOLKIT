from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def wifi_list_isConnected(self, p_name, p_timeOut=30):
        #
        # Verify the expected network is listed as connected in 'available networks'.
        #        
        try:
        	self.wait_for_element_present("xpath", DOM.Settings.wifi_list_connected_xp % p_name, timeout=p_timeOut)
        	return True
        except:
        	return False
