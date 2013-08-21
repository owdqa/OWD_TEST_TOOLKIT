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
        self.UTILS.logResult("info", "Launching Everything ME.")
        boolOK = False
        try:
            self.wait_for_element_displayed(*DOM.EME.start_eme_icon, timeout=1)
            x = self.marionette.find_element(*DOM.EME.start_eme_icon)
            x.tap()
            boolOK = True
        except:
            self.UTILS.logResult("info", "Everything ME is already 'running', so just tapping the search field.")
            x = self.marionette.find_element(*DOM.EME.search_field)
            x.click()
            boolOK = True
            
        self.UTILS.TEST(boolOK, "EME Starting up ...")
            
        self.UTILS.waitForElements(DOM.EME.groups, "EME groups", True, 30)

