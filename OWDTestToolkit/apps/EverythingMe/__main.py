from OWDTestToolkit.global_imports import *

import  addAppToHomescreen                 ,\
        addGroup                           ,\
        pickGroup                          ,\
        removeGroups                       ,\
        searchForApp                       ,\
        launchFromGroup                    ,\
        addMultipleGroups

class EverythingMe (
            addAppToHomescreen.main,
            addGroup.main,
            pickGroup.main,
            removeGroups.main,
            searchForApp.main,
            addMultipleGroups.main,
            launchFromGroup.main):
    
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
            self.UTILS.logResult("info", "Everything ME is already 'running', so just waking it up ...")
            self._relaunch()
            try:
                self.wait_for_element_displayed(*DOM.EME.groups, timeout=3)
            except:
                self._relaunch()
            boolOK = True
            
        self.UTILS.TEST(boolOK, "EME Starting up ...")
            
        self.UTILS.waitForElements(DOM.EME.groups, "EME groups", True, 10)

    def _relaunch(self):
        #
        # Private function to re-launch.
        # This gets complicated:
        # 1. el.tap() and el.click() only work *sometimes*, so use the keyboard to relaunch.
        # 2. Sometimes the messges app randomly launches instead of evme!
        #
        x = self.marionette.find_element(*DOM.EME.search_field)
        x.send_keys("waking up evme")
        
        x = self.marionette.find_element(*DOM.EME.search_clear)
        x.tap()

