from OWDTestToolkit.global_imports import *

import  addAppToHomescreen                 ,\
        addGroup                           ,\
        pickGroup                          ,\
        removeGroup                        ,\
        searchForApp                       

class EverythingMe (
            addAppToHomescreen.main,
            addGroup.main,
            pickGroup.main,
            removeGroup.main,
            searchForApp.main):
    
    def __init__(self, p_parent):
        self.apps       = p_parent.apps
        self.data_layer = p_parent.data_layer
        self.parent     = p_parent
        self.marionette = p_parent.marionette
        self.UTILS      = p_parent.UTILS
        self.actions    = Actions(self.marionette)

    def launch(self):
        #
        # Launch the app.
        #
        
        self.UTILS.goHome()
        
        #
        # Scroll to the left to expose the 'everything.me' screen.
        #
        x = self.UTILS.getElement(DOM.EME.search_field, "Search field")
        x.tap()
        self.UTILS.waitForElements(DOM.EME.groups, "EME groups", True, 30)

