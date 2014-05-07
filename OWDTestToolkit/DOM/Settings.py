import GLOBAL
frame_locator = ('src', "settings")
settings_header = ('xpath', GLOBAL.app_head_specific.format('Settings'))
back_button = ('class name', 'icon icon-back')

call_settings = ('id', "menuItem-callSettings")
call_callerID = ('id', "menuItem-callerId")
call_log_number_xpath = ("xpath", "/html/body/div/div[5]/form/section/ol/li[2]")
call_show_number = ("xpath", "/html/body/div/div[5]/form/section/ol/li[3]")
call_button = ('xpath', "/html/body/section[20]/div/ul/li[4]/span")
call_fdn = ('xpath', '//a[@data-href="#call-fdnSettings"]')

fdn_enable = ('xpath', '//li[@id="fdn-enabled"]')
fdn_status = ('xpath', '//li[@id="fdn-enabled"]//small')
fdn_auth_numbers = ('xpath', '//a[@href="#call-fdnList"]')
fdn_pin2_input = ('xpath', '//section[@id="call-pin2-dialog"]//div[@class="sim-code-area sim-pinArea"]/input')
fdn_pin2_done = ('xpath', '//section[@id="call-pin2-dialog"]//button[@data-l10n-id="done"]')
fdn_puk2_pin2_input = ('xpath', '//section[@id="call-pin2-dialog"]//div[@class="sim-code-area sim-newPinArea"]/input')
fdn_enter_puk2_input = ('xpath', '//section[@id="call-pin2-dialog"]//div[@class="sim-code-area sim-pukArea"]/input')
fdn_confirm_pin2_input = ('xpath', '//section[@id="call-pin2-dialog"]//div[@class="sim-code-area sim-confirmPinArea"]/input')

airplane_mode_switch = ("id", "menuItem-airplaneMode")
wifi_mode_switch = ("id", "menuItem-wifi")
wifi_mode_desc = ("id", "wifi-desc")

app_permissions = ('id', "menuItem-appPermissions")
app_permissions_header = ('xpath', GLOBAL.app_head_specific.format('App permissions'))
app_perm_camera = ('xpath', './/*[@id="appPermissions"]//a[text()="Camera"]')
app_perm_camera_geo = ('xpath', './/*[@id="appPermissions-details"]//span[text()="Geolocation"]/select')

wifi = ('id', 'menuItem-wifi')
wifi_header = ('xpath', GLOBAL.app_head_specific.format('Wi-Fi'))
wifi_enabled = ('xpath', ".//*[@id='wifi-enabled']/label")
wifi_available_networks = ('xpath', "//*[@id='wifi-availableNetworks']/li/aside[contains(@class, 'pack-end wifi-icon level-')]")
wifi_network_name = ('xpath', "//*[@id='wifi-availableNetworks']/li/aside/a[text()={}]")
wifi_available_status = ".//*[@id='wifi-availableNetworks']/li[%s]//small"
wifi_available_name = ".//*[@id='wifi-availableNetworks']/li[%s]//a"
wifi_name_xpath = '//*[@id="wifi-availableNetworks"]//a[text()="{}"]'
wifi_connected = ('xpath', '//small[text()="Connected"]')
wifi_list_connected_xp = "//*[@id='wifi-availableNetworks']/li[@class='active']//a[text()='{}']"

wifi_login_header = ("xpath", "//section[@id='wifi-auth']//h1")
wifi_login_user = ('name', 'identity')
wifi_login_pass = ('xpath', '//section[@id="wifi-auth"]//input[@name="password"]')
wifi_login_ok_btn = ('xpath', "//section[@id='wifi-auth']//button[@type='submit']/span[@data-l10n-id='ok']")

wifi_details_header = ("xpath", "//section[@id='wifi-status']//h1")
wifi_details_forget_btn = ("xpath", ".//button//span[text()='Forget']")
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

cellData = ('id', 'menuItem-cellularAndData')
celldata_header = ('xpath', GLOBAL.app_head_specific.format('Cellular & Data'))
celldata_DataConn = ('name', "ril.data.enabled")
celldata_DataConn_switch = ('id', "menuItem-enableDataCall")
celldata_DataConn_ON = ('xpath', "//button[@data-l10n-id='turnOn']")
enable_data_connection = ('xpath', "//section[@id='carrier']//span[@data-l10n-id='dataConnection']/..")
enable_data_roaming = ('xpath', "//section[@id='carrier']//span[@data-l10n-id='dataRoaming']/..")
celldata_DataSettings = ('xpath', "//section[@id='carrier']//button[@data-l10n-id='dataSettings']")
celldata_MsgSettings = ('xpath', "//*[@id='carrier']//button[@data-l10n-id='messageSettings']")
custom_settings_apn = ('xpath', "//*[@id='carrier-dataSettings']//li//span[@data-l10n-id='custom']")
celldata_data_apn = ('xpath', "//*[@id='ril.data.apn']")
celldata_apn_user = ('xpath', "//*[@id='ril.data.user']")
celldata_apn_passwd = ('xpath', "//*[@id='ril.data.passwd']")
celldata_ok_button = ('xpath', "//*[@id='carrier-dataSettings']/header/menu/button/span[@data-l10n-id='ok']")
celldata_mms_ok_button = ('xpath', "//*[@id='carrier-mmsSettings']/header/menu/button/span[@data-l10n-id='ok']")
apn_settings_list = ('xpath', "//li//input[@name='defaultApn']")
selected_apn = ('css selector', 'label > input[name=defaultApn]:checked + span')
default_apn = ('xpath', "//*[@id='carrier-dataSettings']//span[text()='{}']/..")
default_apn_mms = ('xpath', "//*[@id='carrier-mmsSettings']//span[text()='{}']/..")
selected_apn_mms = ('css selector', 'label > input[name=mmsApn]:checked + span')
mms_second = ('xpath', "/html/body/section[24]/div/ul/li[2]/label")
apn_sixth = ('xpath', "/html/body/section[23]/div/ul/li[6]/label")
data_settings_back_btn = ('xpath', '//section[@id="carrier-dataSettings"]//button/span[@data-l10n-id="back"]')
mms_settings_back_btn = ('xpath', '//section[@id="carrier-mmsSettings"]//button/span[@data-l10n-id="back"]')

bluetooth = ("id", "menuItem-bluetooth")
bluetooth_desc = ("id", "bluetooth-desc")

sound = ('id', 'menuItem-sound')
sound_alarm_vol = ('name', 'audio.volume.alarm')

hotspot = ("id", "menuItem-internetSharing")
hotspot_header = ('xpath', GLOBAL.app_head_specific.format('Internet sharing'))
hotspot_switch = ("xpath", "/html/body/section[32]/div/ul/li/label")
hotspot_settings = ("xpath", "/html/body/section[32]/div/ul/li[6]/label/button")

msg_settings = ("xpath", "//*[@data-l10n-id='messagingSettings']")
auto_retrieve_select_btn = ("name", "ril.mms.retrieval_mode")

auto_retrieve_select_off = ("xpath", "//section[@id='value-selector-container']/ol/li[1]")
auto_retrieve_select_roaming = ("xpath", "//section[@id='value-selector-container']/ol/li[2]")
auto_retrieve_select_no_roaming = ("xpath", "//section[@id='value-selector-container']/ol/li[3]")

auto_retrieve_selected_item = ("xpath", "//section[@id='value-selector-container']/ol/li[@aria-selected='true']")

ok_btn = ("xpath", "//menu[@id='select-options-buttons']/button")
delivery_report = ("xpath", "//*[@data-l10n-id='message-delivery-reports']")

sim_security = ('id', 'menuItem-simSecurity')
sim_security_tag = ('id', 'simCardLock-desc')
sim_security_header = ('xpath', GLOBAL.app_head_specific.format('SIM security'))
sim_security_pin = ('xpath', '//li[@class="simpin-enabled simpin-enabled-0 simpin-0"]')
sim_security_change_pin = ('xpath', '//li[@class="simpin-change simpin-change-0 simpin-0"]//button[@data-l10n-id="changeSimPin"]')
sim_security_enter_pin_header = ('xpath', GLOBAL.app_head_specific.format('Enter SIM PIN'))
sim_security_enter_pin_input = ('xpath', '//div[@class="sim-code-area sim-pinArea"]/input')
sim_security_enter_pin_done = ('xpath', '//section[@id="simpin-dialog"]//button[text()="Done"]')

networkOperator_button = ("xpath", "/html/body/section[29]/div/ul[3]/li/label/button")
networkOperator_types = ("id", "preferredNetworkType")
networkOperator_GSM = ("xpath", "/html/body/div/div[5]/form/section/ol/li[2]/label/span")
networkOperator_CDMA = ("xpath", "/html/body/div/div[5]/form/section/ol/li[6]/label/span")
networkOperator_EVDO = ("xpath", "/html/body/div/div[5]/form/section/ol/li[7]/label/span")
networkOperator_Auto = ("xpath", "/html/body/div/div[5]/form/section/ol/li[8]/label/span")
networkOperator_WCDMA = ("xpath", "/html/body/div/div[5]/form/section/ol/li[3]/label/span")
networkOperator_PrefWCDMA = ("xpath", "/html/body/div/div[5]/form/section/ol/li/label/span")
networkOperator_PrefGSM = ("xpath", "/html/body/div/div[5]/form/section/ol/li[4]/label/span")
networkOperator_PrefEVDO = ("xpath", "/html/body/div/div[5]/form/section/ol/li[5]/label/span")
networkOperator_OK_btn = ("xpath", "/html/body/div/div[5]/form/menu/button")

change_pin_done_btn = ('xpath', '//section[@id="simpin-dialog"]//button[@data-l10n-id="done"]')
change_pin_old_input = ('xpath', '//section[@id="simpin-dialog"]//div[@class="pin-dialog"]//div[@class="sim-code-area sim-pinArea"]/input')
change_pin_new_input = ('xpath', '//section[@id="simpin-dialog"]//div[@class="pin-dialog"]//div[@class="sim-code-area sim-newPinArea"]/input')
change_pin_confirm_input = ('xpath', '//section[@id="simpin-dialog"]//div[@class="pin-dialog"]//div[@class="sim-code-area sim-confirmPinArea"]/input')
change_pin_error = ('xpath', '//section[@id="simpin-dialog"]//div[@class="sim-errorMsg error"]//div[@class="sim-messageHeader"]')