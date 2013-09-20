from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def waitForNoNetworkActivity(self, p_timeout=10):
        #
        # Waits for the network activity icon in the status bar to dissappear.<br>
        # <b>NOTE:</b> Leaves you in the root iframe and returns True or False.
        #
        self.checkMarionetteOK()
        self.marionette.switch_to_frame()
        
        #
        # The network activity icon sometimes 'comes and goes', so make sure it's
        # not displayed for at least 5 seconds before reporting it as 'gone'.
        #
        for i in range(0,10):
            try:
                self.wait_for_element_not_displayed(*DOM.Statusbar.network_activity, timeout=p_timeout)
                try:
                    self.wait_for_element_displayed(*DOM.Statusbar.network_activity, timeout=5)
                    #
                    # It came back again - this isn't 'gone.
                    #
                except:
                    #
                    # It didn't reappear in 5 seconds: it's gone.
                    #
                    time.sleep(1)
                    return True
            except:
                time.sleep(0.5)
        
        #
        # If you ge to here then it never went away.
        #        
        return False
