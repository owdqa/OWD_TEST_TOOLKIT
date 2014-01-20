from OWDTestToolkit.global_imports import *


class main(GaiaTestCase):

    def clickThumbMMS(self, p_num):
        #
        # Clicks a thumbnail from the gallery.
        #
        gallery_items = self.getGalleryItems()
        for index, item in enumerate(gallery_items):
            if index == p_num:
                my_item = self.UTILS.getElements(DOM.Gallery.thumbnail_items, "Gallery item list", True, 20, False)[index]
                my_item.tap()

        time.sleep(2)

        crop = self.UTILS.getElement(DOM.Gallery.crop_done, "Crop Done")
        crop.tap()

        self.UTILS.switchToFrame(*DOM.Messages.frame_locator)