from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def wifi_list_tapName(self, p_wifi_name):
		#
		# Tap the network name in the list.
		#
		_wifi_name_element = ("xpath", DOM.Settings.wifi_name_xpath % p_wifi_name)
		x= self.UTILS.getElement(_wifi_name_element, "Wifi '" + p_wifi_name + "'", True, 30, True)
		
		x.tap()

		time.sleep(2)
