from OWDTestToolkit.global_imports import *

import  cellular_and_data                  ,\
        wifi_list_isConnected              ,\
        wifi_list_isNotConnected           ,\
        goSound                            ,\
        setAlarmVolume                     ,\
        setRingerAndNotifsVolume           ,\
        setTimeToNow                       ,\
        wifi_connect                       ,\
        turn_dataConn_on                   ,\
        wifi_switchOn                      ,\
        wifi                               ,\
        hotSpot                            ,\
        enable_hotSpot                     ,\
        disable_hotSpot                    ,\
        goBack                             ,\
        wifi_list_tapName                  ,\
        first_time_use                     ,\
        wifi_forget

class Settings (
            cellular_and_data.main,
            wifi_list_isConnected.main,
            wifi_list_isNotConnected.main,
            goSound.main,
            setAlarmVolume.main,
            setRingerAndNotifsVolume.main,
            setTimeToNow.main,
            wifi_connect.main,
            turn_dataConn_on.main,
            wifi_switchOn.main,
            wifi.main,
            hotSpot.main,
            enable_hotSpot.main,
            disable_hotSpot.main,
            goBack.main,
            wifi_list_tapName.main,
            first_time_use.main,
            wifi_forget.main):
    
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

