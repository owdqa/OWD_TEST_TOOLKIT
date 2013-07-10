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
            self.logResult("info", "Switching to root-level iframe.")
            self.marionette.switch_to_frame()
            
        #
        # We need to get all of them because some apps (browser) have more than one
        # matching iframe.
        #
        if p_str == "":
            #
            # Use "=" because we want this field to be an empty string. 
            #           
            x = self.getElements( ("xpath", "//iframe[@" + p_attrib + "='" + p_str + "']"),
                                 "Iframe where '" + p_attrib + "' = '" + p_str + "'", False)
        else:
            x = self.getElements( ("xpath", "//iframe[contains(@" + p_attrib + ", '" + p_str + "')]"),
                                 "Iframe where '" + p_attrib + "' contains '" + p_str + "'", False)
        
        
        self.logResult("info", "(Switching to this frame.)")
        
        boolOK=False
        for i in x:
            try:
                self.marionette.switch_to_frame(i)
                boolOK=True
            except:
                pass
            
        self.TEST(boolOK, "Successfully switched to iframe.")
