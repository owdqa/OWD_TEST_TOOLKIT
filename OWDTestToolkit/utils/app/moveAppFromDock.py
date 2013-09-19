from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def moveAppFromDock(self, p_name):
        #
        # Moves the app 'p_name' from the dock to the homescreen.
        #
        self.goHome()
        self.scrollHomescreenRight()
        x = self.getElements(DOM.Home.docked_apps, "Dock apps")
        boolMoved = False
        for i in x:
            if i.get_attribute("aria-label") == p_name:
                self.logResult("info", "Trying to move '%s' from the doc to the homescreen ..." % p_name)
                self.actions.press(i).wait(1).move_by_offset(0,-100).wait(1).release().perform()
                self.touchHomeButton()
                boolMoved = True
                break
        
        if not boolMoved:
            self.logResult("info", "App '%s' was not found in the dock." % p_name)
            return False
        
        #
        # Check the app is not in the dock.
        #
        self.switchToFrame(*DOM.Home.frame_locator)
        
        try:
            self.wait_for_element_present(*DOM.Home.docked_apps, timeout=1)
            x = self.getElements(DOM.Home.docked_apps, "Dock apps")
            for i in x:
                if i.get_attribute("aria-label") == p_name:
                    self.logResult("info", "<b>NOTE:</b>App '%s' is still in the dock after moving!" % p_name)
                    return False
                    break
        except:
            pass
            
        #
        # Check the app has not been removed.
        #
        return self.findAppIcon(p_name)
