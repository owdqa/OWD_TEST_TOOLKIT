import time
from OWDTestToolkit import DOM


class network(object):

    def __init__(self, parent):
        self.parent = parent
        self.marionette = parent.marionette

    def disableAllNetworkSettings(self):
        #
        # Turns off all network settings (wifi, dataconn, bluetooth and airplane mode).
        #
        if self.parent.data_layer.get_setting('ril.radio.disabled'):
            self.parent.data_layer.set_setting('ril.radio.disabled', False)

        if self.parent.device.has_mobile_connection:
            self.parent.data_layer.disable_cell_data()

        self.parent.data_layer.disable_cell_roaming()

        if self.parent.device.has_wifi:
            self.parent.general.checkMarionetteOK()
            try:
                self.parent.data_layer.enable_wifi()
            except:
                self.parent.reporting.logResult(False, "Enabled wifi")

            self.parent.general.checkMarionetteOK()
            try:
                self.parent.data_layer.forget_all_networks()
            except:
                self.parent.reporting.logResult(False, "Forgot all wifi networks")

            self.parent.general.checkMarionetteOK()
            try:
                self.parent.data_layer.disable_wifi()
            except:
                self.parent.reporting.logResult(False, "Disabled wifi")

    def is_network_type_enabled(self, network_type):
        #
        # Returns True or False.<br><br>
        # Accepted 'types' are:<br>
        # <b>data</b><br>
        # <b>wifi</b><br>
        # <b>airplane</b><br>
        # <i>bluetooth (**NOT WORKING CURRENTLY!!**)</i>
        #
        if network_type == "data":
            return self.parent.data_layer.is_cell_data_enabled
        elif network_type == "wifi":
            return self.parent.data_layer.is_wifi_enabled
        elif network_type == "airplane":
            return self.parent.data_layer.get_setting('ril.radio.disabled')
        elif network_type == "bluetooth":
            return self.parent.data_layer.bluetooth_is_enabled
        else:
            self.parent.test.test(False, 
                "Incorrect parameter '{}' passed to UTILS.is_network_type_enabled()!".format(network_type), True)

    def turnOnDataConn(self):
        """Turn the data connection on.
        """
        enabled = self.parent.data_layer.get_setting("ril.data.enabled")
        if not enabled:
            data_conn_switch = self.parent.element.getElement(DOM.Settings.enable_data_connection,
                                                              "Enable data connection")
            data_conn_switch.tap()
            x = self.parent.element.getElement(DOM.Settings.celldata_DataConn_ON, "Confirm enabling data connection")
            x.tap()

    def _wait_for_item(self, network_type, value):
        if value:
            self.parent.parent.wait_for_condition(lambda m: self.is_network_type_enabled(
                network_type), timeout=30, message="Checking network item is enabled")
        else:
            self.parent.parent.wait_for_condition(lambda m: not self.is_network_type_enabled(
                network_type), timeout=30, message="Checking network item is disabled")

    def wait_for_network_item_disabled(self, network_type):
        #
        # Waits for network 'item' to be disabled.
        # <br><br>
        # Accepted 'types' are:<br>
        # <b>data</b><br>
        # <b>wifi</b><br>
        # <b>airplane</b><br>
        # <b>bluetooth</b>
        #
        self._wait_for_item(network_type, False)

    def wait_for_network_item_enabled(self, network_type, retries=30):
        #
        # Waits for network 'item' to be enabled.
        # <br><br>
        # Accepted 'types' are:<br>
        # <b>data</b><br>
        # <b>wifi</b><br>
        # <b>airplane</b><br>
        # <b>bluetooth</b>
        #
        self._wait_for_item(network_type, True)

    def waitForNoNetworkActivity(self, p_timeout=10):
        #
        # Waits for the network activity icon in the status bar to dissappear.<br>
        # <b>NOTE:</b> Leaves you in the root iframe and returns True or False.
        #
        self.parent.general.checkMarionetteOK()
        self.marionette.switch_to_frame()

        #
        # The network activity icon sometimes 'comes and goes', so make sure it's
        # not displayed for at least 5 seconds before reporting it as 'gone'.
        #
        for i in range(10):
            try:
                self.parent.parent.wait_for_element_not_displayed(*DOM.Statusbar.network_activity, timeout=p_timeout)
                try:
                    self.parent.parent.wait_for_element_displayed(*DOM.Statusbar.network_activity, timeout=5)
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
        # If you get here then it never went away.
        #
        return False
