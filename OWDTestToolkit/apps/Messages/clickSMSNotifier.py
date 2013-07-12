from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def clickSMSNotifier(self, p_num):
        #
        # Click new sms in the home page status bar notificaiton.
        #
        self.UTILS.logResult("info", "Clicking statusbar notification of new SMS from " + p_num + " ...")

        #
        # Switch to the 'home' frame to click the notifier.
        #
        self.marionette.switch_to_frame()
        self.UTILS.displayStatusBar()
        x=( DOM.Messages.statusbar_new_sms[0],
            DOM.Messages.statusbar_new_sms[1] % p_num)
        x = self.UTILS.getElement(x, "Statusbar notification for " + p_num)
        x.tap()

        #
        # Switch back to the messaging app.
        #
        self.UTILS.switchToFrame(*DOM.Messages.frame_locator)
        
        #
        # Wait for the message thread to finish loading.
        #
        self.UTILS.waitForElements(("xpath", "//h1[text()='" + p_num + "']"), 
                                   "SMS thread header for " + str(p_num), True, 20)
        self.waitForReceivedMsgInThisThread()
        

