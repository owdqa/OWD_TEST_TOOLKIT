from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def toggleSelectGmailContact(self, p_num):
        #
        # Toggles select / de-select a gmail contact( marionette doesn't work here yet, so use JS).
        # p_num is the actualt contact number (1 -> x).
        #
        self.UTILS.logResult("info", "Selecting contact %s ..." % p_num)
        
        x = p_num - 1
        self.marionette.execute_script("document.getElementsByClassName('block-item')[%s].click()" % x)
        
        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Screenshot of current position", x)

