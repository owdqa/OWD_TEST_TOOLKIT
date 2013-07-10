from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def goToGallery(self):
        #
        # Clicks the Gallery button to switch to the Gallery application
        # (warning: this will land you in the gallery iframe).
        #
        galleryBTN = self.UTILS.getElement(DOM.Camera.gallery_button, "Gallery button")
        galleryBTN.tap()
        self.UTILS.switchToFrame(*DOM.Gallery.frame_locator)
        
