frame_locator           = ("src", "email")
username                = ('class name', 'sup-info-name')
email_addr              = ('class name', 'sup-info-email')
password                = ('class name', 'sup-info-password')
login_next_btn          = ('class name', 'sup-info-next-btn')
login_cont_to_email_btn = ("xpath", "//button[text()='Continue to Mail']")
sup_header              = ('xpath', '//h1[text()="New Account"]')
sup_next_btn            = ('class name', 'sup-info-next-btn')
email_accounts_list     = ('class name', 'tng-account-item-label list-text')

compose_msg_btn         = ('class name', 'msg-compose-btn')
compose_to_from_contacts= ("xpath", "//div[@class='cmp-to-container cmp-addr-container']//span[@class='cmp-peep-name']")
compose_to              = ('class name', 'cmp-to-text cmp-addr-text')
compose_cc              = ('class name', 'cmp-cc-text cmp-addr-text')
compose_bcc             = ('class name', 'cmp-bcc-text cmp-addr-text')
compose_subject         = ('class name', 'cmp-subject-text')

compose_msg             = ('class name', 'cmp-body-text') # Caution: there's >1 of these in the html!

compose_send_btn        = ('class name', 'icon icon-send')
compose_send_failed_msg = ('xpath', './/*[text()="Sending email failed"]')
compose_send_failed_ok  = ("id", "cmp-send-failed-ok")
compose_sending_spinner = ('class name', 'cmp-messages-sending')

settings_menu_btn       = ('xpath', '//header//a[@class="msg-folder-list-btn"]')

settings_set_btn        = ('class name', 'fld-nav-settings-btn bottom-btn')
settings_del_acc_btn    = ('class name', 'tng-account-delete')
settings_del_conf_btn   = ('xpath', '//button[@id="account-delete-ok"]')
settings_add_account_btn= ('class name', 'tng-account-add')

goto_accounts_btn       = ('class name', 'fld-accounts-btn')    
accounts_list_names     = ('class name', 'fld-account-name')

folderList_header       = ('class name', 'fld-folders-header-account-label')
folderList_name_xpath   = '//*[text()="{}"]'

folder_message_list     = ('class name', 'msg-header-item')
folder_headers_list     = ('class name', 'msg-header-author-and-date')
folder_subject_list     = ('class name', 'msg-header-subject')
folder_refresh_button   = ("class name", "msg-refresh-btn bottom-btn msg-nonsearch-only")
folder_sync_spinner     = ("xpath", "//span[@data-l10n-id='messages-syncing']")

open_email_from         = ('xpath', "//div[@class='msg-envelope-from-line']//span[@class='msg-peep-content msg-peep-address']")
open_email_to           = ('xpath', "//div[@class='msg-envelope-to-line']//span[@class='msg-peep-content msg-peep-address']")
open_email_subject      = ('class name', 'msg-envelope-subject')

# NOTE: complex, but there's > 1 of these so you have to be this specific!
delete_this_email_btn   = ("xpath", "//div[@class='msg-reader-action-toolbar bottom-toolbar']//button[@class='msg-delete-btn bottom-btn']")
# NOTE: Nightmare - you need to getElements(this, desc, False) and loop through the list, there's > 1 of everything here!!
delete_confirm_buttons  = ("xpath", "//button[@id='msg-delete-ok']")
deleted_email_notif     = ("xpath", ".//*[@id='cardContainer']//p[text()='1 message deleted']")

confirm_ok = ("xpath", "//form[@class='modal-dialog-confirm generic-dialog visible']/menu/button[@data-l10n-id='ok']")
confirm_msg = ("class name", "modal-dialog-confirm-message")