from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def get_os_variable(self, p_name, p_validate=True):
        #
        # Get a variable from the OS.
        #
        if p_name == "ENTER":
            return ""
        else:
            x = False
            try:
                x = os.environ[p_name]
            except:
                self.logResult("info", "NOTE: OS variable '" + p_name + "' was not set.")
                
                if p_validate:
                    self.reportResults()
                    os._exit(1)
                    
                return False
                
            return x

