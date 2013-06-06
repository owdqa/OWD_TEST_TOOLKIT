from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):
    def disableAllNetworkSettings(self):
        #
        # Turns off all network settings (wifi, dataconn, bluetooth and airplane mode).
        #
        if self.data_layer.get_setting('ril.radio.disabled'):
            # Turn off airplane mode.
            self.data_layer.set_setting('ril.radio.disabled', False)
        if self.device.has_mobile_connection:
            # Turn off dataconn.
            self.data_layer.disable_cell_data()
        if self.device.has_wifi:
            # Turn off wifi.
            self.data_layer.disable_wifi()
        if self.data_layer.bt_is_bluetooth_enabled:
            # Turn off bluetooth.
            self.data_layer.bt_disable_bluetooth()
            
    def getNetworkConnection(self):
        #
        # Tries several methods to get ANY network connection
        # (either wifi or dataConn).
        #
        
        # make sure airplane mode is off.
        if self.isNetworkTypeEnabled("airplane"):
            self.toggleViaStatusBar("airplane")
        
        # make sure at least dataconn is on.
        if not self.isNetworkTypeEnabled("data"):
            self.toggleViaStatusBar("data")
            
            # Devic eshows data mode in status bar.
            self.waitForStatusBarNew(DOM.Statusbar.dataConn, p_timeOut=60)
            
                
    def isNetworkTypeEnabled(self, p_type):
        #
        # Returns True or False.<br><br>
        # Accepted 'types' are:<br>
        # <b>data</b><br>
        # <b>wifi</b><br>
        # <b>airplane</b><br>
        # <i>bluetooth (**NOT WORKING CURRENTLY!!**)</i>
        #
        return {
            "data"      : self.data_layer.is_cell_data_enabled,
            "wifi"      : self.data_layer.is_wifi_enabled,
            "airplane"  : self.data_layer.get_setting('ril.radio.disabled')#,
#             "bluetooth" : self.data_layer.bt_is_bluetooth_enabled
            }.get(p_type)
        
        self.TEST(False, "Incorrect parameter '" + str(p_type) + "' passed to UTILS.isNetworkTypeEnabled()!", True)
        
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
        return boolOK