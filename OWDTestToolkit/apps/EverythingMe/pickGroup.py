from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def pickGroup(self, p_name):
        #
        # Pick a group from the main icons.
        #
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "<b>Choosing group '%s' from here ...</b>" % p_name, x)
        x = self.UTILS.getElements(DOM.EME.groups, "EME group list")
        boolOK = False
        for i in range(0,len(x)):
            if x[i].get_attribute("data-query") == p_name:
            	self.UTILS.logResult("info", "Group found - tapping it ...")
                x[i].tap()
                
                # I've had 'odd' problems with this tap not doing anything
                # randomly, so I'm adding another chance.
                boolChk = False
                try:
                	self.wait_for_element_present(*DOM.EME.apps_not_installed, timeout=10)
            	except:
            		x = self.marionette.find_elements(*DOM.EME.groups)
            		if x[i].is_displayed():
            			x[i].tap()

        		break
            		
    	try:
    		self.wait_for_element_displayed(*DOM.EME.apps_not_installed, timeout=20)
    		self.UTILS.logResult("info", "(Apps for group %s were displayed.)" % p_name)
    		boolOK = True
    	except:
			x = self.UTILS.screenShotOnErr()
			self.UTILS.logResult("info", "(<b>NOTE:</b>Apps for group %s were not displayed.)|%s|%s" % \
								(p_name,x[0],x[1]))
        
        #
        # At this point the geolocation sometimes wants to know
        # if it can remember our location.
        #
        self.UTILS.clearGeolocPermission()
        
        
        return boolOK
    
