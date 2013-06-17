loading_overlay      = ('id', 'loading-overlay')
app_head_specific    = "//h1[text()='%s']"
app_head             = ('tag name', "h1")
app_titlebar_name    = ('class name', 'titlebarIcon')
keyboard_iframe      = ("src", "app://keyboard.gaiamobile.org/index.html")
# modal_ok_button      = ("id", "modal-dialog-confirm-ok")
modal_ok_button      = ("id", "modal-dialog-alert-ok")
# conf_screen_ok_button = ("class name","value-option-confirm affirmative full")
conf_screen_ok_button = ('xpath', '//button[@class="value-option-confirm affirmative full"]')

scroller_curr_val    = ("class name", "picker-unit active")
