from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def addAppToHomescreen(self, p_name):
        #
        # Pick an app from the apps listed in this group.
        #
        x = self.UTILS.getElements(DOM.EME.apps, "Apps list", True, 30)
        for appLink in x:
            if appLink.get_attribute("data-name") == p_name:
                from marionette import Actions
                actions = Actions(self.marionette)
                actions.press(appLink).wait(2).release()
                actions.perform()
                
                self.marionette.switch_to_frame()
                x = self.UTILS.getElement(DOM.EME.add_app_to_homescreen, "Add app to homescreen button")
                x.tap()
                
                #
                # Might need to do this again for Geoloc. ...
                #
                try:
                    x = self.marionette.find_element(*DOM.EME.add_app_to_homescreen)
                    x.tap()
                except:
                    pass
                
                # This isn't obvious, but you need to scroll the screen right
                # to reset the position for finding the app later, so I'm
                # doing it here.
                time.sleep(2)
                self.UTILS.goHome()
                self.UTILS.scrollHomescreenRight()

                return True
        
        return False

