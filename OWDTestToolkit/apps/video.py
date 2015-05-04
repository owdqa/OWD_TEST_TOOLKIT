import time
import datetime
from OWDTestToolkit import DOM
from OWDTestToolkit.utils.decorators import retry


class Video(object):

    def __init__(self, p_parent):
        self.apps = p_parent.apps
        self.data_layer = p_parent.data_layer
        self.parent = p_parent
        self.marionette = p_parent.marionette
        self.UTILS = p_parent.UTILS

    def launch(self):
        #
        # Launch the app.
        #
        self.app = self.apps.launch(self.__class__.__name__)
        self.UTILS.element.waitForNotElements(
            DOM.GLOBAL.loading_overlay, self.__class__.__name__ + " app - loading overlay")
        return self.app

    def check_thumb_duration(self, position, expected_duration, margin=3):
        """
        Check the duration of a video thumbnail.
        """
        thumb = self.UTILS.element.getElements(DOM.Video.thumbnails_thumbs, "thumbnails")[position]
        time.sleep(1)
        duration_text = thumb.find_element(*DOM.Video.thumbnail_duration).text.strip()
        duration_in_secs = self.convert_str_to_seconds(duration_text)

        # Note: we give some margin in case the things went a little bit slower when recording the video
        interval = range(expected_duration - margin, expected_duration + margin + 1, 1)
        self.UTILS.test.test(duration_in_secs in interval, "Interval: {}  duration_in_secs: {} expected: {}".
                             format(interval, duration_in_secs, expected_duration))

    def convert_str_to_seconds(self, the_string):
        """
        Converts a str of the form "aa:bb" into seconds
        """
        processed = time.strptime(the_string, '%M:%S')
        return (int(datetime.timedelta(minutes=processed.tm_min, seconds=processed.tm_sec).total_seconds()))

    def check_video_length(self, position, expected_duration, margin=3):
        """
        This method asserts that the video has the desired duration
        @param  int expected_duration   specifies the video duration in seconds
        """

        # Play the video and get total duration
        self.play_video(position)
        time.sleep(1)
        self.UTILS.element.getElement(('id', 'player-view'), "Player view").tap()
        video_length = self.UTILS.element.getElement(DOM.Video.player_time_slider_duration, "Video length")
        real_duration = self.convert_str_to_seconds(video_length.text)

        # Note: we give some margin in case the things went a little bit slower when recording the video
        interval = range(expected_duration - margin, expected_duration + margin + 1, 1)
        self.UTILS.test.test(real_duration in interval, "Interval: {}  duration_in_secs: {} expected: {}".
                             format(interval, real_duration, expected_duration))

    def _click_on_video_external(self, position, frame_to_change):
        """
        Private method which handles image selection and image cropping
        @param  int     position            thumbnail to click
        @param  tuple   frame_to_change     frame to switch once the image has been cropped
        """
        self.parent.wait_for_element_displayed(*DOM.Video.thumbnails_thumbs)
        time.sleep(3)
        all_videos = self.marionette.find_elements(*DOM.Video.thumbnails_thumbs)
        my_video = all_videos[position]
        my_video.tap()

        time.sleep(1)

        doneButton = self.UTILS.element.getElement(DOM.Video.done_button, "Done Button")
        doneButton.tap()

        self.UTILS.iframe.switchToFrame(*frame_to_change)

    def click_on_video_at_position_mms(self, position):
        """
        Clicks a thumbnail from the gallery in order to attach it to a MMS
        """
        self._click_on_video_external(position, DOM.Messages.frame_locator)

    def click_on_video_at_position_email(self, position):
        """
        Clicks a thumbnail from the gallery in order to attach it to an email
        """
        self._click_on_video_external(position, DOM.Email.frame_locator)

    def play_video(self, position):
        """
        Clicks the thumbnail to start the video.
        """

        # Get the list of video items and click the 'num' one.
        all_videos = self.UTILS.element.getElements(DOM.Video.thumbnails_thumbs, "Videos")
        my_video = all_videos[position]
        self.UTILS.element.simulateClick(my_video)

        # Wait for the video to start playing before returning.
        self.UTILS.element.waitForElements(DOM.Video.player_video_loaded, "Loaded video", True, 20, False)

    def is_video_playing(self):
        return not "paused" in self.marionette.find_element(*DOM.Video.player_toolbar_play).get_attribute('class')

    def show_controls(self):
        self.parent.wait_for_element_displayed(*DOM.Video.player_video)
        self.marionette.find_element(*DOM.Video.player_video).tap()
        self.parent.wait_for_element_displayed(*DOM.Video.player_video_controls)

    @retry(5, 1)
    def is_this_video_being_played(self, video_name):
        self.show_controls()
        video_title = self.UTILS.element.getElement(DOM.Video.video_title, "Video title")

        if video_name == video_title.text and self.is_video_playing():
            return True
        else:
            raise

    def tap_on_play_button(self):
        self.parent.wait_for_element_displayed(*DOM.Video.player_toolbar_play)
        self.marionette.find_element(*DOM.Video.player_toolbar_play).tap()

    def wait_for_list(self):
        self.parent.wait_for_element_not_displayed('id', 'throbber', timeout=30)
        self.parent.wait_for_element_not_displayed('id', 'overlay', timeout=30)

