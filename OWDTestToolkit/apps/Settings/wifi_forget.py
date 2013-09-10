from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def wifi_forget(self, p_silent=True):
        #
        # Forget the wifi (assumes you have clicked the wifi name).<br>
        # If p_silent is True, then it will not assert if this wifi is aready known.<br>
        # If p_silent is True, then it will assert (and expect) that this wifi is already known.<br>
        # Either way, it will return True for forgotten, or False for 'not known'.
        #
        try:
        	self.wait_for_element_displayed(*DOM.Settings.wifi_details_header, timeout=2)
    	except:
    		return False
    	
        self._wifiName = self.UTILS.getElement(DOM.Settings.wifi_details_header, "Header").text
        self.UTILS.logResult("info", "Forgetting wifi '%s' ..." % self._wifiName)
        boolConnected = False
        try:
            #
            # Already connected to this wifi (or connected automatically).
            # 'Forget' it (so we can reconnect as-per test) and tap the wifi name again.
            #
            self.wait_for_element_displayed(*DOM.Settings.wifi_details_forget_btn, timeout=3)
            x = self.marionette.find_element(*DOM.Settings.wifi_details_forget_btn)
            x.tap()
            boolConnected = True
            
            #
            # Takes a few seconds to disconnect, so check a few times.
            #
            boolForgotten = False
            for i in range(1,10):
                if _checkDisconnected():
                    boolForgotten = True
                    break
                else:
                    time.sleep(2)
                
        except:
            pass
        
        if not p_silent:
            _x = "was" if boolConnected else "was not"
            _y = "and has been succesfully" if boolForgotten else "but could not be"
            
            self.UTILS.TEST(boolConnected and boolForgotten, 
						"Wifi network '%s' %s connected %s forgotten." % (self._wifiName_x,_y))
            
        return boolConnected

    def _checkDisconnected(self):
        #
        # Private function to wait until this wifi network is no longer marked as "Connected".
        #
        x = self.marionette.find_elements(*DOM.Settings.wifi_available_networks)
        for i in x:
            if i.find_element("tag name", "a").text == self._wifiName:
                if i.find_element("tag name", "small").text != "Connected":
                    return True
                    break
                else:
                    return False
                    break