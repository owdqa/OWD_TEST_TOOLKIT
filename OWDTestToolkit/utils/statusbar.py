import time
from OWDTestToolkit import DOM


class statusbar(object):

    def clearAllStatusBarNotifs(self, p_silent=False):
        #
        # Opens the statusbar, presses "Clear all", then closes the status bar.<br>
        # <b>p_silent</b> will supress any pass/fail (useful if this isn't relevant
        # to the test, or if you're just using it for a bit of housekeeping).
        #
        if p_silent:
            try:
                self.displayStatusBar()
                self.wait_for_element_displayed(*DOM.Statusbar.clear_all_button, timeout=1)
                x = self.marionette.find_element(*DOM.Statusbar.clear_all_button)
                x.tap()
                time.sleep(1)
                self.hideStatusBar()
            except:
                if p_silent:
                    pass
                raise

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
        orig_iframe = self.currentIframe()
        self.marionette.switch_to_frame()

        found = False
        try:
            self.wait_for_element_displayed(*p_dom, timeout=1)
            found = True
        except:
            pass

        if orig_iframe:
            self.switchToFrame("src", orig_iframe)

        return found

    def openSettingFromStatusbar(self):
        #
        # As it says on the tin - opens the settings
        # app via the statusbar.
        #
        self.displayStatusBar()
        x = self.getElement(DOM.Statusbar.settings_button, "Settings button")
        x.tap()

        time.sleep(2)

        self.marionette.switch_to_frame()
        self.switchToFrame(*DOM.Settings.frame_locator)

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
        self.logResult("info", "Toggling " + p_type + " mode via statusbar ...")
        orig_iframe = self.currentIframe()

        #
        # Toggle (and wait).
        #
        _wifi = {"name": "wifi", "notif": DOM.Statusbar.wifi, "toggle": DOM.Statusbar.toggle_wifi}
        _data = {"name": "data", "notif": DOM.Statusbar.dataConn, "toggle": DOM.Statusbar.toggle_dataconn}
        _bluetooth = {"name": "bluetooth", "notif": DOM.Statusbar.bluetooth, "toggle": DOM.Statusbar.toggle_bluetooth}
        _airplane = {"name": "airplane", "notif": DOM.Statusbar.airplane, "toggle": DOM.Statusbar.toggle_airplane}

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
        self.touchHomeButton()
        if orig_iframe:
            self.switchToFrame("src", orig_iframe)

        return boolReturn

    def _sb_doToggle(self, p_def, p_type):
        #
        # (private) Toggle a button in the statusbar.
        # Don't call this directly, it's used by toggleViaStatusBar().
        #
        boolWasEnabled = self.isNetworkTypeEnabled(p_type)

        #
        # Open the status bar.
        #
        self.displayStatusBar()

        x = self.getElement(p_def["toggle"], "Toggle " + p_def["name"] + " icon")
        x.tap()

        boolReturn = True
        if boolWasEnabled:
            boolReturn = self.waitForNetworkItemDisabled(p_type)
        else:
            boolReturn = self.waitForNetworkItemEnabled(p_type)

        return boolReturn

    def waitForStatusBarNew(self, p_dom=DOM.Statusbar.status_bar_new, p_displayed=True, p_timeOut=20):
        #
        # Waits for a new notification in the status bar (20s timeout by default).
        #
        orig_iframe = self.currentIframe()
        self.marionette.switch_to_frame()

        x = self.waitForElements(p_dom, "This statusbar icon", p_displayed, p_timeOut)

        # Only switch if not called from the 'start' screen ...
        if orig_iframe != '':
            self.switchToFrame("src", orig_iframe, False)

        return x
