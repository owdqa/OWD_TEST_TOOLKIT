import time
from gaiatest   import GaiaTestCase
from marionette import Marionette
from OWDTestToolkit import *

class AppBrowser(GaiaTestCase):
    
    #
    # When you create your instance of this class, include the
    # "self" object so we can access the calling class' objects.
    #
    def __init__(self, p_parent):
        self.apps       = p_parent.apps
        self.data_layer = p_parent.data_layer
        self.marionette = p_parent.marionette
        self.UTILS      = p_parent.UTILS

    def launch(self):
        #
        # Launch the app.
        #
        self.apps.kill_all()
        self.app = self.apps.launch('Browser')
        self.UTILS.waitForNotElements(DOM.GLOBAL.loading_overlay, "Browser app - loading overlay");

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
        
    def waitForPageToFinishLoading(self):
        #
        # Waits for the current url to finish loading.
        #
        self.UTILS.waitForElements(   DOM.Browser.throbber, "Animated 'wait' icon", True, 5, False)
        self.UTILS.waitForNotElements(DOM.Browser.throbber, "Animated 'wait' icon", True, 90, False)
        
    
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
        self.UTILS.switchToFrame(*DOM.Browser.website_frame)
        
#         time.sleep(10)

        try:
            x = self.marionette.find_element(*DOM.Browser.page_problem)
            if x.is_displayed():
                return False
        except:
            return True
