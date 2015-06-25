import GLOBAL

from OWDTestToolkit.utils.i18nsetup import I18nSetup
_ = I18nSetup(I18nSetup).setup()


frame_locator = ('src', "settings")
settings_header = ('xpath', GLOBAL.app_head_specific.format(_('Settings').encode("utf8")))
back_button = ('css selector', 'gaia-header button[data-icon=back]')

call_settings_option = ('id', 'call-settings')
call_settings_sim_card_number = ('id', 'menuItem-call-sim{}')
call_settings = ('id', "menuItem-callSettings")
call_callerID = ('id', "menuItem-callerId")
call_fdn = ('xpath', '//a[@data-href="#call-fdnSettings"]')

puk_code_input = ('css selector', '#simpin-dialog div.sim-pukArea input')
unlock_new_pin_input = ('css selector', '#simpin-dialog div.sim-newPinArea input')
unlock_confirm_new_pin_input = ('css selector', '#simpin-dialog div.sim-confirmPinArea input')
unlock_done_btn = ('css selector', '#simpin-dialog button[data-l10n-id=done]')

fdn_enable = ('id', 'fdn-enabled')
fdn_status = ('css selector', '#fdn-enabled small')
fdn_settings_header = ('xpath', '//h1[@data-l10n-id="fdnSettings-header"]')
fdn_auth_numbers = ('css selector', '[data-l10n-id=fdn-authorizedNumbers]')
fdn_pin2_input = ('css selector', '#call-pin2-dialog .sim-code-area.sim-pinArea input')
fdn_pin2_done = ('xpath', '//section[@id="call-pin2-dialog"]//button[@data-l10n-id="done"]')
fdn_puk2_pin2_input = ('xpath', '//section[@id="call-pin2-dialog"]//div[@class="sim-code-area sim-newPinArea"]/input')
fdn_enter_puk2_input = ('xpath', '//section[@id="call-pin2-dialog"]//div[@class="sim-code-area sim-pukArea"]/input')
fdn_confirm_pin2_input = ('css selector', '#call-pin2-dialog .sim-code-area.sim-confirmPinArea input')
fdn_input_error_msg = ('xpath', '//section[@id="call-pin2-dialog"]//div[@data-l10n-id="fdnErrorMsg"]')
fdn_pin2_tries_left = ('xpath', '//section[@id="call-pin2-dialog"]//div[@data-l10n-id="inputCodeRetriesLeft"]')
fdn_pin2_back_btn = ('xpath', '//section[@id="call-pin2-dialog"]//button/span[@data-l10n-id="back"]')
fdn_pin2_sim_locked = ('xpath', '//section[@id="call-pin2-dialog"]//div[@data-l10n-id="simCardLockedMsg"]')

fdn_auth_numbers_back = ('css selector', '#call-fdnList gaia-header')
fdn_add_auth_number = ('xpath', '//section[@id="call-fdnList"]//button[@id="fdnContact"]')
fdn_add_auth_number_name = ('xpath', '//section[@id="call-fdnList-add"]//input[@id="fdnContact-name"]')
fdn_add_auth_number_number = ('xpath', '//section[@id="call-fdnList-add"]//input[@id="fdnContact-number"]')
fdn_add_auth_number_done = ('xpath', '//section[@id="call-fdnList-add"]//button[@id="fdnContact-submit"]')

fdn_auth_numbers_list = ('css selector', '#call-fdnList #fdn-contactsContainer li')
fdn_auth_numbers_list_elem = ('xpath', '//ul[@id="fdn-contactsContainer"]//small[contains(text(), "{}")]')
fdn_auth_numbers_list_item = ('xpath', '//section[@id="call-fdnList"]//ul[@id="fdn-contactsContainer"]/li[{}]')
fdn_auth_number_action_header = ('xpath', '//form[@id="call-fdnList-action"]//span[@id="fdnAction-name"]')
fdn_auth_number_action_call = ('xpath', '//form[@id="call-fdnList-action"]//button[@id="fdnAction-call"]')
fdn_auth_number_action_edit = ('xpath', '//form[@id="call-fdnList-action"]//button[@id="fdnAction-edit"]')
fdn_auth_number_action_delete = ('xpath', '//form[@id="call-fdnList-action"]//button[@id="fdnAction-delete"]')
fdn_auth_number_action_cancel = ('xpath', '//form[@id="call-fdnList-action"]//button[@id="fdnAction-cancel"]')
fdn_warning_header = ('xpath', '//form[@id="confirmation-message"]//h1')
fdn_warning_body = ('xpath', '//form[@id="confirmation-message"]//p')
fdn_warning_ok = ('xpath', '//form[@id="confirmation-message"]//button[@class="full"]')

fdn_reset_pin2_btn = ('xpath', '//section[@id="call-fdnSettings"]//button[@data-l10n-id="fdnReset"]')

airplane_mode_switch = ("id", "menuItem-airplaneMode")
wifi_mode_switch = ("id", "menuItem-wifi")
wifi_mode_desc = ("id", "wifi-desc")

app_permissions = ('id', "menuItem-appPermissions")
app_permissions_header = ('xpath', GLOBAL.app_head_specific.format(_('App permissions')))

wifi = ('id', 'menuItem-wifi')
wifi_header = ('xpath', GLOBAL.app_head_specific.format('Wi-Fi'))
wifi_enabled = ('css selector', '.wifi-enabled label')
# Jump the unwanted li inside .wifi-availableNetworks
wifi_available_networks = ('css selector', '.wifi-availableNetworks li:not(.explanation):not([data-state="on"]):not([data-state="ready"])')
wifi_network_name = ('xpath', "//*[@id='wifi-availableNetworks']/li/aside/a[text()={}]")
wifi_name_xpath = '//ul[@class="wifi-availableNetworks"]//span[text()="{}"]'
wifi_connected = ('xpath', '//small[text()="{}"]'.format(_("Connected")))
wifi_list_connected_xp = "//*[@id='wifi-availableNetworks']/li[@class='active']//a[text()='{}']"

wifi_login_header = ("css selector", '#wifi-auth h1')
wifi_login_user = ('name', 'identity')
wifi_login_pass = ('css selector', '#wifi-auth input[name=password]')
wifi_login_ok_btn = ('css selector', '#wifi-auth button[type=submit] span[data-l10n-id=ok]')

wifi_details_header = ("css selector", "#wifi-status h1")
wifi_details_forget_btn = ("xpath", ".//button//span[text()='{}']".format(_('Forget')))
wifi_details_security = ("css selector", "span[data-l10n-id=security] + span")
wifi_details_signal = ("css selector", "span[data-l10n-id=signalStrength] + span")
wifi_details_ipaddress = ("css selector", "span[data-l10n-id=ipAddress] + span")
wifi_details_linkspeed = ("css selector", "span[data-l10n-id=linkSpeed] + span")

wifi_advanced_manage = ("css selector", "button.manageNetworks")
wifi_advanced_mac = ("css selector", "small[data-name=deviceinfo\.mac]")
wifi_advanced_knownNets = ("css selector", "#wifi-manageNetworks ul.wifi-knownNetworks li")
wifi_advanced_joinHidden = ("css selector", "button.joinHidden")
wifi_advanced_forgetBtn = ("id", "confirm-option")
wifi_advanced_cancelBtn = ("css selector", "button[data-l10n-id=cancel]")

data_connectivity = ('id', 'data-connectivity')
cellData = ('id', 'menuItem-cellularAndData')
celldata_header = ('css selector', 'h1[data-l10n-id=cellularAndData-header]')
cellData_sim_card_number = ('id', 'menuItem-carrier-sim{}')
sim_settings_header = ('css selector', 'h1[data-l10n-id="simSettings"]')

celldata_DataConn = ('name', "ril.data.enabled")
celldata_DataConn_switch = ('id', "menuItem-enableDataCall")
celldata_DataConn_confirm_header = ('css selector', '#carrier-dc-warning span[data-l10n-id=dataConnection-warning-head]')
celldata_DataConn_ON = ('css selector', "section#carrier-dc-warning button[data-l10n-id=turnOn]")

enable_data_connection = ('xpath', "//section[@id='carrier']//span[@data-l10n-id='dataConnection']/..")
enable_data_roaming = ('xpath', "//section[@id='carrier']//span[@data-l10n-id='dataRoaming']/..")

custom_settings_apn = ('css selector', 'section#carrier-dataSettings li span[data-l10n-id=custom]')
cellData_apn_settings = ('css selector', 'section#carrier-detail button[data-l10n-id=apnSettings]')
celldata_DataSettings = ('css selector', 'section#apn-settings button[data-l10n-id=dataSettings]')
celldata_MsgSettings = ('css selector', 'section#apn-settings button[data-l10n-id=messageSettings]')

networkOperator_button = ('css selector', '#carrier-detail button[data-l10n-id="networkOperator"]')
networkOperator_header = ('css selector', '#carrier-operatorSettings gaia-header h1')
networkOperator_types = ("id", "preferredNetworkType")
networkOperator_select_type = ("xpath", "//section[@class='value-selector-container']//span[text()='{}']")
networkOperator_OK_btn = ("css selector", "menu.value-selector-buttons button[data-l10n-id='ok']")

apn_settings_header = ('css selector', 'h1[data-l10n-id=apnSettings-header]')
celldata_data_apn = ('css selector', "input.apn")
celldata_apn_user = ('css selector', "input.user")
celldata_apn_passwd = ('css selector', "input.password")
apn_ok_button = ('css selector', "#apn-editor button.ok")
apn_settings_list = ('css selector', 'section#apn-list ul.apn-list li.apn-item')
apn_item_by_name = ('xpath', "//section[@id='apn-list']//span[text()='{}']")
add_new_apn = ('css selector', 'button[data-l10n-id=add-apn]')
apn_editor_header = ('css selector', 'h1[data-l10n-id=apn-editor-header]')

bluetooth = ("id", "menuItem-bluetooth")
bluetooth_desc = ("id", "bluetooth-desc")

sound = ('id', 'menuItem-sound')
sound_alarm_vol = ('name', 'audio.volume.alarm')

hotspot = ("id", "menuItem-internetSharing")
hotspot_header = ('xpath', GLOBAL.app_head_specific.format(_('Internet sharing')))
hotspot_switch = ("css selector", "#hotspot span[data-l10n-id=wifi-hotspot]")
hotspot_switch_input = ('xpath', '//section[@id="hotspot"]//input[@id="tethering-wifi-enabled"]/..')
hotspot_settings = ("css selector", "#hotspot-settings-section button[data-l10n-id=hotspotSettings]")

msg_settings = ("id", "menuItem-messagingSettings")
auto_retrieve_select_btn = ("name", "ril.mms.retrieval_mode")

auto_retrieve_select = ("xpath", "//section[@class='value-selector-container']//span[text()='{}']")

auto_retrieve_selected_item = ("css selector", ".value-selector-container li[aria-selected=true]")
auto_retrieve_ok_btn = ('css selector', 'button.value-option-confirm.affirmative.full[data-l10n-id=ok]')

ok_btn = ("xpath", "//menu[@id='select-options-buttons']/button")
delivery_report = ("xpath", "//*[@data-l10n-id='message-delivery-reports']")

sim_manager = ('id', 'menuItem-simManager')
sim_security_option = ('id', 'simSecurity-settings')
sim_security = ('id', 'menuItem-simSecurity')
sim_security_tag = ('id', 'simCardLock-desc')
sim_security_header = ('css selector', 'h1[data-l10n-id=simSecurity-header]')
sim_security_pin = ('css selector', 'li.simpin-enabled.simpin-enabled-0.simpin-0')
sim_security_change_pin = ('css selector', 'li.simpin-change button[data-l10n-id=changeSimPin]')
sim_security_enter_pin_header = ('xpath', GLOBAL.app_head_specific.format(_('Enter SIM PIN')))
sim_security_enter_pin_input = ('css selector', 'div.sim-code-area.sim-pinArea input')
sim_security_enter_pin_done = ('css selector', '#simpin-dialog button[data-l10n-id=done]')

sim_manager_option = ('id', 'simCardManager-settings')
sim_manager_sim_security = ('id', 'sim-manager-security-entry')
sim_manager_header = ('xpath', GLOBAL.app_head_specific.format(_('SIM manager').encode("utf8")))
dual_sim_switch_pin_sim1 = ('css selector', '#simpin-container .simpin-enabled.simpin-enabled-0.simpin-0')
dual_sim_change_pin_sim1 = ('css selector', '#simpin-container .simpin-change.simpin-change-0.simpin-0')

screen_lock_menu = ('id', 'menuItem-screenLock')
lockscreen_input = ('css selector', '.lockscreen-enable')
lockscreen_label = ('xpath', '//input[@class="lockscreen-enable"]/..')
passcode_lock = ('css selector', '.lockscreen-enabled')
passcode_enable = ('css selector', '.passcode-enable')
passcode_input = ('id', 'passcode-pseudo-input')
passcode_confirm = ('id', 'passcode-pseudo-confirm-input')
passcode_btn_create = ('css selector', '.passcode-create')
passcode_keyb_btn = ('css selector', '#lockscreen-passcode-pad a[data-key="{}"]')

change_pin_done_btn = ('xpath', '//section[@id="simpin-dialog"]//button[@data-l10n-id="done"]')
change_pin_old_input = ('css selector', '#simpin-dialog .pin-dialog .sim-code-area.sim-pinArea input')
change_pin_new_input = ('css selector', '#simpin-dialog .pin-dialog .sim-code-area.sim-newPinArea input')
change_pin_confirm_input = ('css selector', '#simpin-dialog .pin-dialog .sim-code-area.sim-confirmPinArea input')
change_pin_error = ('css selector', '#simpin-dialog .sim-errorMsg.error .sim-messageHeader')
change_pin_skip = ('css selector', '#simpin-dialog button[data-l10n-id=skip]')

downloads = ("id", "menuItem-downloads")
downloads_header = ("id", "downloads")
downloads_edit_mode_header = ("id", "downloads-title-edit")
downloads_edit_button = ("id", "downloads-edit-button")

# Firefox accounts
fxa = ('id', 'menuItem-fxa')
fxa_logged_out_screen = ('id', 'fxa-logged-out')
fxa_logged_in_screen = ('id', 'fxa-logged-in')
fxa_log_out_btn = ('id', 'fxa-logout')
fxa_log_in_btn = ('id', 'fxa-login')
fxa_logged_in_text = ('id', 'fxa-logged-in-text')

# Languages
language_item = ('id', 'menuItem-languageAndRegion')
language_selector = ('css selector', '#languages select[name="language.current"]')
language_option_xpath = '//section[@id="value-selector-container"]//span[contains(text(), "{}")]'
language_option_ok_btn = ('css selector', '#select-options-buttons button.affirmative[data-l10n-id="ok"]')

# Information
device_info_item = ('id', 'menuItem-deviceInfo')
device_more_info = ('css selector', '#about button[data-l10n-id=more-info]')
reset_phone_button = ('id', 'reset-phone')
confirm_reset_btn = ('id', 'confirm-reset-phone')

# Developer
developer_menu = ('id', 'menuItem-developer')
service_workers_item = ('css selector', '.menu-item[href*=developer-service-workers]')
service_worker_div = ('css selector', 'div[data-scope="{}"]')
service_worker_header = ('css selector', 'h2')
service_worker_scope = ('css selector', 'li span[data-l10n-id=service-worker-scope] + small')
service_worker_script_spec = ('css selector', 'li span[data-l10n-id=service-worker-script-spec] + small')
service_worker_current_url = ('css selector', 'li span[data-l10n-id=service-worker-current-worker-url] + small')
service_worker_active_cache_name = ('css selector', 'li span[data-l10n-id=service-worker-active-cache-name] + small')
service_worker_waiting_cache_name = ('css selector', 'li span[data-l10n-id=service-worker-waiting-cache-name] + small')
service_worker_update_btn = ('css selector', 'li button[data-l10n-id=service-worker-update]')
service_worker_unregister_btn = ('css selector', 'li button[data-l10n-id=service-worker-unregister]')
