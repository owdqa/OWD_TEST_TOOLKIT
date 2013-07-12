from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def open_url(self, p_url):
        #
        # Open url.
        #
        x=self.UTILS.getElement(DOM.Browser.url_input, "Url input field")
        self.UTILS.logComment("Using URL " + p_url)
        x.send_keys(p_url)
        
        x=self.UTILS.getElement(DOM.Browser.url_go_button, "'Go to url' button")
        x.tap()
        
        self.UTILS.TEST(self.check_page_loaded(p_url), "Web page loaded correctly.")
        
        #
        # Take a screenshot.
        #
        fnam = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot:|" + fnam[1])
        
