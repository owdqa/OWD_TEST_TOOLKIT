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
        # If EME has already been launched, then the DOM has changed.
        #
        try:
            x = self.marionette.find_element(*DOM.EME.search_field)
            x.tap()
            self.UTILS.logResult("info", "Everything ME was already 'running', so just tapped the search field.")
        except:
            self.UTILS.logResult("info", "Launching Everything ME.")
            x = self.UTILS.getElement(DOM.EME.start_eme_icon, "EME launch icon")
            x.tap()
            
        self.UTILS.waitForElements(DOM.EME.groups, "EME groups", True, 30)

