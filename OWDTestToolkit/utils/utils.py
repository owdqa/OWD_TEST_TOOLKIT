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

        self.marionette.set_search_timeout(10000)
        self.marionette.set_script_timeout(10000)

        _t = time.time() - self.start_time
        _t = round(_t, 0)
        _t = str(datetime.timedelta(seconds=_t))
        self.logResult("debug", "(Initializing 'UTILS' took %s seconds.)" % _t)

        #
        # The following items used to be set here - I've left them in incase
        # it causes an issue later. In the meantime it's best to set these
        # in specific test cases for speed.
        #
#         a=self.setSetting("vibration.enabled",          True,   True)
#         b=self.setSetting("audio.volume.notification",  0,      True)
#         c=self.setSetting('ril.radio.disabled',         False,  True)
#         a=self.setPermission('Camera', 'geolocation', 'deny', True)
#         b=self.setPermission('Homescreen', 'geolocation', 'deny', True)
#         try:
#             self.setTimeToNow()
#         except:
#             self.logResult("info", "WARNING: Failed to set the current time on this device!")
#         try:
#             self.setupDataConn()
#         except:
#             self.logResult("info", "WARNING: Failed to set up the data conn details (APN etc...)!")
#         self.data_layer.remove_all_contacts()
#         self.apps.kill_all()
#         time.sleep(2)
#         self.parent.lockscreen.unlock()

