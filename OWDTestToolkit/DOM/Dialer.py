frame_locator          = ('src', 'dialer')
frame_locator_calling  = ('name', 'call_screen')

option_bar_call_log    = ("id", "option-recents")
option_bar_contacts    = ("id", "option-contacts")
option_bar_keypad      = ("id", "option-keypad")

phone_number           = ('id', 'phone-number-view') # Beware: this number may have a country code prefix on it.

add_to_contacts_button      = ("id", "keypad-callbar-add-contact")
create_new_contact_btn      = ("id", "create-new-contact-menuitem")
add_to_existing_contact_btn = ("id", "add-to-existing-contact-menuitem")
call_number_button          = ("id", "keypad-callbar-call-action")

add_to_conts_cancel_btn= ("id", "cancel_activity")

outgoing_call_locator  = ('css selector', 'div.direction.outgoing')
outgoing_call_number   = ("xpath", "//*[contains(@class,'number font-light')]") #Note: maybe + prefix.
outgoing_call_numberXP = "//*[contains(@class, 'number font-light') and contains(text(), '%s')]" #Note: maybe + prefix.
hangup_bar_locator     = ('id', 'callbar-hang-up-action')

dialler_button_xpath   = "//div[@class='keypad-key' and @data-value='%s']"
phone_number_area      = ("id", "fake-phone-number-view")

call_log_btn           = ("id", "option-recents")
call_log_filter        = ("id", "call-log-filter")
call_log_numbers       = ("xpath", "//li[contains(@class,'log-item')")
call_log_number_xpath  = "//li[contains(@class,'log-item') and contains(@data-phone-number,'%s')]"
call_log_edit_btn      = ("id", "call-log-icon-edit")

call_log_numtap_call            = ("id", "call-menuitem")
call_log_numtap_create_new      = ("id", "create-new-contact-menuitem")
call_log_numtap_add_to_existing = ("id", "add-to-existing-contact-menuitem")
call_log_numtap_cancel          = ("id", "cancel-action-menu")

call_log_contact_name_iframe    = ("id", "iframe-contacts")
call_log_number_cont_highlight  = "//button[contains(@id, 'call-or-pick') and @class='activity icon icon-call remark' and contains(@data-tel, '%s')]"