from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def isAppInstalled(self, p_appName):
        #
        # Return whether an app is present on the homescreen (i.e. 'installed').
        #
        self.switchToFrame(*DOM.Home.frame_locator)

        x = ('css selector', DOM.Home.app_icon_css % p_appName)
        try:
            self.marionette.find_element(*x)
            self.logResult("info", "App <b>%s</b> is currently installed." % p_appName)
            return True
        except:
            self.logResult("info", "App <b>%s</b> is not currently installed." % p_appName)
            return False

