import GLOBAL
frame_locator          = ('src', 'app://settings.gaiamobile.org/index.html#root')
settings_header        = ('xpath', GLOBAL.app_head_specific % 'Settings')
back_button            = ('class name', 'icon icon-back')

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
wifi_login_user        = ('name', 'identity')
wifi_login_pass        = ('name', 'password')
wifi_login_ok_btn      = ('xpath', ".//button//span[text()='OK']")
wifi_connected         = ('xpath', '//small[text()="Connected"]')

cellData               = ('id', 'menuItem-cellularAndData')
celldata_header        = ('xpath', GLOBAL.app_head_specific % 'Cellular & Data')
celldata_DataConn      = ('name', "ril.data.enabled")

celldata_DataConn_ON   = ('xpath', "//button[@data-l10n-id='turnOn']")

sound                  = ('id', 'menuItem-sound')
sound_alarm_vol        = ('name', 'audio.volume.alarm')
