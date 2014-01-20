from OWDTestToolkit.global_imports import *


class main(GaiaTestCase):

    def createMMSMusic(self):

        attach = self.UTILS.getElement(DOM.Messages.attach_button, "Attach button")
        attach.tap()

        self.marionette.switch_to_frame()

        music = self.UTILS.getElement(DOM.Messages.mms_from_music, "From music")
        music.tap()

        self.UTILS.switchToFrame(*DOM.Music.frame_locator)