from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def isIconInStatusBar(self, p_dom):
        #
        # Check an icon is in the statusbar, then return to the
        # given frame (doesn't wait, just expects it to be there).
        #
        orig_iframe = self.currentIframe()
        self.marionette.switch_to_frame()
        
        isThere = False
        try:
            self.wait_for_element_displayed(*p_dom, timeout=1)
            isThere = True
        except:
            pass
        
        if orig_iframe:
            self.switchToFrame("src", orig_iframe)
        
        return isThere
        
