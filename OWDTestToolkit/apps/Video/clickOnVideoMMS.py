from OWDTestToolkit.global_imports import *


class main(GaiaTestCase):

    def clickOnVideoMMS(self, p_num):
        #
        # Clicks the thumbnail to start the video.
        #

        #
        # Get the list of video items and click the 'p_num' one.
        #

        time.sleep(2)

        all_videos = self.UTILS.getElements(DOM.Video.thumbnails, "Videos")
        my_video = all_videos[p_num]
        my_video.tap()

        time.sleep(1)

        doneButton = self.UTILS.getElement(DOM.Video.done_button, "Done Button")
        doneButton.tap()

        self.UTILS.switchToFrame(*DOM.Messages.frame_locator)