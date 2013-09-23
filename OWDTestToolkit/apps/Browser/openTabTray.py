from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def openTabTray(self):
        #
        # Opens the tab tray (can be one of several methods).
        #
        self.UTILS.switchToFrame(*DOM.Browser.frame_locator)
        try:
            # We may already be in the 'tray' ...
            self.wait_for_element_displayed(*DOM.Browser.tab_tray_screen, timeout=1)
            return
        except:
            # Nope!
            try:
                x = self.marionette.find_element(*DOM.Browser.tab_tray_counter)
                x.tap()
            except:
                x = self.marionette.find_element(*DOM.Browser.tab_tray_open)
                x.tap()
