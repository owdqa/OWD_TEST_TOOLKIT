from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def addAppToDock(self, p_appName):
        
        _appIcon = self.findAppIcon(p_appName)
        
        if not _appIcon:
            self.logResult("info", "Cannot find icon for app '%s'." % p_appName)
            return False
        
        #
        # Put screen into edit mode.
        #
        self.actions.press(_appIcon).wait(2).release().perform()
        
        #
        # Move it to the dock.
        #
        _docked_apps = self.getElements(DOM.Home.docked_apps, "Docked apps (before adding app)")
        _BEFORECOUNT = len(_docked_apps)

        self.actions.press(_appIcon).wait(2).move(_docked_apps[0]).release().perform()
        time.sleep(1)

        self.touchHomeButton()
        self.switchToFrame(*DOM.Home.frame_locator)
        
        _docked_apps = self.getElements(DOM.Home.docked_apps, "Docked apps (after adding app)")
        _AFTERCOUNT = len(_docked_apps)

        self.logResult("info", "Before adding '%s' there were %s apps in the dock, now there are %s." % \
                             (p_appName, _BEFORECOUNT, _AFTERCOUNT))

        if _AFTERCOUNT > _BEFORECOUNT:
            return True
        else:
            return False