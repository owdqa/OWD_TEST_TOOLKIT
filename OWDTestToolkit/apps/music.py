from OWDTestToolkit import DOM
import time


class Music(object):

    def __init__(self, parent):
        self.apps = parent.apps
        self.data_layer = parent.data_layer
        self.parent = parent
        self.marionette = parent.marionette
        self.UTILS = parent.UTILS

    def launch(self):
        #
        # Launch the app.
        #
        self.app = self.apps.launch(self.__class__.__name__)
        self.UTILS.element.waitForNotElements(DOM.GLOBAL.loading_overlay, self.__class__.__name__ + " app - loading overlay")
        return self.app

    def click_on_song_mms(self):
        song = self.UTILS.element.getElement(DOM.Music.song1, "Song")
        song.tap()

        time.sleep(1)

        doneButton = self.UTILS.element.getElement(DOM.Music.done_button, "Done Button")
        doneButton.tap()

        self.UTILS.iframe.switchToFrame(*DOM.Messages.frame_locator)

    def click_on_song_email(self):
        song = self.UTILS.element.getElement(DOM.Music.song1, "Song")
        song.tap()

        time.sleep(1)

        doneButton = self.UTILS.element.getElement(DOM.Music.done_button, "Done Button")
        doneButton.tap()

        self.UTILS.iframe.switchToFrame(*DOM.Email.frame_locator)

    def play_song(self, position):
        songs = self.UTILS.element.getElements(DOM.Music.music_songs, "Songs")

        if (position <= len(songs)):
            songs[position].tap()
        else:
            self.UTILS.test.TEST(False, "Position greater than the number of songs stored in the device")
