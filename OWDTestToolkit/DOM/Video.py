from OWDTestToolkit.utils.i18nsetup import I18nSetup
_ = I18nSetup(I18nSetup).setup()

frame_locator = ('src', 'video')
no_videos_message = ('xpath', 'h1[@id="overlay-title" and text() = "{}"]'.format(_("Add videos to get started")))
no_videos_go_to_camera = ('id', 'overlay-action-button')

# Thumbnails view
thumbnails_thumbs = ('css selector', 'ul.thumbnail-group-container li.thumbnail')

# IMPORTANT: Use the following locators nested with a specific thumbnail
thumbnail_title = ('class name', 'title')
thumbnail_duration = ('xpath', '//span[contains(@class, "duration-text")]')
thumbnail_size = ('xpath', '//span[contains(@class, "size-text")]')
thumbnail_type = ('xpath', '//span[contains(@class, "type-text")]')

thumbnails_go_to_camera = ('id', 'thumbnails-video-button')
thumbnails_select_mode = ('id', 'thumbnails-select-button')

# Select mode
select_mode_number_selected = ('id', 'thumbnails-number-selected')
select_mode_close = ('id', 'thumbnails-cancel-button')
select_mode_delete = ('id', 'thumbnails-delete-button')
select_mode_share = ('id', 'thumbnails-share-button')

# Player view
player_video = ('id', 'player-view')
player_video_loaded = ('css selector', 'video[style]')
player_time_slider = ('id', 'timeSlider')
player_time_slider_elapsed = ('id', 'elapsed-text')
player_time_slider_duration = ('id', 'duration-text')
player_toolbar = ('id', 'videoToolBar')
player_toolbar_prev = ('id', 'seek-backward')
player_toolbar_next = ('id', 'seek-forward')
player_toolbar_play = ('id', 'play')
player_back = ('id', 'close')
player_options = ('id', 'options')
player_video_controls = ('id', 'videoControls')
elapsed_time = ('id', 'elapsed-text')

# Other (attachments)
done_button = ("id", 'picker-done')
video_title = ("id", 'video-title')
