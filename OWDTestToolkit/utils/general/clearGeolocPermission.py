from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def clearGeolocPermission(self, p_allow=False):
        #
        # Since this appers all over the place I've added this
        # as a common method in UTILS.<br>
        # This method clears the Geolocation permission dialog
        # (if necessary) with p_allow.
        #
        permission_yes = ("id", "permission-yes")
        permission_no  = ("id", "permission-no")
        orig_frame = self.currentIframe()
        self.marionette.switch_to_frame()
        try:
            if p_allow:
                self.wait_for_element_displayed(*permission_yes, timeout=2)
                x = self.marionette.find_element(*permission_yes)
            else:
                self.wait_for_element_displayed(*permission_no, timeout=2)
                x = self.marionette.find_element(*permission_no)
                
            x.tap()
            
        except:
            pass
        
        self.switchToFrame("src", orig_frame)
        
    
