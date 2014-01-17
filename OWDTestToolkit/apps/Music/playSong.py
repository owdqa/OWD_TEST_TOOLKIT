from OWDTestToolkit.global_imports import *


class main(GaiaTestCase):

    def playSong(self):

        song = self.UTILS.getElement(DOM.Music.song, "Song")
        song.tap()
