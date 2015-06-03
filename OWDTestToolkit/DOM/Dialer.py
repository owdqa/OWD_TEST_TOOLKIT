from OWDTestToolkit.utils.i18nsetup import I18nSetup
_ = I18nSetup(I18nSetup).setup()

frame_locator = ('src', 'dialer')
frame_locator_calling = ('name', 'call_screen')
call_screen_locator = ("css selector", "div.callscreenWindow.active")
call_screen_frame_locator = ('css selector', 'div.callscreenWindow.active iframe')

# Main options
option_bar_call_log = ("id", "option-recents")
option_bar_contacts = ("id", "option-contacts")
option_bar_keypad = ("id", "option-keypad")

# Keypad
keypad = ("id", "keypad")
dialer_button_xpath = "//section[@id='keypad']//div[contains(@class,'keypad-key') and @data-value='{}']"
phone_number = ('id', 'phone-number-view')

# Actions
add_to_contacts_button = ("id", "keypad-callbar-add-contact")
create_new_contact_btn = ("css selector", "button[data-l10n-id=createNewContact]")
add_to_existing_contact_btn = ("css selector", "button[data-l10n-id=addToExistingContact]")
cancel_action = ("css selector", 'form[tabindex="-1"] button[data-l10n-id=cancel]')
call_number_button = ("id", "keypad-callbar-call-action")
keypad_delete = ("id", "keypad-delete")
add_to_conts_cancel_btn = ("id", "cancel_activity")

# Suggestions
suggestion_overlay = ('id', 'contact-list-overlay')
suggestion_count = ("id", "suggestion-count")
# When only a single suggestion is displayed, we have a div instead a button
suggestion_item_single = ('css selector', 'div.js-suggestion-item.contact-item')
suggestion_item = ('css selector', 'button.js-suggestion-item.contact-item.ci--action-menu')
suggestion_item_name = ('css selector', 'button.js-suggestion-item.contact-item.ci--action-menu div.js-name.ci__name.ellipsis')
suggestion_list = ('id', 'contact-list')
suggestion_list_cancel = ("id", "contact-list-overlay-cancel")

# Call in progress
outgoing_call_locator = ("css selector", '#calls .outgoing')
outgoing_call_number = ("css selector", '#calls .outgoing .number.font-light')
outgoing_call_numberXP = "//*[contains(@class, 'number font-light') and contains(text(), '{}')]"
hangup_bar_locator = ('id', 'callbar-hang-up')
answer_callButton = ("id", 'callbar-answer')

# Call log
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
call_log_missed_number = ('css selector', 'li.log-item.missed-call[data-phone-number="{}"]')
call_log_numtap_send_msg = ("css selector", "form.call-group-menu button[data-l10n-id=sendSms]")
call_log_numtap_call_info = ("css selector", "form.call-group-menu button[data-l10n-id=callInformation]")
call_log_numtap_create_new = ("id", "call-info-create")
call_log_numtap_add_to_existing = ("id", "call-info-add")
call_log_numtap_cancel = ("css selector", "form.call-group-menu button[data-l10n-id=cancel]")
call_log_contact_name_iframe = ("id", "iframe-contacts")
call_log_number_cont_highlight = "//button[contains(@id, 'call-or-pick') and @class='activity icon icon-call remark' and contains(@data-tel, '{}')]"

# Call log call info
call_info_title = ('id', 'call-info-title')
call_info_calls = ('id', 'ci__calls-wrapper')
call_info_contact = ('id', 'ci__contact-wrapper')
call_info_contact_go_to_contact_details = ('id', 'call-info-details')

# Others
call_busy_button_ok = ("css selector", "#confirmation-message menu button.full")
imei_header = ('xpath', '//h1[text()="IMEI"]')
imei_contents = ('css selector', '#mmi-screen #mmi-container #message')
mmi_send_btn = ('id', 'send')
fdn_warning_msg = _('FDN (Fixed Dialing Numbers) is activated and the following number is not in your FDN list: {}')
message_callerID = ('id', 'message')
contacts_sub_iframe = ("id", "iframe-contacts")
contact_list_header = ('id', 'contacts-list-header')