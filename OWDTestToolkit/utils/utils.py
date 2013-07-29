from OWDTestToolkit.global_imports import *

import  app         ,\
        date_and_time,\
        debug       ,\
        element     ,\
        general     ,\
        home        ,\
        iframe      ,\
        network     ,\
        reporting   ,\
        statusbar   ,\
        test


class UTILS(app.main        ,
            date_and_time.main,
            debug.main      ,
            element.main    ,
            general.main    ,
            home.main       ,
            iframe.main     ,
            network.main    ,
            reporting.main  ,
            statusbar.main  ,
            test.main):
    #
    # When you create your instance of this class, include the
    # "self" object so we can access the calling class' objects.
    #
    def __init__(self, p_parent):
        self.parent         = p_parent
        self.device         = p_parent.device
        self.data_layer     = p_parent.data_layer
        self.apps           = p_parent.apps
        self.marionette     = p_parent.marionette
        self.actions        = Actions(self.marionette)

        #
        # Globals used for reporting ...
        #
        self._resultArray   = []
        self._commentArray  = []
        self.errNum         = 0
        self.passed         = 0
        self.failed         = 0
        self.start_time     = time.time()
        self.last_timestamp = time.time()
        
        #
        # Other globals ...
        #
        self._DEFAULT_ELEMENT_TIMEOUT = 5   

        #
        # Get run details from the OS.
        #
        varStr = "Setting OS variables ..."
        self.testNum        = self.get_os_variable("TEST_NUM", True)
        self.det_fnam       = self.get_os_variable("DET_FILE", True)
        self.sum_fnam       = self.get_os_variable("SUM_FILE", True)
        self.logResult("info", "Get OS variables ..." +\
                               "|self.testNum  = '" + str(self.testNum)  + "'." +\
                               "|self.det_fnam = '" + str(self.det_fnam) + "'." +\
                               "|self.sum_fnam = '" + str(self.sum_fnam) + "'."
                               )
                
        #
        # Set device defaults.
        #
        a=self.setSetting("vibration.enabled",          True,   True)
        b=self.setSetting("audio.volume.notification",  0,      True)
        c=self.setSetting('ril.radio.disabled',         False,  True)
        self.logResult("info", "Default device settings ..." +\
                               "|Set 'vibration.enabled'         = True  " + ("[OK]" if a else "[UNABLE TO SET!]!") +\
                               "|Set 'audio.volume.notification' = 0     " + ("[OK]" if b else "[UNABLE TO SET!]!") +\
                               "|Set 'ril.radio.disabled'        = False " + ("[OK]" if c else "[UNABLE TO SET!]!")
                                )
    
        a=self.setPermission('Camera', 'geolocation', 'deny', True)
        b=self.setPermission('Homescreen', 'geolocation', 'deny', True)
        self.logResult("info", "Default app permissions ..." +\
                               "|Set 'Camera'     -> 'geolocation' = True  " + ("[OK]" if a else "[UNABLE TO SET!]!") +\
                               "|Set 'Homescreen' -> 'geolocation' = True  " + ("[OK]" if a else "[UNABLE TO SET!]!")
                               )
            

        self.marionette.set_search_timeout(20)

        try:
            self.setTimeToNow()
        except:
            self.logResult("info", "WARNING: Failed to set the current time on this device!")
        
        try:
            self.setupDataConn()
        except:
            self.logResult("info", "WARNING: Failed to set up the data conn details (APN etc...)!")
            
        #
        # Remove any current contacts (it would be nice to do more, but at the
        # moment this will do).
        #
        self.data_layer.remove_all_contacts()
        self.apps.kill_all()
        time.sleep(2)
        
        #
        # Unlock (if necessary).
        #
        self.parent.lockscreen.unlock()
