from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def waitForStatusBarNew(self, p_dom=DOM.Statusbar.status_bar_new, p_displayed=True, p_timeOut=20):
        #
        # Waits for a new notification in the status bar (20s timeout by default).
        #
        orig_iframe = self.currentIframe()
        self.marionette.switch_to_frame()

        x = self.waitForElements(p_dom,
                             "This statusbar icon",
                             p_displayed,
                             p_timeOut)
        
        # Only switch if not called from the 'start' screen ...
        if orig_iframe != '':
            self.switchToFrame("src", orig_iframe, False)

        return x