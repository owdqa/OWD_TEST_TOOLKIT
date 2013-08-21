from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def pickGroup(self, p_name):
        #
        # Pick a group from the main icons.
        #
        self.UTILS.logResult("info", "<b>Choosing group '%s' ...</b>" % p_name)
        x = self.UTILS.getElements(DOM.EME.groups, "EME group list")
        boolOK = False
        for groupLink in x:
            if groupLink.get_attribute("data-query") == p_name:
            	self.UTILS.logResult("info", "Group found - tapping it ...")
                groupLink.tap()
#                 time.sleep(10)
                
                # I've had 'odd' problems with this tap not doing anything
                # randomly, so I'm adding another chance.
                boolChk = False
                try:
                	self.wait_for_element_present(*DOM.EME.apps, timeout=10)
                	boolChk = True
            	except:
            		pass
            	if not boolChk:
            		groupLink.tap()
            		
            	self.UTILS.waitForElements(DOM.EME.apps, "Apps list for group %s" % p_name)
            		
            	
                boolOK = True
                break
        
        #
        # At this point the geolocation sometimes wants to know
        # if it can remember our location.
        #
        self.UTILS.clearGeolocPermission()
        
        
        return boolOK
    
