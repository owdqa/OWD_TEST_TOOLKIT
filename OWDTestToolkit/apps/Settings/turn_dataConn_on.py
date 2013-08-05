from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def turn_dataConn_on(self, p_wifiOFF=False):
        #
        # Click slider to turn data connection on.
        #

        #
        # First, make sure we're in "Settings".
        #
        try:
            self.wait_for_element_present(*DOM.Settings.frame_locator, timeout=2)
            x = self.marionette.find_element(*DOM.Settings.frame_locator)
        except:
            #
            # Settings isn't running, so start it.
            #
            self.launch()
            self.cellular_and_data()
        
        if p_wifiOFF:
            if self.data_layer.get_setting("wifi.enabled"):
                self.data_layer.disable_wifi()
            
        time.sleep(1)

        if not self.data_layer.get_setting("ril.data.enabled"):
            #
            # If we disabled the wifi we'll be in the wrong frame here, so just make sure ...
            #
            self.marionette.switch_to_frame()
            self.UTILS.switchToFrame(*DOM.Settings.frame_locator)
            
            x = self.UTILS.getElement(DOM.Settings.celldata_DataConn, 
                                      "Connect to cellular and data switch",
                                      False, 5, False)
            try:
                x.tap()
            except:
                #
                # The element isn't visible, but we still want to enable dataconn,
                # so try using the 'back door' ...
                #
                self.UTILS.logResult("info", "(Marionette issue) Unable to start dataconn via U.I. - trying to force it using gaia data layer instead.")
                try:
                    self.data_layer.connect_to_cell_data()
                    self.UTILS.logResult("info", "(Marionette issue) Success!")
                except:
                    self.UTILS.logResult("info", "(Marionette issue) Unsuccessful!")

            self.marionette.switch_to_frame()
            self.UTILS.switchToFrame(*DOM.Settings.frame_locator)
            
        #
        # If we get prompted for action, say 'Turn ON'.
        #
        # (Because it's only 'if', we don't verfy this element.)
        #
        time.sleep(2)
        try:
            self.wait_for_element_displayed(*DOM.Settings.celldata_DataConn_ON, timeout=2)
            x = self.marionette.find_element(*DOM.Settings.celldata_DataConn_ON)
            if x.is_displayed():
                x.tap()
        except:
            pass

        #
        # Give it time to start up.
        #
        time.sleep(5)
        
        #
        # Check to see if data conn is now enabled (it may be, even if the icon doesn't appear).
        #
        self.UTILS.TEST(
            self.data_layer.get_setting("ril.data.enabled"),    
            "Data connection is enabled", True)
        
        #
        # Give the statusbar icon time to appear, then check for it.
        #
        # NOTE: 'p_wifiOFF' works here: if it's true then the icon SHOULD be there, else
        #       it shouldn't.
        #
        if not self.data_layer.get_setting("wifi.enabled"):
            x = self.UTILS.isIconInStatusBar(DOM.Statusbar.dataConn)
            self.UTILS.TEST(x, 
                            "Data connection icon is present in the status bar.", 
                            True)
        
        self.UTILS.goHome()


