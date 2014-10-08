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
        self.app = self.apps.launch(self.__class__.__name__)
        self.UTILS.element.waitForNotElements(
            DOM.GLOBAL.loading_overlay, self.__class__.__name__ + " app - loading overlay")
        self._wait_for_camera_ready()
        return self.app

    def _wait_for_camera_ready(self):
        self.parent.wait_for_condition(lambda m: "enabled" in m.find_element(
            *DOM.Camera.controls_pane).get_attribute("class"), timeout=10, message="Camera ready")

    def is_video_being_recorded(self):
        try:
            self.parent.wait_for_condition(lambda m: "recording" in m.find_element(
                *DOM.Camera.controls_pane).get_attribute("class"), timeout=10, message="Video recording")
            return True
        except:
            return False

    def go_to_gallery(self):
        """
        Clicks the Gallery button to switch to the Gallery application
        (warning: this will land you in the gallery iframe).
        """
        gallery_button = self.UTILS.element.getElement(DOM.Camera.gallery_button, "Gallery button")
        gallery_button.tap()
        self.UTILS.iframe.switchToFrame(*DOM.Gallery.frame_locator)

    def click_on_thumbnail_at_pos(self, num):
        """
        Click on a certain thumbnail.
        """

        thumb_list = self.UTILS.element.getElements(DOM.Camera.thumbnail, "Camera thumbnails")
        the_thumb = thumb_list[num]
        the_thumb.tap()

    def check_video_length(self, vid_num, from_ss, to_ss):
        """
        Check the length of a video.
        """

        self.click_on_thumbnail_at_pos(vid_num)

        #
        # Click the button to play the video and make sure it takes between
        # 5 and 9 seconds to complete (to allow time delay in element
        # loading).
        #
        play_button = self.UTILS.element.getElement(DOM.Camera.video_play_button, "Video play button")
        play_button.tap()

        # Start the timer when the pause button is visible.
        self.UTILS.element.waitForElements(DOM.Camera.video_pause_button,
                                           "Video pause button", True, 20, False)
        start_time = time.time()

        # Stop the timer when the pause button is no longer visible.
        self.UTILS.element.waitForNotElements(DOM.Camera.video_pause_button,
                                              "Video pause button", True, 20, False)

        elapsed_time = int(time.time() - start_time)

        self.UTILS.test.TEST((elapsed_time >= from_ss), "Video is not shorter than expected (played for {:.2f} seconds)."
                             .format(elapsed_time))
        self.UTILS.test.TEST((elapsed_time <= to_ss), "Video is not longer than expected (played for {:.2f} seconds)."
                             .format(elapsed_time))

    def take_video(self, video_length):
        """
        Record a video.
        video_length is the number of seconds to record for.
        """

        # Switch to video.
        self.switch_source()

        # Record a video and click the thumbnail to play it.
        capture_button = self.UTILS.element.getElement(DOM.Camera.capture_button, "Capture button")
        time.sleep(1)
        capture_button.tap()
        
        self.UTILS.test.TEST(self.is_video_being_recorded(), "Video recording")
        self.UTILS.element.waitForElements(DOM.Camera.open_thumbs,
                                           "Thumbnail appears after recording video", True, 10, False)

        # Record for video_length seconds
        time.sleep(video_length)
        # Stop recording
        capture_button.tap()

        self.UTILS.element.waitForNotElements(DOM.Camera.recording_timer, "Video timer", True, 10, False)
        self.UTILS.element.waitForElements(DOM.Camera.open_thumbs,
                                           "Thumbnail appears after recording video", True, 10, False)

    def switch_source(self):
        """
        Switch between still shot and video.
        """
        switch_btn = self.UTILS.element.getElement(DOM.Camera.switch_source, "Source switcher")
        switch_btn.tap()
        self._wait_for_camera_ready()

    def take_picture(self):
        """
        Take a picture.
        """
        x = self.UTILS.element.getElement(DOM.Camera.capture_button, "Capture button")
        time.sleep(4)
        x.tap()
        self.UTILS.element.waitForElements(DOM.Camera.open_thumbs, "Camera thumbnails")

    # def takeAndSelectPicture(self):
    #     self.take_picture()

    # Confirm the picture.
    #     time.sleep(5)
    #     select_button = self.UTILS.element.getElement(DOM.Camera.select_button, "Select Camera photo")
    #     select_button.tap()
