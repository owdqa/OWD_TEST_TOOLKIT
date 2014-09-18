from OWDTestToolkit import DOM
import time


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

    def checkVideoLength(self, vid_num, from_ss, to_ss):
        self.UTILS.reporting.logResult("info", "CANNOT USE checkVideoLength() AT THIS TIME!")
        return

        #
        # Check the length of a video by playing it.
        #

        #
        # Play the video.
        #
        self.startVideo(vid_num)
        time.sleep(1)
        x = self.UTILS.element.getElement(DOM.Video.current_video_duration,
                                          "Duration of current video",
                                          False, 3, False)
        self.UTILS.reporting.logResult("info", "Video duration during playback was " + x.text + ".")

        elapsed_time = float(x.text[-2:])

        #
        # Check the elapsed time.
        #
        self.UTILS.test.TEST((elapsed_time >= from_ss), "Video is not shorter than expected (played for {:.2f} seconds).".
                             format(elapsed_time))
        self.UTILS.test.TEST((elapsed_time <= to_ss), "Video is not longer than expected (played for {:.2f} seconds).".
                             format(elapsed_time))

    def clickOnVideoMMS(self, num):
        #
        # Clicks the thumbnail to start the video.
        #

        #
        # Get the list of video items and click the 'num' one.
        #
        time.sleep(2)

        all_videos = self.UTILS.element.getElements(DOM.Video.thumbnails, "Videos")
        my_video = all_videos[num]
        my_video.tap()

        time.sleep(1)

        doneButton = self.UTILS.element.getElement(DOM.Video.done_button, "Done Button")
        doneButton.tap()

        self.UTILS.iframe.switchToFrame(*DOM.Messages.frame_locator)

    def clickOnVideoEmail(self, num):
        #
        # Clicks the thumbnail to start the video.
        #

        #
        # Get the list of video items and click the 'num' one.
        #
        time.sleep(2)

        all_videos = self.UTILS.element.getElements(DOM.Video.thumbnails, "Videos")
        my_video = all_videos[num]
        my_video.tap()

        time.sleep(1)

        doneButton = self.UTILS.element.getElement(DOM.Video.done_button, "Done Button")
        doneButton.tap()

        self.UTILS.iframe.switchToFrame(*DOM.Email.frame_locator)

    def startVideo(self, num):
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

    def is_this_video_being_played(self, video_name):
        self.show_controls()
        video_title = self.UTILS.element.getElement(DOM.Video.video_title, "Video title")
        self.UTILS.test.TEST(video_name == video_title.text and self.is_video_playing(),
                             "This video [{}] is actually being played".format(video_name))
