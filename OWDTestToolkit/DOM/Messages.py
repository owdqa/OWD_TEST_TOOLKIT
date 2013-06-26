frame_locator          = ('src', 'app://sms.gaiamobile.org/index.html')

#statusbar_new_sms      = ('xpath', ".//*[@id='desktop-notifications-container']/div[@class='notification']/div[text()='%s']")
statusbar_new_sms      = ('xpath', ".//*[@id='desktop-notifications-container']/div[@class='notification']/div[contains(text(),'%s')]")
#lockscreen_notif_xpath = "//*[@id='desktop-notifications-container']//div[text()='%s']"
lockscreen_notif_xpath = "//*[@id='desktop-notifications-container']//div[contains(text(),'%s')]"
create_new_message_btn = ('id', 'icon-add')

type_and_carrier_field = ("xpath", "//*[@id='contact-carrier']")

target_numbers         = ("xpath", "//*[@id='messages-recipients-list']/span")
add_contact_button     = ("id", "messages-contact-pick-button")
cancel_add_contact     = ("id", "cancel_activity")
contact_no_phones_msg  = ("xpath", "//form[@id='confirmation-message']//p[text()='No phones']")
contact_no_phones_ok   = ("xpath", "//form[@id='confirmation-message']//button[text()='OK']")

input_message_area     = ('id', 'messages-input')
input_message_area     = ('id', 'messages-input')

send_message_button    = ('id', 'messages-send-button')
message_sending_spinner= ("xpath", "//aside[@class='pack-end'][-1]/progress")

header_back_button     = ("id","messages-back-button")

threads                = ("xpath", "//p[@class='name']")
threads_list           = ('xpath', '//article[@id="threads-container"]//li')
thread_selector_xpath  = "//*[@id='threads-container']//li//a/p[text()='%s']"
thread_timestamp_xpath = thread_selector_xpath + "/..//time"
no_threads_message     = ("id", "no-result-message")
edit_threads_button    = ("id", "threads-edit-icon")
cancel_edit_threads    = ("id", "threads-cancel-button")
check_all_threads_btn  = ("id", "threads-check-all-button")
check_all_messages_btn = ("id", "messages-check-all-button")
delete_threads_button  = ("id", "threads-delete-button")

message_list           = ('xpath', '//article[@id="messages-container"]//li')
unread_message         = ('css selector', 'li > a.unread')
messages_from_num      = "//*[contains(@id, '%s')]"
message_timestamps     = ("xpath", ".//*[@id='messages-container']/header")
message_header         = ("id", "messages-header-text")
received_messages      = ('xpath', "//li[@class='bubble'][a[@class='received']]")
edit_messages_icon     = ("id","messages-edit-icon")
edit_msgs_delete_btn   = ("id","messages-delete-button")
edit_msgs_sel_all_btn  = ("id","messages-check-all-button")

airplane_warning_header= ("id", "dialog-title")
airplane_warning_ok    = ("id", "dialog-no")