from global_imports import *
from gaiatest import GaiaTestCase

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
                        x = self.marionette.find_element("xpath",
                                                         xpath_str + "//span[text()='" + p_appName + "']")

                        #
                        # Found it - return tihs list item!
                        #
                        myEl = self.marionette.find_element("xpath", xpath_str)
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
        return False
    
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

    def uninstallApp(self, p_appName):
        #
        # Remove an app using the UI.
        #

        #
        # Verify that the app is installed.
        #
        if not self.isAppInstalled(p_appName):
            return False
        
        #
        # Find the app icon.
        #
        myApp = self.findAppIcon(p_appName)
        if not myApp: return
        
        #
        # We found it! Long-press to into edit mode
        #
        self.actions.press(myApp).wait(2).release()
        self.actions.perform()
    
        #
        # Delete it (and refresh the 'myApp' object to include the new button).
        #
        # NOTE: This kind of 'element-within-an-element' isn't necessarily
        #       appropriate for 'verify', so don't.
        #
        delete_button = self.getElement( ("xpath", 
                                          DOM.Home.app_delete_icon_xpath % p_appName), 
                                        "Delete button", False, 5, True)
        delete_button.tap()
            
        #
        # Confirm deletion.
        #
        delete = self.getElement(DOM.Home.app_confirm_delete, "Confirm app delete button")
        delete.tap()

        #
        # Once it's gone, go home and check the icon is no longer there.
        #
        time.sleep(2)
        self.touchHomeButton()
        self.touchHomeButton()
        self.TEST(not self.isAppInstalled(p_appName), "App is uninstalled after deletion.")
        
        return True


    ##
    ## Quickly install an app. - CURRENTLY NEEDS MORE INFO THAN  HAVE.
    ##
    #def installAppQuick(self, p_name):
        ##
        ## The url address usually uses the name of the app, minus spaces
        ## and in lowercase.
        ##
        #appURL   = p_name.lower()
        #appURL   = appURL.replace(" ", "")
        #MANIFEST = "app://%s.gaiamobile.org/manifest.webapp" % appURL
        #self.marionette.switch_to_frame()
        #self.marionette.execute_script(
            #'navigator.mozApps.install("%s")' % MANIFEST)
    