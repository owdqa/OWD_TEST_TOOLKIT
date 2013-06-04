import time
from gaiatest   import GaiaTestCase
from marionette import Marionette
from OWDTestToolkit import *

class AppGallery(GaiaTestCase):
    
    #
    # When you create your instance of this class, include the
    # "self" object so we can access the calling class' objects.
    #
    def __init__(self, p_parent):
        self.apps       = p_parent.apps
        self.data_layer = p_parent.data_layer
        self.marionette = p_parent.marionette
        self.UTILS      = p_parent.UTILS


    def launch(self, p_counter=0):
        #
        # Launch the app.
        #
        self.apps.kill_all()
        self.app = self.apps.launch('Gallery')
        self.UTILS.waitForNotElements(DOM.GLOBAL.loading_overlay, "Gallery app - loading overlay");
        
        #
        # Due to a bug I'm verifying that one of two things happen now.
        # Either thumbnails are displayed, nor a note saying there's nothing to see.
        #
        # If neither of these things happen, then restart and try again.
        #
        time.sleep(3)
        if p_counter >= 4:
            #
            # After 5 tries just move on (or we'll be here all day!).
            #
            return
        
        try:
            x = self.marionette.find_elements(*DOM.Gallery.no_thumbnails_message)
            return
        except:
            try:
                x = self.thumbCount()
                if x > 0:
                    return
            except:
                pass
        
        self.logResult("info", "(Restarting - no thumbnails or message found ...)")
        self.launch(p_counter + 1)

    def thumbCount(self):
        #
        # Returns the number of thumbnails.
        #
        x = self.UTILS.getElements(DOM.Gallery.thumbnail_items, "Gallery thumbnails", False)
        if x:
            return len(x)
        else:
            return 0

    def waitForThumbnails(self, p_count, p_failOnErr=False):
        #
        # Waits until p_count thumbnails are present
        # (because it can take a few seconds).
        # Since there could be a bug in the Gallery app
        # which prevents this, there is a 10s timeout.
        #
        x = 0
        y = 0
        boolOK = True
        while x < p_count:
            time.sleep(1)
            x = self.thumbCount()
            
            # Added a timeout of 10s in case the gallery app has a bug.
            y = y + 1
            if y > 10:
                boolOK = False
                break
        self.UTILS.TEST(boolOK, str(p_count) + " thumbnails appear in under 10s (" + str(x) + " found).", p_failOnErr)
        
        return boolOK

    def getGalleryItems(self):
        #
        # Returns a list of gallery item objects.
        #
        self.UTILS.waitForElements(DOM.Gallery.thumbnail_items, "Thumbnails", True, 20, False)
        return self.marionette.execute_script("return window.wrappedJSObject.files;")
        
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


    def playCurrentVideo(self):
        #
        # Plays the video we've loaded (in gallery you have to click the thumbnail first,
        # THEN press a play button - it doesn't play automatically).
        #
        playBTN = self.UTILS.getElement(DOM.Gallery.video_play_button, "Video play button")
        playBTN.click()
        playBTN.tap()
        
        self.UTILS.waitForNotElements(DOM.Gallery.video_pause_button, "Pause button", True, 20, False);

    def checkVideoLength(self, p_from_SS, p_to_SS):
        #
        # Check the length of a video.
        #
            
        # Start the timer.
        start_time = time.time()
        
        # Play the video.
        self.playCurrentVideo()
        
        # Stop the timer.
        elapsed_time = int(time.time() - start_time)
        
        self.UTILS.TEST((elapsed_time > p_from_SS), "Video is not shorter than expected (played for %.2f seconds)." % elapsed_time)
        self.UTILS.TEST((elapsed_time < p_to_SS), "Video is not longer than expected (played for %.2f seconds)." % elapsed_time)

    def deleteThumbnails(self, p_num_array):
        #
        # Deletes the thumbnails listed in p_num_array
        # (following an index starting at number 0).<br>
        # The list must be numeric, i.e "deleteThumbnails( (0,1,2) )".
        #
        
        #
        # Get the amount of thumbnails we currently have.
        #
        before_thumbcount = self.thumbCount()
        delete_thumbcount = len(p_num_array)
        target_thumbcount = before_thumbcount - delete_thumbcount
        
        #
        # Click the 'select' button.
        #
        x = self.UTILS.getElement(DOM.Gallery.thumbnail_select_mode_btn, "Select button")
        x.tap()
        
        #
        # Report 'the plan'.
        #
        self.UTILS.logResult("info", 
                             "Delete " + str(delete_thumbcount) + " of the " + str(before_thumbcount) + " thumbnails ...")
        
        #
        # Select 3 of them.
        #
        x = self.UTILS.getElements(DOM.Gallery.thumbnail_items, "Thumbnails")
        for i in p_num_array:
            x[i].tap()
            
        #
        # Press the trash icon.
        #
        x = self.UTILS.getElement(DOM.Gallery.thumbnail_trash_icon, "Trash icon")
        x.tap()
        
        #
        # Confirm.
        #
        myIframe = self.UTILS.currentIframe()
        self.marionette.switch_to_frame()
        x = self.UTILS.getElement(DOM.Gallery.thumbnail_trash_confirm_btn, "Confirm ok button")
        x.tap()
        self.UTILS.switchToFrame("src", myIframe)
        
        #
        # Now report how many thumbnails there are (should be 2).
        #
        if target_thumbcount < 1:
            self.UTILS.waitForElements(DOM.Gallery.no_thumbnails_message, 
                                       "Message saying there are no thumbnails", False, 5)
        else:
            #
            # Come out of 'select' mode.
            #
            x = self.UTILS.getElement(DOM.Gallery.thumbnail_cancel_sel_mode_btn, "Exit select mode button")
            x.tap()
            
            x = self.thumbCount()
            self.UTILS.TEST(x == target_thumbcount, 
                            str(target_thumbcount) + " thumbnails after deletion (there were " + str(x) + ").")
        