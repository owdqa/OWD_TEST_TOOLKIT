from OWDTestToolkit import DOM
import time
from marionette import Actions
from OWDTestToolkit.utils.decorators import retry


class Music(object):

    def __init__(self, parent):
        self.apps = parent.apps
        self.data_layer = parent.data_layer
        self.parent = parent
        self.marionette = parent.marionette
        self.UTILS = parent.UTILS

    def launch(self):
        self.app = self.apps.launch(self.__class__.__name__)
        self.UTILS.element.waitForNotElements(DOM.GLOBAL.loading_overlay, self.__class__.__name__ +
                                              " app - loading overlay")
        return self.app

    @retry(5)
    def click_on_song(self, title=None, frame=None):
        dom_elem = DOM.Music.first_song if not title\
            else (DOM.Music.song_by_title[0], DOM.Music.song_by_title[1].format(title))
        song = self.UTILS.element.getElement(dom_elem, "Song")
        time.sleep(1)
        song.tap()
        time.sleep(1)

        doneButton = self.UTILS.element.getElement(DOM.Music.done_button, "Done Button")
        doneButton.tap()

        self.UTILS.iframe.switchToFrame(*frame)

    def click_on_song_mms(self, title=None):
        self.click_on_song(title, DOM.Messages.frame_locator)

    def click_on_song_email(self, title=None):
        self.click_on_song(title, DOM.Email.frame_locator)

    def play_from_tiles_by_position(self, position):
        songs = self.UTILS.element.getElements(DOM.Music.music_songs, "Songs")

        if (position < len(songs)):
            songs[position].tap()
        else:
            self.UTILS.test.test(False, "Position greater than the number of songs stored in the device")

    def play_from_tiles_by_artist(self, artist):
        songs = self.UTILS.element.getElements(DOM.Music.music_songs, "Songs")

        for song in songs:
            try:
                title = song.find_element('css selector', '.tile-title-artist')
                if title.text.lower() == artist.lower():
                    song.tap()
                    break
            except:

                # Song not found, so keep looping
                pass

    def get_total_songs(self):
        
        # Make sure we're in the mix tab (the left)
        try:
            self.UTILS.reporting.logResult("info", "Try to get the Mix Tab")
            self.parent.wait_for_element_displayed(*DOM.Music.mix_tab)

            mix_tab = self.marionette.find_element(*DOM.Music.mix_tab)
            mix_tab.tap()

            try:
                self.parent.wait_for_element_displayed(*DOM.Music.music_songs)
                return len(self.marionette.find_elements(*DOM.Music.music_songs))
            except:
                return 0
        except:  # This could be the music frame comes from the SMS app or Email (attach)
            self.parent.wait_for_element_displayed(*('id', 'views-list-anchor'))
            try:
                self.parent.wait_for_element_displayed(*('css selector', '#views-list-anchor .list-item'))
                return len(self.marionette.find_elements(*('css selector', '#views-list-anchor .list-item')))
            except:
                return 0

    def is_player_playing(self):
        # get 4 timestamps during approx. 1 sec
        # ensure that newer timestamp has greater value than previous one
        timestamps = []
        for i in range(4):
            timestamps.append(self.player_current_timestamp)
            time.sleep(.25)
        return all([timestamps[i - 1] < timestamps[i] for i in range(1, 3)])

    @property
    def player_current_timestamp(self):
        player = self.marionette.find_element(*DOM.Music.audio)
        return float(player.get_attribute('currentTime'))

    def tap_play(self):
        play_button = self.marionette.find_element(*DOM.Music.controls_play)
        # TODO: Change this to a simple tap when bug 862156 is fixed
        Actions(self.marionette).tap(play_button).perform()
