from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def findAppIcon(self, p_appName, p_reloadHome=True):
        #
        # Scroll around the homescreen until we find our app icon.
        #
        if p_reloadHome:
            #
            # If this doesn't happen, it is assumed you are already
            # in the correct iframe.
            #
            self.goHome()

        #
        # Bit long-winded, but it ensures the icon is displayed.
        #
        # We need to return the entire 'li' element, not just the
        # 'span' element (otherwise we can't use what's returned
        # to find the delete icon when the homescreen is in edit mode).
        #
        # As these dom specs are only ever going to be useful here,
        # I'm not defining them in DOM.
        #
        for i_page in range(1, 10):
            try:
                # (16 apps per page)
                for i_li in range(1,17):
                    try:
                        xpath_str = "//div[@class='page'][%s]//li[%s]" % (i_page, i_li)
                        self.wait_for_element_present("xpath",
                                                      xpath_str + "//span[text()='" + p_appName + "']",
                                                      timeout=1)
                        
                        time.sleep(1)
                        
                        #
                        # Found it - return tihs list item!
                        #
                        myEl = self.marionette.find_element("xpath", xpath_str)
                        self.logResult("info", "Found app icon for <b>%s</b>." % p_appName)
                        return myEl
                    except:
                        pass
            except:
                pass

            #
            # No such app in this page, try again (only scroll of we reloaded the home page).
            #
            if p_reloadHome: self.scrollHomescreenRight()

        #
        # If we get here, we didn't find it!
        #
        self.logResult("info", "Could not find icon for app <b>%s</b>." % p_appName)
        return False
    
