from OWDTestToolkit.global_imports import *


class main(GaiaTestCase):

    def createMMSVideo(self):

        attach = self.UTILS.getElement(DOM.Messages.attach_button, "Attach button")
        attach.tap()

        self.marionette.switch_to_frame()

        video = self.UTILS.getElement(DOM.Messages.mms_from_video, "From video")
        video.tap()

        self.UTILS.switchToFrame(*DOM.Video.frame_locator)