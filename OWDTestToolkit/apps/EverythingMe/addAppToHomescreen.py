from OWDTestToolkit.global_imports import *


class main(GaiaTestCase):

    def addAppToHomescreen(self, p_name):
        #
        # Pick an app from the apps listed in this group.
        #
        x = self.UTILS.getElements(DOM.EME.app_to_install, "The first game that is not installed already")[0]
        APP_NAME = x.get_attribute("data-name")
        self.UTILS.logResult("debug", "icon displayed: %s" % str(x.is_displayed()))

        self.UTILS.TEST(APP_NAME == p_name, "" + APP_NAME + "'is the correct app", True)

        from marionette import Actions
        actions = Actions(self.marionette)
        actions.press(x).wait(2).release()
        try:
            actions.perform()
        except:
            pass

        x = self.UTILS.getElement(DOM.EME.add_app_to_homescreen, "Add app to homescreen button")
        x.tap()

        return True