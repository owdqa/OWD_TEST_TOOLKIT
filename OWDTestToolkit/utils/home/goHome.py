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
        
        self.switchToFrame(*DOM.Home.frame_locator, p_quitOnError=False)
            
        time.sleep(1)

