import time
from marionette import Actions
from OWDTestToolkit import DOM
from gaiatest.apps.keyboard.app import Keyboard


class Browser(object):

    """Object representing the Browser application.
    """

    search_manifest_url = "app://search.gaiamobile.org/manifest.webapp"

    def __init__(self, parent):
        self.apps = parent.apps
        self.data_layer = parent.data_layer
        self.parent = parent
        self.marionette = parent.marionette
        self.UTILS = parent.UTILS
        self.actions = Actions(self.marionette)
        self.keyboard = Keyboard(self.marionette)

    def launch(self):
        """
        Launch the app.
        """
        self.app = self.apps.launch(self.__class__.__name__)
        self.UTILS.element.waitForNotElements(DOM.GLOBAL.loading_overlay,
                                              self.__class__.__name__ + " app - loading overlay")
        return self.app

    def open_url(self, url, timeout=30, trusted=True):
        self.marionette.switch_to_frame()
        self.parent.wait_for_element_displayed(*DOM.Browser.url_input)
        url_input = self.marionette.find_element(*DOM.Browser.url_input)
        url_input.tap()

        # Now, rocketbar should be displayed
        self.parent.wait_for_element_displayed(*DOM.Browser.rocket_bar_input)
        rocket_bar_input = self.marionette.find_element(*DOM.Browser.rocket_bar_input)
        rocket_bar_input.clear()
        rocket_bar_input.send_keys(url)
        self.keyboard.tap_enter()

        self.marionette.switch_to_frame()
        self.wait_for_page_to_load()
        self.switch_to_content()

        # If the site is trusted, check for the warning and get rid of it.
        if trusted:
            # If the untrusted site warning is present, just accept it. Otherwise, silently pass.
            try:
                understand = self.marionette.find_element(*DOM.Browser.understand_risks)
                understand.tap()
                btn = self.marionette.find_element(*DOM.Browser.add_permanent_exception)
                btn.tap()
            except:
                pass

    def wait_for_page_to_load(self, timeout=30):
        self.parent.wait_for_condition(lambda m: m.find_element(
            *DOM.Browser.browser_app).get_attribute("loading-state") == "false", timeout=timeout)

    def switch_to_content(self):
        web_frames = self.marionette.find_elements(*DOM.Browser.frame_locator)
        for web_frame in web_frames:
            if web_frame.is_displayed():
                self.marionette.switch_to_frame(web_frame)
                break

    def switch_to_chrome(self):
        self.marionette.switch_to_frame()

        try:
            app_frame = self.app.frame
        except AttributeError:
            app_frame = self.apps.displayed_app.frame

        self.marionette.switch_to_frame(app_frame)

    def loaded_url(self):
        """
        Returns the url of the currently loaded web page.
        """
        web_frames = self.marionette.find_elements(*DOM.Browser.frame_locator)
        for web_frame in web_frames:
            if web_frame.is_displayed():
                return web_frame.get_attribute("src")
                
    ################################################################################
    ################################################################################
    ################################################################################


    def tap_go_button(self, timeout=30):
        self.marionette.find_element(*DOM.Browser.url_go_button).tap()
        # TODO wait_for_throbber can resolve before the page has started loading
        time.sleep(2)
        try:
            self.wait_for_throbber_not_visible(timeout=timeout)
        except:
            # maybe something went wrong, so try to find the reload button
            self.switch_to_content()
            screenshot = self.UTILS.debug.screenShotOnErr()
            self.UTILS.reporting.logResult('info', "Screenshot when failing open_url", screenshot)
            if self.is_page_not_loaded():
                self.retry_load_page()
                self.switch_to_chrome()
                self.wait_for_throbber_not_visible(timeout=timeout)

        self.parent.wait_for_element_displayed(*DOM.Browser.bookmarkmenu_button)
        self.switch_to_content()

    def wait_for_throbber_not_visible(self, timeout=30):
        # TODO see if we can reduce this timeout in the future. >10 seconds is poor UX
        self.parent.wait_for_condition(lambda m: not self.is_throbber_visible(), timeout=timeout)

    def is_page_not_loaded(self):
        try:
            self.parent.wait_for_element_displayed(*DOM.Browser.embarrasing_tag)
            self.UTILS.reporting.logResult('info', 'Page not loaded')
            return True
        except:
            self.UTILS.reporting.logResult('info', 'Page loaded')
            return False

    def retry_load_page(self):
        self.parent.wait_for_element_displayed(*DOM.Browser.embarrasing_reload)
        reload_btn = self.marionette.find_element(*DOM.Browser.embarrasing_reload)
        reload_btn.tap()

    def is_throbber_visible(self):
        return self.marionette.find_element(*DOM.Browser.throbber).get_attribute('class') == 'loading'

    def switch_to_frame_by_url(self, url, position=0):
        """
        Switch to a frame inside the browser with the given url.

        The frame with the given url will be switched to. It can be selected the position
        as well, in case there are more frames for the same url.
        Returns True if the switch was successful. False otherwise.
        """
        web_frames = self.marionette.find_elements(*DOM.Browser.frame_locator)
        result = False
        for web_frame in web_frames:
            if url in web_frame.get_attribute("src") and web_frame.is_displayed():
                result = self.marionette.switch_to_frame(web_frame)
                break
        return result
