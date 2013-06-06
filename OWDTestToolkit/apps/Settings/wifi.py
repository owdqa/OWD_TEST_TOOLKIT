from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def wifi(self):
        #
        # Open wifi settings.
        #
        x = self.UTILS.getElement(DOM.Settings.wifi, "Wifi settings link")
        x.tap()
        
        self.UTILS.waitForElements(DOM.Settings.wifi_header, "Wifi header appears.", True, 20, False)

