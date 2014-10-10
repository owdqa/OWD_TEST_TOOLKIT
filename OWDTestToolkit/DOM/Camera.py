frame_locator = ("src", "camera")

# Superior HUD
top_hud = ('class name', 'hud visible')
top_hud_switch_camera = ('xpath', '//div[contains(@class="hud_btn hud_camera")]')
top_hud_switch_flash_auto = ('xpath', '//div[contains(@class="hud_btn hud_flash icon-flash-auto")]')
top_hud_switch_flash_on = ('xpath', '//div[contains(@class="hud_btn hud_flash icon-flash-on")]')
top_hud_switch_flash_off = ('xpath', '//div[contains(@class="hud_btn hud_flash icon-flash-off")]')
top_hud_settings = ('xpath', '//div[contains(@class="hud_btn hud_settings")]')

# Settings menu
settings = ('class name', 'settings visible')
settings_menu_title = ('xpath', '//h2[@class="settings_title"]')
settings_close = ('xpath', '//div[contains(@class="settings-close")]')
settings_items = ('xpath', '//div[@class="settings_items"]')
settings_hdr = ('xpath', '//div[@class="settings_items"]//li[contains(@class="setting hdr)]')
settings_hdr_value = ('xpath', '//div[@class="settings_items"]//li[contains(@class="setting hdr")]//h5[@class="setting_value"]')
settings_timer = ('xpath', '//div[@class="settings_items"]//li[contains(@class="setting timer")]')
settings_timer_value = ('xpath', '//div[@class="settings_items"]//li[contains(@class="setting timer")]//h5[@class="setting_value"]')
settings_grid = ('xpath', '//div[@class="settings_items"]//li[contains(@class="setting hdr-setting")]')
settings_grid_value = ('xpath', '//div[@class="settings_items"]//li[contains(@class="setting grid")]//h5[@class="setting_value"]')

# Camera controls
controls_pane = ('xpath', '//div[contains(@class, "controls")]')
capture_button = ('class name', 'capture-button')
switch_source = ('xpath', '//div[contains(@class, "mode-switch")]')
open_thumbs = ('css selector', '.controls-left > [name=thumbnail]')

# Preview section
preview = ('class name', 'preview-gallery')
preview_header = ('xpath', '//div[contains(@class, "preview-menu")]//header')
preview_back = ('xpath', '//div[contains(@class, "preview-menu")]//header//button[@name="back"]')
preview_share = ('xpath', '//div[contains(@class, "preview-menu")]//header//button[@name="share"]')
preview_options = ('xpath', '//div[contains(@class, "preview-menu")]//header//button[@name="options"]')
preview_count_text = ('xpath', '//div[contains(@class, "preview-menu")]//div[contains(@class, "count-text")]')

preview_container = ('xpath', '//div[@class="preview-gallery"]//div[contains(@class, "frame-container")]')
preview_container_video = ('xpath', '//div[@class="preview-gallery"]//div[contains(@class, "frame-container")]//img[@class="videoPoster"]')
preview_video_controls = ('class name', 'videoPlayerControls')
preview_video_play = ('class name', 'videoPlayerPlayButton')
preview_video_pause = ('class name', 'videoPlayerPauseButton')
preview_video_slider_elapsed = ('class name', 'videoPlayerElapsedText')
preview_video_slider_duration = ('class name', 'videoPlayerDurationText')

# Recording timer
recording_timer = ('class name', 'recording-timer visible')

# action menu
action_menu_gallery = ("xpath", "//form[@data-type='action']//button[@name='gallery']")
action_menu_delete = ("xpath", "//form[@data-type='action']//button[@name='delete']")
action_menu_cancel = ("xpath", "//form[@data-type='action']//button[@name='cancel']")

# Dialog menu
dialog_menu_no = ('id', 'dialog-no')
dialog_menu_yes = ('id', 'dialog-yes')

# Attach picture just taken
select_button = ('css selector', '.select-button')
retake_button = ('css selector', '.retake-button')