from OWDTestToolkit.utils.i18nsetup import I18nSetup
_ = I18nSetup(I18nSetup).setup()

frame_locator = ('src', 'dialer')
frame_locator_calling = ('name', 'call_screen')

message_callerID = ('id', 'message')

option_bar_call_log = ("id", "option-recents")
option_bar_contacts = ("id", "option-contacts")
option_bar_keypad = ("id", "option-keypad")

keypad = ("id", "keypad")
dialer_button_xpath = "//section[@id='keypad']//div[contains(@class,'keypad-key') and @data-value='{}']"
phone_number_area = ("id", "fake-phone-number-view")
# Beware: this number may have a country code prefix on it.
phone_number = ('id', 'phone-number-view')

contacts_sub_iframe = ("id", "iframe-contacts")

add_to_contacts_button = ("id", "keypad-callbar-add-contact")
create_new_contact_btn = ("css selector", "button[data-l10n-id=createNewContact]")
add_to_existing_contact_btn = ("css selector", "button[data-l10n-id=addToExistingContact]")
call_number_button = ("id", "keypad-callbar-call-action")
keypad_delete = ("id", "keypad-delete")

add_to_conts_cancel_btn = ("id", "cancel_activity")

suggestion_overlay = ('id', 'suggestion-overlay')
suggestion_count = ("id", "suggestion-count")
# When only a single suggestion is displayed, we have a div instead a button
suggestion_item_single = ('xpath', '//div[@class="js-suggestion-item suggestion-item"]')
suggestion_item = ('xpath', '//button[@class="js-suggestion-item suggestion-item si--action-menu"]')
suggestion_item_name = ('xpath', '//button[@class="js-suggestion-item suggestion-item si--action-menu"]//div[@class="js-name si__name ellipsis"]')
suggestion_list = ('id', 'suggestion-list')
suggestion_list_cancel = ("id", "suggestion-overlay-cancel")

outgoing_call_locator = ("xpath", '//*[@id="calls"]//section[contains(@class, "outgoing")]')
outgoing_call_number = ("xpath", '//*[@id="calls"]//section[contains(@class, "outgoing")]//div[contains(@class, "numberWrapper")]/div[contains(@class, "number font-light")]')  # Note: maybe + prefix.
outgoing_call_numberXP = "//*[contains(@class, 'number font-light') and contains(text(), '{}')]"  # Note: maybe + prefix.
hangup_bar_locator = ('id', 'callbar-hang-up')
answer_callButton = ("id", 'callbar-answer')

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
call_log_missed = ('id', 'missed-filter')
call_log_missed_number_xpath = '//a[contains(@id, "{}")]//aside[contains(@class, "icon-missed")]'

call_log_numtap_send_msg = ("id", "send-sms-menuitem")
call_log_numtap_create_new = ("id", "create-new-contact-menuitem")
call_log_numtap_add_to_existing = ("id", "add-to-existing-contact-menuitem")
call_log_numtap_cancel = ("id", "cancel-action-menu")

call_log_contact_name_iframe = ("id", "iframe-contacts")
call_log_number_cont_highlight = "//button[contains(@id, 'call-or-pick') and @class='activity icon icon-call remark' and contains(@data-tel, '{}')]"

call_busy_button_ok = ("css selector", "#confirmation-message menu button.full")

imei_header = ('xpath', '//h1[text()="IMEI"]')
imei_contents = ('css selector', '#mmi-screen #mmi-container #message')

mmi_send_btn = ('id', 'send')

fdn_warning_msg = _('FDN (Fixed Dialing Numbers) is activated and the following number is not in your FDN list: {}')
