from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def getGalleryItems(self):
        #
        # Returns a list of gallery item objects.
        #
        self.UTILS.waitForElements(DOM.Gallery.thumbnail_items, "Thumbnails", True, 20, False)
        return self.marionette.execute_script("return window.wrappedJSObject.files;")
        
