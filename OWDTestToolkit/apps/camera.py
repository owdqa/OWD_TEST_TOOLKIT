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
        options = self.UTILS.element.getElement(DOM.Camera.preview_options, "preview options")
        time.sleep(1)
        options.tap()

        gallery_option = self.UTILS.element.getElement(DOM.Camera.action_menu_gallery, "Gallery option")
        time.sleep(1)
        gallery_option.tap()

        self.UTILS.iframe.switchToFrame(*DOM.Gallery.frame_locator)

    def click_on_thumbnail_at_pos(self, num):
        """
        Click on a certain thumbnail.
        """

        thumb_list = self.UTILS.element.getElements(DOM.Camera.thumbnail, "Camera thumbnails")
        the_thumb = thumb_list[num]
        the_thumb.tap()

    def _convert_str_to_seconds(self, the_string):
        """
        Converts a str of the form "aa:bb" into seconds
        """
        processed = time.strptime(the_string, '%M:%S')
        return (int(datetime.timedelta(minutes=processed.tm_min, seconds=processed.tm_sec).total_seconds()))

    def check_video_length(self, expected_duration):
        """
        This method asserts that the video has the desired duration
        @expected_duration: specify the video duration in seconds
        """

        # Play the video and get total duration
        self.play_current_video()
        video_length = self.UTILS.element.getElement(DOM.Gallery.preview_video_slider_duration, "Video length")
        real_duration = self._convert_str_to_seconds(video_length.text)

        # Note: we give 1 second margin in case the things went a little bit slower when recording the video
        interval = [expected_duration, expected_duration - 1, expected_duration + 1]
        self.UTILS.test.TEST(real_duration in interval, "Duration matches")

    def _tap_on_capture_button(self):
        capture_button = self.UTILS.element.getElement(DOM.Camera.capture_button, "Capture button")
        time.sleep(1)
        capture_button.tap()

    def take_video(self, video_length):
        """
        Record a video.
        video_length is the number of seconds to record for.
        """

        # Switch to video.
        self.switch_source()

        # Record a video and click the thumbnail to play it.
        self._tap_on_capture_button()

        self.UTILS.test.TEST(self.is_video_being_recorded(), "Video recording")
        self.UTILS.element.waitForNotElements(DOM.Camera.open_thumbs,
                                              "Thumbnail appears after recording video", True, 10, False)

        # Record for video_length seconds. Looks like it always takes one second more
        time.sleep(video_length)
        # Stop recording
        self._tap_on_capture_button()

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
        capture_button = self.UTILS.element.getElement(DOM.Camera.capture_button, "Capture button")
        time.sleep(4)
        capture_button.tap()
        self.UTILS.element.waitForElements(DOM.Camera.open_thumbs, "Camera thumbnails")

    def open_preview(self):
        """
        Open the preview screen by clicking thumbnail's shortcut
        """
        open_thumbs = self.UTILS.element.getElement(DOM.Camera.open_thumbs, "Thumbnail bubble")
        time.sleep(1)
        open_thumbs.tap()
        self.UTILS.element.waitForElements(DOM.Camera.preview_header, "Preview header")

        # Check the last picture is shown
        count_text = self.UTILS.element.getElement(DOM.Camera.preview_count_text, "Preview count")
        self.UTILS.reporting.logResult('info', "The text is: {}".format(count_text.text))
        self.UTILS.test.TEST(count_text.text.split(
            "/")[0] == "1", "Once we open the preview screen, the last picture is shown")

    def delete_from_preview(self, confirm=True):
        options = self.UTILS.element.getElement(DOM.Camera.preview_options, "preview options")
        time.sleep(1)
        options.tap()

        delete_option = self.UTILS.element.getElement(DOM.Camera.action_menu_delete, "Delete option")
        time.sleep(1)
        delete_option.tap()

        if confirm:
            confirm = self.UTILS.element.getElement(DOM.Camera.dialog_menu_yes, "Delete option")
            time.sleep(1)
            confirm.tap()
        else:
            cancel = self.UTILS.element.getElement(DOM.Camera.dialog_menu_no, "Delete option")
            time.sleep(1)
            cancel.tap()

    def play_current_video(self):
        """
        Plays the video that has previously been loaded (by pressing its thumbnail first), then press a play button.
        """
        play_btn = self.UTILS.element.getElement(DOM.Gallery.preview_video_play, "Video play button")
        time.sleep(1)
        self.UTILS.element.simulateClick(play_btn)

        self.UTILS.element.waitForElements(DOM.Gallery.preview_video_pause, "Pause button", True, 20, False)

    # def takeAndSelectPicture(self):
    #     self.take_picture()

    # Confirm the picture.
    #     time.sleep(5)
    #     select_button = self.UTILS.element.getElement(DOM.Camera.select_button, "Select Camera photo")
    #     select_button.tap()
