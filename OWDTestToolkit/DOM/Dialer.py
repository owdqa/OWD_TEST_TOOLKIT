frame_locator = ('src', 'dialer')
frame_locator_calling = ('name', 'call_screen')

message_calleID = ("xpath", "/html/body/article/section[2]/div")
button_calleID = ('xpath', "/html/body/div/div[5]/form/menu/button")

option_bar_call_log = ("id", "option-recents")
option_bar_contacts = ("id", "option-contacts")
option_bar_keypad = ("id", "option-keypad")

keypad = ("id", "keypad")
dialer_button_xpath = "//section[@id='keypad']//div[contains(@class,'keypad-key') and @data-value='{}']"
dialer_button_1 = ("xpath", "/html/body/section/article[3]/div/article/section/div/div")
phone_number_area = ("id", "fake-phone-number-view")
# Beware: this number may have a country code prefix on it.
phone_number = ('id', 'phone-number-view')

contacts_sub_iframe = ("id", "iframe-contacts")

add_to_contacts_button = ("id", "keypad-callbar-add-contact")
create_new_contact_btn = ("id", "create-new-contact-menuitem")
add_to_existing_contact_btn = ("id", "add-to-existing-contact-menuitem")
call_number_button = ("id", "keypad-callbar-call-action")
keypad_delete = ("id", "keypad-delete")

add_to_conts_cancel_btn = ("id", "cancel_activity")

suggestion_count = ("id", "suggestion-count")
suggestion_item = ("class name", "suggestion-item")
suggestion_item_name = ('css selector', '#suggestion-bar .js-name.si__name.ellipsis')
suggestion_list = ("xpath", "//ul[@id='suggestion-list']/li")
suggestion_list_cancel = ("id", "suggestion-overlay-cancel")

outgoing_call_locator = ("xpath", '//*[@id="calls"]//section[contains(@class, "outgoing")]')
outgoing_call_number = ("xpath", '//*[@id="calls"]//section[contains(@class, "outgoing")]//div[contains(@class, "numberWrapper")]/div[contains(@class, "number font-light")]') #Note: maybe + prefix.
outgoing_call_numberXP = "//*[contains(@class, 'number font-light') and contains(text(), '{}')]" #Note: maybe + prefix.
hangup_bar_locator = ('id', 'callbar-hang-up')
answer_callButton = ("xpath", "//*[@id='callbar-answer']")

call_log_btn = ("id", "option-recents")
call_log_filter = ("id", "call-log-filter")
call_log_numbers = ("xpath", "//li[contains(@class,'log-item')]")
call_log_number_xpath = "//li[contains(@class,'log-item') and contains(@data-phone-number,'{}')]"
call_log_name_xpath = "//li[contains(@class,'log-item')]//span[@class='primary-info-main' and text()='{}']"
call_log_edit_btn = ("id", "call-log-icon-edit")
call_log_edit_header = ("id", "edit-mode-header")
call_log_edit_selAll = ("id", "select-all-threads")
call_log_edit_delete = ("id", "delete-button")
call_log_no_calls_msg = ("id", "no-result-message")
call_log_delete_btn = ("id", "delete-button")
call_log_confirm_delete = ('xpath', '//form[@id="confirmation-message"]/menu/button[@class="danger"]')

call_log_numtap_call = ("id", "call-menuitem")
call_log_numtap_create_new = ("id", "create-new-contact-menuitem")
call_log_numtap_add_to_existing = ("id", "add-to-existing-contact-menuitem")
call_log_numtap_cancel = ("id", "cancel-action-menu")

call_log_contact_name_iframe = ("id", "iframe-contacts")
call_log_number_cont_highlight = "//button[contains(@id, 'call-or-pick') and @class='activity icon icon-call remark' and contains(@data-tel, '{}')]"

call_busy_button_ok = ("xpath", '//form[@id="confirmation-message"]/menu/button[@class="full"]')
number_busy_windows_ok_button = ("xpath", "//form[@id='confirmation-message']/menu/button[@class='full']")