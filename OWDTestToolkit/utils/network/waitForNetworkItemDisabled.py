from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def waitForNetworkItemDisabled(self, p_type, p_timeOut=60):
        #
        # Waits for network 'item' to be disabled.
        # <br><br>
        # Accepted 'types' are:<br>
        # <b>data</b><br>
        # <b>wifi</b><br>
        # <b>airplane</b><br>
        # <b>bluetooth</b>
        #
        boolOK = False
        for i in range(1,(p_timeOut/2)):
            if not self.isNetworkTypeEnabled(p_type):
                boolOK = True
                break
            time.sleep(2)
        self.TEST(boolOK, "'" + p_type + "' mode disabled within " + str(p_timeOut) + " seconds.")
