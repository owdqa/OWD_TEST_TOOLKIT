from OWDTestToolkit import DOM
import time


class app(object):

    def _getAppFrame(self, p_name):
        #
        # Private function that returns the frame_locator for an app by name.
        #
        if p_name == "Browser":
            app_frame = DOM.Browser.frame_locator
        elif p_name == "Calculator":
            app_frame = DOM.Calculator.frame_locator
        elif p_name == "Calendar":
            app_frame = DOM.Calendar.frame_locator
        elif p_name == "Camera":
            app_frame = DOM.Camera.frame_locator
        elif p_name == "Clock":
            app_frame = DOM.Clock.frame_locator
        elif p_name == "Contacts":
            app_frame = DOM.Contacts.frame_locator
        elif p_name == "Phone":
            app_frame = DOM.Dialer.frame_locator
        elif p_name == "Email":
            app_frame = DOM.Email.frame_locator
        elif p_name == "Facebook":
            app_frame = DOM.Facebook.frame_locator
        elif p_name == "FTU":
            app_frame = DOM.FTU.frame_locator
        elif p_name == "Gallery":
            app_frame = DOM.Gallery.frame_locator
        elif p_name == "Home":
            app_frame = DOM.Home.frame_locator
        elif p_name == "Keyboard":
            app_frame = DOM.Keyboard.frame_locator
        elif p_name == "Marketplace":
            app_frame = DOM.Market.frame_locator
        elif p_name == "Messages":
            app_frame = DOM.Messages.frame_locator
        elif p_name == "Settings":
            app_frame = DOM.Settings.frame_locator
        elif p_name == "Video":
            app_frame = DOM.Video.frame_locator
        return app_frame

    def addAppToDock(self, app_name):
        #
        # Adds <i>app_name</i> to the homescreen dock if possible
        # (if the dock already the maximum number of apps in it a message
        # will be added to the details log and the function will return False).
        #
        _app_icon = self.findAppIcon(app_name)

        if not _app_icon:
            self.logResult("info", "Cannot find icon for app '{}'.".format(app_name))
            return False

        #
        # Put screen into edit mode.
        #
        self.actions.press(_app_icon).wait(2).release().perform()

        #
        # Move it to the dock.
        #
        _docked_apps = self.getElements(DOM.Home.docked_apps, "Docked apps (before adding app)")
        _count_before = len(_docked_apps)

        self.actions.press(_app_icon).wait(2).move(_docked_apps[0]).release().perform()
        time.sleep(1)

        self.touchHomeButton()
        self.switchToFrame(*DOM.Home.frame_locator)

        _docked_apps = self.getElements(DOM.Home.docked_apps, "Docked apps (after adding app)")
        _count_after = len(_docked_apps)

        self.logResult("info", "Before adding '{}' there were {} apps in the dock, now there are {}.".\
                       format(app_name, _count_before, _count_after))

        if _count_after > _count_before:
            return True
        else:
            self.logResult("info", "<b>NOTE:</b> Could not add app to dock as it already contains {}.".\
                           format(_count_after))
            return False

    def findAppIcon(self, app_name):
        #
        # Scroll around the homescreen until we find our app icon.
        #

        #
        # I had all kinds of weird issues when returning to this method,
        # this awful solution works.
        #
        self.goHome()

        try:
            #
            # If this works, then the icon is visible at the moment.
            #
            x = self.marionette.find_element('css selector', DOM.Home.app_icon_css.format(app_name))
            self.logResult("debug", "icon displayed: %s" % str(x.is_displayed()))
            if x.is_displayed():
                return x
        except:
            pass

        self.scrollHomescreenRight()
        time.sleep(0.5)

        _pages = self.getElements(DOM.Home.app_icon_pages, "Homescreen icon pages")
        for i in _pages:
            try:
                #
                # If this works, then the icon is visible at the moment.
                #
                x = self.marionette.find_element('css selector', DOM.Home.app_icon_css.format(app_name))
                self.logResult("debug", "icon displayed: {}".format(x.is_displayed()))
                if x.is_displayed():
                    return x
            except:
                pass

            self.scrollHomescreenRight()
        return False

    def isAppInstalled(self, app_name):
        #
        # Return whether an app is present on the homescreen (i.e. 'installed').
        #
        self.switchToFrame(*DOM.Home.frame_locator)

        x = ('css selector', DOM.Home.app_icon_css.format(app_name))
        try:
            self.marionette.find_element(*x)
            self.logResult("info", "App <b>{}</b> is currently installed.".format(app_name))
            return True
        except:
            self.logResult("info", "App <b>{}</b> is not currently installed.".format(app_name))
            return False

    def _GaiaApp(self, origin, name, frame, src):
        #
        # Private function to return a 'GaiaApp' object to use in UTILS.killApp() calls.
        #
        class GaiaApp(object):
            def __init__(self, origin, name, frame, src):
                self.frame = frame
                self.frame_id = frame
                self.src = src
                self.name = name
                self.origin = origin

            def __eq__(self, other):
                return self.__dict__ == other.__dict__

        return GaiaApp(origin, name, frame, src)

    def killApp(self, app_name):
        #
        # Kills the app specified by app_name.
        #

        # Because these app aren't consistently named, or may be 'guessed'
        # incorrectly ...
        if app_name == "Dialer":
            app_name = "Phone"
        if app_name == "SMS":
            app_name = "Messages"
        if app_name == "Market":
            app_name = "Marketplace"

        self.logResult("info", "Killing app '{}' ...".format(app_name))

        # Get the right DOM frame def. for this app.
        app_dom = self._getAppDOM(app_name)

        self.marionette.switch_to_frame()
        _frame = self.marionette.find_element("xpath", "//iframe[contains(@{}, '{}')]".format(app_dom[0], app_dom[1]))
        _src = _frame.get_attribute("src")
        _origin = _src

        myApp = self._GaiaApp(_origin, app_name, _frame, _src)

        self.apps.kill(myApp)

    def launchAppViaHomescreen(self, app_name):
        #
        # Launch an app via the homescreen.
        #
        ok = False
        if self.findAppIcon(app_name):
            time.sleep(1)
            x = ('css selector', DOM.Home.app_icon_css.format(app_name))
            myApp = self.getElement(x, "App icon")
            myApp.tap()
            time.sleep(10)
            ok = True
        return ok

    def moveAppFromDock(self, app_name):
        #
        # Moves the app 'app_name' from the dock to the homescreen.
        #
        self.goHome()
        self.scrollHomescreenRight()
        x = self.getElements(DOM.Home.docked_apps, "Dock apps")
        is_moved = False
        for i in x:
            if i.get_attribute("aria-label") == app_name:
                self.logResult("info", "Trying to move '{}' from the doc to the homescreen ...".format(app_name))
                self.actions.press(i).wait(1).move_by_offset(0, -100).wait(1).release().perform()
                self.touchHomeButton()
                is_moved = True
                break

        if not is_moved:
            self.logResult("info", "App '{}' was not found in the dock.".format(app_name))
            return False

        #
        # Check the app is not in the dock.
        #
        self.switchToFrame(*DOM.Home.frame_locator)

        try:
            self.wait_for_element_present(*DOM.Home.docked_apps, timeout=1)
            x = self.getElements(DOM.Home.docked_apps, "Dock apps")
            for i in x:
                if i.get_attribute("aria-label") == app_name:
                    self.logResult("info", "<b>NOTE:</b>App '{}' is still in the dock after moving!".format(app_name))
                    return False
                    break
        except:
            pass

        #
        # Check the app has not been removed.
        #
        return self.findAppIcon(app_name)

    def setPermission(self, app_name, item, value, quiet=False):
        #
        # Just a container function to catch any issues when using gaiatest's
        # 'set_permission()' function.
        #
        try:
            self.apps.set_permission(app_name, item, value)

            if not quiet:
                self.logResult("info", "Setting  permission for app '{}' -> '{}' to '{}' returned no issues.".\
                               format(app_name, item, value))
            return True
        except:
            if not quiet:
                self.logresult("info", "WARNING: unable to set permission for app '{}' -> '{}' to '{}'!".\
                               format(app_name, item, value))
            return False

    def switchToApp(self, app_name):
        #
        # Switches to the app (or launches it if it's not open).
        #

        # Because these app aren't consistently named, or may be 'guessed'
        # incorrectly ...
        if app_name == "Dialer":
            app_name = "Phone"
        if app_name == "SMS":
            app_name = "Messages"
        if app_name == "Market":
            app_name = "Marketplace"

        app_frame = self._getAppFrame(app_name)

        self.marionette.switch_to_frame()
        try:
            self.wait_for_element_present("xpath", "//iframe[contains(@{}, '{}')]".format(app_frame[0], app_frame[1]),
                                          timeout=1)
            self.logResult("info", "(Looks like app '{}' is already running - just switching to it's iframe ...)".\
                           format(app_name))
            self.switchToFrame(*app_frame)
        except:
            #
            # The app isn't open yet, so try to launch it.
            #
            # (This throws an error, even though the app launches. 'Hacky', but it works.)
            try:
                self.logResult("info", "(Looks like app '{}' is not currently running, so I'll launch it.)".\
                               format(app_name))
                self.apps.launch(app_name)
                self.waitForNotElements(DOM.GLOBAL.loading_overlay, "{} app loading 'overlay'".format(app_name))
                self.switchToFrame(*app_frame)
            except:
                pass

    def uninstallApp(self, app_name):
        #
        # Remove an app using the UI.
        #
        self.logResult("info", "Making sure app <b>{}</b> is uninstalled.".format(app_name))

        myApp = self.findAppIcon(app_name)
        if myApp:
            self.actions.press(myApp).wait(2).release()
            self.actions.perform()

            delete_button = self.getElement(("xpath", DOM.Home.app_delete_icon_xpath.format(app_name)),
                                            "Delete button", False, 5, True)
            delete_button.tap()

            delete = self.getElement(DOM.Home.app_confirm_delete, "Confirm app delete button")
            delete.tap()

            time.sleep(2)
            self.touchHomeButton()

            self.TEST(not self.isAppInstalled(app_name), "App is uninstalled after deletion.")
        else:
            self.logResult("info", "(No need to uninstall {}.)".format(app_name))
