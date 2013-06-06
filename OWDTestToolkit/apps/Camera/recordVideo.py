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
#         self.wait_for_condition(lambda m: m.find_element(*DOM.Camera.video_timer).text == p_length_str_MMSS)
        time.sleep(p_length)
            
        # Stop recording
        captureBTN.tap()

        self.UTILS.waitForNotElements(DOM.Camera.video_timer, "Video timer", True, 10, False);

        self.UTILS.waitForElements(DOM.Camera.thumbnail, 
                                    "Thumbnail appears after recording video", True, 10, False)
        
        # TEST: Thumbnail has not been previewed yet.
        prev_marker = self.UTILS.getElement(DOM.Camera.thumbnail_preview_marker, "Thumbnail preview marker", False)
        self.UTILS.TEST((prev_marker.get_attribute("class") == "offscreen"), "Image is not previewed as soon as picture is taken.")
        
