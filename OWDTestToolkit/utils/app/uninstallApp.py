from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def uninstallApp(self, p_appName):
        #
        # Remove an app using the UI.
        #
        self.logResult("info", "Making sure app <b>%s</b> is uninstalled." % p_appName)


        myApp = self.findAppIcon(p_appName)
        if myApp:  
            self.actions.press(myApp).wait(2).release()
            self.actions.perform()
    
            delete_button = self.getElement( ("xpath", 
                                              DOM.Home.app_delete_icon_xpath % p_appName), 
                                            "Delete button", False, 5, True)
            delete_button.tap()
    
            delete = self.getElement(DOM.Home.app_confirm_delete, "Confirm app delete button")
            delete.tap()
    
            time.sleep(2)
            self.touchHomeButton()
    
            self.TEST(not self.isAppInstalled(p_appName), "App is uninstalled after deletion.")
        else:
            self.logResult("info", "(No need to uninstall %s.)" % p_appName)


# 
#         #
#         # Verify that the app is installed.
#         #
#         if not self.isAppInstalled(p_appName):
#             return False
#         
#         #
#         # Find the app icon.
#         #
#         myApp = self.findAppIcon(p_appName)
#         if not myApp: return
#         
#         #
#         # We found it! Long-press to into edit mode
#         #
#         self.actions.press(myApp).wait(2).release()
#         self.actions.perform()
#     
#         #
#         # Delete it (and refresh the 'myApp' object to include the new button).
#         #
#         # NOTE: This kind of 'element-within-an-element' isn't necessarily
#         #       appropriate for 'verify', so don't.
#         #
#         delete_button = self.getElement( ("xpath", 
#                                           DOM.Home.app_delete_icon_xpath % p_appName), 
#                                         "Delete button", False, 5, True)
#         delete_button.tap()
#             
#         #
#         # Confirm deletion.
#         #
#         delete = self.getElement(DOM.Home.app_confirm_delete, "Confirm app delete button")
#         delete.tap()
# 
#         #
#         # Once it's gone, go home and check the icon is no longer there.
#         #
#         time.sleep(2)
#         self.touchHomeButton()
#         self.touchHomeButton()
#         self.TEST(not self.isAppInstalled(p_appName), "App is uninstalled after deletion.")
#         
#         return True
