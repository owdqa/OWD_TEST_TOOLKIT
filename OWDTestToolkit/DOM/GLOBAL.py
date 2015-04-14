loading_overlay = ('id', 'loading-overlay')
app_head_specific = "//h1[text()='{}']"
app_head = ('tag name', "h1")
app_titlebar_name = ('class name', 'titlebarIcon')
modal_confirm_ok = ("id", "confirm-ok")
modal_alert_ok = ("id", "modal-dialog-alert-ok")
modal_alert_ok2 = ("id", "modal-dialog-confirm-ok")
modal_alert_msg2 = ("id", "modal-dialog-confirm-message")
modal_valueSel_ok = ('css selector', 'button.value-option-confirm')
modal_valueSel_list = ("css selector", "#value-selector-container li")
modal_valueSel_option = ('xpath', '//section[@id="value-selector-container"]//li//span[text()="{}"]')
modal_valueSel_option_selected = ('xpath', '//section[@id="value-selector-container"]//li//span[text()="{}"]/ancestor::li')
conf_screen_ok_button = ('css selector', 'button.value-option-confirm.affirmative.full')

scroller_curr_val = ("css selector", ".picker-unit.selected")
pin_input = ("css selector", "#dialog-overlay #simpin-dialog .container #pinArea .input-wrapper input")
pin_ok_button = ("xpath", '//div[@id="simpin-dialog"]//button[@data-l10n-id="ok"]')
pin_skip_button = ("xpath", "//div[@id='simpin-dialog']//button[@data-l10n-id='skip']")
lockscreen_network_locator = ('xpath', '//div[@id="lockscreen-conn-states"]//span[@class="connstate-line"]')

puk_puk_input = ('xpath', '//div[@id="pukArea"]//input')
puk_new_pin_input = ('xpath', '//div[@id="newPinArea"]//input')
puk_confirm_pin_input = ('xpath', '//div[@id="confirmPinArea"]//input')
puk_ok_btn = ('xpath', '//div[@id="simpin-dialog"]//button[@data-l10n-id="ok"]')

confirmation_msg_header = ('xpath', '//form[@id="confirmation-message"]//h1[contains(text(), "{}")]')
confirmation_msg_content = ('xpath', '//form[@id="confirmation-message"]//p[contains(text(), "{}")]')
confirmation_msg_ok_btn = ('xpath', '//form[@id="confirmation-message"]//button[@class="full"]')

confirm_form_delete_btn = ('css selector', 'form[data-type=confirm] button.danger')

# Action menu
action_menu = ('xpath', '//form[@data-type="action" and @data-z-index-level="action-menu"]/menu')
action_menu_option = (
    'xpath', u'//form[@data-type="action" and @data-z-index-level="action-menu"]//button[text()="{}"]')
action_menu_cancel_btn = (
    'xpath', '//form[@data-type="action" and @data-z-index-level="action-menu"]//button[@data-l10n-id="cancel" and @data-action="cancel"]')

# Modal dialogs
modal_dialog = ('css selector', 'form.modal-dialog-alert')
modal_dialog_alert_title = ("css selector", 'form.modal-dialog-alert h3.modal-dialog-alert-title')
modal_dialog_alert_msg = ("css selector", 'form.modal-dialog-alert span.modal-dialog-alert-message')
modal_dialog_alert_ok = ("css selector", 'form.modal-dialog-alert button.modal-dialog-alert-ok')

# App permision (top-frame)
app_permission_dialog = ('id', 'permission-dialog')
app_permission_msg = ('id', 'permission-message')
app_permission_btn_yes = ('id', 'permission-yes')
app_permission_btn_no = ('id', 'permission-no')

# App install dialog
app_install_ok = ('id', 'app-install-install-button')
app_install_cancel = ('id', 'app-install-cancel-button')

# Bottom toaster
system_banner = ('xpath', '//section[@data-z-index-level="system-notification-banner"]')
system_banner_msg = ('xpath', '//section[@data-z-index-level="system-notification-banner"]//p[contains(text(), "{}")]')

charge_warning = ('css selector', '#charge-warning.visible')
charge_warning_ok_btn = ('id', 'charge-warning-ok')

# Frame
frame_containing = ("xpath", "//iframe[contains({},'{}')]")

# Battery
battery_icon = ('id', 'statusbar-battery')

#Sleep menu
sleep_menu = ('id', 'sleep-menu')
sleep_menu_airplane_mode = ('css selector', '#sleep-menu li[data-value="airplane"]')
sleep_menu_silent_off = ('css selector', '#sleep-menu li[data-value="silentOff"]')
sleep_menu_restart = ('css selector', '#sleep-menu li[data-value="restart"]')
sleep_menu_power = ('css selector', '#sleep-menu li[data-value="power"]')
sleep_menu_cancel = ('css selector', '#sleep-menu button[data-l10n-id="cancel"]')
