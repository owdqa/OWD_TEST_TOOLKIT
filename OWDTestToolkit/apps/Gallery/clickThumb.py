from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def clickThumb(self, p_num):
        #
        # Clicks a thumbnail from the gallery.
        #
        boolPIC=False
        gallery_items = self.getGalleryItems()
        for index, item in enumerate(gallery_items):
            if index == p_num:
                my_item = self.UTILS.getElements(DOM.Gallery.thumbnail_items, "Gallery item list", True, 20, False)[index]
                my_item.tap()

                if 'video' in item['metadata']:
                    booLPIC=False
                    self.UTILS.waitForElements(DOM.Gallery.current_image_vid, "Video playing", True, 20, False)
                else:
                    booLPIC=True
                    self.UTILS.waitForElements(DOM.Gallery.current_image_pic, "Image", True, 20, False)
                break
        
        if boolPIC:
            #
            # TEST: Thumbnails are not visible when vieweing an image.
            #
            thumbs = self.UTILS.getElement(DOM.Gallery.thumbnail_list_section, "Thumbnail list section", False)
            self.UTILS.TEST( (thumbs.get_attribute("class") == "hidden"), "Thumbnails are not present when vieweing image in gallery.")
            
            #
            # TEST: Image is displayed as expected.
            #
            try: 
                thisIMG = self.UTILS.getElement(DOM.Gallery.current_image_pic, "Current image")
                try:
                    x = str(thisIMG.get_attribute('src'))
                    self.UTILS.TEST((x != ""), "Image source is not empty in gallery after clicking thumbnail.")
                except: 
                    self.UTILS.logResult(False, "Image source exists in gallery after clicking thumbnail.")
            except: self.UTILS.logResult(False, "Image is displayed as expected after clicking icon in gallery.")
            
            #
            # Get a screenshot of the image from the galery thumbnail.
            #
            img_gallery_view = self.UTILS.screenShot("_GALLERY_VIEW")        
            self.UTILS.logComment("    Clicking the thumbnail in the gallery   : " + img_gallery_view)


