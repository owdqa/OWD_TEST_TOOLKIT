from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def wifi_forget(self, p_silent=True):
		#
		# Forget the wifi 8assumes you have clicked the wifi name).<br>
		# If p_silent is True, then it will not assert if this wifi is aready known.<br>
		# If p_silent is True, then it will assert (and expect) that this wifi is already known.<br>
		# Either way, it will return True for forgotten, or False for 'not known'.
		#
		boolConnected = False
		try:
			#
			# Already connected to this wifi (or connected automatically).
			# 'Forget' it (so we can reconnect as-per test) and tap the wifi name again.
			#
			self.wait_for_element_displayed(*DOM.Settings.wifi_details_forget_btn, timeout=3)
			x = self.marionette.find_element(*DOM.Settings.wifi_details_forget_btn)
			x.tap()
			boolConnected = True
		except:
			pass
		
		if not p_silent:
			self.UTILS.TEST(boolConnected, "Wifi network was connected, but is now forgotten.")
			
		return boolConnected