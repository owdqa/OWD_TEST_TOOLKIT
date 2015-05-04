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
        app_header = self.UTILS.element.getElement(DOM.Market.app_details_header, "App details header")
        self.UTILS.test.test(app_header.text == app, "Title in app detail is {} (expected: {})".\
                             format(app_header.text, app))

        install_btn = self.UTILS.element.getElement(DOM.Market.install_button, "Install button")

        # Sometimes this needs to be clicked ... sometimes tapped ... just do 'everything'!
        install_btn.tap()

        #
        # Confirm the installation of the app.
        #
        self.marionette.switch_to_frame()

        yes_button = self.UTILS.element.getElement(DOM.Market.confirm_install_button, "Confirm install button")
        yes_button.tap()

        self.marionette.switch_to_frame()
        msg = "{} installed".format(app)
        installed_app_msg = (DOM.GLOBAL.system_banner_msg[0], DOM.GLOBAL.system_banner_msg[1].format(msg))
        self.UTILS.element.waitForElements(installed_app_msg, msg, timeout=60)
        return True

    def search_for_app(self, app):
        #
        # Search for an app in the market.
        #
        self.UTILS.iframe.switchToFrame(*DOM.Market.frame_locator, via_root_frame=False)
        self.UTILS.reporting.debug("*** Searching {}".format(app))
        search_field = self.UTILS.element.getElement(DOM.Market.search_query, "Search field", timeout=30)
        self.UTILS.reporting.debug("*** Search field: {}".format(search_field))
        search_field.send_keys(app + Keys.RETURN)

    def select_search_result_app(self, app, author):
        #
        # Select the application we want from the list returned by
        # search_for_app().
        #
        self.UTILS.element.waitForElements(DOM.Market.search_results_area, "Search results area")
        results = self.UTILS.element.getElements(DOM.Market.search_results, "Search results")

        if len(results) <= 0:
            return False

        for result in results:
            if  result.find_element(*DOM.Market.app_name).text == app and \
                result.find_element(*DOM.Market.author).text == author:
                result.tap()
                return True

        return False
