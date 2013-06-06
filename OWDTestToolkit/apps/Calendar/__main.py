from OWDTestToolkit.global_imports import *

import  addEvent                           ,\
        _calcStep                          ,\
        createEvent                        ,\
        getEventPreview                    ,\
        _scrollBackward                    ,\
        _scrollForward                     ,\
        _select                            ,\
        setView                            

class Calendar (
            addEvent.main,
            _calcStep.main,
            createEvent.main,
            getEventPreview.main,
            _scrollBackward.main,
            _scrollForward.main,
            _select.main,
            setView.main):
    
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
        self.app = self.apps.launch(self.__class__.__name__)
        self.UTILS.waitForNotElements(DOM.GLOBAL.loading_overlay, self.__class__.__name__ + " app - loading overlay")

