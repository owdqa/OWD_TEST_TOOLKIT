from global_imports import *
from gaiatest import GaiaTestCase

class main(GaiaTestCase):
    def scrollHomescreenRight(self):
        #
        # Scroll to next page (right).
        # Should change this to use marionette.flick() when it works.
        #
        self.marionette.execute_script('window.wrappedJSObject.GridManager.goToNextPage()')
    
    def scrollHomescreenLeft(self):
        #
        # Scroll to previous page (left).
        # Should change this to use marionette.flick() when it works.
        #
        self.marionette.execute_script('window.wrappedJSObject.GridManager.goToPreviousPage()')
    
    def touchHomeButton(self):
        #
        # Touch the home button (sometimes does something different to going home).
        #
        self.marionette.switch_to_frame()
        self.marionette.execute_script("window.wrappedJSObject.dispatchEvent(new Event('home'));")
    
    def holdHomeButton(self):
        #
        # Long hold the home button to bring up the 'current running apps'.
        #
        self.marionette.switch_to_frame()
        self.marionette.execute_script("window.wrappedJSObject.dispatchEvent(new Event('holdhome'));")
    
    def goHome(self):
        #
        # Return to the home screen.
        #
        
        # (Sometimes the home button needs to be tapped twice, i.e. if you're
        # in a results screen of EME.)
        self.touchHomeButton()
        self.touchHomeButton()
        
        self.apps.kill_all()
        self.marionette.switch_to_frame()
        
        self.switchToFrame(*DOM.Home.homescreen_iframe, p_quitOnError=False)
            
        time.sleep(1)

