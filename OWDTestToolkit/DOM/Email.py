from OWDTestToolkit.utils.i18nsetup import I18nSetup
_ = I18nSetup(I18nSetup).setup()


frame_locator = ("src", "email")
username = ('class name', 'sup-info-name')
email_addr = ('class name', 'sup-info-email')
password = ('class name', 'sup-info-password')
folder_name = ('css selector', 'span.msg-list-header-folder-name')
message_list_locator = ('css selector', '.card-message-list')

login_account_info_next_btn = ('xpath', '//section[@data-type="setup_account_info"]//button[contains(@class, "sup-info-next-btn")]')
login_account_prefs_next_btn = ('css selector', '.card-setup-account-prefs button.sup-info-next-btn')
login_cont_to_email_btn = ("xpath", "//button[text()='{}']".format(_("Continue to Mail")))
sup_header = ('xpath', '//h1[text()="{}"]'.format(_("New Account")))
sup_next_btn = ('class name', 'sup-info-next-btn')
email_accounts_list = ('class name', 'tng-account-item-label list-text')

manual_setup = ('class name', 'sup-manual-config-btn')
manual_setup_next = ('class name', 'sup-manual-next-btn')
manual_setup_sup_header = ('xpath', '//h1[@data-l10n-id="setup-manual-config-header"]')
manual_setup_account_type = ('xpath', '//select[@class="mail-select sup-manual-account-type"]')
manual_setup_account_options = ('xpath', '//form[@id="select-option-popup"]')
manual_setup_account_option = ('xpath', '//form[@id="select-option-popup"]//li[@role="option"]//span[text()="{}"]')
manual_setup_account_type_ok = ('xpath', '//form[@id="select-option-popup"]//menu[@id="select-options-buttons"]/button[@data-type="ok"]')
manual_setup_activesync_host = ('class name', 'sup-manual-activesync-hostname')
manual_setup_activesync_user = ('class name', 'sup-manual-activesync-username')
setup_account_header = ('xpath', '//h1[@data-l10n-id="setup-account-header3"]')

compose_header = ('css selector', '.cmp-compose-header')
compose_msg_btn = ('class name', 'msg-compose-btn')
compose_to_from_contacts = ("css selector", "div.cmp-to-container.cmp-addr-container span.cmp-peep-name")
compose_to_from_contacts_address = ("css selector", "div.cmp-to-container.cmp-addr-container span.cmp-peep-address collapsed")
compose_to = ('class name', 'cmp-to-text cmp-addr-text')
compose_cc = ('class name', 'cmp-cc-text cmp-addr-text')
compose_bcc = ('class name', 'cmp-bcc-text cmp-addr-text')
compose_subject = ('class name', 'cmp-subject-text')

# Caution: there's >1 of these in the html!
compose_msg = ('class name', 'cmp-body-text')

reply_btn = ('class name', "msg-reply-btn")
reply_menu_reply = ('xpath', './/form[@class="msg-reply-menu"]//button[@class="msg-reply-menu-reply"]')
reply_menu_reply_all = ('xpath', './/form[@class="msg-reply-menu"]//button[@class="msg-reply-menu-reply-all"]')
reply_menu_forward = ('xpath', './/form[@class="msg-reply-menu"]//button[@class="msg-reply-menu-forward"]')
reply_menu_cancel = ('xpath', './/form[@class="msg-reply-menu"]//button[@class="msg-reply-menu-cancel"]')

compose_send_btn = ('class name', 'icon icon-send')
compose_send_failed_msg = ('xpath', './/*[text()="{}"]'.format(_("Sending email failed")))
compose_send_failed_ok = ("id", "cmp-send-failed-ok")
compose_sending_spinner = ('class name', 'cmp-messages-sending')
compose_attach_btn = ('class name', 'icon icon-attachment')

attach_video_btn = ("xpath", "//form//button[text()='{}']".format(_("Video")))
attach_music_btn = ("xpath", "//form//button[text()='{}']".format(_("Music")))
attach_gallery_btn = ("xpath", "//form//button[text()='{}']".format(_("Gallery")))
attach_camera_btn = ("xpath", "//form//button[text()='{}']".format(_("Camera")))

settings_menu_btn = ('xpath', '//header//a[@class="msg-folder-list-btn"]')

settings_set_btn = ('xpath', '//a[@class="fld-nav-toolbar bottom-toolbar"]//span[@data-l10n-id="drawer-settings-link"]')
settings_del_acc_btn = ('class name', 'tng-account-delete')
settings_del_conf_btn = ('xpath', '//button[@id="account-delete-ok"]')
settings_add_account_btn = ('class name', 'tng-account-add')

goto_accounts_btn = ('class name', 'fld-accounts-btn')
accounts_list_names = ('class name', 'fld-account-name')

folder_list_container = ('xpath', '//div[@class="fld-folders-container"]')
folderList_header = ('class name', 'fld-folders-header-account-label')
folderList_name_xpath = '//span[@class="fld-folder-name" and text()="{}"]'
email_entry = ('css selector', '#cardContainer .msg-header-item:not([data-index="-1"])')

folder_message_container = ('class name', 'msg-messages-container')
folder_message_list = ('class name', 'msg-header-item')
folder_headers_list = ('class name', 'msg-header-author-and-date')
folder_subject_list = ('class name', 'msg-header-subject')
folder_refresh_button = ("class name", "icon msg-refresh-btn")
folder_sync_spinner = ("xpath", "//span[@data-l10n-id='messages-syncing']")

msg_list_new_mail_notification = ("class name", "msg-list-topbar")

open_email_from = ('xpath', "//div[@class='msg-envelope-line msg-envelope-from-line']//span[@class='msg-peep-content msg-peep-address']")
# NOTE: incoherent use of classes here, that's why i'm using 'or' conditional
open_email_to = ('xpath', "//div[@class='msg-envelope-line msg-envelope-to-line']//span[@class='msg-peep-content' or @class='msg-peep-content msg-peep-address']")
open_email_subject = ('class name', 'msg-envelope-subject')
open_email_attached_file = ("xpath", "//ul[@class='msg-attachments-container']/li[contains(@class, 'msg-attachment-item')]")
open_email_body = ('class name', 'msg-body-content')
open_email_body_link = ("css selector", "a.moz-external-link")

# NOTE: complex, but there's > 1 of these so you have to be this specific!
delete_this_email_btn = ('xpath', '//div[@class="card-message-reader card center"]//button[@class="icon msg-delete-btn"]')
# NOTE: Nightmare - you need to getElements(this, desc, False) and loop through the list, there's > 1 of everything here!!
deleted_email_notif = ("xpath", "//section[contains(@class, 'banner customized')]//p[text()='{}']".format(_("1 message deleted")))

confirm_ok = ("xpath", '//form[@class="confirm-dialog-form"]//button[@data-l10n-id="dialog-button-ok"]')
email_not_setup_ok = ('xpath', '//button[@class="confirm-dialog-ok recommend"]')
confirm_msg = ('xpath', '//form[@class="confirm-dialog-form"]//p[@class="confirm-dialog-message"]')

new_account_error_msg = ('css selector', 'section.card-setup-account-info div.scrollregion-below-header div.sup-error-region div.sup-error-message')

toaster_sending_mail = ('xpath', '//section[contains(@class, "toaster actionable")]//p[@class="toaster-text" and contains(text(), "Sending mail")]')
toaster_sent_mail = ('xpath', '//section[contains(@class, "toaster actionable")]//p[@class="toaster-text" and text()="Email sent."]')

switch_account_panel_one_account = ('class name', 'card-folder-picker card anim-vertical anim-overlay one-account center opened')

switch_account_scroll_outer = ('xpath', '//div[@class="fld-acct-scrollouter"]')
switch_account_scroll = ('class name', 'fld-acct-header closed')
switch_account_current_account = ('xpath', '//div[@class="fld-acct-scrollouter"]//a[@class="fld-acct-header closed"]//span[@class="fld-acct-header-account-label"]')
switch_account_accounts_to_change = ('xpath', '//div[@class="fld-accountlist-container"]//a[@class="fld-account-item"]//span[@class="fld-account-name"]')  # This selector does not return the current account

# Open external link confirmation
confirmation_browser_cancel = ('id', 'msg-browse-cancel')
confirmation_browser_ok = ('id', 'msg-browse-ok')

confirmation_delete_cancel = ('id', 'msg-delete-cancel')
confirmation_delete_ok = ('id', 'msg-delete-ok')
