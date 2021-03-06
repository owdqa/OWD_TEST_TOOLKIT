import time
from OWDTestToolkit import DOM
from gaiatest.apps.system.app import System
from OWDTestToolkit.utils.decorators import retry


class statusbar(object):

    def __init__(self, parent):
        self.parent = parent
        self.marionette = parent.marionette
        self.system = System(self.marionette)

    def clearAllStatusBarNotifs(self):
        """Open the system tray and clear all notifications.
        """
        self.marionette.switch_to_frame()
        utility_tray = self.system.open_utility_tray()
        # utility_tray.wait_for_notification_container_displayed()
        # Gaiatestcase wait_for_notification_container_displayed not working properly
        # so we have to manually wait some time in order to make sure the statusbar
        # is fully shown
        time.sleep(2)
        utility_tray.clear_all_notifications()

    def displayStatusBar(self):
        """
        Displays the status / notification bar in the home screen.
        The only reliable way I have to do this at the moment is via JS
        (tapping it only worked sometimes).
        """
        self.marionette.switch_to_frame()
        self.marionette.execute_script("window.wrappedJSObject.UtilityTray.show()")
        time.sleep(0.5)

    def hideStatusBar(self):
        """
        Displays the status / notification bar in the home screen.
        The only reliable way I have to do this at the moment is via JS
        (tapping it only worked sometimes).
        """
        self.marionette.switch_to_frame()
        self.marionette.execute_script("window.wrappedJSObject.UtilityTray.hide()")

    def isIconInStatusBar(self, p_dom):
        """
        Check an icon is in the statusbar, then return to the
        given frame (doesn't wait, just expects it to be there).
        """
        orig_iframe = self.parent.iframe.currentIframe()
        self.marionette.switch_to_frame()

        found = False
        try:
            self.parent.parent.wait_for_element_displayed(*p_dom, timeout=1)
            found = True
        except:
            pass

        if orig_iframe:
            self.parent.iframe.switchToFrame("src", orig_iframe)

        return found

    def openSettingFromStatusbar(self):
        """
        As it says on the tin - opens the settings
        app via the statusbar.
        """
        self.displayStatusBar()
        x = self.parent.element.getElement(DOM.Statusbar.settings_button, "Settings button")
        x.tap()

        time.sleep(2)

        self.marionette.switch_to_frame()
        self.parent.iframe.switchToFrame(*DOM.Settings.frame_locator)

    def toggleViaStatusBar(self, p_type):
        """
        Uses the statusbar to toggle items on or off. Just toggles.
        Accepted 'types' are: data, wifi, airplane, bluetooth
        """
        self.parent.reporting.logResult("info", "Toggling " + p_type + " mode via statusbar ...")

        # Toggle (and wait)
        if p_type == "data":
            locator = DOM.Statusbar.toggle_dataconn
        if p_type == "wifi":
            locator = DOM.Statusbar.toggle_wifi
        if p_type == "bluetooth":
            locator = DOM.Statusbar.toggle_bluetooth
        if p_type == "airplane":
            locator = DOM.Statusbar.toggle_airplane

        return self._toggle_and_wait(locator, p_type)

    def _toggle_and_wait(self, locator, p_type):
        """
        (private) Toggle a button in the statusbar and waits for the item to be enabled/disabled
        Don't call this directly, it's used by toggleViaStatusBar().
        """

        # Open the status bar.
        self.displayStatusBar()
        boolWasEnabled = self.parent.network.is_network_type_enabled(p_type)

        toggle_icon = self.parent.element.getElement(locator, "Toggle {} icon".format(p_type))
        toggle_icon.tap()
        """
        Sometimes, when we activate data connection, the devices goes till settings and
        show a confirmation screen. We have to accept it.
        """
        success = self.parent.iframe.switchToFrame(DOM.Settings.frame_locator[0], DOM.Settings.frame_locator[1],
                                         quit_on_error=True, via_root_frame=True, test=False)
        if success:
            self.parent.element.waitForElements(DOM.Settings.celldata_DataConn_confirm_header,
                "Confirmation header", True, 40)

            ok_btn = self.marionette.find_element(*DOM.Settings.celldata_DataConn_ON)
            ok_btn.tap()
        else:
            # No confirmation required
            self.parent.reporting.logResult("debug", "No 3G confirmation asked")

        if boolWasEnabled:
            boolReturn = self.parent.network.wait_for_network_item_disabled(p_type)
        else:
            boolReturn = self.parent.network.wait_for_network_item_enabled(p_type)

        self.hideStatusBar()
        return boolReturn

    def waitForStatusBarNew(self, p_dom=DOM.Statusbar.status_bar_new, p_displayed=True, p_timeOut=20):

        # Waits for a new notification in the status bar (20s timeout by default).
        orig_iframe = self.parent.iframe.currentIframe()
        self.marionette.switch_to_frame()

        x = self.parent.element.waitForElements(p_dom, "This statusbar icon", p_displayed, p_timeOut)

        # Only switch if not called from the 'start' screen ...
        if orig_iframe != '':
            self.parent.iframe.switchToFrame("src", orig_iframe, False)

        return x

    def click_on_notification(self, dom, text, frame_to_change=None, timeout=30):
        """
        Clicks on a certain notification looking for the given text in the
        given DOM element (title or detail) for the specified timeout.
        If frame_to_change is not None, frame will be set to its value.
        """
        self.displayStatusBar()
        time.sleep(1)
        elem_dom = (dom[0], dom[1].format(text))
        self.parent.parent.wait_for_element_displayed(elem_dom[0], elem_dom[1], timeout)
        notif = self.marionette.find_element(elem_dom[0], elem_dom[1])
        notif.tap()

        if frame_to_change:
            self.parent.iframe.switchToFrame(*frame_to_change)

    def click_on_notification_title(self, text, frame_to_change=None, timeout=30):
        """Clicks on a certain notification (given by its title)
        """
        self.click_on_notification(DOM.Statusbar.notification_statusbar_title, text, frame_to_change, timeout)

    def click_on_notification_detail(self, text, frame_to_change=None, timeout=30):
        """Clicks on a certain notification (given by its body)
        """
        self.click_on_notification(DOM.Statusbar.notification_statusbar_detail, text, frame_to_change, timeout)

    @retry(2, 10)
    def wait_for_notification_toaster_title(self, text, frame_to_change=None, notif_text=None, timeout=30):
        """
        Waits for a new popup notification which contains a certain title
        """
        self.marionette.switch_to_frame()

        dom = (DOM.Statusbar.notification_toaster_title[0], DOM.Statusbar.notification_toaster_title[1].format(text))
        self.parent.reporting.debug(u"** Waiting for notification toaster title: [{}]".format(dom))
        self.parent.parent.wait_for_element_present(dom[0], dom[1], timeout)

        # Check if the notification actually exists or if it is a "ghost" one.
        # Note that we can use either @text or @notif_text
        self.wait_for_notification_statusbar_title(notif_text if notif_text else text)

        if frame_to_change:
            f = self.marionette.find_element(*frame_to_change)
            self.marionette.switch_to_frame(f)

    @retry(5, 10)
    def wait_for_notification_toaster_detail(self, text, frame_to_change=None, notif_text=None, timeout=30):
        """
        Waits for a new popup notification which contains a certain body
        """
        self.marionette.switch_to_frame()

        dom = (DOM.Statusbar.notification_toaster_detail[0], DOM.Statusbar.notification_toaster_detail[1].format(text))
        self.parent.reporting.debug(u"** Waiting for notification toaster detail: [{}]".format(dom))
        self.parent.parent.wait_for_element_present(dom[0], dom[1], timeout)

        # Check if the notification actually exists or if it is a "ghost" one.
        # Note that we can use either @text or @notif_text
        self.wait_for_notification_statusbar_detail(notif_text if notif_text else text)

        if frame_to_change:
            self.parent.iframe.switchToFrame(*frame_to_change)

    def wait_for_notification_toaster_with_titles(self, titles, dom=DOM.Statusbar.notification_toaster_title,
                                                  frame_to_change=None, timeout=30):
        """
        Waits for a new toaster notification whose title is one of the texts in the titles list.
        """
        self.marionette.switch_to_frame()

        exception = None
        title = None
        for t in titles:
            self.parent.reporting.log_to_file(u"Waiting for notification with title {}".format(t))
            toaster = (dom[0], dom[1].format(t))
            try:
                self.parent.parent.wait_for_element_present(toaster[0], toaster[1], timeout)
                if frame_to_change:
                    self.parent.iframe.switchToFrame(*frame_to_change)
                # Success. Clear the exception, if any
                exception = None
                self.parent.reporting.log_to_file(u"Title found: {}".format(t))
                title = t
                break
            except Exception as e:
                # If the element is not displayed before timeout, store exception, just in case another
                # title appears
                exception = e

        # Oops! Error, raise the exception
        if exception is not None:
            raise exception
        # Return the title found, so it can be used later, to click on or whatever
        return title

    def wait_for_notification_statusbar_title(self, text):
        self.marionette.switch_to_frame()

        self.parent.reporting.debug(u"** Waiting for notification statusbar title: [{}]".format(text))
        dom = (DOM.Statusbar.notification_statusbar_title[0],
               DOM.Statusbar.notification_statusbar_title[1].format(text))
        self.marionette.find_element(dom[0], dom[1])

    def wait_for_notification_statusbar_detail(self, text):
        self.marionette.switch_to_frame()

        self.parent.reporting.debug(u"** Waiting for notification statusbar detail: [{}]".format(text))
        dom = (DOM.Statusbar.notification_statusbar_detail[0],
             DOM.Statusbar.notification_statusbar_detail[1].format(text))
        self.marionette.find_element(dom[0], dom[1])
