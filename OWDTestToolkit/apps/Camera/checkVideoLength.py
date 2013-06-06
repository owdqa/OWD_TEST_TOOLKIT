from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def checkVideoLength(self, p_vid_num, p_from_SS, p_to_SS):
        #
        # Check the length of a video.
        #
            
        #
        # Find the thumbnail for this video and click it.
        #
        self.clickThumbnail(p_vid_num)
        
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
                                      "Video pause button", True, 20, False);
        
        elapsed_time = int(time.time() - start_time)
        
        self.UTILS.TEST((elapsed_time >= p_from_SS), "Video is not shorter than expected (played for %.2f seconds)." % elapsed_time)
        self.UTILS.TEST((elapsed_time <= p_to_SS), "Video is not longer than expected (played for %.2f seconds)." % elapsed_time)

