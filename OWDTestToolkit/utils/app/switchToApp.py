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
        
        app_frame = self._getAppFrame(p_name)
        
        self.marionette.switch_to_frame()
        try:
            self.wait_for_element_present("xpath", "//iframe[contains(@%s, '%s')]" % (app_frame[0], app_frame[1]), timeout=1)
            self.logResult("info", "(Looks like app '%s' is already running - just switching to it's iframe ...)" % p_name)
            self.switchToFrame(*app_frame)
        except:
            #
            # The app isn't open yet, so try to launch it.
            #
            # (This throws an error, even though the app launches. 'Hacky', but it works.)
            try:
                self.logResult("info", "(Looks like app '%s' is not currently running, so I'll launch it.)" % p_name)
                self.apps.launch(p_name)
#                 self.marionette.execute_async_script("GaiaApps.launchWithName('%s')" % p_name, script_timeout=5)
                self.waitForNotElements(DOM.GLOBAL.loading_overlay, "%s app loading 'overlay'" % p_name)
                self.switchToFrame(*app_frame)
            except:
                pass




        