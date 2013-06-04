import time
from gaiatest   import GaiaTestCase
from marionette import Marionette
from OWDTestToolkit import *
from marionette.keys import Keys

class AppMarket(GaiaTestCase):
    
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
        self.app = self.apps.launch('Marketplace')
        self.UTILS.waitForNotElements(DOM.GLOBAL.loading_overlay, "Market app - loading overlay");
        self.UTILS.switchToFrame(*DOM.Market.frame_locator)
                    
    def searchForApp(self, p_app):
        #
        # Search for an app in the market.
        #

        #
        # Scroll a little to make the search area visible.
        #
# Changed to a frame-in-frame so can't be used like this just now.
#         self.marionette.execute_script('window.scrollTo(0, 10)')        
#         
#         from marionette.keys import Keys
#         self.UTILS.typeThis(DOM.Market.search_query, 
#                             "Search field",
#                             p_app + Keys.RETURN)
        
        x = self.UTILS.getElement(DOM.Market.search_query, "Search field")
        x.send_keys(p_app + Keys.RETURN)


    def selectSearchResultApp(self, p_app, p_author):
        #
        # Select the application we want from the list returned by
        # searchForApp().
        #
        self.UTILS.waitForElements(DOM.Market.search_results_area, "Search results area")
        results = self.UTILS.getElements(DOM.Market.search_results, "Search results")
        
        if len(results) <= 0:
            return False
        
        for app in results:
            if  app.find_element(*DOM.Market.app_name).text == p_app and \
                app.find_element(*DOM.Market.author).text == p_author:
                app.tap()
                return True
            
        return False


    def installApp(self, p_app, p_author):
        #
        # Install an app.
        #
        self.searchForApp(p_app)
        
        if not self.selectSearchResultApp(p_app, p_author):
            self.UTILS.logResult(False, "App '" + p_app + "' with author '" + \
                                   p_author + "' is found in the market.")
            return False
        
        #
        # Click to install the app.
        #
        x = self.UTILS.getElement(DOM.Market.app_details_header, "App details header")
        self.UTILS.TEST(x.text == p_app, "Title in app details matches '" + p_app + "' (it was '" + x.text + "').")
        
        x = self.UTILS.getElement(DOM.Market.install_button, "Install button")
        
        # Sometimes this needs to be clicked ... sometimes tapped ... just do 'everything'!
        x.click()
        x.tap()

        #
        # Confirm the installation of the app.
        #
        self.marionette.switch_to_frame()

        yes_button = self.UTILS.getElement(DOM.Market.confirm_install_button, "Confirm install button")
        yes_button.tap()

        self.UTILS.waitForNotElements(DOM.Market.confirm_install_button, "Confirm install button")

        #
        # Wait for the download statusbar to finish.
        #        
        self.UTILS.displayStatusBar()
        x = ("xpath", "//div[text()='Downloading %s']" % p_app)
        self.UTILS.waitForElements(x, "Download status bar")
        self.UTILS.waitForNotElements(x, "Download status bar", True, 180, False)
        self.UTILS.hideStatusBar()
        
        return True

        
        
    
