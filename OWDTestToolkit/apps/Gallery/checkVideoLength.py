from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def checkVideoLength(self, p_from_SS, p_to_SS):
        #
        # Check the length of a video.
        #
            
        # Start the timer.
        start_time = time.time()
        
        # Play the video.
        self.playCurrentVideo()
        
        # Stop the timer.
        elapsed_time = int(time.time() - start_time)
        
        self.UTILS.TEST((elapsed_time > p_from_SS), "Video is not shorter than expected (played for %.2f seconds)." % elapsed_time)
        self.UTILS.TEST((elapsed_time < p_to_SS), "Video is not longer than expected (played for %.2f seconds)." % elapsed_time)

