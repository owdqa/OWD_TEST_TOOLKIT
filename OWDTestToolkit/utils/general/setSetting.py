from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def setSetting(self, p_item, p_val):
        #
        # Just a container function to catch any issues when using gaiatest's
        # 'set_setting()' function.
        #
        try:
            self.data_layer.set_setting(p_item, p_val)
            self.logResult("info", "Setting '" + p_item + "' to '" + str(p_val) + "' returned no issues.")
            return True
        except:
            self.logresult("info", "WARNING: Unable to set '" + p_item + "' to '" + str(p_val) + "'!")
            return False   
             
