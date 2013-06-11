from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def cellular_and_data(self):
        #
        # Open cellular and data settings.
        #
        x = self.UTILS.getElement(DOM.Settings.cellData, "Cellular and Data settings link")
        x.tap()
        
        self.UTILS.waitForElements(DOM.Settings.celldata_header, "Celldata header", True, 20, False)

