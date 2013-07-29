frame_locator           = ('src', 'clock')

analog_face             = ("id", "analog-clock-svg")
digital_face            = ("id", "digital-clock-display")
new_alarm_btn           = ('id', 'alarm-new')

time_button             = ('id', "time-menu")
time_scroller           = ('xpath', "//div[@id='value-picker-%s']")
time_scroller_ampm      = ('xpath', "//div[@id='value-picker-hour24-state']")
time_picker_ok          = ("xpath", "//button[text()='OK']")
alarm_label             = ("name", "alarm.label")
alarm_done              = ('id', 'alarm-done')
alarm_delete_button     = ("id", "alarm-delete")

alarm_preview_alarms    = ('id', 'alarm-item')
alarm_preview_time      = ("class name", "time")
alarm_preview_ampm      = ("class name", "hour24-state")
alarm_preview_label     = ("class name", "label")
alarm_preview_repeat    = ("class name", "repeat")


alarm_notifier          = ('id', 'statusbar-alarm')

alarm_alert_iframe      = ("data-url", "app://clock.gaiamobile.org/onring.html")
alarm_alert_time        = ('id', 'ring-clock-time')
alarm_alert_ampm        = ('id', 'ring-clock-hour24-state')
alarm_alert_label       = ('id', 'ring-alarm-label')
alarm_alert_close       = ('id', 'ring-button-close')


