import time
from OWDTestToolkit import DOM


class home(object):

    def goHome(self):
        #
        # Return to the home screen.
        #

        # (Sometimes the home button needs to be tapped twice, i.e. if you're
        # in a results screen of EME.)
        self.touchHomeButton()
        self.touchHomeButton()

        self.apps.kill_all()

        self.switchToFrame(*DOM.Home.frame_locator, p_quitOnError=False)

        time.sleep(1)

    def holdHomeButton(self):
        #
        # Long hold the home button to bring up the 'current running apps'.
        #
        self.marionette.switch_to_frame()
        self.marionette.execute_script("window.wrappedJSObject.dispatchEvent(new Event('holdhome'));")

    def putHomeInEditMode(self):
        #
        # Just uses the first icon it comes across to put the homescreen into edit mode.
        #
        self.goHome()
        self.scrollHomescreenRight()
        time.sleep(0.5)

        x = self.getElements(DOM.Home.app_icon_pages, "Icon pages on homescreen")
        _first_icon = x[0].find_element("xpath", "./ol/li[@class='icon']")
        self.actions.press(_first_icon).wait(2).release().perform()

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
        #
        # Touch the home button (sometimes does something different to going home).
        #
        self.marionette.switch_to_frame()
        self.marionette.execute_script("window.wrappedJSObject.dispatchEvent(new Event('home'));")
