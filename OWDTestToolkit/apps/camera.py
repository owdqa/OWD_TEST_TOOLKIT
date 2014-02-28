import time
from OWDTestToolkit import DOM


class Camera(object):

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
        self.UTILS.waitForNotElements(DOM.GLOBAL.loading_overlay, self.__class__.__name__ + " app - loading overlay")
        return self.app

    def goToGallery(self):
        #
        # Clicks the Gallery button to switch to the Gallery application
        # (warning: this will land you in the gallery iframe).
        #
        galleryBTN = self.UTILS.getElement(DOM.Camera.gallery_button, "Gallery button")
        galleryBTN.tap()
        self.UTILS.switchToFrame(*DOM.Gallery.frame_locator)

    def clickThumbnail(self, num):
        #
        # Click thumbnail.
        #
        thumbEls = self.UTILS.getElements(DOM.Camera.thumbnail, "Camera thumbnails")
        myThumb = thumbEls[num]
        myThumb.tap()

        img_camera_view = self.UTILS.screenShot("_CAMERA_VIEW")
        self.UTILS.logComment("    Clicking the thumbnail in the camera   : " + img_camera_view)

    def checkVideoLength(self, vid_num, from_ss, to_ss):
        #
        # Check the length of a video.
        #

        #
        # Find the thumbnail for this video and click it.
        #
        self.clickThumbnail(vid_num)

        #
        # Click the button to play the video and make sure it takes between
        # 5 and 9 seconds to complete (to allow time delay in element
        # loading).
        #
        playBTN = self.UTILS.getElement(DOM.Camera.video_play_button, "Video play button")
        playBTN.tap()

        # Start the timer when the pause button is visible.
        self.UTILS.waitForElements(DOM.Camera.video_pause_button,
                                   "Video pause button", True, 20, False)
        start_time = time.time()

        # Stop the timer when the pause button is no longer visible.
        self.UTILS.waitForNotElements(DOM.Camera.video_pause_button,
                                      "Video pause button", True, 20, False)

        elapsed_time = int(time.time() - start_time)

        self.UTILS.TEST((elapsed_time >= from_ss), "Video is not shorter than expected (played for {:.2f} seconds)."
                        .format(elapsed_time))
        self.UTILS.TEST((elapsed_time <= to_ss), "Video is not longer than expected (played for {:.2f} seconds)."
                        .format(elapsed_time))

    def recordVideo(self, p_length):
        #
        # Record a video.
        # p_length is the number of seconds to record for.
        #

        #
        # Switch to video.
        #
        self.switchSource()

        #
        # Record a video and click the thumbnail to play it.
        #
        captureBTN = self.UTILS.getElement(DOM.Camera.capture_button, "Capture button")
        captureBTN.tap()

        # Record for 5 seconds
        time.sleep(p_length)

        # Stop recording
        captureBTN.tap()

        self.UTILS.waitForNotElements(DOM.Camera.video_timer, "Video timer", True, 10, False)

        self.UTILS.waitForElements(DOM.Camera.thumbnail,
                                   "Thumbnail appears after recording video", True, 10, False)

    def switchSource(self):
        #
        # Switch between still shot and video.
        #
        switchBTN = self.UTILS.getElement(DOM.Camera.switch_source_btn, "Source switcher")
        switchBTN.tap()
        self.UTILS.waitForElements(DOM.Camera.capture_button_enabled, "Enabled capture button")

    def takePicture(self):
        #
        # Take a picture.
        #
        x = self.UTILS.getElement(DOM.Camera.capture_button, "Capture button")
        x.tap()
        self.UTILS.waitForElements(DOM.Camera.thumbnail, "Camera thumbnails")
