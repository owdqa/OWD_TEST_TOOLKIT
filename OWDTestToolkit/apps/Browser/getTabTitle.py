from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):
        
    def getTabTitle(self, p_num):
        #
        # Returns the title of tab p_num (assume we are in the main browser frame).
        #
        try:
            # We may already be in the 'tray' ...
            self.wait_for_element_displayed(*DOM.Browser.tab_tray_screen, timeout=1)
        except:
            # Nope!
            x = self.UTILS.getElement(DOM.Browser.tab_tray_open, "Tab tray open button")
            x.tap()
            
        self.UTILS.waitForElements(DOM.Browser.tab_tray_screen, "Tab screen", True, 2, False)

        x      = self.UTILS.getElements(DOM.Browser.tab_tray_tab_list, "Tab list")
        _title = x[p_num-1].find_element(*DOM.Browser.tab_tray_tab_item_title)
        
        return _title.text.encode('ascii', 'ignore')

