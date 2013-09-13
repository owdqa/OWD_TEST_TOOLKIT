from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def touchHomeButton(self):
        #
        # Touch the home button (sometimes does something different to going home).
        #
        self.marionette.switch_to_frame()
        self.marionette.execute_script("window.wrappedJSObject.dispatchEvent(new Event('home'));")
