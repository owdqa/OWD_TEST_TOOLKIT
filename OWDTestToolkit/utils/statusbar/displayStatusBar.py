from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def displayStatusBar(self):
        #
        # Displays the status / notification bar in the home screen.
        #
        # The only reliable way I have to do this at the moment is via JS
        # (tapping it only worked sometimes).
        #
        self.marionette.switch_to_frame()
        self.marionette.execute_script("window.wrappedJSObject.UtilityTray.show()")
        
        self.TEST(False, "ROY")