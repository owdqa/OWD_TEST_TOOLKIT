from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def setDataConnEnabled(self):
        #
        # Enable data.
        #
        
        self.UTILS.waitForElements(DOM.FTU.section_cell_data, "Cellular data connection section")

        # (the switch has an "id", but if you use that it never becomes 'visible'!)
        x = self.UTILS.getElement(DOM.FTU.dataconn_switch, "Data connection switch")
        x.tap()
        
        # Wait a moment, then check data conn is on.
        time.sleep(3)
        self.UTILS.TEST(
            self.data_layer.get_setting("ril.data.enabled"),    
            "Data connection is enabled after trying to enable it.", True)
        
