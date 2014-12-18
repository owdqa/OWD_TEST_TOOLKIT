from OWDTestToolkit import DOM
import time


class Ftu(object):

    def __init__(self, parent):
        self.apps = parent.apps
        self.data_layer = parent.data_layer
        self.parent = parent
        self.marionette = parent.marionette
        self.UTILS = parent.UTILS

    def launch(self):
        self.app = self.apps.launch(self.__class__.__name__)
        self.UTILS.element.waitForNotElements(DOM.GLOBAL.loading_overlay, self.__class__.__name__ + " app - loading overlay")
        return self.app

    def end_tour(self):
        """
        Click to end the Tour.
        """
        x = self.UTILS.element.getElement(DOM.FTU.tour_finished_btn, "Finish tour button")
        x.tap()
        time.sleep(1)

    def next_screen(self):
        """
        Click to the next screen (works until you get to the tour).
        """
        x = self.UTILS.element.getElement(DOM.FTU.next_button, "Next button")
        x.tap()
        time.sleep(0.5)

    def next_tour_screen(self):
        """
        Click to next page of the Tour.
        """
        x = self.UTILS.element.getElement(DOM.FTU.tour_next_btn, "Tour 'next' button")
        x.tap()
        time.sleep(1)

    def set_data_conn_enabled(self):
        """
        Enable data.
        """
        self.UTILS.element.waitForElements(DOM.FTU.section_cell_data, "Cellular data connection section")

        # (the switch has an "id", but if you use that it never becomes 'visible'!)
        x = self.UTILS.element.getElement(DOM.FTU.dataconn_switch, "Data connection switch")
        x.tap()

        # Wait a moment, then check data conn is on.
        time.sleep(3)
        self.UTILS.test.test(self.parent.data_layer.get_setting("ril.data.enabled"),
                        "Data connection is enabled after trying to enable it.", True)

    def set_language(self, language):
        """
        Set the language (assume we're in the language screen).
        """
        time.sleep(1)
        x = self.UTILS.element.getElements(DOM.FTU.language_list, "Language list", True, 20, False)

        if len(x) > 0:
            for i in x:
                if i.text == language:
                    i.tap()
                    return True
        return False

    def set_network(self, wlan_name, username, passwd):
        """
        Join a wifi network.
        """
        time.sleep(5)
        x = self.UTILS.element.getElements(DOM.FTU.wifi_networks_list, "Wifi network list")
        x.tap()

        # Pick the one we chose.
        x = self.UTILS.element.getElement(('id', wlan_name), "Wifi network '" + wlan_name + "'")
        x.tap()

        # In case we are asked for a username and password ...
        time.sleep(2)
        try:
            self.parent.wait_for_element_displayed(*DOM.FTU.wifi_login_user, timeout=2)
            wifi_login_user = self.marionette.find_element(*DOM.FTU.wifi_login_user)
            wifi_login_pass = self.marionette.find_element(*DOM.FTU.wifi_login_pass)
            wifi_login_join = self.marionette.find_element(*DOM.FTU.wifi_login_join)
            wifi_login_user.send_keys(username)
            wifi_login_pass.send_keys(passwd)
            wifi_login_join.tap()
        except:
            pass

    def set_timezone(self, continent, city):
        """
        Set the timezone.
        """
        self.UTILS.element.waitForElements(DOM.FTU.timezone, "Timezone area")

        # Continent.
        tz_buttons = self.UTILS.element.getElements(DOM.FTU.timezone_buttons, "Timezone buttons (for continent)")
        # Must be 'clicked' not 'tapped'
        tz_buttons[0].click()
        self.UTILS.general.selectFromSystemDialog(continent)

        # City.
        tz_buttons = self.UTILS.element.getElements(DOM.FTU.timezone_buttons, "Timezone buttons (for city)")
        # Must be 'clicked' not 'tapped'
        tz_buttons[1].click()
        self.UTILS.general.selectFromSystemDialog(city)

        self.UTILS.test.test(continent + "/" + city in self.UTILS.element.getElement(DOM.FTU.timezone_title, "Timezone title").text,
                        "Locality is set up correctly")

    def skipTour(self):
        """
        Click to skip the Tour.
        """
        x = self.UTILS.element.getElement(DOM.FTU.tour_skip_btn, "Skip tour button")
        x.tap()
        time.sleep(1)

    def startTour(self):
        """
        Click to start the Tour.
        """
        x = self.UTILS.element.getElement(DOM.FTU.tour_start_btn, "Start tour button")
        x.tap()
        time.sleep(0.5)
