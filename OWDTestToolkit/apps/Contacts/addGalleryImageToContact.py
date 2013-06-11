from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def addGalleryImageToContact(self, p_num):
        #
        # Adds an image for this contact from the gallery
        # (assumes we're already in the 'new contact' or
        # 'edit conact' screen, and also that we have already
        # added an image to the gallery).
        #
#         self.UTILS.addFileToDevice(p_file, destination='DCIM/100MZLLA')
#         AppGallery(self).launch()

        #
        # Click the 'add picture' link.
        #
        x = self.UTILS.getElement(DOM.Contacts.add_photo, "'Add picture' link")
        x.tap()
        time.sleep(2)
        
        # Switch to the 'make a choice' iframe.
        self.marionette.switch_to_frame()
        
        # Choose to get a picture from the Gallery.
        x = self.UTILS.getElement(DOM.Contacts.photo_from_gallery, "Gallery link")
        x.tap()
        
        # Switch to Gallery iframe.
        time.sleep(2)
        self.UTILS.switchToFrame(*DOM.Gallery.frame_locator)
        
        # Select the thumbnail (assume it's the only one).
        x = self.UTILS.getElements(DOM.Contacts.picture_thumbnails, "Thumbnails for pictures")
        if x:
            x[p_num].tap()
            
            time.sleep(1)
            
            # Tap 'crop done' button.
            boolOK = True
            try:
                x = self.UTILS.getElement(DOM.Contacts.picture_crop_done_btn, "Crop 'done' button")
                x.tap()
            except:
                boolOK = False
    
            self.UTILS.TEST(boolOK, "Can finish cropping the picture and return to Contacts app.")
                
            time.sleep(1)
        
        # Back to contacts app iframe.
        self.marionette.switch_to_frame()
        self.UTILS.switchToFrame(*DOM.Contacts.frame_locator)
