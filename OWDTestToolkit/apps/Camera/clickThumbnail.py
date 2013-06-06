from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def clickThumbnail(self, p_num):
        #
        # Click thumbnail.
        #
        thumbEls = self.UTILS.getElements(DOM.Camera.thumbnail, "Camera thumbnails")
        myThumb = thumbEls[p_num]
        myThumb.tap()
        
        img_camera_view = self.UTILS.screenShot("_CAMERA_VIEW")        
        self.UTILS.logComment("    Clicking the thumbnail in the camera   : " + img_camera_view)


