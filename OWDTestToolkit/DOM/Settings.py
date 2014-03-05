import GLOBAL
frame_locator          = ('src', "settings")
settings_header        = ('xpath', GLOBAL.app_head_specific.format('Settings'))
back_button            = ('class name', 'icon icon-back')

call_settings = ('id', "menuItem-callSettings")
call_callerID = ('id', "menuItem-callerId")
call_log_number_xpath = ("xpath", "/html/body/div/div[5]/form/section/ol/li[2]")
call_show_number = ("xpath", "/html/body/div/div[5]/form/section/ol/li[3]")
call_button = ('xpath',"/html/body/section[20]/div/ul/li[4]/span")


airplane_mode_switch   = ("id", "menuItem-airplaneMode")
wifi_mode_switch       = ("id", "menuItem-wifi")
wifi_mode_desc         = ("id", "wifi-desc")

app_permissions        = ('id', "menuItem-appPermissions")
app_permissions_header = ('xpath', GLOBAL.app_head_specific.format('App permissions'))
app_perm_camera        = ('xpath', './/*[@id="appPermissions"]//a[text()="Camera"]')
app_perm_camera_geo    = ('xpath', './/*[@id="appPermissions-details"]//span[text()="Geolocation"]/select') 

wifi                   = ('id', 'menuItem-wifi')
wifi_header            = ('xpath', GLOBAL.app_head_specific.format('Wi-Fi'))
wifi_enabled           = ('xpath', ".//*[@id='wifi-enabled']/label")
wifi_available_networks= ('xpath', ".//*[@id='wifi-availableNetworks']/li")
wifi_available_status  = ".//*[@id='wifi-availableNetworks']/li[%s]//small"
wifi_available_name    = ".//*[@id='wifi-availableNetworks']/li[%s]//a"
wifi_name_xpath        = './/*[@id="wifi-availableNetworks"]//a[text()="%s"]'
wifi_connected         = ('xpath', '//small[text()="Connected"]')
wifi_list_connected_xp = "//*[@id='wifi-availableNetworks']/li[@class='active']//a[text()='%s']"

wifi_login_header      = ("xpath", "//section[@id='wifi-auth']//h1")
wifi_login_user        = ('name', 'identity')
wifi_login_pass        = ('name', 'password')
wifi_login_ok_btn      = ('xpath', ".//button//span[text()='OK']")

wifi_details_header     = ("xpath", "//section[@id='wifi-status']//h1")
wifi_details_forget_btn = ("xpath", ".//button//span[text()='Forget']")
wifi_details_security   = ("xpath", "//a[@data-l10n-id='security']/span")
wifi_details_signal     = ("xpath", "//a[@data-l10n-id='signalStrength']/span")
wifi_details_ipaddress  = ("xpath", "//a[@data-l10n-id='ipAddress']/span")
wifi_details_linkspeed  = ("xpath", "//a[@data-l10n-id='linkSpeed']/span")

wifi_advanced_btn       = ("id", "manageNetworks")
wifi_advanced_mac       = ("xpath", "//small[@data-name='deviceinfo.mac']")
wifi_advanced_knownNets = ("xpath", "//*[@id='wifi-knownNetworks']/li")
wifi_advanced_joinHidden= ("id", "joinHidden")
wifi_advanced_forgetBtn = ("xpath", "//*[@id='confirm-option']")
wifi_advanced_cancelBtn = ("xpath", "//button[@data-l10n-id='cancel']")

cellData               = ('id', 'menuItem-cellularAndData')
celldata_header        = ('xpath', GLOBAL.app_head_specific.format('Cellular & Data'))
celldata_DataConn      = ('name', "ril.data.enabled")
celldata_DataConn_ON   = ('xpath', "//button[@data-l10n-id='turnOn']")

bluetooth              = ("id", "menuItem-bluetooth")
bluetooth_desc         = ("id", "bluetooth-desc")

sound                  = ('id', 'menuItem-sound')
sound_alarm_vol        = ('name', 'audio.volume.alarm')

hotspot                 = ("id", "menuItem-internetSharing")
hotspot_header          = ('xpath', GLOBAL.app_head_specific.format('Internet sharing'))
hotspot_switch          = ("xpath", "/html/body/section[32]/div/ul/li/label")
hotspot_settings        = ("xpath", "/html/body/section[32]/div/ul/li[6]/label/button")

msg_settings             = ("xpath", "//*[@data-l10n-id='messagingSettings']")
auto_retrieve_select_btn     = ("name","ril.mms.retrieval_mode")

auto_retrieve_select_off           = ("xpath", "//section[@id='value-selector-container']/ol/li[1]")
auto_retrieve_select_roaming       = ("xpath", "//section[@id='value-selector-container']/ol/li[2]")
auto_retrieve_select_no_roaming    = ("xpath", "//section[@id='value-selector-container']/ol/li[3]")

auto_retrieve_selected_item    = ("xpath", "//section[@id='value-selector-container']/ol/li[@aria-selected='true']")

ok_btn             = ("xpath", "//menu[@id='select-options-buttons']/button")



