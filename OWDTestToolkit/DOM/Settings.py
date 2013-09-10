import GLOBAL
frame_locator          = ('src', "settings")
settings_header        = ('xpath', GLOBAL.app_head_specific % 'Settings')
back_button            = ('class name', 'icon icon-back')

airplane_mode_switch   = ("id", "menuItem-airplaneMode")
wifi_mode_switch       = ("id", "menuItem-wifi")
wifi_mode_desc         = ("id", "wifi-desc")

app_permissions        = ('id', "menuItem-appPermissions")
app_permissions_header = ('xpath', GLOBAL.app_head_specific % 'App permissions')
app_perm_camera        = ('xpath', './/*[@id="appPermissions"]//a[text()="Camera"]')
app_perm_camera_geo    = ('xpath', './/*[@id="appPermissions-details"]//span[text()="Geolocation"]/select') 

wifi                   = ('id', 'menuItem-wifi')
wifi_header            = ('xpath', GLOBAL.app_head_specific % 'Wi-Fi')
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

cellData               = ('id', 'menuItem-cellularAndData')
celldata_header        = ('xpath', GLOBAL.app_head_specific % 'Cellular & Data')
celldata_DataConn      = ('name', "ril.data.enabled")
celldata_DataConn_ON   = ('xpath', "//button[@data-l10n-id='turnOn']")

bluetooth              = ("id", "menuItem-bluetooth")
bluetooth_desc         = ("id", "bluetooth-desc")

sound                  = ('id', 'menuItem-sound')
sound_alarm_vol        = ('name', 'audio.volume.alarm')

hotspot                 = ("id", "menuItem-internetSharing")
hotspot_header          = ('xpath', GLOBAL.app_head_specific % 'Internet sharing')
hotspot_switch          = ("xpath", "//a[@data-l10n-id='wifi-hotspot']")
hotspot_settings        = ("xpath", "//button[@class='hotspot-wifiSettings-btn']")
