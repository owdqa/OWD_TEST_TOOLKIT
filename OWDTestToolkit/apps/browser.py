import time
from OWDTestToolkit import DOM


class Browser(object):

    """Object representing the Browser application.
    """

    def __init__(self, parent):
        self.apps = parent.apps
        self.data_layer = parent.data_layer
        self.parent = parent
        self.marionette = parent.marionette
        self.UTILS = parent.UTILS

    def launch(self):
        """
        Launch the app.
        """
        self.app = self.apps.launch(self.__class__.__name__)
        self.UTILS.waitForNotElements(DOM.GLOBAL.loading_overlay, self.__class__.__name__ + " app - loading overlay")
        return self.app

    def addNewTab(self):
        """
        Adds a new tab (assume we are in the main Browser iframe).
        """
        x = self.UTILS.getElement(DOM.Browser.tab_tray_open, "Tab tray open button")
        x.tap()
        x = self.UTILS.getElement(DOM.Browser.tab_tray_new_tab_btn, "New tab button")
        x.tap()
        self.UTILS.waitForElements(DOM.Browser.url_input, "New tab")

    def check_page_loaded(self, url):
        """Check the page didn't have a problem.
        """
        self.waitForPageToFinishLoading()

        url = self.loadedURL()
        self.UTILS.logResult("info", "The loaded url is now <a href=\"{0}\">{0}</a>".format(url))

        self.UTILS.switchToFrame(*DOM.Browser.website_frame, p_viaRootFrame=False)

        # Take a screenshot.
        fnam = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot of web page in browser:|" + fnam[1])

        try:
            self.wait_for_element_present(*DOM.Browser.page_problem, timeout=1)
            x = self.marionette.find_element(*DOM.Browser.page_problem)
            if x.is_displayed():
                return False
        except Exception:
            return True

    def closeTab(self, num):
        """
        Closes the browser tab numbered num (starting at '1').
        Assumes we are in the main Browser iframe.
        """
        self.UTILS.logResult("info", "Closing tab {} ...".format(num))
        self.openTabTray()

        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot before removing tab:", x)

        # You have to do this twice for some reason.
        self.UTILS.logResult("info", "(FYI: I have to tap this icon twice, so there will be two checks below ...)")
        x = self.UTILS.getElements(DOM.Browser.tab_tray_tab_list, "Tab list (for first tap)")
        initial_count = len(x)
        close = x[num - 1].find_element(*DOM.Browser.tab_tray_tab_item_close)
        close.tap()

        x = self.UTILS.getElements(DOM.Browser.tab_tray_tab_list, "Tab list (for second tap)")
        close = x[num - 1].find_element(*DOM.Browser.tab_tray_tab_item_close)
        close.tap()

        # Wait for this tab to go.
        time.sleep(1)
        try:
            self.wait_for_element_displayed(*DOM.Browser.tab_tray_tab_list)
            x = self.UTILS.getElements(DOM.Browser.tab_tray_tab_list, "Tab list after removal")
            _after_count = len(x)
            self.UTILS.TEST(_after_count < initial_count, "The tab has been removed.")
        except Exception:
            # If this was the only tab, then we'll be taken away from the tab tray automatically.
            pass

        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot after removing tab:", x)

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
            self.UTILS.TEST(False, "(failing because an unknown tab name ('{}')\
             was passed to \"getAwesomeList()\".)".format(tab_name))
            return False

        self.UTILS.logResult("info", "Examining the list of sites for the <b>{}</b> tab ...".format(tab_name))

        self.UTILS.switchToFrame(*DOM.Browser.frame_locator)
        x = self.UTILS.getElement(DOM.Browser.url_input, "Search input field")
        x.tap()

        x = self.UTILS.getElement(details[tab]["tab"], "<b>{}</b> tab".format(tab_name))
        x.tap()
        self.UTILS.TEST(x.get_attribute("class") == "selected", "<b>{}</b> tab is selected".format(tab_name))

        x = ""
        try:
            self.wait_for_element_displayed(*details[tab]["links"], timeout=2)
            x = self.UTILS.getElements(details[tab]["links"], "{} links".format(tab_name))
        except Exception:
            self.UTILS.logResult("info", "<i>(No list items found for <b>{}</b> tab.)</i>".format(tab_name))

        return x

    def getTabNumber(self, title):
        """
        Returns the number of the browser tab with a title that contains
        title, or False if it's not found.
        It assumes we are in the main browser frame.
        """
        self.openTabTray()
        self.UTILS.waitForElements(DOM.Browser.tab_tray_screen, "Tab screen", True, 2, False)

        x = self.UTILS.getElements(DOM.Browser.tab_tray_tab_list, "Tab list")
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

        self.UTILS.waitForElements(DOM.Browser.tab_tray_screen, "Tab screen", True, 2, False)

        x = self.UTILS.getElements(DOM.Browser.tab_tray_tab_list, "Tab list")
        _title = x[num - 1].find_element(*DOM.Browser.tab_tray_tab_item_title)

        return _title.text.encode('ascii', 'ignore')

    def loadedURL(self):
        """
        Returns the url of the currently loaded web page.
        """
        self.UTILS.switchToFrame(*DOM.Browser.frame_locator)
        x = self.UTILS.getElement(("xpath", "//iframe[contains(@%s,'%s')]" % \
                                (DOM.Browser.browser_page_frame[0],
                                DOM.Browser.browser_page_frame[1])), "Loaded page", False, 1, False)
        return x.get_attribute("src")

    def open_url(self, p_url):
        """
        Open url.
        """
        self.UTILS.switchToFrame(*DOM.Browser.frame_locator)
        x = self.UTILS.getElement(DOM.Browser.url_input, "Url input field")
        self.UTILS.logComment("Using URL " + p_url)
        x.clear()
        x.send_keys(p_url)

        x = self.UTILS.getElement(DOM.Browser.url_go_button, "'Go to url' button")
        x.tap()

        self.UTILS.TEST(self.check_page_loaded(p_url), "Web page loaded correctly.")

    def openTab(self, num):
        """
        Tries to open the tab numbered num (starting at 1).
        """
        self.openTabTray()

        x = self.UTILS.getElements(DOM.Browser.tab_tray_tab_list, "Tabs list")[num - 1]
        y = x.find_element(*DOM.Browser.tab_tray_tab_item_image)
        y.tap()
        y.tap()
        time.sleep(1)

    def openTabTray(self):
        """
        Opens the tab tray (can be one of several methods).
        """
        self.UTILS.switchToFrame(*DOM.Browser.frame_locator)
        try:
            # We may already be in the 'tray' ...
            self.wait_for_element_displayed(*DOM.Browser.tab_tray_screen, timeout=1)
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
        x = self.UTILS.getElement(DOM.Browser.url_input, "Search input field")
        x.send_keys(string)
        x = self.UTILS.getElement(DOM.Browser.url_go_button, "'Go' button")
        x.tap()
        self.waitForPageToFinishLoading()

    def trayCounterValue(self):
        """
        Returns the tray counter value (filtering weird characters out).
        Assumes we are in the main browser iframe.
        The value is returned as a string rather than an int.
        """
        x = self.UTILS.getElement(DOM.Browser.tab_tray_counter, "Tab tray counter")
        y = x.text.encode('ascii', 'ignore').strip()
        z = ""
        for i in y:
            if i in "0123456789":
                z = z + i
        return z

    def waitForPageToFinishLoading(self):
        """
        Waits for the current url to finish loading.
        """
        time.sleep(3)
        try:
            self.wait_for_element_displayed(*DOM.Browser.throbber)
        except Exception:
            pass
        self.UTILS.waitForNotElements(DOM.Browser.throbber, "Animated 'wait' icon", True, 120, False)

        time.sleep(2)
