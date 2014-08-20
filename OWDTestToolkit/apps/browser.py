import time
from OWDTestToolkit import DOM
from gaiatest.apps.keyboard.app import Keyboard


class Browser(object):

    """Object representing the Browser application.
    """

    def __init__(self, parent):
        self.apps = parent.apps
        self.data_layer = parent.data_layer
        self.parent = parent
        self.marionette = parent.marionette
        self.UTILS = parent.UTILS
        self.keyboard = Keyboard(self.marionette)

    def launch(self):
        """
        Launch the app.
        """
        self.app = self.apps.launch(self.__class__.__name__)
        self.UTILS.element.waitForNotElements(DOM.GLOBAL.loading_overlay,
                                              self.__class__.__name__ + " app - loading overlay")
        return self.app

    def addNewTab(self):
        """
        Adds a new tab (assume we are in the main Browser iframe).
        """
        x = self.UTILS.element.getElement(DOM.Browser.tab_tray_open, "Tab tray open button")
        x.tap()
        x = self.UTILS.element.getElement(DOM.Browser.tab_tray_new_tab_btn, "New tab button")
        x.tap()
        self.UTILS.element.waitForElements(DOM.Browser.url_input, "New tab")

    def closeTab(self, num):
        """
        Closes the browser tab numbered num (starting at '1').
        Assumes we are in the main Browser iframe.
        """
        self.UTILS.reporting.logResult("info", "Closing tab {} ...".format(num))
        self.openTabTray()

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot before removing tab:", x)

        # You have to do this twice for some reason.
        self.UTILS.reporting.logResult("info", "(I have to tap this icon twice, so there will be two checks below...)")
        x = self.UTILS.element.getElements(DOM.Browser.tab_tray_tab_list, "Tab list (for first tap)")
        initial_count = len(x)
        close = x[num - 1].find_element(*DOM.Browser.tab_tray_tab_item_close)
        close.tap()

        x = self.UTILS.element.getElements(DOM.Browser.tab_tray_tab_list, "Tab list (for second tap)")
        close = x[num - 1].find_element(*DOM.Browser.tab_tray_tab_item_close)
        close.tap()

        # Wait for this tab to go.
        time.sleep(1)
        try:
            self.parent.wait_for_element_displayed(*DOM.Browser.tab_tray_tab_list)
            x = self.UTILS.element.getElements(DOM.Browser.tab_tray_tab_list, "Tab list after removal")
            _after_count = len(x)
            self.UTILS.test.TEST(_after_count < initial_count, "The tab has been removed.")
        except Exception:
            # If this was the only tab, then we'll be taken away from the tab tray automatically.
            pass

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Screenshot after removing tab:", x)

    def getAwesomeList(self, tab_name):
        """Returns a list of elements from the awesomescreen tabs.

        tab_name must be one of: "top sites", "bookmarks", "history"

        These elements have some handy attributes:
        href - containing the url (may have 'extra' info in it, so use 'x in y').
        .find_element("tag name","h5") - contains the title of this page.
        """
        details = {}
        details["top_sites"] = {"tab": DOM.Browser.awesome_top_sites_tab,
                                 "links": DOM.Browser.awesome_top_sites_links}
        details["bookmarks"] = {"tab": DOM.Browser.awesome_bookmarks_tab,
                                 "links": DOM.Browser.awesome_bookmarks_links}
        details["history"] = {"tab": DOM.Browser.awesome_history_tab,
                               "links": DOM.Browser.awesome_history_links}

        # Make sure the input is correct.
        tab = tab_name.lower().replace(" ", "_")
        try:
            _blah = details[tab]
        except Exception:
            self.UTILS.test.TEST(False, "(failing because an unknown tab name ('{}')\
             was passed to \"getAwesomeList()\".)".format(tab_name))
            return False

        self.UTILS.reporting.logResult("info", "Examining the list of sites for the <b>{}</b> tab ...".format(tab_name))

        self.UTILS.iframe.switchToFrame(*DOM.Browser.frame_locator)
        x = self.UTILS.element.getElement(DOM.Browser.url_input, "Search input field")
        x.tap()

        x = self.UTILS.element.getElement(details[tab]["tab"], "<b>{}</b> tab".format(tab_name))
        x.tap()
        self.UTILS.test.TEST(x.get_attribute("class") == "selected", "<b>{}</b> tab is selected".format(tab_name))

        x = ""
        try:
            self.parent.wait_for_element_displayed(*details[tab]["links"], timeout=2)
            x = self.UTILS.element.getElements(details[tab]["links"], "{} links".format(tab_name))
        except Exception:
            self.UTILS.reporting.logResult("info", "<i>(No list items found for <b>{}</b> tab.)</i>".format(tab_name))

        return x

    def getTabNumber(self, title):
        """
        Returns the number of the browser tab with a title that contains
        title, or False if it's not found.
        It assumes we are in the main browser frame.
        """
        self.openTabTray()
        self.UTILS.element.waitForElements(DOM.Browser.tab_tray_screen, "Tab screen", True, 2, False)

        x = self.UTILS.element.getElements(DOM.Browser.tab_tray_tab_list, "Tab list")
        found = False
        for i in range(len(x)):
            _title = x[i].find_element(*DOM.Browser.tab_tray_tab_item_title)
            _title = _title.text.encode('ascii', 'ignore')
            if title.lower() in _title.lower():
                found = i
                break
        return found

    def getTabTitle(self, num):
        """
        Returns the title of tab numbered num (assume we are in the main browser frame).
        """
        self.openTabTray()

        self.UTILS.element.waitForElements(DOM.Browser.tab_tray_screen, "Tab screen", True, 2, False)

        x = self.UTILS.element.getElements(DOM.Browser.tab_tray_tab_list, "Tab list")
        _title = x[num - 1].find_element(*DOM.Browser.tab_tray_tab_item_title)

        return _title.text.encode('ascii', 'ignore')

    def loaded_url(self):
        """
        Returns the url of the currently loaded web page.
        """
        web_frames = self.marionette.find_elements(*DOM.Browser.website_frame)
        for web_frame in web_frames:
            if web_frame.is_displayed():
                return web_frame.get_attribute("src")

    def open_url(self, url, timeout=30):
        # """
        # Open url.
        # """
        
        self.switch_to_chrome()

        self.parent.wait_for_element_displayed(*DOM.Browser.url_input)
        self.marionette.find_element(*DOM.Browser.url_input).tap()
        self.keyboard.send(url)
        self.tap_go_button(timeout=timeout)

        self.check_page_loaded(url, False)
        self.switch_to_content()


    def check_page_loaded(self, url, check_throbber=True):
        self.switch_to_chrome()

        if check_throbber:
            self.wait_for_throbber_not_visible()
        
        url_value = self.loaded_url()
        
        if url_value:
            self.UTILS.test.TEST(url in url_value, "Loaded URL matches the desired URL")
        else:
            self.UTILS.test.TEST(False, "Loaded URL matches the desired URL")


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

    def switch_to_content(self):
        web_frames = self.marionette.find_elements(*DOM.Browser.website_frame)
        for web_frame in web_frames:
            if web_frame.is_displayed():
                self.marionette.switch_to_frame(web_frame)
                break

    def switch_to_chrome(self):
        self.marionette.switch_to_frame()
        self.marionette.switch_to_frame(self.app.frame)

    def openTab(self, num):
        """
        Tries to open the tab numbered num (starting at 1).
        """
        self.openTabTray()

        x = self.UTILS.element.getElements(DOM.Browser.tab_tray_tab_list, "Tabs list")[num - 1]
        y = x.find_element(*DOM.Browser.tab_tray_tab_item_image)
        y.tap()
        y.tap()
        time.sleep(1)

    def openTabTray(self):
        """
        Opens the tab tray (can be one of several methods).
        """
        self.UTILS.iframe.switchToFrame(*DOM.Browser.frame_locator)
        try:
            # We may already be in the 'tray' ...
            self.parent.wait_for_element_displayed(*DOM.Browser.tab_tray_screen, timeout=1)
            return
        except Exception:
            try:
                x = self.marionette.find_element(*DOM.Browser.tab_tray_counter)
                x.tap()
            except:
                x = self.marionette.find_element(*DOM.Browser.tab_tray_open)
                x.tap()

    def searchUsingUrlField(self, string):
        """
        Searches for string using the URL field.
        """
        x = self.UTILS.element.getElement(DOM.Browser.url_input, "Search input field")
        x.send_keys(string)
        x = self.UTILS.element.getElement(DOM.Browser.url_go_button, "'Go' button")
        x.tap()
        self.wait_for_throbber_not_visible()

    def trayCounterValue(self):
        """
        Returns the tray counter value (filtering weird characters out).
        Assumes we are in the main browser iframe.
        The value is returned as a string rather than an int.
        """
        x = self.UTILS.element.getElement(DOM.Browser.tab_tray_counter, "Tab tray counter")
        y = x.text.encode('ascii', 'ignore').strip()
        z = ""
        for i in y:
            if i in "0123456789":
                z = z + i
        return z

    def addCurrentPageToBookmarks(self):
        """
        Adds the current page to bookmarks and checks that it was correctly added
        """
        self.UTILS.iframe.switchToFrame(*DOM.Browser.frame_locator)

        #
        # Add the page to the bookmark
        #
        x = self.UTILS.element.getElement(DOM.Browser.bookmarkmenu_button, "Bookmark button")
        x.tap()

        x = self.UTILS.element.getElement(DOM.Browser.bookmark_button, "Bookmark button")
        x.tap()

        x = self.UTILS.element.getElement(DOM.Browser.url_input, "Bookmark button")
        x.tap()

        x = self.UTILS.element.getElement(DOM.Browser.bookmarks_tab, "Bookmark tab")
        x.tap()

        #
        # Very that the bookmark is correctly created
        #
        self.UTILS.element.waitForElements(DOM.Browser.bookmark_item1, "Bookmark")
