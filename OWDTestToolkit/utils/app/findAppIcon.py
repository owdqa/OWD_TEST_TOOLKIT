from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def findAppIcon(self, p_appName):
        #
        # Scroll around the homescreen until we find our app icon.
        #

        #
        # I had all kinds of weird issues when returning to this method,
        # this awful solution works.
        #
        self.goHome()
        time.sleep(1)
        self.goHome()

        try:
            #
            # If this works, then the icon is visible at the moment.
            #
            x = self.marionette.find_element('css selector', DOM.Home.app_icon_css.format(p_appName))
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
                x = self.marionette.find_element('css selector', DOM.Home.app_icon_css.format(p_appName))
                self.logResult("debug", "icon displayed: %s" % str(x.is_displayed()))
                if x.is_displayed():
                    return x
            except:
                pass

            self.scrollHomescreenRight()

        return False
