from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def clearAllStatusBarNotifs(self, p_silent=False):
        #
        # Opens the statusbar, presses "Clear all", then closes the status bar.<br>
        # <b>p_silent</b> will supress any pass/fail (useful if this isn't relevant
        # to the test, or if you're just using it for a bit of housekeeping).
        #
        if p_silent:
            try:
                self.displayStatusBar()
                self.wait_for_element_displayed(*DOM.Statusbar.clear_all_button, timeout=1)
                x = self.marionette.find_element(*DOM.Statusbar.clear_all_button)
                x.tap()
                time.sleep(1)
                self.hideStatusBar()
            except:
                pass
        else:
            self.displayStatusBar()
            x = self.getElement(DOM.Statusbar.clear_all_button, "'Clear all' button")
            x.tap()
            time.sleep(1)
            self.hideStatusBar()

        
