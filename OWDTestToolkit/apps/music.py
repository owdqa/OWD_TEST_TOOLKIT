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

    def click_on_song_mms(self, title=None):
        dom_elem = DOM.Music.song1  if not title\
                                    else (DOM.Music.song_by_title[0], DOM.Music.song_by_title[1].format(title))
        song = self.UTILS.element.getElement(dom_elem, "Song")
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

    def play_from_tiles_by_position(self, position):
        songs = self.UTILS.element.getElements(DOM.Music.music_songs, "Songs")

        if (position < len(songs)):
            songs[position].tap()
        else:
            self.UTILS.test.TEST(False, "Position greater than the number of songs stored in the device")

    def play_from_tiles_by_artist(self, artist):
        songs = self.UTILS.element.getElements(DOM.Music.music_songs, "Songs")

        for song in songs:
            try:
                title = song.find_element('css selector', '.tile-title-artist')
                if title.text.lower() == artist.lower():
                    song.tap()
                    break
            except:
                #
                # Song not found, so keep looping
                #
                pass

    def get_total_songs(self):
        #
        # Make sure we're in the mix tab (the left)
        #
        mix_tab = self.UTILS.element.getElement(DOM.Music.mix_tab, "Mix tab")
        mix_tab.tap()

        try:
            self.parent.wait_for_element_displayed(*DOM.Music.music_songs)
            return len(self.marionette.find_elements(*DOM.Music.music_songs))
        except:
            return 0
