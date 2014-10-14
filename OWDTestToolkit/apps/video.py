import time
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

    def checkThumbDuration(self, thumb_num, length_str_mmss, error_margin_ss):
        #
        # Check the duration of a video thumbnail.
        #
        durations = self.UTILS.element.getElements(DOM.Video.thumb_durations,
                                                   "Thumbnail durations", True, 20, False)

        if not durations:
            return False

        myDur = durations[thumb_num].text.strip()

        #
        # Video length didn't match exactly, but is it within the acceptable error margin?
        #
        from datetime import datetime, timedelta

        actual_time = datetime.strptime(myDur, '%M:%S')
        expect_time = datetime.strptime(length_str_mmss, '%M:%S')
        margin_time = timedelta(seconds=error_margin_ss)

        diff_time = actual_time - expect_time

        in_errorMargin = False

        # Less than expected, but within the error margin?
        if margin_time >= diff_time:
            in_errorMargin = True

        self.UTILS.test.TEST(in_errorMargin,
                             "Expected video length on thumbnail to be {}, +- {} seconds (it was {} seconds).".
                             format(length_str_mmss, error_margin_ss, myDur))

    def _convert_str_to_seconds(self, the_string):
        """
        Converts a str of the form "aa:bb" into seconds
        """
        processed = time.strptime(the_string, '%M:%S')
        return (int(datetime.timedelta(minutes=processed.tm_min, seconds=processed.tm_sec).total_seconds()))

    def check_video_length(self, expected_duration):
        """
        This method asserts that the video has the desired duration
        @param  int expected_duration   specifies the video duration in seconds
        """

        # Play the video and get total duration
        self.play_current_video()
        video_length = self.UTILS.element.getElement(DOM.Gallery.preview_current_video_duration, "Video length")
        real_duration = self._convert_str_to_seconds(video_length.text)

        # Note: we give 1 second margin in case the things went a little bit slower when recording the video
        interval = [expected_duration, expected_duration - 1, expected_duration + 1]
        self.UTILS.test.TEST(real_duration in interval, "Duration matches")

    def _click_on_video_external(self, position, frame_to_change):
        """
        Private method which handles image selection and image cropping
        @param  int     position            thumbnail to click 
        @param  tuple   frame_to_change     frame to switch once the image has been cropped
        """
        all_videos = self.UTILS.element.getElements(DOM.Video.thumbnails, "Videos")
        my_video = all_videos[num]
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

    def click_on_video_at_position_email(self, num):
        """
        Clicks a thumbnail from the gallery in order to attach it to an email
        """
        self._click_on_video_external(position, DOM.Email.frame_locator)

    def play_video(self, num):
        #
        # Clicks the thumbnail to start the video.
        #

        #
        # Get the list of video items and click the 'num' one.
        #
        all_videos = self.UTILS.element.getElements(DOM.Video.thumbnails, "Videos")
        my_video = all_videos[num]
        my_video.tap()

        #
        # Wait for the video to start playing before returning.
        #
        self.UTILS.element.waitForElements(DOM.Video.video_loaded, "Loaded video", True, 20, False)

    def is_video_playing(self):
        return self.marionette.find_element(*DOM.Video.video_player).get_attribute('paused') == 'false'

    def show_controls(self):
        self.parent.wait_for_element_displayed(*DOM.Video.video_player)
        self.marionette.find_element(*DOM.Video.video_player).tap()
        self.parent.wait_for_element_displayed(*DOM.Video.video_controls)

    @retry(5, 1)
    def is_this_video_being_played(self, video_name):
        self.show_controls()
        video_title = self.UTILS.element.getElement(DOM.Video.video_title, "Video title")

        if video_name == video_title.text and self.is_video_playing():
            return True
        else:
            raise
