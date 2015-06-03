from OWDTestToolkit.utils.i18nsetup import I18nSetup
_ = I18nSetup(I18nSetup).setup()


frame_locator = ('src', 'clock')

analog_face = ('id', 'analog-clock-face')
digital_face = ('id', 'digital-clock-face')
new_alarm_btn = ('id', 'alarm-new')

time_button = ('css selector', '#edit-alarm #time-select ~ button')
time_scroller = ('css selector', '.value-picker-{}-wrapper')
time_scroller_ampm = ('css selector', '.value-picker-hour24-state')
time_picker_ok = ("css selector", "#time-picker-buttons button[data-l10n-id=ok]")
alarm_label = ("name", "alarm.label")
alarm_done = ('id', 'alarm-done')
alarm_delete_button = ("id", "alarm-delete")

edit_alarm_repeat_menu = ('id', 'repeat-menu')
edit_alarm_repeat = ('id', 'repeat-select')
edit_alarm_selector_xpath = "//section[@id='value-selector-container']//span[text()='{}']"
edit_alarm_repeat_ok = ('css selector', '#select-options-buttons button[data-l10n-id=ok]')
edit_alarm_sound_menu = ('id', 'sound-menu')
edit_alarm_sound = ('id', 'sound-select')
edit_alarm_snooze_menu = ('id', 'snooze-menu')
edit_alarm_snooze = ('id', 'snooze-select')

alarm_preview_alarms = ('class name', 'alarm-item')
alarm_preview_time = ("class name", "time")
alarm_preview_ampm = ("css selector", ".time small")
alarm_preview_label = ("class name", "label")
alarm_preview_repeat = ("class name", "repeat")

alarm_notifier = ('id', 'statusbar-alarm')

alarm_alert_iframe = ("data-url", "app://clock.gaiamobile.org/onring.html")
alarm_alert_time = ('id', 'ring-clock-time')
alarm_alert_ampm = ('id', 'ring-clock-hour24-state')
alarm_alert_label = ('id', 'ring-alarm-label')
alarm_alert_close = ('id', 'ring-button-close')
alarm_button_stop = ('id', 'ring-button-stop')
alarm_button_snooze = ('id', 'ring-button-snooze')
alarm_attention_screen = ('css selector', 'iframe.active[data-frame-type=attention]')
