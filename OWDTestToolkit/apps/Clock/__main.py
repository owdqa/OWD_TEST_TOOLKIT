from OWDTestToolkit.global_imports import *

import  checkAlarmPreview                  ,\
        checkAlarmRingDetails              ,\
        checkStatusbarIcon                 ,\
        createAlarm                        ,\
        deleteAllAlarms                    

class Clock (
            checkAlarmPreview.main,
            checkAlarmRingDetails.main,
            checkStatusbarIcon.main,
            createAlarm.main,
            deleteAllAlarms.main):
    
    def __init__(self, parent):
        self.apps       = parent.apps
        self.data_layer = parent.data_layer
        self.parent     = parent
        self.marionette = parent.marionette
        self.UTILS      = parent.UTILS
        self.actions    = Actions(self.marionette)

    def launch(self):
        #
        # Launch the app.
        #
        self.app = self.apps.launch(self.__class__.__name__)
        self.UTILS.waitForNotElements(DOM.GLOBAL.loading_overlay, self.__class__.__name__ + " app - loading overlay")
        return self.app

