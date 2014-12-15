frame_locator = ("src", "camera")

# Superior HUD - TODO: check possible changes in 2.1
top_hud = ('class name', 'hud visible')
top_hud_switch_camera = ('xpath', '//div[contains(@class, "hud_btn hud_camera")]')
top_hud_switch_flash_auto = ('xpath', '//div[contains(@class, "hud_btn hud_flash icon-flash-auto")]')
top_hud_switch_flash_on = ('xpath', '//div[contains(@class, "hud_btn hud_flash icon-flash-on")]')
top_hud_switch_flash_off = ('xpath', '//div[contains(@class, "hud_btn hud_flash icon-flash-off")]')
top_hud_settings = ('xpath', '//div[contains(@class, "hud_btn hud_settings")]')

# Settings menu - TODO: check possible changes in 2.1
settings = ('class name', 'settings visible')
settings_menu_title = ('xpath', '//h2[@class="settings_title"]')
settings_close = ('xpath', '//div[contains(@class, "settings-close")]')
settings_items = ('xpath', '//div[@class="settings_items"]')
settings_hdr = ('xpath', '//div[@class="settings_items"]//li[contains(@class, "setting hdr)]')
settings_hdr_value = ('xpath', '//div[@class="settings_items"]//li[contains(@class, "setting hdr")]//h5[@class="setting_value"]')
settings_timer = ('xpath', '//div[@class="settings_items"]//li[contains(@class, "setting timer")]')
settings_timer_value = ('xpath', '//div[@class="settings_items"]//li[contains(@class, "setting timer")]//h5[@class="setting_value"]')
settings_grid = ('xpath', '//div[@class="settings_items"]//li[contains(@class, "setting hdr-setting")]')
settings_grid_value = ('xpath', '//div[@class="settings_items"]//li[contains(@class, "setting grid")]//h5[@class="setting_value"]')

# Camera controls
controls_pane = ('css selector', '.controls')
capture_button = ('css selector', '.capture-button')
switch_source = ('css selector', '.test-switch')
open_thumbs = ('css selector', '.test-thumbnail')

# Preview section
preview = ('class name', 'preview-gallery')
preview_header = ('css selector', 'div.preview-menu gaia-header')
preview_back = ('css selector', 'div.preview-menu gaia-header button[name=back]')
preview_share = ('css selector', 'div.preview-menu gaia-header button[name=share]')
preview_options = ('css selector', 'div.preview-menu gaia-header button[name=options]')
preview_count_text = ('css selector', 'div.preview-gallery div.count-text')

preview_container = ('css selector', 'div.preview-gallery div.frame-container')
preview_container_video = ('css selector', 'div.preview-gallery div.frame-container img.videoPoster')
preview_video_controls = ('class name', 'videoPlayerControls')
preview_video_play = ('class name', 'videoPlayerPlayButton')
preview_video_pause = ('class name', 'videoPlayerPauseButton')
preview_video_slider_elapsed = ('class name', 'videoPlayerElapsedText')
preview_video_slider_duration = ('class name', 'videoPlayerDurationText')

# Recording timer - TODO: check possible changes in 2.1
recording_timer = ('class name', 'recording-timer visible')

# action menu - TODO: check possible changes in 2.1
action_menu_gallery = ("xpath", "//form[@data-type='action']//button[@name='gallery']")
action_menu_delete = ("xpath", "//form[@data-type='action']//button[@name='delete']")
action_menu_cancel = ("xpath", "//form[@data-type='action']//button[@name='cancel']")

# Dialog menu - TODO: check possible changes in 2.1
dialog_menu_no = ('id', 'dialog-no')
dialog_menu_yes = ('id', 'dialog-yes')

# Attach picture just taken - TODO: check possible changes in 2.1
select_button = ('css selector', '.select-button')
retake_button = ('css selector', '.retake-button')