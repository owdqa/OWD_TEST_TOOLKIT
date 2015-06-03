import time
import datetime
from OWDTestToolkit import DOM
from marionette_driver.marionette import Actions

class Camera(object):

    def __init__(self, parent):
        self.apps = parent.apps
        self.data_layer = parent.data_layer
        self.parent = parent
        self.marionette = parent.marionette
        self.UTILS = parent.UTILS
        self.actions = Actions(self.marionette)

    def launch(self):
        self.app = self.apps.launch(self.__class__.__name__)
        self.UTILS.element.waitForNotElements(
            DOM.GLOBAL.loading_overlay, self.__class__.__name__ + " app - loading overlay")
        self._wait_for_camera_ready()
        return self.app

    def _wait_for_camera_ready(self):
        self.parent.wait_for_condition(lambda m: m.find_element(
            *DOM.Camera.controls_pane).get_attribute('data-enabled') == 'true', timeout=10, message="Camera ready")

    def is_video_being_recorded(self):
        try:
            self.parent.wait_for_condition(lambda m: m.find_element(
                *DOM.Camera.controls_pane).get_attribute('data-recording') == 'true', timeout=10, message="Video recording")
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

    def convert_str_to_seconds(self, the_string):
        """
        Converts a str of the form "aa:bb" into seconds
        """
        processed = time.strptime(the_string, '%M:%S')
        return (int(datetime.timedelta(minutes=processed.tm_min, seconds=processed.tm_sec).total_seconds()))

    def check_video_length(self, expected_duration, margin=2):
        """
        This method asserts that the video has the desired duration
        @expected_duration: specify the video duration in seconds
        """

        # Play the video and get total duration
        self.play_current_video()
        video_length = self.UTILS.element.getElement(DOM.Camera.preview_video_slider_duration, "Video length")
        real_duration = self.convert_str_to_seconds(video_length.text)

        # Note: we give 1 second margin in case the things went a little bit slower when recording the video
        interval = range(expected_duration - margin, expected_duration + margin + 1, 1)
        self.UTILS.test.test(real_duration in interval, "Duration matches")

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

        self.UTILS.test.test(self.is_video_being_recorded(), "Video recording")
 
        # Record for video_length seconds. Looks like it always takes one second more
        # Wait for duration
        timer_text = '00:{:02d}'.format(video_length)
        self.parent.wait_for_condition(lambda m: m.find_element(
            *DOM.Camera.recording_timer).text >= timer_text, timeout=video_length + 10)
        
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
        self.actions.press(switch_btn).move_by_offset(0, 0).release().perform()
        self._wait_for_camera_ready()

    def take_picture(self):
        """
        Take a picture.
        """
        self.parent.wait_for_condition(lambda m: m.find_element(
            *DOM.Camera.controls_pane).get_attribute('data-enabled') == 'true', 20)
        capture_button = self.UTILS.element.getElement(DOM.Camera.capture_button, "Capture button")
        time.sleep(1)
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
        self.UTILS.test.test(count_text.text.split(
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
        play_btn = self.UTILS.element.getElement(DOM.Camera.preview_video_play, "Video play button")
        time.sleep(1)
        self.UTILS.element.simulateClick(play_btn)
        play_btn.tap()

        self.UTILS.element.waitForElements(DOM.Camera.preview_video_pause, "Pause button", True, 20, False)

    def take_and_select_picture(self):
        """
        This method takes a picture and hits on select. It is 
        """
        self.parent.wait_for_condition(lambda m: m.find_element(
            *DOM.Camera.controls_pane).get_attribute('data-enabled') == 'true', 20)
        capture_button = self.UTILS.element.getElement(DOM.Camera.capture_button, "Capture button")
        time.sleep(1)
        capture_button.tap()

        # Confirm the picture.
        select_button = self.UTILS.element.getElement(DOM.Camera.select_button, "Select Camera photo", timeout=10)
        time.sleep(1)
        select_button.tap()
