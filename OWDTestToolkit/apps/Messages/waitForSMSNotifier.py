from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def waitForSMSNotifier(self, p_num, p_timeout=40):
        #
        # Get the element of the new SMS from the status bar notification.
        #
        self.UTILS.logResult("info", "Waiting for statusbar notification of new SMS from " + p_num + " ...")

        #
        # Create the string to wait for.
        #
        x=( DOM.Messages.statusbar_new_sms[0],
            DOM.Messages.statusbar_new_sms[1] % p_num)
        
        #
        # Wait for the notification to be present for this number 
        # in the popup messages (this way we make sure it's coming from our number,
        # as opposed to just containing our number in the notification).
        #
        time.sleep(5)
        x = self.UTILS.waitForStatusBarNew(x, p_displayed=False, p_timeOut=p_timeout)

        self.UTILS.logResult(x, "SMS notifier from " + p_num + " found in status bar.")
        return x
    
