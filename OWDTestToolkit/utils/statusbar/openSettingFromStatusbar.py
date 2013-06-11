from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def openSettingFromStatusbar(self):
        #
        # As it says on the tin - opens the settings
        # app via the statusbar.
        #
        self.displayStatusBar()
        x = self.getElement(DOM.Statusbar.settings_button, "Settings button")
        x.tap()
        
        time.sleep(2)
        
        self.marionette.switch_to_frame()
        self.switchToFrame(*DOM.Settings.frame_locator)
        
