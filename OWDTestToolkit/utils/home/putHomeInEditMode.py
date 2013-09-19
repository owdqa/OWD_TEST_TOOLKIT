from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def putHomeInEditMode(self):
        #
        # Just uses the first icon it comes across to put the homescreen into edit mode.
        #
        self.goHome()
        self.scrollHomescreenRight()
        time.sleep(0.5)

        x = self.getElements(DOM.Home.app_icon_pages, "Icon pages on homescreen")
        _first_icon = x[0].find_element("xpath", "./ol/li[@class='icon']")
        self.actions.press(_first_icon).wait(2).release().perform()


