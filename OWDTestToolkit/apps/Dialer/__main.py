from OWDTestToolkit.global_imports import *

import  callThisNumber              ,\
        createContactFromThisNum    ,\
        hangUp                      ,\
        enterNumber                 ,\
        openCallLog                 ,\
        callLog_call                ,\
        callLog_createContact       ,\
        callLog_addToContact        ,\
        addThisNumberToContact      ,\
        _complete_addNumberToContact

class Dialer (
            callThisNumber.main,
            createContactFromThisNum.main,
            hangUp.main,
            enterNumber.main,
            openCallLog.main,
            callLog_call.main,
            callLog_createContact.main,
            callLog_addToContact.main,
            addThisNumberToContact.main,
            _complete_addNumberToContact.main):
    
    def __init__(self, p_parent):
        self.apps       = p_parent.apps
        self.data_layer = p_parent.data_layer
        self.parent     = p_parent
        self.marionette = p_parent.marionette
        self.UTILS      = p_parent.UTILS

    def launch(self):
        #
        # Launch the app (it's called a different name to the everyone knows it as, so hardcode it!).
        #
        self.app = self.apps.launch("Phone")
        self.UTILS.waitForNotElements(DOM.GLOBAL.loading_overlay, self.__class__.__name__ + " app - loading overlay")
        return self.app
        
        
        
        