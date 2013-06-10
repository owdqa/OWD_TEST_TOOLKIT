from OWDTestToolkit.global_imports import *

import  installApp                         ,\
        searchForApp                       ,\
        selectSearchResultApp              

class Marketplace (
            installApp.main,
            searchForApp.main,
            selectSearchResultApp.main):
    
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
        self.apps.kill_all()
        
        # WARNING: Marketplace is in a weird place - you need to use "Marketplace Dev"!!
#         self.app = self.apps.launch(self.__class__.__name__)
        self.app = self.apps.launch("Marketplace Dev")

        self.UTILS.waitForNotElements(DOM.Market.market_loading_icon, 
                                      self.__class__.__name__ + " app - loading icon",
                                      True,
                                      30)

