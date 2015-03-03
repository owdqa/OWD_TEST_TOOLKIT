from OWDTestToolkit.utils.i18nsetup import I18nSetup
_ = I18nSetup(I18nSetup).setup()


frame_locator = ('src', 'sms')

main_header = ('css selector', 'h1[data-l10n-id="messages"]')
statusbar_new_sms = ('xpath', ".//*[@id='desktop-notifications-container']/div[@class='notification']/div[contains(text(),'{}')]")
new_sms_popup_msg = ("xpath", "//div[@id='toaster-detail' and contains(text(),'{}')]")
new_sms_popup_num = ("xpath", "//div[@id='toaster-title' and contains(text(),'{}')]")
lockscreen_notif_xpath = "//*[@id='desktop-notifications-container']//div[contains(text(),'{}')]"
create_new_message_btn = ('id', 'icon-add')

edit_mode_wrapper = ("xpath", "//article[@id='main-wrapper' and @class='wrapper edit']")
service_unavailable_msg = ("xpath", "//*[@data-l10n-id='sendGeneralErrorTitle']")
service_unavailable_ok = ("xpath", "//*[@data-l10n-id='sendGeneralErrorBtnOk']")

type_and_carrier_field = ("id", "contact-carrier")

target_numbers_empty = ("id", "to-label")
target_numbers = ("css selector", "#messages-recipients-list span")
add_contact_button = ("id", "messages-contact-pick-button")
cancel_add_contact = ("id", "cancel_activity")
contact_no_phones_msg = ("xpath", "//form[@id='confirmation-message']//p[text()='{}']".format(_("No phones")))
contact_no_phones_ok = ("xpath", "//form[@id='confirmation-message']//button[text()='{}']".format(_("OK")))

input_message_area = ('id', 'messages-input')

send_message_button = ('id', 'messages-send-button')
messages_counter = ('id', 'messages-counter-label')
attach_button = ('id', 'messages-attach-button')
message_sending_spinner = ("xpath", "//aside[@class='message-status']/progress")

header_back_button = ("id", "messages-back-button")
header_close_button = ('id', 'messages-close-button')

# This field will allow to retrieve phone numbers and emails in the body of the last SM or MM
phone_info_in_msg = ('xpath', '//*[@id="messages-container"]//li[last()]//a[@data-action="dial-link"]')
email_info_in_msg = ('xpath', '//*[@id="messages-container"]//li[last()]//a[@data-action="email-link"]')

threads = ("css selector", "p.name")
threads_list = ('css selector', '#threads-container li')

threads_list_element = ('xpath', '//article[@id="threads-container"]/div/ul/li/a/p')

thread_target_names = ('xpath', '//article[@id="threads-container"]//li//p[@class="name"]')
thread_selector_xpath = "//*[@id='threads-container']//li//a/p[contains(text(),'{}')]/../.."
thread_selector_checked = ('xpath', "//*[@id='threads-container']//li//a/p[contains(text(),'{}')]/../../label/input")
thread_timestamp_xpath = thread_selector_xpath + "/..//time"
no_threads_message = ("id", "no-result-message")
edit_threads_button = ("id", "threads-options-icon")
cancel_edit_threads = ("css selector", "button[data-l10n-id='settings'] + button[data-l10n-id='cancel']")
check_all_threads_btn = ("id", "threads-check-all-button")
check_all_messages_btn = ("id", "messages-check-all-button")
delete_threads_button = ("css selector", "button[data-l10n-id='deleteMessages-label']")

message_list = ('xpath', '//div[@id="messages-container"]//li')
message_timestamps = ("xpath", "//div[@id='messages-container']/div[@class='messages-date-group'][last()]/header")
last_message = ('xpath', '//div[@id="messages-container"]//div[last()]//li[last()]')
message_body_xpath = '//div[@id="messages-container"]//div[last()]//li[last()]//div[@class="message-body"]'
last_message_body = ('xpath', message_body_xpath)
last_message_time = ('xpath', message_body_xpath + '/time')
last_sent_message = ('xpath', "//li[contains(@class, 'sent')][last()]")
last_message_text = ('xpath', '//div[@id="messages-container"]//div[last()]//li[last()]//div[@class="message-content"]//p')
last_message_mms_text = ('xpath', '//div[@id="messages-container"]//div[last()]//li[last()]//div[@class="message-content"]//p/span')
# Use this with a find_element over the result of getting last_message
last_message_text_nested = ('xpath', '//div[@class="message-content"]//p')

message_send_timestamp = ('xpath', '//section[@id="thread-messages"]/h1[@data-title={}]/../../article[@id="messages-container"]/ul/li[last()]')
unread_message = ('css selector', 'li > a.unread')
messages_from_num = "//*[contains(@id, '{}')]"
message_header = ("id", "messages-header-text")
received_messages = ('xpath', "//li[@class='bubble'][a[@class='received']]")

edit_messages_icon = ('xpath', "//section[@id='thread-messages']//span[@class='icon icon-options']")
edit_threads_header = ('id', 'threads-edit-mode')
threads_delete_button = ('id', 'threads-delete-button')
delete_threads_ok_btn = ('xpath', '//button[@class="danger" and @data-l10n-id="delete"]')
delete_messages_btn = ('xpath', "//button[@data-l10n-id='deleteMessages-label']")
delete_messages_ok_btn = ('id', "messages-delete-button")

edit_msgs_delete_btn = ("id", "messages-delete-button")
edit_msgs_header = ("id", "messages-edit-mode")
edit_msgs_sel_all_btn = ("id", "messages-check-all-button")

airplane_warning_message = ('css selector', 'strong[data-l10n-id="sendFlightModeTitle"]')
airplane_warning_ok = ('css selector', 'button[data-l10n-id="sendFlightModeBtnOk"]')

received_sms = ('xpath', "//li[@class='message sms received incoming']/section/div/p")
received_mms = ('xpath', "//li[@class='message mms received incoming']/section/div/p")
received_mms_subject = ('css selector', ".message.mms.received.incoming.has-subject div.message-body")

forward_btn_msg_opt = ('css selector', "button[data-l10n-id=forward]")
cancel_btn_msg_opt = ('css selector', "button[data-l10n-id=forward] ~ button[data-l10n-id=cancel]")

messages_options_btn = ("id", "messages-options-icon")
addsubject_btn_msg_opt = ('xpath', '//form[@data-type="action"]//button[@data-l10n-id="add-subject"]')
message_convert_notice = ('css selector', "#messages-convert-notice p")
deletesubject_btn_msg_opt = ("xpath", "//*[@data-l10n-id='remove-subject']")
cancel_btn_msg = ("xpath", "//body[@role='application']/form/menu/button[@data-l10n-id='cancel']")
target_subject = ("id", "messages-subject-input")

attach_preview_img_type = ("xpath", "//*[@class='attachment-container preview']")
attach_preview_video_audio_type = ("xpath", "//*[@class='attachment-container nopreview']")
last_message_attachment_img = ('xpath', '//*[@id="messages-container"]//li[last()]//div[@class="attachment-container preview"]')
last_message_attachment_av = ('xpath', '//*[@id="messages-container"]//li[last()]//div[@class="attachment-container nopreview"]')
# Use this selector, after having used either last_message_attachment_img, last_message_attachment_av
last_message_thumbnail = ('xpath', '//div[contains(@class, "thumbnail-placeholder")]')

header_call_btn = ('css selector', 'form.contact-prompt button[data-l10n-id="call"]')
header_send_message_btn = ('css selector', 'form.contact-prompt button[data-l10n-id="sendMessage"]')
header_create_new_contact_btn = ('css selector', 'form.contact-prompt button[data-l10n-id="createNewContact"]')
header_add_to_contact_btn = ('css selector', 'form.contact-prompt button[data-l10n-id="addToExistingContact"]')
contact_cancel_btn = ('css selector', 'form.contact-prompt button[data-l10n-id="cancel"]')
header_send_email_btn = ('css selector', 'form.contact-prompt button[data-l10n-id="sendEmail"]')

mms_from_video = ("xpath", "//button[@class='icon' and contains(@style, 'app://video')]")
mms_from_camera = ("xpath", "//button[@class='icon' and contains(@style, 'app://camera')]")
mms_from_gallery = ("xpath", "//button[@class='icon' and contains(@style, 'app://gallery')]")
mms_from_music = ("xpath", "//button[@class='icon' and contains(@style, 'app://music')]")
mms_cancel_button = ("css selector", "button.icon + button[data-l10n-id=cancel]")

mms_icon = ("css selector", "span.mms-icon")

attached_opt_view = ("xpath", "//*[@data-l10n-id='view-attachment-image']")
attached_opt_remove = ("xpath", "//*[@data-l10n-id='remove-attachment-image']")
attached_opt_replace = ("xpath", "//*[@data-l10n-id='replace-attachment-image']")

message_expected_content = ('xpath', "//div[@class='message-content']//p/span[text()='{}']")

wap_push_message_link = ('xpath', "//*[@id='si-sl-screen']//a[@data-action='url-link']")

sms_class_0_ok_btn = ('css selector', 'button.modal-dialog-alert-ok.confirm.affirmative')
send_email_failed = ('xpath', '//span[@class="modal-dialog-alert-message"]')

save_as_draft_btn = ('xpath', '//button[@data-l10n-id="save-as-draft"]')
discard_msg_btn = ('xpath', '//button[@data-l10n-id="discard-message"]')
cancel_save_msg = ('xpath', '//button[@data-l10n-id="cancel"]')

button_download_attachment = ('xpath', '//button[@data-l10n-id="download-attachment"]')
button_downloading_attachment = ('xpath', '//button[@data-l10n-id="downloading-attachment"]')
mms_attachment_names = ('css selector', '.attachment-container .file-name')
mms_attachment_sizes = ('css selector', '.attachment-container .size-indicator')
mms_resize_msg = ('id', 'messages-resize-notice')
mms_max_length_msg = ('id', 'messages-max-length-notice')

fdn_blocked_title = ('css selector', '[data-l10n-id=fdnBlocked2Title]')
fdn_blocked_btn_ok = ('css selector', '[data-l10n-id=fdnBlocked2BtnOk]')

remove_contact_from_to_field = ('css selector', 'button.danger[data-l10n-id="remove"]')