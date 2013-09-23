from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def openTab(self, p_num):
        #
        # Tries to open the tab p_num (starting at 1).
        #
        self.UTILS.switchToFrame(*DOM.Browser.frame_locator)
        
        try:
            # We may already be in the 'tray' ...
            self.wait_for_element_displayed(*DOM.Browser.tab_tray_screen, timeout=1)
        except:
            # Nope!
            x = self.UTILS.getElement(DOM.Browser.tab_tray_open, "Tab tray open button")
            x.tap()

        x = self.UTILS.getElements(DOM.Browser.tab_tray_tab_list, "Tabs list")[p_num-1]
        y = x.find_element(*DOM.Browser.tab_tray_tab_item_image)
        y.tap()
        y.tap()
        time.sleep(1)
        

