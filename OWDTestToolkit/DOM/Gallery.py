from OWDTestToolkit.utils.i18nsetup import I18nSetup
_ = I18nSetup(I18nSetup).setup()

frame_locator = ("src", "gallery")
loading_bar = ("id", 'progress')

# Thumbnails screen
thumbnail_items = ('css selector', 'div.thumbnail')
thumbnail_select_mode = ("id", "thumbnails-select-button")
thumbnail_cancel_select_mode = ('id', 'thumbnails-cancel-button')
thumbnail_number_selected = ('id', 'thumbnails-number-selected')
thumbnail_trash_icon = ("id", "thumbnails-delete-button")
thumbnail_trash_confirm = ("id", "confirm-ok")
thumbnail_trash_cancel = ("id", "confirm-cancel")
thumbnail_camera_button = ("id", "thumbnails-camera-button")

# Preview screen
preview = ('id', 'fullscreen-view')
preview_back = ('id', 'fullscreen-back-button-tiny')

preview_toolbar = ('id', 'fullscreen-toolbar')
preview_toolbar_camera = ('id', 'fullscreen-camera-button-tiny')
preview_toolbar_edit = ('id', 'fullscreen-edit-button-tiny')
preview_toolbar_share = ('id', 'fullscreen-share-button-tiny')
preview_toolbar_info = ('id', 'fullscreen-info-button-tiny')
preview_toolbar_delete = ('id', 'fullscreen-delete-button-tiny')

preview_current_image = ('xpath', '//div[@class="frame" and contains(@style, "0px")]//div[@class="image-view"]')
preview_current_video = ('xpath', '//div[@class="frame" and contains(@style, "0px")]//img[@class="videoPoster"]')
preview_current_video_play = ('xpath', '//div[@class="frame" and contains(@style, "0px")]//button[@class="videoPlayerPlayButton"]')
preview_current_video_pause = ('xpath', '//div[@class="frame" and contains(@style, "0px")]//button[@class="videoPlayerPauseButton"]')
preview_current_video_duration = ('xpath', '//div[@class="frame" and contains(@style, "0px")]//span[@class="videoPlayerDurationText"]')

# Others
no_thumbnails_message = ("xpath", "//h1[@id='overlay-title' and text()='{}']".format(_("No photos or videos")))
crop_done = ("xpath", "//*[@id='crop-done-button']")
file_name_header = ('css selector', 'h1#filename')
download_manager_preview = ('css selector', 'div#frame div.image-view')