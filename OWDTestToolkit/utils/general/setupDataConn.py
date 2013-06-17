from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def setupDataConn(self):
        #
        # Set the phone's time (using gaia data_layer instead of the UI).
        #
        APN  = "telefonica.es"
        ID   = "telefonica"
        PASS = "telefonica"
        HOST = "10.138.255.133"
        PORT = "8080"
        
        self.logResult("info", "ENSURING DATA CONN SETTINGS ARE CORRECT.")
        logstr = "Before ..."
        logstr = logstr + "|APN            = \"" + self.data_layer.get_setting("ril.data.apn") + "\""
        logstr = logstr + "|Identifier     = \"" + self.data_layer.get_setting("ril.data.user") + "\""
        logstr = logstr + "|Password       = \"" + self.data_layer.get_setting("ril.data.passwd") + "\""
        logstr = logstr + "|HTTPproxy_host = \"" + self.data_layer.get_setting("ril.data.httpProxyHost") + "\""
        logstr = logstr + "|HTTPproxy_port = \"" + self.data_layer.get_setting("ril.data.httpProxyPort") + "\""
        self.logResult("info", logstr)

        self.data_layer.set_setting("ril.data.apn"          , APN)
        self.data_layer.set_setting("ril.data.user"         , ID)
        self.data_layer.set_setting("ril.data.passwd"       , PASS)
        self.data_layer.set_setting("ril.data.httpProxyHost", HOST)
        self.data_layer.set_setting("ril.data.httpProxyPort", PORT)

        logstr = "After ..."
        logstr = logstr + "|APN            = \"" + self.data_layer.get_setting("ril.data.apn") + "\""
        logstr = logstr + "|Identifier     = \"" + self.data_layer.get_setting("ril.data.user") + "\""
        logstr = logstr + "|Password       = \"" + self.data_layer.get_setting("ril.data.passwd") + "\""
        logstr = logstr + "|HTTPproxy_host = \"" + self.data_layer.get_setting("ril.data.httpProxyHost") + "\""
        logstr = logstr + "|HTTPproxy_port = \"" + self.data_layer.get_setting("ril.data.httpProxyPort") + "\""
        self.logResult("info", logstr)

