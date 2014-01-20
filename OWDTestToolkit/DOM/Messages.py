frame_locator          = ('src', 'sms')

statusbar_new_sms      = ('xpath', ".//*[@id='desktop-notifications-container']/div[@class='notification']/div[contains(text(),'%s')]")
new_sms_popup_msg      = ("xpath", "//div[@id='toaster-detail' and contains(text(),'%s')]")
new_sms_popup_num      = ("xpath", "//div[@id='toaster-title' and contains(text(),'%s')]")
lockscreen_notif_xpath = "//*[@id='desktop-notifications-container']//div[contains(text(),'%s')]"
create_new_message_btn = ('id', 'icon-add')

edit_mode_wrapper      = ("xpath", "//article[@id='main-wrapper' and @class='wrapper edit']")
service_unavailable_msg= ("xpath", "//*[@data-l10n-id='sendGeneralErrorTitle']")
service_unavailable_ok = ("xpath", "//*[@data-l10n-id='sendGeneralErrorBtnOk']")

type_and_carrier_field = ("xpath", "//*[@id='contact-carrier']")

target_numbers_empty   = ("xpath", "//*[@id='messages-recipients-list']/span[@data-number='']")
target_numbers         = ("xpath", "//*[@id='messages-recipients-list']/span")
add_contact_button     = ("id", "messages-contact-pick-button")
cancel_add_contact     = ("id", "cancel_activity")
contact_no_phones_msg  = ("xpath", "//form[@id='confirmation-message']//p[text()='This contact does not have a phone number']")
contact_no_phones_ok   = ("xpath", "//form[@id='confirmation-message']//button[text()='OK']")

input_message_area     = ('id', 'messages-input')

send_message_button    = ('id', 'messages-send-button')
attach_button          = ('id', 'messages-attach-button')
message_sending_spinner= ("xpath", "//aside[@class='pack-end'][-1]/progress")

header_back_button     = ("id","messages-back-button")

threads                = ("xpath", "//p[@class='name']")
threads_list           = ('xpath', '//article[@id="threads-container"]//li')
thread_target_names    = ('xpath', '//article[@id="threads-container"]//li//p[@class="name"]')
thread_selector_xpath  = "//*[@id='threads-container']//li//a/p[contains(text(),'%s')]"
thread_timestamp_xpath = thread_selector_xpath + "/..//time"
no_threads_message     = ("id", "no-result-message")
edit_threads_button    = ("id", "threads-edit-icon")
cancel_edit_threads    = ("id", "threads-cancel-button")
check_all_threads_btn  = ("id", "threads-check-all-button")
check_all_messages_btn = ("id", "messages-check-all-button")
delete_threads_button  = ("id", "threads-delete-button")

message_list           = ('xpath', '//article[@id="messages-container"]//li')
message_timestamps     = ("xpath", "//article[@id='messages-container']/header")
unread_message         = ('css selector', 'li > a.unread')
messages_from_num      = "//*[contains(@id, '%s')]"
message_timestamps     = ("xpath", ".//*[@id='messages-container']/header")
message_header         = ("id", "messages-header-text")
received_messages      = ('xpath', "//li[@class='bubble'][a[@class='received']]")
edit_messages_icon     = ("id","messages-edit-icon")
edit_msgs_delete_btn   = ("id","messages-delete-button")
edit_msgs_header       = ("id","messages-edit-mode")
edit_msgs_sel_all_btn  = ("id","messages-check-all-button")

airplane_warning_message= ("xpath", "//p/*[contains(text(),'Airplane')]")
airplane_warning_ok    = ("xpath", "//button[text()='OK']")

header_call_btn                 = ("xpath", "/html/body/form/menu/button")
header_send_message_btn         = ("xpath", "//button[text()='Send message']")
header_create_new_contact_btn   = ("xpath", "/html/body/form/menu/button[2]")
header_add_to_contact_btn       = ("xpath", "/html/body/form/menu/button[3]")
header_cancel_btn               = ("xpath", "/html/body/form/menu/button[5]")
header_cancel_btn_no_send       = ("xpath", "/html/body/form/menu/button[4]")

mms_from_video                  = ("xpath", "/html/body/div/form[9]/menu/button")
mms_from_camera                 = ("xpath", "/html/body/div/form[9]/menu/button[4]")
mms_from_gallery                = ("xpath", "/html/body/div/form[9]/menu/button[3]")
mms_from_music                  = ("xpath", "/html/body/div/form[9]/menu/button[2]")
mms_cancel_button               = ("xpath", "/html/body/div/form[9]/menu/button[5]")

mms_icon                        = ("xpath", "/html/body/article/section/article/ul/li/a/p[2]/span")