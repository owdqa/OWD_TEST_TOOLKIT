from OWDTestToolkit.utils.i18nsetup import I18nSetup
_ = I18nSetup(I18nSetup).setup()

frame_locator = ('src', 'loop')
loading_overlay = ('id', 'loading-overlay')
app_header = ('xpath', '//section[@id="calllog-panel"]//h1[text()="Firefox Hello"]')
error_screen_ok = ('id', 'error-screen-ok')

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

# Mobile ID login
mobile_id_frame_locator = ('src', 'mobile_id')
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
mobile_id_add_phone_number_from_list = ('id', 'do-automatic-msisdn') # This goes back to the previous step

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
settings_select_call_mode_option = ('xpath', '//select[@id="video-default-setting"]/option[@data-l10n-id="{}"]')
settings_select_camera = ('id', 'camera-default-setting')
settings_select_camera_option = ('xpath', '//select[@id="camera-default-setting"]/option[@data-l10n-id="{}"]')
settings_clean_calls = ('id', 'settings-clean-calls-button')
settings_clean_shared_links =  ('id', 'settings-clean-urls-button')

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