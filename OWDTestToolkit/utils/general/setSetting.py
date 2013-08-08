from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def setSetting(self, p_item, p_val, p_silent=False):
        #
        # Just a container function to catch any issues when using gaiatest's
        # 'set_setting()' function.
        #
        try:
            self.data_layer.set_setting(p_item, p_val)
            
            if not p_silent:
                self.logResult("info", "Setting '" + p_item + "' to '" + str(p_val) + "' returned no issues.")
                
            return True
        except:
            if not p_silent:
                self.logresult("info", "WARNING: Unable to set '" + p_item + "' to '" + str(p_val) + "'!")
                
            return False   
             
