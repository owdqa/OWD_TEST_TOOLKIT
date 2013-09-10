from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def framePresent(self, p_attrib, p_str, p_viaRootFrame=True):
        #
        # Checks for the presence of an iframe containing the attribute value <b>p_str</b>.<br>
        # For example: ("src", "contacts") or ("src", "sms") etc...<br><br>
        # NOTE: You *usually* need to do this via the 'root' frame (almost all iframes
        # are contained in the root-level frame).<br><br>
        # Performs this 'silently' and just returns True or False.
        #
        if p_viaRootFrame:
            self.checkMarionetteOK()
            self.marionette.switch_to_frame()
            
        if p_str == "":
            #
            # Use "=" because we want this field to be an empty string. 
            #           
            _frameDef = ("xpath", "//iframe[@%s='%s']" % (p_attrib, p_str))
        else:
            _frameDef = ("xpath", "//iframe[contains(@%s,'%s')]" % (p_attrib, p_str))
            
        x = ""
        try:
            self.wait_for_element_present(*_frameDef, timeout=2)
            return True
        except:
            return False
            
        
        
        
        
        