from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def switchSource(self):
        #
        # Switch between still shot and video.
        #
        switchBTN = self.UTILS.getElement(DOM.Camera.switch_source_btn, "Source switcher")
        switchBTN.tap()
        self.UTILS.waitForElements(DOM.Camera.capture_button_enabled, "Enabled capture button")

