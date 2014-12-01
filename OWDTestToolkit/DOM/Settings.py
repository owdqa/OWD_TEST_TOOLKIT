import GLOBAL

from OWDTestToolkit.utils.i18nsetup import I18nSetup
_ = I18nSetup(I18nSetup).setup()


frame_locator = ('src', "settings")
settings_header = ('xpath', GLOBAL.app_head_specific.format(_('Settings').encode("utf8")))
back_button = ('class name', 'icon icon-back')

call_settings_option = ('id', 'call-settings')
call_settings_sim_card_number = ('id', 'menuItem-call-sim{}')
call_settings = ('id', "menuItem-callSettings")
call_callerID = ('id', "menuItem-callerId")
call_fdn = ('xpath', '//a[@data-href="#call-fdnSettings"]')

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

fdn_auth_numbers_back = ('xpath', '//section[@id="call-fdnList"]//span[@data-l10n-id="back"]')
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
# app_perm_camera = ('xpath', './/*[@id="appPermissions"]//a[text()="Camera"]')
# app_perm_camera_geo = ('xpath', './/*[@id="appPermissions-details"]//span[text()="Geolocation"]/select')

wifi = ('id', 'menuItem-wifi')
wifi_header = ('xpath', GLOBAL.app_head_specific.format('Wi-Fi'))
wifi_enabled = ('xpath', ".//*[@id='wifi-enabled']/label")
wifi_available_networks = ('xpath', "//*[@id='wifi-availableNetworks']/li/aside[contains(@class, 'pack-end wifi-icon level-')]")
wifi_network_name = ('xpath', "//*[@id='wifi-availableNetworks']/li/aside/a[text()={}]")
wifi_name_xpath = '//*[@id="wifi-availableNetworks"]//a[text()="{}"]'
wifi_connected = ('xpath', '//small[text()="{}"]'.format(_("Connected")))
wifi_list_connected_xp = "//*[@id='wifi-availableNetworks']/li[@class='active']//a[text()='{}']"

wifi_login_header = ("xpath", "//section[@id='wifi-auth']//h1")
wifi_login_user = ('name', 'identity')
wifi_login_pass = ('xpath', '//section[@id="wifi-auth"]//input[@name="password"]')
wifi_login_ok_btn = ('xpath', "//section[@id='wifi-auth']//button[@type='submit']/span[@data-l10n-id='ok']")

wifi_details_header = ("xpath", "//section[@id='wifi-status']//h1")
wifi_details_forget_btn = ("xpath", ".//button//span[text()='{}']".format(_('Forget')))
wifi_details_security = ("xpath", "//a[@data-l10n-id='security']/span")
wifi_details_signal = ("xpath", "//a[@data-l10n-id='signalStrength']/span")
wifi_details_ipaddress = ("xpath", "//a[@data-l10n-id='ipAddress']/span")
wifi_details_linkspeed = ("xpath", "//a[@data-l10n-id='linkSpeed']/span")

wifi_advanced_btn = ("id", "manageNetworks")
wifi_advanced_mac = ("xpath", "//small[@data-name='deviceinfo.mac']")
wifi_advanced_knownNets = ("xpath", "//*[@id='wifi-knownNetworks']/li")
wifi_advanced_joinHidden = ("id", "joinHidden")
wifi_advanced_forgetBtn = ("xpath", "//*[@id='confirm-option']")
wifi_advanced_cancelBtn = ("xpath", "//button[@data-l10n-id='cancel']")

data_connectivity = ('id', 'data-connectivity')
cellData = ('id', 'menuItem-cellularAndData')
cellData_sim_card_number = ('id', 'menuItem-carrier-sim{}')
celldata_header = ('xpath', GLOBAL.app_head_specific.format(_('Cellular & Data').encode("utf8")))
celldata_DataConn = ('name', "ril.data.enabled")
celldata_DataConn_switch = ('id', "menuItem-enableDataCall")
celldata_DataConn_confirm_header = ('xpath', '//section[@id="carrier-dc-warning"]//span[@data-l10n-id="dataConnection-warning-head"]')
celldata_DataConn_ON = ('xpath', "//section[@id='carrier-dc-warning']//button[@data-l10n-id='turnOn']")
enable_data_connection = ('xpath', "//section[@id='carrier']//span[@data-l10n-id='dataConnection']/..")
enable_data_roaming = ('xpath', "//section[@id='carrier']//span[@data-l10n-id='dataRoaming']/..")
celldata_DataSettings = ('xpath', "//section[@id='carrier']//button[@data-l10n-id='dataSettings']")
celldata_MsgSettings = ('xpath', "//*[@id='carrier']//button[@data-l10n-id='messageSettings']")
custom_settings_apn = ('xpath', "//*[@id='carrier-dataSettings']//li//span[@data-l10n-id='custom']")
celldata_data_apn = ('id', "ril.data.apn")
celldata_apn_user = ('id', "ril.data.user")
celldata_apn_passwd = ('id', "ril.data.passwd")
celldata_ok_button = ('css selector', "#carrier-dataSettings span[data-l10n-id=ok]")
celldata_mms_ok_button = ('css selector', "#carrier-mmsSettings span[data-l10n-id=ok]")
apn_settings_list = ('xpath', "//li//input[@name='defaultApn']")
selected_apn = ('css selector', 'label > input[name=defaultApn]:checked + span')
default_apn = ('xpath', "//*[@id='carrier-dataSettings']//span[text()='{}']/..")
default_apn_mms = ('xpath', "//*[@id='carrier-mmsSettings']//span[text()='{}']/..")
selected_apn_mms = ('css selector', 'label > input[name=mmsApn]:checked + span')
data_settings_back_btn = ('xpath', '//section[@id="carrier-dataSettings"]//button/span[@data-l10n-id="back"]')
mms_settings_back_btn = ('xpath', '//section[@id="carrier-mmsSettings"]//button/span[@data-l10n-id="back"]')

bluetooth = ("id", "menuItem-bluetooth")
bluetooth_desc = ("id", "bluetooth-desc")

sound = ('id', 'menuItem-sound')
sound_alarm_vol = ('name', 'audio.volume.alarm')

hotspot = ("id", "menuItem-internetSharing")
hotspot_header = ('xpath', GLOBAL.app_head_specific.format(_('Internet sharing')))
hotspot_switch = ("css selector", "#hotspot span[data-l10n-id=wifi-hotspot]")
hotspot_switch_input = ("css selector", "#hotspot input[name='tethering.wifi.enabled']")
hotspot_settings = ("css selector", "#hotspot-settings-section button[data-l10n-id=hotspotSettings]")

msg_settings = ("css selector", "[data-l10n-id='messagingSettings']")
auto_retrieve_select_btn = ("name", "ril.mms.retrieval_mode")

auto_retrieve_select_off = ("xpath", "//section[@id='value-selector-container']/ol/li[1]")
auto_retrieve_select_roaming = ("xpath", "//section[@id='value-selector-container']/ol/li[2]")
auto_retrieve_select_no_roaming = ("xpath", "//section[@id='value-selector-container']/ol/li[3]")

auto_retrieve_selected_item = ("xpath", "//section[@id='value-selector-container']/ol/li[@aria-selected='true']")

ok_btn = ("xpath", "//menu[@id='select-options-buttons']/button")
delivery_report = ("xpath", "//*[@data-l10n-id='message-delivery-reports']")

sim_security_option = ('id', 'simSecurity-settings')
sim_security = ('id', 'menuItem-simSecurity')
sim_security_tag = ('id', 'simCardLock-desc')
sim_security_header = ('xpath', GLOBAL.app_head_specific.format(_('SIM security').encode("utf8")))
sim_security_pin = ('xpath', '//li[@class="simpin-enabled simpin-enabled-0 simpin-0"]')
sim_security_change_pin = ('css selector', 'li.simpin-change button[@data-l10n-id="changeSimPin"]')
sim_security_enter_pin_header = ('xpath', GLOBAL.app_head_specific.format(_('Enter SIM PIN')))
sim_security_enter_pin_input = ('xpath', '//div[@class="sim-code-area sim-pinArea"]/input')
sim_security_enter_pin_done = ('xpath', '//section[@id="simpin-dialog"]//button[text()="{}"]'.format(_("Done")))

sim_manager_option = ('id', 'simCardManager-settings')
sim_manager_sim_security = ('id', 'sim-manager-security-entry')
sim_manager_header = ('xpath', GLOBAL.app_head_specific.format(_('SIM manager').encode("utf8")))
dual_sim_switch_pin_sim1 = ('css selector', '#simpin-container .simpin-enabled.simpin-enabled-0.simpin-0')
dual_sim_change_pin_sim1 = ('css selector', '#simpin-container .simpin-change.simpin-change-0.simpin-0')

screen_lock_menu = ('id', 'menuItem-screenLock')
passcode_lock = ('css selector', '.lockscreen-enabled')
passcode_enable = ('css selector', '.passcode-enable')
passcode_input = ('id', 'passcode-pseudo-input')
passcode_confirm = ('id', 'passcode-pseudo-confirm-input')
passcode_btn_create = ('css selector', '.passcode-create')
passcode_keyb_btn = ('css selector', '#lockscreen-passcode-pad a[data-key="{}"]')

networkOperator_button = ('css selector', '#carrier button[data-l10n-id="networkOperator"]')
networkOperator_types = ("id", "preferredNetworkType")
networkOperator_select_type = ("xpath", "//*[@id='value-selector-container']//span[text()='{}']")
networkOperator_OK_btn = ("css selector", "#select-option-popup #select-options-buttons button[data-l10n-id='ok']")

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
