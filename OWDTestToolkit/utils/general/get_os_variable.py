from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def get_os_variable(self, p_name, p_validate=True):
        #
        # Get a variable from the OS.
        #
        if p_name == "ENTER":
            return ""
        else:
            try:
                x = os.environ[p_name]
            except:
                x = False
            
            if p_validate:
                self.TEST(x, "Variable '" + p_name + "' set to: " + str(x), True)
                
            return x

    #
    # (Can't use the 'push_resource' from gaiatest because I want to use
    # *any* directory specified by the caller.)
    #
