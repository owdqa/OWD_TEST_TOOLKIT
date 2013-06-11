from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

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
        
