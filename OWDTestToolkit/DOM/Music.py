frame_locator = ('src', 'music')

audio = ('id', 'player-audio')
done_button = ("xpath", "//*[@id='title-done']")
song_by_title = ("xpath", '//a[@data-key-range="{}"]')
first_song = ("xpath", '//a[@data-option="title"]') # Must be xpath
song_title_amr = ("xpath", "//*[@data-l10n-id='unknownTitle']")
song_title = ("xpath", "//*[@data-l10n-id='music']")

title_song = ('id', 'title-text')

music_songs = ('css selector', '#views-tiles-anchor .tile')
progress_bar = ('xpath', '//progress[@id="player-seek-bar-progress"]')
seek_elapsed = ('id', 'player-seek-elapsed')

mix_tab = ('id', 'tabs-mix')
controls_play = ('id', 'player-controls-play')
