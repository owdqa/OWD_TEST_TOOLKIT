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
        
        self.scrollHomescreenRight()
        time.sleep(1)
        x = self.getElements(DOM.Home.app_icon_pages, "Icon pages on homescreen")
         
        ICON_POS = False
        for pagenum in x:
            #
            # For each page of icons ...
            #
            time.sleep(0.5)
            ICON_POS = ICON_POS + 1
            for i in pagenum.find_elements("xpath", "./ol/li[@class='icon']"):
                #
                # For each icon on this page of icons ...
                #
                if i.get_attribute("aria-label") == p_appName:
                    self.logResult("info", "Icon for %s found on page %s." % (p_appName, ICON_POS))
                    return i
                    break
            self.scrollHomescreenRight()
             
        self.logResult("info", "Icon for '%s' not found on the homescreen." % p_appName)
        return False
