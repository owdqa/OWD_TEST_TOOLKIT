from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def getNetworkConnection(self):
        #
        # Tries several methods to get ANY network connection
        # (either wifi or dataConn).
        #
        
        # The other methods seem to hit a marionette error just now,
        # but gaiatest has this method so I'll stick to that if it works.
        try:
            self.connect_to_network()
            return
        except:
            # make sure airplane mode is off.
            if self.isNetworkTypeEnabled("airplane"):
                self.toggleViaStatusBar("airplane")
            
            # make sure at least dataconn is on.
            if not self.isNetworkTypeEnabled("data"):
                self.toggleViaStatusBar("data")
                
                # Device shows data mode in status bar.
                self.waitForStatusBarNew(DOM.Statusbar.dataConn, p_timeOut=60)
            
                
