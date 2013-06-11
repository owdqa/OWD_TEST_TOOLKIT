from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def isIconInStatusBar(self, p_dom, p_returnFrame=False):
        #
        # Check an icon is in the statusbar, then return to the
        # given frame (doesn't wait, just expects it to be there).
        #
        orig_iframe = self.currentIframe()
        self.marionette.switch_to_frame()
        x = self.marionette.find_element(*p_dom)
        isThere = x.is_displayed()
        
        if orig_iframe:
            self.switchToFrame("src", orig_iframe)
        
        return isThere
        
