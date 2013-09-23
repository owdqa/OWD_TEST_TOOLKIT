from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def openTab(self, p_num):
        #
        # Tries to open the tab p_num (starting at 1).
        #
        self.openTabTray()

        x = self.UTILS.getElements(DOM.Browser.tab_tray_tab_list, "Tabs list")[p_num-1]
        y = x.find_element(*DOM.Browser.tab_tray_tab_item_image)
        y.tap()
        y.tap()
        time.sleep(1)
        

