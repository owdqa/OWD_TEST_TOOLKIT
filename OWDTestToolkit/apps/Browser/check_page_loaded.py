from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def check_page_loaded(self, p_url):
        #
        # Check the page didn't have a problem.
        #
        self.waitForPageToFinishLoading()
        
        _url = self.loadedURL()
        self.UTILS.logResult("info", "FYI: The loaded url is now <a href=\"%s\">%s</a>" % (_url,_url))
                
        self.UTILS.switchToFrame(*DOM.Browser.website_frame, p_viaRootFrame=False)

		#
		# Take a screenshot.
		#
        fnam = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot of web page in browser:|" + fnam[1])
		        
        try:
            self.wait_for_element_present(*DOM.Browser.page_problem, timeout=1)
            x = self.marionette.find_element(*DOM.Browser.page_problem)
            if x.is_displayed():
                return False
        except:
            return True
