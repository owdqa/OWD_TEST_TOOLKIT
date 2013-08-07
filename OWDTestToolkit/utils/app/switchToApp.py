from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def switchToApp(self, p_name):
        #
        # Switches to the app (or launches it if it's not open).
        #
        
        # Because these app aren't consistently named, or may be 'guessed'
        # incorrectly ...
        if p_name == "Dialer" or p_name == "Dialer" : p_name = "Phone"
        if p_name == "SMS"                          : p_name = "Messages"
        if p_name == "Market"                       : p_name = "Marketplace"
        
        self.touchHomeButton()
        
        # This throws an error (even though the app launches). 'Hacky', but it works.
        self.checkMarionetteOK()
        try:
            self.marionette.execute_async_script("GaiaApps.launchWithName('%s')" % p_name, script_timeout=5)
        except:
            pass

        app_dom = self._getAppDOM(p_name)
        self.switchToFrame(*app_dom)

        self.waitForNotElements(DOM.GLOBAL.loading_overlay, "%s app loading 'overlay'" % p_name)


        