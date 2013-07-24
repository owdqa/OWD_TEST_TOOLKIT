frame_locator          = ('src', 'dialer')
frame_locator_calling  = ('name', 'call_screen0')


# Beware: this number may have a country code prefix on it.
phone_number           = ('id', 'phone-number-view')

add_to_contacts_button = ("id", "keypad-callbar-add-contact")
create_new_contact_btn = ("id", "create-new-contact-menuitem")
call_number_button     = ("id", "keypad-callbar-call-action")

outgoing_call_locator  = ('css selector', 'div.direction.outgoing')
outgoing_call_number   = ("class name", "number font-light noAdditionalContactInfo")
hangup_bar_locator     = ('id', 'callbar-hang-up-action')

dialler_button_xpath   = "//div[@class='keypad-key' and @data-value='%s']"
phone_number_area      = ("id", "fake-phone-number-view")

call_log_btn           = ("id", "option-recents")
call_log_filter        = ("id", "call-log-filter")
call_log_numbers       = ("class name", "log-item")
call_log_number_xpath  = "//li[@class='log-item' and @data-phone-number='%s']"

call_log_numtap_call            = ("id", "call-menuitem")
call_log_numtap_create_new      = ("id", "create-new-contact-menuitem")
call_log_numtap_add_to_existing = ("id", "add-to-existing-contact-menuitem")
call_log_numtap_cancel          = ("id", "cancel-action-menu")

