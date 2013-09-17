loading_overlay      = ('id', 'loading-overlay')
app_head_specific    = "//h1[text()='%s']"
app_head             = ('tag name', "h1")
app_titlebar_name    = ('class name', 'titlebarIcon')
modal_confirm_ok     = ("id", "modal-dialog-confirm-ok")
modal_alert_ok       = ("id", "modal-dialog-alert-ok")
modal_alert_msg      = ("id", "modal-dialog-alert-message")
modal_valueSel_ok    = ('css selector', 'button.value-option-confirm')
modal_valueSel_list  = ("xpath", "//section[@id='value-selector-container']//li")
# conf_screen_ok_button = ("class name","value-option-confirm affirmative full")
conf_screen_ok_button = ('xpath', '//button[@class="value-option-confirm affirmative full"]')

scroller_curr_val    = ("class name", "picker-unit active")
