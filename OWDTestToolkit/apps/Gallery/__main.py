from OWDTestToolkit.global_imports import *

import  checkVideoLength                   ,\
        clickThumbMMS                      ,\
        clickThumb                         ,\
        deleteThumbnails                   ,\
        getGalleryItems                    ,\
        playCurrentVideo                   ,\
        thumbCount                         ,\
        waitForThumbnails                  

class Gallery (
            checkVideoLength.main,
            clickThumb.main,
            clickThumbMMS.main,
            deleteThumbnails.main,
            getGalleryItems.main,
            playCurrentVideo.main,
            thumbCount.main,
            waitForThumbnails.main):
    
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
        self.UTILS.waitForNotElements(DOM.Gallery.loading_bar, "Loading bar", True, 10)
        return self.app

