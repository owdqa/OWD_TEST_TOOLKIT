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
        utility_tray.wait_for_notification_container_displayed()
        utility_tray.clear_all_notifications()

    def displayStatusBar(self):
        #
        # Displays the status / notification bar in the home screen.
        #
        # The only reliable way I have to do this at the moment is via JS
        # (tapping it only worked sometimes).
        #
        self.marionette.switch_to_frame()
        self.marionette.execute_script("window.wrappedJSObject.UtilityTray.show()")
        time.sleep(0.5)

    def hideStatusBar(self):
        #
        # Displays the status / notification bar in the home screen.
        #
        # The only reliable way I have to do this at the moment is via JS
        # (tapping it only worked sometimes).
        #
        self.marionette.execute_script("window.wrappedJSObject.UtilityTray.hide()")

    def isIconInStatusBar(self, p_dom):
        #
        # Check an icon is in the statusbar, then return to the
        # given frame (doesn't wait, just expects it to be there).
        #
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
        #
        # As it says on the tin - opens the settings
        # app via the statusbar.
        #
        self.displayStatusBar()
        x = self.parent.element.getElement(DOM.Statusbar.settings_button, "Settings button")
        x.tap()

        time.sleep(2)

        self.marionette.switch_to_frame()
        self.parent.iframe.switchToFrame(*DOM.Settings.frame_locator)

    def toggleViaStatusBar(self, p_type):
        #
        # Uses the statusbar to toggle items on or off.<br>
        # <b>NOTE:</b> Doesn't care if it's toggling items ON or OFF. It just toggles!
        # <br><br>
        # Accepted 'types' are:<br>
        # <b>data</b><br>
        # <b>wifi</b><br>
        # <b>airplane</b><br>
        # <b>bluetooth</b>
        #
        self.parent.reporting.logResult("info", "Toggling " + p_type + " mode via statusbar ...")
        orig_iframe = self.marionette.get_active_frame()

        #
        # Toggle (and wait).
        #
        _wifi = {"name": "wifi", "notif": DOM.Statusbar.wifi, "toggle": DOM.Statusbar.toggle_wifi}
        _data = {"name": "data", "notif": DOM.Statusbar.dataConn, "toggle": DOM.Statusbar.toggle_dataconn}
        _bluetooth = {"name": "bluetooth", "notif": DOM.Statusbar.bluetooth, "toggle": DOM.Statusbar.toggle_bluetooth}
        _airplane = {"name": "airplane", "notif": DOM.Statusbar.airplane, "toggle": DOM.Statusbar.toggle_airplane}
        self.parent.reporting.log_to_file("*** toggle: p_type = {}".format(p_type))

        if p_type == "data":
            typedef = _data
        if p_type == "wifi":
            typedef = _wifi
        if p_type == "bluetooth":
            typedef = _bluetooth
        if p_type == "airplane":
            typedef = _airplane

        boolReturn = self._sb_doToggle(typedef, p_type)

        #
        # Close the statusbar and return to the original frame (if required).
        #
        self.parent.home.touchHomeButton()
        if orig_iframe:
            self.marionette.switch_to_frame(orig_iframe)

        return boolReturn

    def _sb_doToggle(self, p_def, p_type):
        #
        # (private) Toggle a button in the statusbar.
        # Don't call this directly, it's used by toggleViaStatusBar().
        #
        boolWasEnabled = self.parent.network.isNetworkTypeEnabled(p_type)

        #
        # Open the status bar.
        #
        self.displayStatusBar()

        x = self.parent.element.getElement(p_def["toggle"], "Toggle " + p_def["name"] + " icon")
        x.tap()

        #
        # Sometimes, when we activate data connection, the devices goes till settings and
        # show a confirmation screen. We have to accept it.
        #
        # try:
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
            boolReturn = self.parent.network.waitForNetworkItemDisabled(p_type)
        else:
            boolReturn = self.parent.network.waitForNetworkItemEnabled(p_type)
        self.hideStatusBar()
        return boolReturn

    def waitForStatusBarNew(self, p_dom=DOM.Statusbar.status_bar_new, p_displayed=True, p_timeOut=20):
        #
        # Waits for a new notification in the status bar (20s timeout by default).
        #
        orig_iframe = self.parent.iframe.currentIframe()
        self.marionette.switch_to_frame()

        x = self.parent.element.waitForElements(p_dom, "This statusbar icon", p_displayed, p_timeOut)

        # Only switch if not called from the 'start' screen ...
        if orig_iframe != '':
            self.parent.iframe.switchToFrame("src", orig_iframe, False)

        return x

    def click_on_notification(self, dom, text, frame_to_change=None, timeout=30):
        #
        # Clicks on a certain notification looking for the given text in the
        # given DOM element (title or detail) for the specified timeout.
        # If frame_to_change is not None, frame will be set to its value.
        #
        self.displayStatusBar()
        time.sleep(1)
        x = (dom[0], dom[1].format(text))
        self.parent.parent.wait_for_element_displayed(x[0], x[1], timeout)
        notif = self.marionette.find_element(x[0], x[1])
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

    @retry(5, 10)
    def wait_for_notification_toaster_title(self, text, frame_to_change=None, timeout=30):
        #
        # Waits for a new popup notification which contains a certain title
        #
        self.marionette.switch_to_frame()

        x = (DOM.Statusbar.notification_toaster_title[0], DOM.Statusbar.notification_toaster_title[1].format(text))
        self.parent.reporting.debug("** Waiting for notification toaster title: [{}]".format(x))
        self.parent.parent.wait_for_element_present(x[0], x[1], timeout)

        # Check if the notification actually exists or if it is a "ghost" one.
        dom = (DOM.Statusbar.notification_statusbar_title[0],
               DOM.Statusbar.notification_statusbar_title[1].format(text))
        self.marionette.find_element(dom[0], dom[1])

        if frame_to_change:
            self.parent.iframe.switchToFrame(*frame_to_change)

    @retry(5, 10)
    def wait_for_notification_toaster_detail(self, text, frame_to_change=None, timeout=30):
        #
        # Waits for a new popup notification which contains a certain body
        #
        self.marionette.switch_to_frame()

        x = (DOM.Statusbar.notification_toaster_detail[0], DOM.Statusbar.notification_toaster_detail[1].format(text))
        self.parent.reporting.debug("** Waiting for notification toaster detail: [{}]".format(x))
        self.parent.parent.wait_for_element_present(x[0], x[1], timeout)
        #self.displayStatusBar()
        dom = (DOM.Statusbar.notification_statusbar_detail[0],
             DOM.Statusbar.notification_statusbar_detail[1].format(text))
        self.marionette.find_element(dom[0], dom[1])

        if frame_to_change:
            self.parent.iframe.switchToFrame(*frame_to_change)

    def wait_for_notification_toaster_with_titles(self, titles, dom=DOM.Statusbar.notification_toaster_title,
                                                  frame_to_change=None, timeout=30):
        #
        # Waits for a new toaster notification whose title is one of the texts in the titles list.
        #
        self.marionette.switch_to_frame()

        exception = None
        title = None
        for t in titles:
            self.parent.reporting.log_to_file("Waiting for notification with title {}".format(t))
            toaster = (dom[0], dom[1].format(t))
            try:
                self.parent.parent.wait_for_element_present(toaster[0], toaster[1], timeout)
                if frame_to_change:
                    self.parent.iframe.switchToFrame(*frame_to_change)
                # Success. Clear the exception, if any
                exception = None
                self.parent.reporting.log_to_file("Title found: {}".format(t))
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
