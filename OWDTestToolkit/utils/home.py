import time
from OWDTestToolkit import DOM
from gaiatest.apps.homescreen.app import Homescreen
from marionette.wait import Wait
from OWDTestToolkit.utils.i18nsetup import I18nSetup
from marionette.by import By
_ = I18nSetup(I18nSetup).setup()


class home(object):

    def __init__(self, parent):
        self.parent = parent
        self.marionette = parent.marionette
        self.homescreen = Homescreen(self.marionette)

    def goHome(self):
        #
        # Return to the home screen.
        #

        # (Sometimes the home button needs to be tapped twice, i.e. if you're
        # in a results screen of EME.)
        self.touchHomeButton()
        self.touchHomeButton()

        self.parent.apps.kill_all()

        self.parent.iframe.switchToFrame(*DOM.Home.frame_locator, quit_on_error=False)

        time.sleep(1)

    def holdHomeButton(self):
        """Hold Home button pressed to show active applications.
        """
        self.parent.parent.device.hold_home_button()

    def putHomeInEditMode(self):
        """Activate Edit Mode by holding an app pressed and then releasing.
        """
        self.homescreen.activate_edit_mode()

    def scrollHomescreenLeft(self):
        #
        # Scroll to previous page (left).
        # Should change this to use marionette.flick() when it works.
        #
        self.marionette.execute_script('window.wrappedJSObject.GridManager.goToPreviousPage()')

    def scrollHomescreenRight(self):
        #
        # Scroll to next page (right).
        # Should change this to use marionette.flick() when it works.
        #
        self.marionette.execute_script('window.wrappedJSObject.GridManager.goToNextPage()')

    def touchHomeButton(self):
        """Touch Home button.
        """
        self._touch_home_button(_("homescreen"))

    def _dispatch_home_button_event(self):
        self.marionette.switch_to_frame()
        self.marionette.execute_script("window.wrappedJSObject.dispatchEvent(new Event('home'));")

    def _touch_home_button(self, homescreen_name):
        apps = self.parent.apps
        if apps.displayed_app.name.lower() != homescreen_name:
            # touching home button will return to homescreen
            self._dispatch_home_button_event()
            Wait(self.marionette).until(
                lambda m: apps.displayed_app.name.lower() == homescreen_name)
            apps.switch_to_displayed_app()
        else:
            apps.switch_to_displayed_app()
            mode = self.marionette.find_element(By.TAG_NAME, 'body').get_attribute('class')
            self._dispatch_home_button_event()
            apps.switch_to_displayed_app()
            if mode == 'edit-mode':
                # touching home button will exit edit mode
                Wait(self.marionette).until(lambda m: m.find_element(
                    By.TAG_NAME, 'body').get_attribute('class') != mode)
            else:
                # touching home button inside homescreen will scroll it to the top
                Wait(self.marionette).until(lambda m: m.execute_script(
                    "return document.querySelector('.scrollable').scrollTop") == 0)
