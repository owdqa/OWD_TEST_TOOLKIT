from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def holdHomeButton(self):
        #
        # Long hold the home button to bring up the 'current running apps'.
        #
        self.marionette.switch_to_frame()
        self.marionette.execute_script("window.wrappedJSObject.dispatchEvent(new Event('holdhome'));")
    
