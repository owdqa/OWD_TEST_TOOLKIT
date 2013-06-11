from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def checkVideoLength(self, p_vid_num, p_from_SS, p_to_SS):
        
        self.UTILS.logResult("info", "CANNOT USE checkVideoLength() AT THIS TIME!")
        return
    
        #
        # Check the length of a video by playing it.
        #
            
#         #
#         # Start the timer.
#         #
#         start_time = time.time()
#         
        #
        # Play the video.
        #
        self.startVideo(p_vid_num)
        
#         #
#         # Stop the timer.
#         #
# #        self.wait_for_element_not_displayed(*DOM.Video.video_frame)
#         self.UTILS.waitForNotElements(DOM.Video.video_frame, "Video frame", True, 20, False);
#         elapsed_time = int(time.time() - start_time)
        time.sleep(1)
        x = self.UTILS.getElement(DOM.Video.current_video_duration,
                                  "Duration of current video",
                                  False, 3, False)
        self.UTILS.logResult("info", "Video duration during playback was " + x.text + ".")
            
        return
        elapsed_time = float(x.text[-2:])
        
        #
        # Check the elapsed time.
        #
        self.UTILS.TEST((elapsed_time >= p_from_SS), "Video is not shorter than expected (played for %.2f seconds)." % elapsed_time)
        self.UTILS.TEST((elapsed_time <= p_to_SS), "Video is not longer than expected (played for %.2f seconds)." % elapsed_time)
