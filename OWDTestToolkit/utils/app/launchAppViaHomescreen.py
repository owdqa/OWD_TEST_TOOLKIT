from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def launchAppViaHomescreen(self, p_appName):
        #
        # Launch an app via the homescreen.
        #
        boolOK = False
        if self.findAppIcon(p_appName):
            time.sleep(1)
            x = ('css selector', DOM.Home.app_icon_css % p_appName)
            myApp = self.getElement(x, "App icon")
            myApp.tap()
            time.sleep(10)
            boolOK = True
        else:
            boolOK = False
        
        return boolOK
            
