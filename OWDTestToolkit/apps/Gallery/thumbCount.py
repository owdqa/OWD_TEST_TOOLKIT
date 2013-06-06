from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def thumbCount(self):
        #
        # Returns the number of thumbnails.
        #
        x = self.UTILS.getElements(DOM.Gallery.thumbnail_items, "Gallery thumbnails", False)
        if x:
            return len(x)
        else:
            return 0

