from OWDTestToolkit.global_imports import *

import  cellular_and_data                  ,\
        checkWifiLisetedAsConnected        ,\
        goSound                            ,\
        setAlarmVolume                     ,\
        setRingerAndNotifsVolume           ,\
        setTimeToNow                       ,\
        tap_wifi_network_name              ,\
        turn_dataConn_on                   ,\
        turn_wifi_on                       ,\
        wifi                               ,\
        hotSpot

class Settings (
            cellular_and_data.main,
            checkWifiLisetedAsConnected.main,
            goSound.main,
            setAlarmVolume.main,
            setRingerAndNotifsVolume.main,
            setTimeToNow.main,
            tap_wifi_network_name.main,
            turn_dataConn_on.main,
            turn_wifi_on.main,
            wifi.main,
            hotSpot.main):
    
    def __init__(self, p_parent):
        self.apps       = p_parent.apps
        self.data_layer = p_parent.data_layer
        self.parent     = p_parent
        self.marionette = p_parent.marionette
        self.UTILS      = p_parent.UTILS

    def launch(self):
        #
        # Launch the app.
        #
        self.app = self.apps.launch(self.__class__.__name__)
        self.UTILS.waitForNotElements(DOM.GLOBAL.loading_overlay, self.__class__.__name__ + " app - loading overlay")
        return self.app

