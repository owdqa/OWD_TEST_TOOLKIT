from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def hotSpot(self):
        #
        # Open 'Internet sharing' settings (also known as 'hotspot').
        #
        self.marionette.execute_script("document.getElementById('%s').scrollIntoView();" % DOM.Settings.hotspot[1])

        x = self.UTILS.getElement(DOM.Settings.hotspot, "'Internet sharing' (hotspot) link")
        x.tap()
        
        self.UTILS.waitForElements(DOM.Settings.hotspot_header, "Hotspot header appears.", True, 20, False)

