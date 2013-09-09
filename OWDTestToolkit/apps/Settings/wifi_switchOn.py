from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def wifi_switchOn(self):
        #
        # Click slider to turn wifi on.
        #
        if not self.data_layer.get_setting("wifi.enabled"):
            x = self.UTILS.getElement(DOM.Settings.wifi_enabled, "Enable wifi switch")
            x.tap()
        
        #
        # Nothing to check for yet, because the network may require login etc...,
        # so just wait a little while before proceeding ...
        #
        time.sleep(3)
        
