from OWDTestToolkit.global_imports import *


class main(GaiaTestCase):

    def clickOnSongMMS(self):

        song = self.UTILS.getElement(DOM.Music.song1, "Song")
        song.tap()

        time.sleep(1)

        doneButton = self.UTILS.getElement(DOM.Music.done_button, "Done Button")
        doneButton.tap()

        self.UTILS.switchToFrame(*DOM.Messages.frame_locator)