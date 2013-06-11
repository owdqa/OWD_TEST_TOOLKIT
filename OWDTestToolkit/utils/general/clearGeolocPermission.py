from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def clearGeolocPermission(self, p_allow=False):
        #
        # Since this appers all over the place I've added this
        # as a common method in UTILS.<br>
        # This method clears the Geolocation permission dialog
        # (if necessary) with p_allow.
        #
        orig_frame = self.currentIframe()
        self.marionette.switch_to_frame()
        try:
            if p_allow:
                x = self.marionette.find_element("id", "permission-yes")
            else:
                x = self.marionette.find_element("id", "permission-no")
                
            x.tap()
            
        except:
            pass
        
        self.switchToFrame("src", orig_frame)
        
    
