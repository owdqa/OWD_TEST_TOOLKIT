from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def switchToFrame(self, p_attrib, p_str, p_quitOnError=True, p_viaRootFrame=True):
        #
        # Switch to the iframe containing the attribute value <b>p_str</b>.<br>
        # For example: ("src", "contacts") or ("src", "sms") etc...<br><br>
        # NOTE: You *usually* need to do this via the 'root' frame (almost all iframes
        # are contained in the root-level frame).
        #
        if p_viaRootFrame:
            self.logResult("debug", "(Switching to root-level iframe.)")
            self.checkMarionetteOK()
            self.marionette.switch_to_frame()
            
        #
        # We need to get all of them because some apps (browser) have more than one
        # matching iframe.
        #
        if p_str == "":
            #
            # Use "=" because we want this field to be an empty string. 
            #           
            _frameDef = ("xpath", "//iframe[@%s='%s']" % (p_attrib, p_str))
        else:
            _frameDef = ("xpath", "//iframe[contains(@%s,'%s')]" % (p_attrib, p_str))
            
        x = ""
        try:
            self.wait_for_element_displayed(*_frameDef, timeout=20)
            x = self.marionette.find_elements(*_frameDef)
        except:
            pass
            
        boolOK=False
        for i in range(0,len(x)):
            #
            # Some iframes have > 1 'version' (such as the web page frame in browser app).
            # The only way to reliably tell them apart is to switch to the displayed one.
            #
            if x[i].is_displayed():
                try:
                    self.marionette.switch_to_frame(x[i])
                    boolOK=True
                    break
                except:
                    pass
                
            x = self.marionette.find_elements(*_frameDef)
                
        #
        # If we didn't manage to switch, then try frames that are not
        # displayed (sometime this is the case).
        #
        if not boolOK:
            x = self.marionette.find_elements(*_frameDef)
            for i in range(0,len(x)):
                try:
                    self.marionette.switch_to_frame(x[i])
                    boolOK=True
                    break
                except:
                    pass

            x = self.marionette.find_elements(*_frameDef)
                
        self.TEST(boolOK, "<i>(Sucessfully switched to iframe where '%s' contains '%s' in 20s.)</i>" % (p_attrib, p_str), p_quitOnError)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        