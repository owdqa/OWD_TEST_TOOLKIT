import time
from gaiatest   import GaiaTestCase
from marionette import Marionette
from OWDTestToolkit import *

class AppSettings(GaiaTestCase):
    
    #
    # When you create your instance of this class, include the
    # "self" object so we can access the calling class' objects.
    #
    def __init__(self, p_parent):
        self.apps       = p_parent.apps
        self.data_layer = p_parent.data_layer
        self.marionette = p_parent.marionette
        self.UTILS      = p_parent.UTILS
        self.parent     = p_parent

    def launch(self):
        #
        # Launch the app.
        #
        self.apps.kill_all()
        self.app = self.apps.launch('Settings')
        self.UTILS.waitForNotElements(DOM.GLOBAL.loading_overlay, "Settings app - loading overlay");

    def cellular_and_data(self):
        #
        # Open cellular and data settings.
        #
        x = self.UTILS.getElement(DOM.Settings.cellData, "Cellular and Data settings link")
        x.tap()
        
        self.UTILS.waitForElements(DOM.Settings.celldata_header, "Celldata header", True, 20, False)

    def turn_dataConn_on(self, p_wifiOFF=False):
        #
        # Click slider to turn data connection on.
        #

        #
        # First, make sure we're in "Settings".
        #
        try:
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
            
            self.UTILS.waitForElements(DOM.Settings.celldata_DataConn, 
                                      "Connect to cellular and data switch",
                                      False, 5, False)
            x = self.marionette.find_element(*DOM.Settings.celldata_DataConn)
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


    def wifi(self):
        #
        # Open wifi settings.
        #
        x = self.UTILS.getElement(DOM.Settings.wifi, "Wifi settings link")
        x.tap()
        
        self.UTILS.waitForElements(DOM.Settings.wifi_header, "Wifi header appears.", True, 20, False)

    def turn_wifi_on(self):
        #
        # Click slider to turn wifi on.
        #
        if not self.data_layer.get_setting("wifi.enabled"):
            x = self.UTILS.getElement(DOM.Settings.wifi_enabled, "Enable wifi switch")
            x.tap()
        
        #
        # Nothing to check for yet, because the network may require login etc...,
        # so just wait a little while before proceeding ...
        #
        time.sleep(3)
        
    def checkWifiLisetedAsConnected(self, p_name):
        #
        # Verify the expected network is listed as connected in 'available networks'.
        #

        # 
        # Wait a little time to be sure the networks are all listed.
        #
        time.sleep(5)
        
        #
        # Compare the available networks - if one's connected then check it's the
        # one we expect (starts at array 3).
        #
        x = self.UTILS.getElements(DOM.Settings.wifi_available_networks, "Available networks list", False, 20, False)
        for i in range(3, len(x)):
            connStatus = self.marionette.find_element('xpath', DOM.Settings.wifi_available_status % i)
            connName   = self.marionette.find_element('xpath', DOM.Settings.wifi_available_name   % i)
            
            if ("Connected" in connStatus.text) and (p_name == connName.text):
                return True
            else:
                return False
        #
        # If we get to here, we didn't find the network we were looking for.
        #
        return False
        
    def tap_wifi_network_name(self, p_wifi_name, p_user, p_pass):
        #
        # Select a network.
        #
        wifi_name_element = DOM.Settings.wifi_name_xpath % p_wifi_name
        x= self.UTILS.getElement(('xpath', wifi_name_element), "Wifi '" + p_wifi_name + "'", True, 30, True)
        if x:
            x.tap()
        else:
            return False
        
        #
        # In case we are asked for a username and password ...
        #
        time.sleep(2)
        wifi_login_user = self.marionette.find_element(*DOM.Settings.wifi_login_user)
        if wifi_login_user.is_displayed():
            wifi_login_pass = self.UTILS.getElement(DOM.Settings.wifi_login_pass, "Wifi password field")
            wifi_login_user.send_keys(p_user)
            wifi_login_pass.send_keys(p_pass)
            time.sleep(1)
            wifi_login_ok   = self.UTILS.getElement(DOM.Settings.wifi_login_ok_btn, "Ok button")
            wifi_login_ok.tap()
        else:
            #
            # We were not asked, so go back to the list.
            #
            backBTN = self.UTILS.getElement(DOM.Settings.back_button, "Back button")
            backBTN.tap()

            self.UTILS.TEST(self.UTILS.headerCheck("Wi-Fi"), "Header is 'Wi-Fi'.")
        
        #
        # A couple of checks to wait for 'anything' to be Connected (only look for 'present' because it
        # might be off the bottom of the page).
        #
        self.UTILS.waitForElements(DOM.Settings.wifi_connected, "Connected Wifi network", False, 30)
        
        self.UTILS.TEST(self.data_layer.get_setting("wifi.enabled"),
            "Wifi connection to '" + p_wifi_name + "' established.", True)

    def setAlarmVolume(self, p_vol):
        #
        # Set the volume for alarms.
        #
        self.data_layer.set_setting('audio.volume.alarm', p_vol)
        
    def setRingerAndNotifsVolume(self, p_vol):
        #
        # Set the volume for ringer and notifications.
        #
        self.data_layer.set_setting('audio.volume.notification', p_vol)
        
    def goSound(self):
        #
        # Go to Sound menu.
        #
        self.launch()
        x = self.UTILS.getElement(DOM.Settings.sound, "Sound setting link")
        x.tap()


    def _getPickerSpinnerElement(self, p_DOM, p_msg):
        #
        # Returns the element for the spinner in a picker.
        # 
        
        # Get the elements that match this one.
        els = self.UTILS.getElements(p_DOM, p_msg, False, 20, True)
        
        # Get the one that's not hidden (the 'hidden'
        # attribute here has no 'value', so we need to just
        # check if it's been set to "".
        boolOK = False
        el     = False
        for i in els:
            if str(i.get_attribute("hidden")) == "false":
                boolOK = True
                el = i
                break
        
        self.UTILS.TEST(boolOK, "... one of them is visible|('hidden' attribute is not set)", True)
        return el

    def setTimeToNow(self):
        #
        # Set date and time to 'now'.<br>
        # WARNING: DOES NOT WORK YET!!! ...<br>
        #   1. Marionette.flick() not working here.<br>
        #   2. Cannot figure out how to tell what the current value is (no 'active' setting here),
        #
        return
        self.launch()
         
        x = ("id", "menuItem-dateAndTime")
        el = self.UTILS.getElement(x, "Date & Time setting")
        el.tap()
         
        x = ("id", "clock-date")
        el = self.UTILS.getElement(x, "Date setting")
        el.click()
         
        time.sleep(2)        
        self.marionette.switch_to_frame()
