from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def waitForNetworkItemEnabled(self, p_type, p_timeOut=60):
        #
        # Waits for network 'item' to be enabled.
        # <br><br>
        # Accepted 'types' are:<br>
        # <b>data</b><br>
        # <b>wifi</b><br>
        # <b>airplane</b><br>
        # <b>bluetooth</b>
        #
        boolOK = False
        for i in range(1,(p_timeOut/2)):
            if self.isNetworkTypeEnabled(p_type):
                boolOK = True
                break
            time.sleep(2)
        self.TEST(boolOK, "'" + p_type + "' mode enabled within " + str(p_timeOut) + " seconds.")
        return boolOK

