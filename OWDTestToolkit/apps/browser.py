import time
from marionette import Actions
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
        self.actions = Actions(self.marionette)

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
            self.UTILS.test.test(_after_count < initial_count, "The tab has been removed.")
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
            self.UTILS.test.test(False, "(failing because an unknown tab name ('{}')\
             was passed to \"getAwesomeList()\".)".format(tab_name))
            return False

        self.UTILS.reporting.logResult(
            "info", "Examining the list of sites for the <b>{}</b> tab ...".format(tab_name))

        self.UTILS.iframe.switchToFrame(*DOM.Browser.frame_locator)
        x = self.UTILS.element.getElement(DOM.Browser.url_input, "Search input field")
        x.tap()

        x = self.UTILS.element.getElement(details[tab]["tab"], "<b>{}</b> tab".format(tab_name))
        x.tap()
        self.UTILS.test.test(x.get_attribute("class") == "selected", "<b>{}</b> tab is selected".format(tab_name))

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

    def open_url(self, url, timeout=30, trusted=True):
        """
        Open url.
        """

        self.switch_to_chrome()

        self.parent.wait_for_element_displayed(*DOM.Browser.url_input)
        url_input = self.marionette.find_element(*DOM.Browser.url_input)
        url_input.clear()
        url_input.send_keys(url)
        self.tap_go_button(timeout=timeout)

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

        self.check_page_loaded(url, False)
        self.switch_to_content()

    def check_page_loaded(self, url, check_throbber=True):
        self.switch_to_chrome()

        if check_throbber:
            self.wait_for_throbber_not_visible()

        url_value = self.loaded_url()

        if url_value:
            self.UTILS.test.test(url in url_value, "Loaded URL matches the desired URL")
            return True
        else:
            self.UTILS.test.test(False, "Loaded URL matches the desired URL")
            return False

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

    def switch_to_frame_by_url(self, url, position=0):
        """
        Switch to a frame inside the browser with the given url.

        The frame with the given url will be switched to. It can be selected the position
        as well, in case there are more frames for the same url.
        Returns True if the switch was successful. False otherwise.
        """
        web_frames = self.marionette.find_elements(*DOM.Browser.website_frame)
        result = False
        for web_frame in web_frames:
            if url in web_frame.get_attribute("src") and web_frame.is_displayed():
                result = self.marionette.switch_to_frame(web_frame)
                break
        return result

    def switch_to_chrome(self):
        self.marionette.switch_to_frame()

        try:
            app_frame = self.app.frame
        except AttributeError:
            app_frame = self.apps.displayed_app.frame

        self.marionette.switch_to_frame(app_frame)

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

        # Add the page to the bookmark
        bookmarkmenu_button = self.UTILS.element.getElement(DOM.Browser.bookmarkmenu_button, "Bookmark menu button")
        bookmarkmenu_button.tap()

        bookmark_button = self.UTILS.element.getElement(DOM.Browser.bookmark_button, "Bookmark button")
        bookmark_button.tap()

        # Check the page has been added as a bookmark. For that, we have to tap on the url input field and then
        # on the bookmark tab that will appear
        url_input = self.UTILS.element.getElement(DOM.Browser.url_input, "url input")
        url_input.tap()
        url_value = url_input.get_attribute("value")

        bookmark_tab = self.UTILS.element.getElement(DOM.Browser.bookmarks_tab, "Bookmark tab")
        bookmark_tab.tap()

        # Verify that the bookmark is correctly created
        elem = (DOM.Browser.bookmark_item[0], DOM.Browser.bookmark_item[1].format(url_value))
        self.UTILS.element.waitForElements(elem, "Bookmark just added", timeout=10)

    def delete_bookmark(self, url=None, title=None):
        """Delete a bookmark by title or by URL.

        One of the url or title parameters must be given for a bookmark to be deleted.
        If none of them is present, the function will return.
        If both of them are present, url is used.
        """
        if title is None and url is None:
            self.UTILS.reporting.debug("No url nor title were provided, so no bookmark is to be deleted")
            return

        self.UTILS.iframe.switchToFrame(*DOM.Browser.frame_locator)

        # Tap in the address bar to get tabs menu
        url_input = self.UTILS.element.getElement(DOM.Browser.url_input, "URL input")
        url_input.tap()

        # Open the bookmarks tab
        bookmarks_tab = self.UTILS.element.getElement(DOM.Browser.awesome_bookmarks_tab, "Bookmarks tab")
        bookmarks_tab.tap()

        # Locate the bookmark by url or by title
        bookmark = None
        if url is not None:
            self.UTILS.reporting.debug("** Looking for bookmark with url [{}]".format(url))
            bookmark = self.UTILS.element.getElementByXpath(DOM.Browser.bookmark_item[1].format(url))
        else:
            self.UTILS.reporting.debug("** Looking for bookmark with title [{}]".format(title))
            bookmark = self.UTILS.element.getElementByXpath(DOM.Browser.bookmark_by_title[1].format(title))

        # No bookmark found. Log condition and return.
        if not bookmark:
            self.UTILS.reporting.debug("No bookmark was found for url [{}] and title [{}]".format(url, title))
            return

        # Perform a long press over the bookmark, to let the unbookmark menu appear
        self.actions.long_press(bookmark, 2).perform()
        unbookmark = self.UTILS.element.getElement(DOM.Browser.bookmark_remove_btn, "Unbookmark button")
        unbookmark.tap()
