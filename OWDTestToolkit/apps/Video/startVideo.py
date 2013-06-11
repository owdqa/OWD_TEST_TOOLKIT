from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def startVideo(self, p_num):
        #
        # Clicks the thumbnail to start the video.
        #

        #
        # Get the list of video items and click the 'p_num' one.
        #
        all_videos = self.UTILS.getElements(DOM.Video.thumbnails, "Videos")
        my_video = all_videos[p_num]
        my_video.tap()

        #
        # Wait for the video to start playing before returning.
        #
        self.UTILS.waitForElements(DOM.Video.video_loaded, "Loaded video", True, 20, False)

        
