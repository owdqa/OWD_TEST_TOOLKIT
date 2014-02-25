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
    def __init__(self, parent):
        self.parent = parent
        self.device = parent.device
        self.data_layer = parent.data_layer
        self.apps = parent.apps
        self.marionette = parent.marionette
        self.actions = Actions(self.marionette)

        #
        # Globals used for reporting ...
        #
        self._resultArray = []
        self._commentArray = []
        self.errNum = 0
        self.passed = 0
        self.failed = 0
        self.start_time = time.time()
        self.last_timestamp = time.time()

        #
        # Other globals ...
        #
        self._DEFAULT_ELEMENT_TIMEOUT = 5

        #
        # Get run details from the OS.
        #
        self.testNum = self.get_os_variable("TEST_NUM", True)
        self.det_fnam = self.get_os_variable("DET_FILE", True)
        self.sum_fnam = self.get_os_variable("SUM_FILE", True)

        self.marionette.set_search_timeout(10000)
        self.marionette.set_script_timeout(10000)

        elapsed = time.time() - self.start_time
        elapsed = round(elapsed, 0)
        elapsed = str(datetime.timedelta(seconds=elapsed))
        self.logResult("debug", "(Initializing 'UTILS' took {} seconds.)".format(elapsed))
