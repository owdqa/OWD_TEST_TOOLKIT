from OWDTestToolkit.global_imports import *


class main(GaiaTestCase):

    def isAppInstalled(self, p_appName):
        #
        # Return whether an app is present on the homescreen (i.e. 'installed').
        #
        self.switchToFrame(*DOM.Home.frame_locator)

        x = ('css selector', DOM.Home.app_icon_css.format(p_appName))
        try:
            self.marionette.find_element(*x)
            self.logResult("info", "App <b>{}</b> is currently installed.".format(p_appName))
            return True
        except:
            self.logResult("info", "App <b>{}</b> is not currently installed.".format(p_appName))
            return False

