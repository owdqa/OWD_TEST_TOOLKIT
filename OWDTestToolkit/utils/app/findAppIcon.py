from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def findAppIcon(self, p_appName):
        #
        # Scroll around the homescreen until we find our app icon.
        #
        self.goHome()
        
        self.scrollHomescreenRight()
        time.sleep(1)
        x = self.getElements( ("xpath", "//div[@id='icongrid']/div[@class='page']"), "blah")
        self.logResult("info", "LEN: %s" % len(x))
         
        ICON_POS = False
        for pagenum in x:
            #
            # For each page of icons ...
            #
            self.scrollHomescreenRight()
            time.sleep(0.5)
            ICON_POS = ICON_POS + 1
            for i in pagenum.find_elements("xpath", "./ol/li[@class='icon']"):
                #
                # For each icon on this page of icons ...
                #
                if i.get_attribute("aria-label") == p_appName:
                    self.logResult("info", "Icon for %s found on page %s." % (p_appName, ICON_POS))
                    return i
             
        self.logResult("info", "<b>NOTE:</b> Icon for '%s' not found!" % p_appName)
        return False
