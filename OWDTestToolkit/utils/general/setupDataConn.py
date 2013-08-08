from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def setupDataConn(self):
        #
        # Set the phone's details for data conn (APN etc...).
        #
        APN  = "telefonica.es"
        ID   = "telefonica"
        PASS = "telefonica"
        HOST = "10.138.255.133"
        PORT = "8080"
        
        self.logResult("info", "Ensuring dataconn settings (APN etc...) are correct.")

        self._setIt("ril.data.apn"          , APN)
        self._setIt("ril.data.user"         , ID)
        self._setIt("ril.data.passwd"       , PASS)
        self._setIt("ril.data.httpProxyHost", HOST)
        self._setIt("ril.data.httpProxyPort", PORT)

        self.logResult("info", "Done.")

    def _setIt(self, p_item, p_val):
        #
        # Just a quick function to report issues setting this.
        #
        try: self.data_layer.set_setting(p_item, p_val)
        except: self.logResult(False, "Unable to set '" + p_item + "' to '" + p_val + "'.")
