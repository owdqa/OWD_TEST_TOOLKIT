from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

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

