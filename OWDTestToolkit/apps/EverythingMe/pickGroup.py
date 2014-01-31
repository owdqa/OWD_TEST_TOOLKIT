from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def pickGroup(self, p_name):
        #
        # Pick a group from the main icons.
        #
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "<b>Choosing group '%s' from here ...</b>" % p_name, x)

        boolOK = False

        x = self.marionette.find_element('css selector', DOM.Home.app_icon_css % p_name)
        self.UTILS.logResult("debug", "icon displayed: %s" % str(x.is_displayed()))
        x.tap()

        try:
            self.wait_for_element_displayed(*DOM.EME.apps_not_installed, timeout=20)
            self.UTILS.logResult("info", "(Apps for group %s were displayed.)" % p_name)
            boolOK = True
        except:
            x = self.UTILS.screenShotOnErr()
            self.UTILS.logResult("info", "(<b>NOTE:</b>Apps for group %s were not displayed.)|%s|%s" % \
                                         (p_name,x[0],x[1]))

        return boolOK