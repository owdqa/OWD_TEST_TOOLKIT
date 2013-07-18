from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def check_page_loaded(self, p_url):
        #
        # Check the page didn't have a problem.
        #

        #
        # Switch to the browser content frame and check the contents.
        #
        # The "src" will have the protocol on the front, such as "http://" or "https://" or whatever.
        # It could also expand to have more on the end of the url, which basically makes it a bit
        # unpredictable, so I'm using the class name.
        # However, if you decide to use it in the future, here's how:
#        iframe_dom = ("xpath", "//iframe[contains(@src,'%s')]" % p_url)
#        ... do the 'wait_for_element...' part. If that passes:
#        x = self.marionette.find_element(*iframe_dom)
#        self.UTILS.switchToFrame("src", x.get_attribute("src"))        iframe_dom = ("class name", "browser-tab")

        self.waitForPageToFinishLoading()
        
        self.UTILS.switchToFrame(*DOM.Browser.website_frame, p_viaRootFrame=False)

		#
		# Take a screenshot.
		#
        fnam = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot:|" + fnam[1])
		        
#         time.sleep(10)

        try:
            x = self.marionette.find_element(*DOM.Browser.page_problem)
            if x.is_displayed():
                return False
        except:
            return True
