import time
import datetime
from marionette import Actions
from app import app
from date_and_time import date_and_time
from debug import debug
from element import element
from general import general
from home import home
from iframe import iframe
from messages import Messages
from network import network
from reporting import reporting
from statusbar import statusbar
from test import test


class UTILS(object):

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
        # Get run details from the OS.
        #
        self.general = general(self)
        self.testNum = self.general.get_os_variable("TEST_NUM", True)
        self.det_fnam = self.general.get_os_variable("DET_FILE", True)
        self.sum_fnam = self.general.get_os_variable("SUM_FILE", True)

        self.app = app(self)
        self.date_and_time = date_and_time(self)
        self.debug = debug(self)
        self.element = element(self, 5)
        self.home = home(self)
        self.iframe = iframe(self)
        self.messages = Messages(self)
        self.network = network(self)
        self.reporting = reporting(self, self._resultArray, self._commentArray)
        self.statusbar = statusbar(self)
        self.test = test(self)

        self.marionette.set_search_timeout(10000)
        self.marionette.set_script_timeout(10000)

        elapsed = time.time() - self.start_time
        elapsed = round(elapsed, 0)
        elapsed = str(datetime.timedelta(seconds=elapsed))
        self.reporting.logResult("debug", "Initializing 'UTILS' took {} seconds.".format(elapsed))
        current_lang = parent.data_layer.get_setting("language.current").split('-')[0]
        self.reporting.log_to_file("Current Toolkit language: [{}]".format(current_lang))
