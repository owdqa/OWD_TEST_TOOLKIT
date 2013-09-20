from OWDTestToolkit.global_imports import *

import  check_page_loaded                  ,\
        open_url                           ,\
        waitForPageToFinishLoading         ,\
        loadedURL                          ,\
        trayCounterValue,\
        searchUsingUrlField,\
        addNewTab

class Browser (
            check_page_loaded.main,
            open_url.main,
            waitForPageToFinishLoading.main,
            loadedURL.main,
            trayCounterValue.main,
            searchUsingUrlField.main,
            addNewTab.main):
    
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

