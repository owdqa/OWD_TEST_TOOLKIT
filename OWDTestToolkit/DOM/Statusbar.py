status_bar_new  = ('xpath', "//*[@id='statusbar-notification'][@data-unread='true']")
wifi            = ('id', 'statusbar-wifi')
dataConn        = ('css selector', '#statusbar-connections .statusbar-data')
bluetooth       = ('id', 'statusbar-bluetooth')
airplane        = ('id', 'statusbar-flight-mode')
signal          = ("xpath", "/html/body/div/div/div[8]/div")
hotspot         = ("id", "statusbar-tethering")
network_activity= ("id", "statusbar-network-activity")

clear_all_button= ('id', 'notification-clear')
toggle_wifi     = ("id", "quick-settings-wifi")
toggle_dataconn = ("id", "quick-settings-data")
toggle_bluetooth= ("id", "quick-settings-bluetooth")
toggle_airplane = ("id", "quick-settings-airplane-mode")

settings_button = ("id", "quick-settings-full-app")

notification_toaster_detail = ("xpath", "//div[@id='toaster-detail' and contains(text(),'{}')]")
notification_toaster_title = ("xpath", "//div[@id='toaster-title' and contains(text(),'{}')]")
notification_statusbar_title = ('xpath', '//div[@id="desktop-notifications-container"]/div[@class="notification"]/div[contains(text(),"{}")]')
notification_statusbar_detail = ('xpath', '//div[@id="desktop-notifications-container"]/div[@class="notification"]/div[@class="detail" and contains(text(),"{}")]')