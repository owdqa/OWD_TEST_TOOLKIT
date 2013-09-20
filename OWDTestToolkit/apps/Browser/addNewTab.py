from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def addNewTab(self):
        #
        # Adds a new tab (assume we are in the main Browser iframe).
        #
        x = self.UTILS.getElement(DOM.Browser.tab_tray_open, "Tab tray open button")
        x.tap()
        x = self.UTILS.getElement(DOM.Browser.tab_tray_new_tab_btn, "New tab button")
        x.tap()
        self.UTILS.waitForElements(DOM.Browser.url_input, "New tab")
