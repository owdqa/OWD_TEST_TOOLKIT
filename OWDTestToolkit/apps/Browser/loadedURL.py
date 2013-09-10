from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def loadedURL(self):
        #
        # Returns the url of the currently loaded web page.
        #
        self.UTILS.switchToFrame(*DOM.Browser.frame_locator)
        x = self.UTILS.getElement(("xpath", "//iframe[contains(@%s,'%s')]" % \
                                (DOM.Browser.browser_page_frame[0],
                                DOM.Browser.browser_page_frame[1])), "Loaded page", False, 1, False)
        return x.get_attribute("src")
        
