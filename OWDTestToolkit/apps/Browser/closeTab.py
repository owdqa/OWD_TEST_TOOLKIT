from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def closeTab(self, p_num):
        #
        # Closes the browser tab p_num (starting at '1').
        # Assumes we are in the main Browser iframe.
        #
        self.UTILS.logResult("info", "Closing tab %s ..." % p_num)
        self.openTabTray()

        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot before removing tab:", x)

        #
        # You have to do this twice for some reaosn.
        #
        self.UTILS.logResult("info", "(FYI: I have to tap this icon twice, so there will be two checks below ...)")
        x = self.UTILS.getElements(DOM.Browser.tab_tray_tab_list, "Tab list (for first tap)")
        _initial_count = len(x)
        _close = x[p_num-1].find_element(*DOM.Browser.tab_tray_tab_item_close)
        _close.tap()

        x = self.UTILS.getElements(DOM.Browser.tab_tray_tab_list, "Tab list (for second tap)")
        _close = x[p_num-1].find_element(*DOM.Browser.tab_tray_tab_item_close)
        _close.tap()
        
        #
        # Wait for this tab to go.
        #
        time.sleep(1)
        try:
            self.wait_for_element_displayed(*DOM.Browser.tab_tray_tab_list)
            
            x = self.UTILS.getElements(DOM.Browser.tab_tray_tab_list, "Tab list after removal")
            _after_count = len(x)
            self.UTILS.TEST(_after_count < _initial_count, "The tab has been removed.")
        except:
            #
            # If this was the only tab, then we'll be taken away from the tab tray automatically.
            #
            pass

        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot after removing tab:", x)

