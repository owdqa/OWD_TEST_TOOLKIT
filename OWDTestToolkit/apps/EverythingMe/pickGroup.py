from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def pickGroup(self, p_name):
        #
        # Pick a group from the main icons.
        #
        x = self.UTILS.getElements(DOM.EME.groups, "EME group list")
        boolOK = False
        for groupLink in x:
            if groupLink.get_attribute("data-query") == p_name:
                groupLink.tap()
                time.sleep(10)
                boolOK = True
                break
        
        #
        # At this point the geolocation sometimes wants to know
        # if it can remember our location.
        #
        self.UTILS.clearGeolocPermission()
        
        return boolOK
    
