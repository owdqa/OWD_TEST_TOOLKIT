from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def isAppInstalled(self, p_appName):
        #
        # Return whether an app is present on the homescreen (i.e. 'installed').
        #
        self.marionette.switch_to_frame()
        self.switchToFrame(*DOM.Home.homescreen_iframe)

        x = ('css selector', DOM.Home.app_icon_css % p_appName)
        try:
            self.marionette.find_element(*x)
            return True
        except:
            return False

