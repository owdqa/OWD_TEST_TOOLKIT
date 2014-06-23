from OWDTestToolkit import DOM
import time


class Gallery(object):

    def __init__(self, parent):
        self.apps = parent.apps
        self.data_layer = parent.data_layer
        self.parent = parent
        self.marionette = parent.marionette
        self.UTILS = parent.UTILS

    def launch(self):
        #
        # Launch the app.
        #
        self.app = self.apps.launch(self.__class__.__name__)
        self.UTILS.element.waitForNotElements(DOM.GLOBAL.loading_overlay, self.__class__.__name__ + " app - loading overlay")
        self.UTILS.element.waitForNotElements(DOM.Gallery.loading_bar, "Loading bar", True, 10)
        return self.app

    def checkVideoLength(self, from_ss, to_ss):
        #
        # Check the length of a video.
        #

        # Start the timer.
        start_time = time.time()

        # Play the video.
        self.playCurrentVideo()

        # Stop the timer.
        elapsed_time = int(time.time() - start_time)

        self.UTILS.test.TEST((elapsed_time > from_ss), "Video is not shorter than expected (played for {:.2f} seconds).".\
                        format(elapsed_time))
        self.UTILS.test.TEST((elapsed_time < to_ss), "Video is not longer than expected (played for {:.2f} seconds).".\
                        format(elapsed_time))

    def clickThumb(self, num):
        #
        # Clicks a thumbnail from the gallery.
        #
        boolPIC = False
        gallery_items = self.getGalleryItems()
        for index, item in enumerate(gallery_items):
            if index == num:
                my_item = self.UTILS.element.getElements(DOM.Gallery.thumbnail_items,
                                                 "Gallery item list", True, 20, False)[index]
                my_item.tap()

                if 'video' in item['metadata']:
                    boolPIC = False
                    self.UTILS.element.waitForElements(DOM.Gallery.current_image_vid, "Video playing", True, 20, False)
                else:
                    boolPIC = True
                    self.UTILS.element.waitForElements(DOM.Gallery.current_image_pic, "Image", True, 20, False)
                break

        if boolPIC:
            #
            # TEST: Thumbnails are not visible when vieweing an image.
            #
            thumbs = self.UTILS.element.getElement(DOM.Gallery.thumbnail_list_section, "Thumbnail list section", False)
            self.UTILS.test.TEST((thumbs.get_attribute("class") == "hidden"),
                             "Thumbnails are not present when vieweing image in gallery.")

            #
            # TEST: Image is displayed as expected.
            #
            try:
                thisIMG = self.UTILS.element.getElement(DOM.Gallery.current_image_pic, "Current image")
                try:
                    x = str(thisIMG.get_attribute('src'))
                    self.UTILS.test.TEST((x != ""), "Image source is not empty in gallery after clicking thumbnail.")
                except:
                    self.UTILS.reporting.logResult(False, "Image source exists in gallery after clicking thumbnail.")
            except:
                self.UTILS.reporting.logResult(False, "Image is displayed as expected after clicking icon in gallery.")

            #
            # Get a screenshot of the image from the galery thumbnail.
            #
            img_gallery_view = self.UTILS.debug.screenShot("_GALLERY_VIEW")
            self.UTILS.reporting.logComment("    Clicking the thumbnail in the gallery   : " + img_gallery_view)

    def clickThumbMMS(self, num):
        #
        # Clicks a thumbnail from the gallery.
        #
        gallery_items = self.getGalleryItems()
        for index, item in enumerate(gallery_items):
            if index == num:
                my_item = self.UTILS.element.getElements(DOM.Gallery.thumbnail_items,
                                                 "Gallery item list", True, 20, False)[index]
                my_item.tap()

        time.sleep(2)

        crop = self.UTILS.element.getElement(DOM.Gallery.crop_done, "Crop Done")
        crop.tap()

        self.UTILS.iframe.switchToFrame(*DOM.Messages.frame_locator)

    def clickThumbEmail(self, num):
        #
        # Clicks a thumbnail from the gallery.
        #
        gallery_items = self.getGalleryItems()
        for index, item in enumerate(gallery_items):
            if index == num:
                my_item = self.UTILS.element.getElements(DOM.Gallery.thumbnail_items,
                                                 "Gallery item list", True, 20, False)[index]
                my_item.tap()

        time.sleep(2)

        crop = self.UTILS.element.getElement(DOM.Gallery.crop_done, "Crop Done")
        crop.tap()

        self.UTILS.iframe.switchToFrame(*DOM.Email.frame_locator)

    def deleteThumbnails(self, num_array):
        #
        # Deletes the thumbnails listed in num_array
        # (following an index starting at number 0).<br>
        # The list must be numeric, i.e "deleteThumbnails( (0,1,2) )".
        #

        #
        # Get the amount of thumbnails we currently have.
        #
        before_thumbcount = self.thumbCount()
        delete_thumbcount = len(num_array)
        target_thumbcount = before_thumbcount - delete_thumbcount

        #
        # Click the 'select' button.
        #
        x = self.UTILS.element.getElement(DOM.Gallery.thumbnail_select_mode_btn, "Select button")
        x.tap()

        #
        # Report 'the plan'.
        #
        self.UTILS.reporting.logResult("info",
                             "Delete " + str(delete_thumbcount) + " of the " + str(before_thumbcount)
                             + " thumbnails ...")

        #
        # Select 3 of them.
        #
        x = self.UTILS.element.getElements(DOM.Gallery.thumbnail_items, "Thumbnails")
        for i in num_array:
            x[i].tap()

        #
        # Press the trash icon.
        #
        x = self.UTILS.element.getElement(DOM.Gallery.thumbnail_trash_icon, "Trash icon")
        x.tap()

        #
        # Confirm.
        #
        x = self.UTILS.element.getElement(DOM.GLOBAL.modal_confirm_ok, "Delete")
        x.tap()
        # myIframe = self.UTILS.iframe.currentIframe()
        # self.marionette.switch_to_frame()
        # self.marionette.execute_script("document.getElementById('%s').click()" % DOM.GLOBAL.modal_confirm_ok[1])
        # self.UTILS.iframe.switchToFrame("src", myIframe)

        #
        # Now report how many thumbnails there are (should be 2).
        #
        if target_thumbcount < 1:
            self.UTILS.element.waitForElements(DOM.Gallery.no_thumbnails_message,
                                       "Message saying there are no thumbnails", False, 5)
        else:
            #
            # Come out of 'select' mode.
            #
            x = self.UTILS.element.getElement(DOM.Gallery.thumbnail_cancel_sel_mode_btn, "Exit select mode button")
            x.tap()

            x = self.thumbCount()
            self.UTILS.test.TEST(x == target_thumbcount,
                            str(target_thumbcount) + " thumbnails after deletion (there were " + str(x) + ").")

    def getGalleryItems(self):
        #
        # Returns a list of gallery item objects.
        #
        self.UTILS.element.waitForElements(DOM.Gallery.thumbnail_items, "Thumbnails", True, 20, False)
        return self.marionette.execute_script("return window.wrappedJSObject.files;")

    def playCurrentVideo(self):
        #
        # Plays the video we've loaded (in gallery you have to click the thumbnail first,
        # THEN press a play button - it doesn't play automatically).
        #
        play_btn = self.UTILS.element.getElement(DOM.Gallery.video_play_button, "Video play button")
        play_btn.click()
        play_btn.tap()

        self.UTILS.element.waitForNotElements(DOM.Gallery.video_pause_button, "Pause button", True, 20, False)

    def thumbCount(self):
        #
        # Returns the number of thumbnails.
        #
        try:
            self.parent.wait_for_element_displayed(*DOM.Gallery.thumbnail_items)
            return len(self.marionette.find_elements(*DOM.Gallery.thumbnail_items))
        except:
            return 0

    def waitForThumbnails(self, cnt, fail_on_err=False):
        #
        # Waits until cnt thumbnails are present
        # (because it can take a few seconds).
        # Since there could be a bug in the Gallery app
        # which prevents this, there is a 10s timeout.
        #
        x = 0
        y = 0
        boolOK = True
        while x < cnt:
            time.sleep(1)
            x = self.thumbCount()

            # Added a timeout of 10s in case the gallery app has a bug.
            y = y + 1
            if y > 10:
                boolOK = False
                break
        self.UTILS.test.TEST(boolOK, str(cnt) + " thumbnails appear in under 10s (" + str(x) + " found).", fail_on_err)

        x = self.UTILS.debug.screenShot("expecting_" + str(cnt) + "_thumbnails")
        self.UTILS.reporting.logResult("info", "Screenshot: " + x)

        return boolOK
