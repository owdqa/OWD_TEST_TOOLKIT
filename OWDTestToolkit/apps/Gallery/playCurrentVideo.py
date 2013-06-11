from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def playCurrentVideo(self):
        #
        # Plays the video we've loaded (in gallery you have to click the thumbnail first,
        # THEN press a play button - it doesn't play automatically).
        #
        playBTN = self.UTILS.getElement(DOM.Gallery.video_play_button, "Video play button")
        playBTN.click()
        playBTN.tap()
        
        self.UTILS.waitForNotElements(DOM.Gallery.video_pause_button, "Pause button", True, 20, False);

