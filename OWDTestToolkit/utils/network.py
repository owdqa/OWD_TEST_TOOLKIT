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

    def getNetworkConnection(self):
        #
        # Tries several methods to get ANY network connection
        # (either wifi or dataConn).
        #

        # The other methods seem to hit a marionette error just now,
        # but gaiatest has this method so I'll stick to that if it works.
        try:
            self.parent.parent.connect_to_network()
            return
        except:
            # make sure airplane mode is off.
            if self.isNetworkTypeEnabled("airplane"):
                self.parent.statusbar.toggleViaStatusBar("airplane")

            # make sure at least dataconn is on.
            if not self.isNetworkTypeEnabled("data"):
                self.parent.statusbar.toggleViaStatusBar("data")

                # Device shows data mode in status bar.
                self.parent.statusbar.waitForStatusBarNew(DOM.Statusbar.dataConn, p_timeOut=60)

    def isNetworkTypeEnabled(self, p_type):
        #
        # Returns True or False.<br><br>
        # Accepted 'types' are:<br>
        # <b>data</b><br>
        # <b>wifi</b><br>
        # <b>airplane</b><br>
        # <i>bluetooth (**NOT WORKING CURRENTLY!!**)</i>
        #
        enabled = False
        if p_type == "data":
            enabled = self.parent.data_layer.is_cell_data_enabled
        elif p_type == "wifi":
            enabled = self.parent.data_layer.is_wifi_enabled
        elif p_type == "airplane":
            enabled = self.parent.data_layer.get_setting('ril.radio.disabled')
        elif p_type == "bluetooth":
            enabled = self.parent.data_layer.bluetooth_is_enabled
        else:
            self.parent.test.TEST(False, "Incorrect parameter '" + str(p_type) +
                              "' passed to UTILS.isNetworkTypeEnabled()!", True)
        return enabled

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

    def waitForNetworkItemDisabled(self, p_type, retries=30):
        #
        # Waits for network 'item' to be disabled.
        # <br><br>
        # Accepted 'types' are:<br>
        # <b>data</b><br>
        # <b>wifi</b><br>
        # <b>airplane</b><br>
        # <b>bluetooth</b>
        #
        is_ok = False
        for i in range(retries):
            if not self.isNetworkTypeEnabled(p_type):
                is_ok = True
                break
            time.sleep(2)
        self.parent.test.TEST(is_ok, "'{}' mode disabled within {} seconds.".format(p_type, retries * 2))

    def waitForNetworkItemEnabled(self, p_type, retries=30):
        #
        # Waits for network 'item' to be enabled.
        # <br><br>
        # Accepted 'types' are:<br>
        # <b>data</b><br>
        # <b>wifi</b><br>
        # <b>airplane</b><br>
        # <b>bluetooth</b>
        #
        is_ok = False
        for i in range(retries):
            if self.isNetworkTypeEnabled(p_type):
                is_ok = True
                break
            time.sleep(2)
        self.parent.test.TEST(is_ok, "'{}' mode enabled within {} seconds.".format(p_type, retries * 2))
        return is_ok

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
