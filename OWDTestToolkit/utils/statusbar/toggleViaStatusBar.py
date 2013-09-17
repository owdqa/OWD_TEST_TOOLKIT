from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def toggleViaStatusBar(self, p_type):
        #
        # Uses the statusbar to toggle items on or off.<br>
        # <b>NOTE:</b> Doesn't care if it's toggling items ON or OFF. It just toggles!
        # <br><br>
        # Accepted 'types' are:<br>
        # <b>data</b><br>
        # <b>wifi</b><br>
        # <b>airplane</b><br>
        # <b>bluetooth</b>
        #
        self.logResult("info", "Toggling " + p_type + " mode via statusbar ...")
        orig_iframe = self.currentIframe()

        #
        # Toggle (and wait).
        #
        _wifi       = {"name":"wifi"     , "notif":DOM.Statusbar.wifi     , "toggle":DOM.Statusbar.toggle_wifi}
        _data       = {"name":"data"     , "notif":DOM.Statusbar.dataConn , "toggle":DOM.Statusbar.toggle_dataconn}
        _bluetooth  = {"name":"bluetooth", "notif":DOM.Statusbar.bluetooth, "toggle":DOM.Statusbar.toggle_bluetooth}
        _airplane   = {"name":"airplane" , "notif":DOM.Statusbar.airplane , "toggle":DOM.Statusbar.toggle_airplane}

        if p_type == "data"     : typedef = _data
        if p_type == "wifi"     : typedef = _wifi
        if p_type == "bluetooth": typedef = _bluetooth
        if p_type == "airplane" : typedef = _airplane
        
        boolReturn = self._sb_doToggle(typedef, p_type)
        
        #
        # Close the statusbar and return to the original frame (if required).
        #
        self.touchHomeButton() 
        if orig_iframe: self.switchToFrame("src", orig_iframe)
        
        return boolReturn
        
    def _sb_doToggle(self, p_def, p_type):
        #
        # (private) Toggle a button in the statusbar.
        # Don't call this directly, it's used by toggleViaStatusBar().
        #
        boolWasEnabled = self.isNetworkTypeEnabled(p_type)

        #
        # Open the status bar.
        #
        self.displayStatusBar()

        x = self.getElement(p_def["toggle"], "Toggle " + p_def["name"] + " icon")
        x.tap()

        boolReturn = True
        if boolWasEnabled:
            boolReturn = self.waitForNetworkItemDisabled(p_type)
        else:
            boolReturn = self.waitForNetworkItemEnabled(p_type)
            
        return boolReturn