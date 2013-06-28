from OWDTestToolkit.global_imports import *

import  app         ,\
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
        self.testNum        = self.get_os_variable("TEST_NUM")
        self.det_fnam       = self.get_os_variable("DET_FILE")
        self.sum_fnam       = self.get_os_variable("SUM_FILE")
        self.logResult("info", "Get OS variables ...|" +\
                               "self.testNum  = '" + str(self.testNum)  + "'.|" +\
                               "self.det_fnam = '" + str(self.det_fnam) + "'.|" +\
                               "self.sum_fnam = '" + str(self.sum_fnam) + "'."
                               )
                
        try:
            self.testDesc   = self.parent._Description
        except:
            self.testDesc   = "(no description found!)"
        

        #
        # Set device defaults.
        #
        self.setSetting("vibration.enabled", True)
        self.setSetting("audio.volume.notification", 0)
        self.setSetting('ril.radio.disabled', False)
    
        self.setPermission('Camera', 'geolocation', 'deny')
        self.setPermission('Homescreen', 'geolocation', 'deny')
            

        self.marionette.set_search_timeout(20)

        self.setTimeToNow()
        
        self.setupDataConn()
         
        #
        # Unlock (if necessary).
        #
        self.parent.lockscreen.unlock()
        
