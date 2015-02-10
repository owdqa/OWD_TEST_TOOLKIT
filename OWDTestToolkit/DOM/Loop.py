from OWDTestToolkit.utils.i18nsetup import I18nSetup
_ = I18nSetup(I18nSetup).setup()

frame_locator = ('src', 'loop')
loading_overlay = ('id', 'loading-overlay')
app_header = ('css selector', 'section#calllog-panel')

# Wizard
wizard = ('id', 'wizard-tutorial-section')
wizard_header = ('id', 'wizard-tutorial-header')
wizard_slideshow = ('id', 'wizard-tutorial-slideshow')
wizard_slideshow_step = ('xpath', '//ul[@id="wizard-tutorial-slideshow"]/li[@class="wizard-tutorial-step"]')
wizard_slideshow_progress = ('id', 'wizard-tutorial-progress')
wizard_slideshow_progress_step = ('id', 'progress-step-{}')
wizard_slideshow_progress_step_active = ('css selector', '#wizard-tutorial-progress li.active')
wizard_login = ('id', 'wizard-login')
wizard_login_phone_number = ('id', 'authenticate-msisdn-button')
wizard_login_ffox_account = ('id', 'authenticate-fxa-button')

# Ffox account login
ffox_account_frame_locator = ('src', 'fxa_module')
ffox_account_login_title = ('xpath', '//h1[@data-l10n-id="firefox-accounts-title"]')
ffox_account_login_mail = ('id', 'fxa-email-input')
ffox_account_login_pass = ('id', 'fxa-pw-input')
ffox_account_login_next = ('id', 'fxa-module-next')
ffox_account_login_done = ('id', 'fxa-module-done')
ffox_account_login_back = ('id', 'fxa-module-back')
ffox_account_login_close = ('id', 'fxa-module-close')
ffox_account_login_overlay = ('id', 'fxa-overlay')
ffox_account_error_overlay = ('id', 'fxa-error-overlay')
ffox_account_error_overlay_title = ('id', 'fxa-error-title')
ffox_account_error_overlay_ok = ('id', 'fxa-error-ok')
ffox_account_age_selector = ('id', 'fxa-age-select')
ffox_account_age_option = ('css selector', '#value-selector-container li[data-option-index="1"]')

# Mobile ID login
mobile_id_frame_locator = ('src', 'mobile_id')
mobile_id_header = ('id', 'header')
mobile_id_close_btn = ('id', 'close-button')
mobile_id_explanation = ('id', 'mobile-id-explanation')
mobile_id_sim_list = ('css selector', 'ul.phone-options-list')
mobile_id_sim_list_item = ('css selector', 'ul.phone-options-list li')
mobile_id_allow_button = ('id', 'allow-button')
mobile_id_verified_button = ('id', 'verify-button')
mobile_id_error = ('id', 'mobileid-error-overlay')
mobile_id_error_ok_btn = ('id', 'mobileid-error-ok')
mobile_id_back = ('id', 'close-button')
mobile_id_add_phone_number = ('id', 'add-msisdn')
mobile_id_add_phone_number_prefix = ('id', 'country-codes-select')
mobile_id_add_phone_number_number = ('id', 'msisdn-input')
mobile_id_add_phone_number_from_list = ('id', 'do-automatic-msisdn')  # This goes back to the previous step

# Call log
call_log = ('id', 'calllog-panel')
open_settings_btn = ('id', 'open-settings-button')
call_log_calls_tab = ('id', 'call-section-filter')
call_log_shared_links_tab = ('id', 'urls-section-filter')

# Call log - sections
calls_section = ('id', 'calls-section')
calls_section_empty = ('css selector', '#calls-section div.section-empty p.section-empty-label')
calls_section_entries = ('id', 'calls-section-entries')
shared_links_section = ('id', 'urls-section')
shared_links_empty = ('css selector', '#urls-section div.section-empty p.section-empty-label')
shared_links_entries = ('id', 'urls-section-entries')
shared_links_entry = ('css selector', '#urls-section-entries li')
shared_links_entry_revoked = ('xpath', '//div[@id="urls-section-entries"]//li//p[@data-revoked="true"]')
shared_links_entry_revoked_nested = ('xpath', '//p[@data-revoked="true"]')
shared_links_entry_available = ('xpath', '//div[@id="urls-section-entries"]//li//p[@data-revoked="false"]')

# Call log - footer
call_from_loop = ('id', 'call-from-loop')

# Settings panel
settings_panel = ('id', 'settings-panel')
settings_panel_header = ('xpath', '//h1[@data-l10n-id="settingsTitle"]')
settings_panel_back_btn = ('id', 'settings-close-button')

# Settings panel - content
settings_select_call_mode = ('id', 'video-default-setting')
settings_selected_call_mode = ('css selector', '#video-default-setting option[value=true]')
settings_select_call_mode_option = ('xpath', '//select[@id="video-default-setting"]/option[@data-l10n-id="{}"]')
settings_select_camera = ('id', 'camera-default-setting')
settings_selected_camera = ('css selector', '#camera-default-setting option:checked')
settings_select_camera_option = ('xpath', '//select[@id="camera-default-setting"]/option[@data-l10n-id="{}"]')
settings_clean_calls = ('id', 'settings-clean-calls-button')
settings_clean_rooms = ('id', 'settings-clean-rooms-button')
settings_clean_shared_links = ('id', 'settings-clean-urls-button')

# Settings panel - footer
settings_logged_as = ('id', 'settings-logout-identity')
settings_logout = ('id', 'settings-logout-button')

# Form action (actions so far: delete, revoke, cleanAll, cleanJustRemoved)
form_action_cancel = ('xpath', '//form[@data-type="action"]//button[last()]')
form_action_action = ('xpath', '//form[@data-type="action"]//button[@data-l10n-id="{}"]')

# Form confirm
form_confirm_cancel = ('xpath', '//form[@data-type="confirm"]//button[@data-l10n-id="cancel"]')
form_confirm_delete = ('xpath', '//form[@data-type="confirm"]//button[@data-l10n-id="delete"]')
form_confirm_logout = ('xpath', '//form[@data-type="confirm"]//button[@data-l10n-id="logOut"]')

error_screen = ('id', 'error-screen')
error_msg = ('id', 'error-message')
error_screen_ok = ('id', 'error-screen-ok')

# Share panel
share_panel = ('id', 'share-panel')
share_panel_close = ('id', 'share-close-button')
share_panel_header = ('xpath', '//h1[@data-l10n-id="shareTitle"]')
share_panel_contact_name = ('id', 'contact-name-to-share')
share_panel_contact_reason = ('id', 'sharing-reason')
share_panel_share_link = ('id', 'link-to-share')
share_panel_sms_share = ('id', 'share-by-sms')
share_panel_email_share = ('id', 'share-by-email')
share_panel_others_share = ('id', 'share-by-others')
share_link_options = ('css selector', '.share-options li')
share_others_header = ('xpath', '//header[text()="{}"]')
share_others_options = ('xpath', '//header[text()="{}"]/..//button')

not_a_hello_user_msg = ('xpath', "//p[@id='sharing-reason' and text()='{}']")
not_a_user_explanation = ('css selector', '.share-explanation[data-l10n-id=noProblem]')

# Call screen
call_frame = ('xpath', '//iframe[@class="active" and @name=""]')  # TODO: fill it!
call_screen_contact_details = ('xpath', '//h1[@id="contact-name-details" and text()="{}"]')
call_screen_counter = ('id', 'counter')
call_screen_status = ('id', 'call-status-info')
call_screen_video_container = ('id', 'local-video')
call_screen_hang_up = ('id', 'hang-up')
call_screen_answer = ('id', 'answer')
call_screen_answer_video = ('id', 'answer-video')
call_screen_mute = ('id', 'call-settings-mute')
call_screen_speaker = ('id', 'call-settings-speaker')
call_screen_video_mode = ('id', 'call-settings-video')
call_screen_resume = ('id', 'resume-button')

# Feedback
feedback = ('id', 'feedback')
feedback_skip = ('id', 'skip-feedback-button')
feedback_rate = ('id', 'rate-feedback-button')

# Footer
toggle_new_communication_button = ('css selector', 'button.toggle-actions')
create_new_room = ('css selector', 'button.create-room')
create_new_call = ('css selector', 'button.new-conversation')

# Rooms
calllog_container = ('id', 'calllog_container')
nav_rooms_button = ('id', 'rooms-section-filter')
nav_calls_button = ('id', 'calls-section-filter')
rooms_section = ('id', 'rooms-section')
calls_section = ('id', 'calls-section')
new_room_input = ('css selector', '#new-room input')
save_room_btn = ('id', 'save-room-action')
rooms_entries = ('css selector', 'rooms-section-entries li')
room_entry = ('css selector', '#rooms-section-entries li[data-room-name="{}"]')
room_edit = ('css selector', 'button.secondary-action.room-time')
room_detail_edit_btn = ('id', 'rdp-edit-button')
room_detail_header = ('css selector', '#room-detail-panel h1[data-l10n-id=roomDetail]')
room_edit_name_input = ('css selector', 'section#new-room input')
room_edit_name_reset = ('css selector', 'section#new-room button[type=reset]')
save_room_btn = ('id', 'save-room-action')

# Room Details view
room_name = ('id', 'rdp-name')
room_back_btn = ('id', 'rdp-back-button')
room_share_section = ('id', 'rdp-share-section')
room_share_button = ('id', 'rdp-share-contact')
room_invitees_section = ('id', 'rdp-invitees-section')
room_show_invitees = ('id', 'rdp-show-invitees')
room_history_section = ('id', 'rdp-history-section')
room_show_history = ('id', 'rdp-show-history')
room_expiration_section = ('id', 'rdp-expiration-section')
room_expiration = ('id', 'rdp-expiration')

# Room sharing and joining
room_share_invalid_contact_ok = ('css selector', 'div[data-manifest-name="Firefox Hello"] button.modal-dialog-alert-ok')
room_share_button_with_text = ('xpath', '//form[@data-type="action"]//button[text()="{}"]')
room_link_in_email = ('css selector', 'a[ext-href*="hello.firefox.com"]')
room_open_link_ok = ('id', 'msg-browse-ok')
room_open_link_cancel = ('id', 'msg-browse-cancel')
room_btn_browser_join = ('css selector', 'button.btn-join')
room_btn_browser_leave = ('css selector', 'button.btn-hangup')
room_select_camera_front = ('css selector', 'li.icon-camera-front label')
room_select_camera_back = ('css selector', 'li.icon-camera-back label')
room_camera_container = ('css selector', 'section.camera-container')
room_button_join = ('css selector', 'button.join')
room_button_cancel = ('css selector', 'button.cancel')

# Room call controls
room_leave_btn = ('id', 'leave-room')
room_settings_togglemic = ('id', 'room-settings-togglemic')
room_settings_togglevideo = ('id', 'room-settings-togglevideo')
room_settings_switch_speaker = ('id', 'room-settings-switchspeaker')

# Conversation (call) detail
new_call_header = ('css selector', 'h1[data-l10n-id=conversationDetailTitle]')
new_call_subject = ('css selector', 'section.fit form input[type=text]')
new_call_subject_chars_left = ('css selector', 'section.fit form p.counter')
new_call_subject_reset = ('css selector', 'section.fit form button[type=reset]')
new_call_camera_back = ('css selector', 'li.icon-camera-back')
new_call_camera_front = ('css selector', 'li.icon-camera-front')
new_call_selected_camera = ('css selector', 'input[name=select-camera]:checked')
new_call_start_call = ('css selector', 'button.call')

# Fallback
new_call_fallback_message = ('css selector', 'form[data-type=confirm] p')
new_call_fallback_new_room = ('css selector', 'button[data-l10n-id=newRoom]')
new_call_fallback_cancel = ('css selector', 'button[data-l10n-id=cancel]')

# Fallback options ( very generic :( )
fallback_options = ('css selector', 'form[data-type=action] menu button')