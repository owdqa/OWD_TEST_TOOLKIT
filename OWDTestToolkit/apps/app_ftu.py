import time
from gaiatest   import GaiaTestCase
from marionette import Marionette
from OWDTestToolkit import *

class AppFTU(GaiaTestCase):
    
    #
    # When you create your instance of this class, include the
    # "self" object so we can access the calling class' objects.
    #
    def __init__(self, p_parent):

        self.apps       = p_parent.apps
        self.data_layer = p_parent.data_layer
        self.marionette = p_parent.marionette
        self.UTILS      = p_parent.UTILS
            
    def launch(self):
        #
        # Launch the app.
        #
        self.apps.kill_all()
        
        # We need WiFi enabled but not connected to a network
        self.data_layer.enable_wifi()
        self.data_layer.forget_all_networks()

        # Cell data must be off so we can switch it on again
        self.data_layer.disable_cell_data()

        self.app = self.apps.launch('FTU')
        self.UTILS.waitForNotElements(DOM.GLOBAL.loading_overlay, "FTU app - loading overlay");

    def setLanguage(self, p_lang):
        #
        # Set the language (assume we're in the language screen).
        time.sleep(1)
        x = self.UTILS.getElements(DOM.FTU.language_list, "Language list", True, 20, False)
        
        if len(x) > 0:
            for i in x:
                if i.text == p_lang:
                    i.tap()
                    return True
        
        return False
        
    def nextScreen(self):
        #
        # Click to the next screen (works until you get to the tour).
        #
        x = self.UTILS.getElement(DOM.FTU.next_button, "Next button")
        x.tap()
        time.sleep(0.5)
        
    def startTour(self):
        #
        # Click to start the Tour.
        #
        x = self.UTILS.getElement(DOM.FTU.tour_start_btn, "Start tour button")
        x.tap()
        time.sleep(0.5)

    def skipTour(self):
        #
        # Click to skip the Tour.
        #
        x = self.UTILS.getElement(DOM.FTU.tour_skip_btn, "Skipt tour button")
        x.tap()
        time.sleep(1)

    def nextTourScreen(self):
        #
        # Click to next page of the Tour.
        #
        x = self.UTILS.getElement(DOM.FTU.tour_next_btn, "Tour 'next' button")
        x.tap()
        time.sleep(1)

    def endTour(self):
        #
        # Click to end the Tour.
        #
        x = self.UTILS.getElement(DOM.FTU.tour_finished_btn, "Finish tour button")
        x.tap()
        time.sleep(1)

    def setDataConnEnabled(self):
        #
        # Enable data.
        #
        
        self.UTILS.waitForElements(DOM.FTU.section_cell_data, "Cellular data connection section")

        # (the switch has an "id", but if you use that it never becomes 'visible'!)
        x = self.UTILS.getElement(DOM.FTU.dataconn_switch, "Data connection switch")
        x.tap()
        
        # Wait a moment, then check data conn is on.
        time.sleep(3)
        self.UTILS.TEST(
            self.data_layer.get_setting("ril.data.enabled"),    
            "Data connection is enabled after trying to enable it.", True)
        
    def setNetwork(self, p_wifiName, p_userName, p_password):
        #
        # Join a wifi network.
        #
        time.sleep(5)
        x = self.UTILS.getElements(DOM.FTU.wifi_networks_list, "Wifi network list")

        #
        # Pick the one we chose.
        #
        x= self.UTILS.getElement(('id', p_wifiName), "Wifi network '" + p_wifiName + "'")
        x.tap()
            
        #
        # In case we are asked for a username and password ...
        #
        time.sleep(2)
        wifi_login_user = self.marionette.find_element(*DOM.FTU.wifi_login_user)
        if wifi_login_user.is_displayed():
            wifi_login_pass = self.marionette.find_element(*DOM.FTU.wifi_login_pass)
            wifi_login_join = self.marionette.find_element(*DOM.FTU.wifi_login_join)
            wifi_login_user.send_keys(p_userName)
            wifi_login_pass.send_keys(p_password)
            wifi_login_join.tap()
        
    def setTimezone(self, p_continent, p_city):
        #
        # Set the timezone.
        #
        self.UTILS.waitForElements(DOM.FTU.timezone, "Timezone area")
        
        # Continent.
        tz_buttons = self.UTILS.getElements(DOM.FTU.timezone_buttons, "Timezone buttons (for continent)")
        tz_buttons[0].click() # Must be 'clicked' not 'tapped'
        self.UTILS.selectFromSystemDialog(p_continent)

        # City.
        tz_buttons = self.UTILS.getElements(DOM.FTU.timezone_buttons, "Timezone buttons (for city)")
        tz_buttons[1].click() # Must be 'clicked' not 'tapped'
        self.UTILS.selectFromSystemDialog(p_city)

        self.UTILS.TEST(
            p_continent + "/" + p_city in self.UTILS.getElement(DOM.FTU.timezone_title, "Timezone title").text,
            "Locality is set up correctly")
