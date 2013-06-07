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
            
