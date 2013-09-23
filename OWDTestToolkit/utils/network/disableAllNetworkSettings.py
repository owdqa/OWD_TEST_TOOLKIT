from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def disableAllNetworkSettings(self):
        #
        # Turns off all network settings (wifi, dataconn, bluetooth and airplane mode).
        #
        if self.data_layer.get_setting('ril.radio.disabled'):
            self.data_layer.set_setting('ril.radio.disabled', False)

        if self.device.has_mobile_connection:
            self.data_layer.disable_cell_data()

        self.data_layer.disable_cell_roaming()

        if self.device.has_wifi:
            self.checkMarionetteOK()            
            try:    self.data_layer.enable_wifi()
            except: self.logResult(False, "Enabled wifi")
            
            self.checkMarionetteOK()            
            try:    self.data_layer.forget_all_networks()
            except: self.logResult(False, "Forgot all wifi networks")
                        
            self.checkMarionetteOK()
            try:    self.data_layer.disable_wifi()
            except: self.logResult(False, "Disabled wifi")
