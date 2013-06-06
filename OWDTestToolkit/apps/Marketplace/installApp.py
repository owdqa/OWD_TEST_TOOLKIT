from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

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

        
        
    
