import time
from OWDTestToolkit import DOM
from gaiatest.apps.homescreen.app import Homescreen


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
        self.parent.parent.device.touch_home_button()
