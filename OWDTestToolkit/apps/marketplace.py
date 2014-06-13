from OWDTestToolkit import DOM
from marionette.keys import Keys

from OWDTestToolkit.utils.i18nsetup import I18nSetup
_ = I18nSetup(I18nSetup).setup()


class Marketplace(object):

    def __init__(self, p_parent):
        self.apps = p_parent.apps
        self.data_layer = p_parent.data_layer
        self.parent = p_parent
        self.marionette = p_parent.marionette
        self.UTILS = p_parent.UTILS

    def launch(self):
        #
        # Launch the app.
        #
        # WARNING: Marketplace is in a weird place - you need to use "Marketplace Dev"!!
        self.UTILS.reporting.logResult("info", "About to launch the marketplace app from the dev server. "\
                       "If it's \"not found\" then either try again later, "\
                       "or contact #marketplace mozilla irc channel.")
        self.app = self.apps.launch("Marketplace")

        self.UTILS.element.waitForNotElements(DOM.Market.market_loading_icon,
                                      self.__class__.__name__ + " app - loading icon",
                                      True, 30)
        return self.app

    def install_app(self, app, author):
        #
        # Install an app.
        #
        self.search_for_app(app)

        if not self.select_search_result_app(app, author):
            self.UTILS.reporting.logResult(False, "App '" + app + "' with author '" + \
                                   author + "' is found in the market.")
            return False

        #
        # Click to install the app.
        #
        x = self.UTILS.element.getElement(DOM.Market.app_details_header, "App details header")
        self.UTILS.test.TEST(x.text == app, "Title in app details matches '" + app + "' (it was '" + x.text + "').")

        x = self.UTILS.element.getElement(DOM.Market.install_button, "Install button")

        # Sometimes this needs to be clicked ... sometimes tapped ... just do 'everything'!
        x.click()
        x.tap()

        #
        # Confirm the installation of the app.
        #
        self.marionette.switch_to_frame()

        yes_button = self.UTILS.element.getElement(DOM.Market.confirm_install_button, "Confirm install button")
        yes_button.tap()

        self.UTILS.element.waitForNotElements(DOM.Market.confirm_install_button, "Confirm install button")

        #
        # Wait for the download statusbar to finish.
        #
        self.UTILS.statusbar.displayStatusBar()
        x = ("xpath", "//div[text()='{} {}']".format(_("Downloading"), app))
        self.UTILS.element.waitForElements(x, "Download status bar")
        self.UTILS.element.waitForNotElements(x, "Download status bar", True, 180, False)
        self.UTILS.statusbar.hideStatusBar()
        return True

    def search_for_app(self, app):
        #
        # Search for an app in the market.
        #

        #
        # Scroll a little to make the search area visible.
        #
        x = self.UTILS.element.getElement(DOM.Market.search_query, "Search field")
        x.send_keys(app + Keys.RETURN)

    def select_search_result_app(self, app, author):
        #
        # Select the application we want from the list returned by
        # search_for_app().
        #
        self.UTILS.element.waitForElements(DOM.Market.search_results_area, "Search results area")
        results = self.UTILS.element.getElements(DOM.Market.search_results, "Search results")

        if len(results) <= 0:
            return False

        for app in results:
            if  app.find_element(*DOM.Market.app_name).text == app and \
                app.find_element(*DOM.Market.author).text == author:
                app.tap()
                return True

        return False
