loading_overlay      = ('id', 'loading-overlay')
app_head_specific    = "//h1[text()='{}']"
app_head             = ('tag name', "h1")
app_titlebar_name    = ('class name', 'titlebarIcon')
modal_confirm_ok     = ("xpath", "//*[@id='confirm-ok']")
modal_confirm_ok2    = ("xpath", "/html/body/div/div[3]/div[2]/div[3]/form[2]/menu/button[2]")
modal_alert_ok       = ("id", "modal-dialog-alert-ok")
modal_alert_ok2      = ("xpath", "//*[@id='modal-dialog-confirm-ok']")
modal_alert_ok3      = ("xpath", "/html/body/div/div[3]/div/div[3]/form[2]/menu/button[2]")
modal_alert_msg      = ("id", "modal-dialog-alert-message")
modal_alert_msg2     = ("xpath", "//*[@id='modal-dialog-confirm-message']")
modal_alert_msg3     = ("xpath", "/html/body/div/div[3]/div/div[3]/form/div/p/span")
modal_valueSel_ok    = ('css selector', 'button.value-option-confirm')
modal_valueSel_list  = ("xpath", "//section[@id='value-selector-container']//li")
# conf_screen_ok_button = ("class name","value-option-confirm affirmative full")
conf_screen_ok_button = ('xpath', '//button[@class="value-option-confirm affirmative full"]')

scroller_curr_val    = ("class name", "picker-unit active")
pin_input = ("css selector", "#dialog-overlay #simpin-dialog .container #pinArea .input-wrapper input")
pin_ok_button = ("xpath", '//div[@id="dialog-overlay"]//button[@data-l10n-id="ok"]')
pin_skip_button = ("xpath", "//div[@id='simpin-dialog']//button[@data-l10n-id='skip']")
lockscreen_network_locator = ('xpath', '//div[@id="lockscreen-header"]//span[@class="connstate-line"]')