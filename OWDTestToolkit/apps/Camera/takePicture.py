from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def takePicture(self):
        #
        # Take a picture.
        #
        x = self.UTILS.getElement(DOM.Camera.capture_button, "Capture button")
        x.tap()
        self.UTILS.waitForElements(DOM.Camera.thumbnail, "Camera thumbnails")
        
