from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def setPermission(self, p_app, p_item, p_val, p_silent=False):
        #
        # Just a container function to catch any issues when using gaiatest's
        # 'set_permission()' function.
        #
        try:
            self.apps.set_permission(p_app, p_item, p_val)

            if not p_silent:
                self.logResult("info", "Setting  permission for app '" + p_app + \
                               "' -> '" + p_item + \
                               "' to '" + \
                               str(p_val) + "' returned no issues.")
            return True
        except:
            if not p_silent:
                self.logresult("info", "WARNING: unable to set  permission for app '" + p_app + \
                               "' -> '" + p_item + \
                               "' to '" + \
                               str(p_val) + "'!")
            return False
            