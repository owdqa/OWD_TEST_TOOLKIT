from OWDTestToolkit.global_imports import *


class main(GaiaTestCase):

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