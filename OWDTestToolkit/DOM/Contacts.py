import GLOBAL
frame_locator          = ("src","contacts")
view_all_header        = ('xpath', GLOBAL.app_head_specific % 'Contacts')
view_all_contact_xpath = '//*[@data-order="%s"]'
view_all_contact_list  = ("xpath", "//li[@class='contact-item']")
view_all_contact_name_xpath  = "//li[@class='contact-item']//p[contains(@data-order,'%s')]"
view_all_contact_JS    = ("xpath", "/html/body/section/article/div[2]/div/section/section/ol/li")
view_all_contact_JSname= ("xpath", "/html/body/section/article/div[2]/div/section/section/ol/li/p/strong")
view_all_contact_HM    = ("xpath", "/html/body/section/article/div[2]/div/section/section/ol/li")
view_all_contact_email = ("xpath", "/html/body/section/article/div[2]/div/section/section/ol/li")
view_all_contact_import= ("xpath", "/html/body/section/article/div[2]/div/section/section[2]/ol/li")
view_all_contact_import2= ("xpath", "/html/body/section/article/div[2]/div/section/section[2]/ol/li[2]")

view_details_title     = ('id', 'contact-name-title')
view_contact_image     = ("id", "cover-img")
view_contact_tel_field = ("id", "call-or-pick-0")
view_contact_email_field = ("id", "email-or-pick-0")
view_contact_address    = ("xpath", "//li[@id='address-details-template-0']//a[@class='action action-block']/b")
view_contact_comments  = ("id", "note-details-template-0")
view_contact_tels_xpath= "//*[contains(@id, 'call-or-pick-') and contains(@data-tel, '%s')]"
dialer_frame           = ("data-url", "oncall")

search_field           = ("xpath", ".//*[@id='search-start']/input")
search_contact_input   = ("id", "search-contact")
search_results_list    = ("xpath",".//*[@id='search-list']/li")
search_cancel_btn      = ('id', 'cancel-search')
search_no_contacts_found = ("id", "no-result")
favourites_section     = ("id", "contacts-list-favorites")
favourites_list_xpath  = "//ol[@id='contacts-list-favorites']//p[@data-order='%s']"
favourite_JS           = ("xpath", "/html/body/section/article/div[2]/div/section/section/ol/li")

social_network_contacts= ('class name', "icon-social icon-fb notorg")
settings_button        = ('id', 'settings-button')
settings_header        = ('xpath', GLOBAL.app_head_specific % 'Settings')
settings_done_button   = ('id', 'settings-close')
settings_fb_enable     = ('xpath', '//li[@class="fb-item"]')
settings_import_fb     = ('id', 'import-fb') 
settings_fb_frame      = ("id", 'fb-extensions')
settings_fb_logout_wait= ('id', 'progress-title')
add_contact_button     = ('id', 'add-contact-button')
add_contact_header     = ('xpath', GLOBAL.app_head_specific % 'Add contact')
favourite_button       = ('id','toggle-favorite')
favourite_marker       = ('id', 'favorite-star')
details_back_button    = ('id', 'details-back')

reset_field_xpath      = ".//*[@id='%s']//button[@id='img-delete-button']"
edit_image             = ("id", "thumbnail-action")
edit_contact_header    = ('xpath', GLOBAL.app_head_specific % 'Edit contact')
edit_update_button     = ('id', 'save-button')
edit_details_button    = ('id', 'edit-contact-button')
edit_cancel_button     = ('id', 'cancel-edit')
delete_contact_btn     = ('id', 'delete-contact')
cancel_delete_btn      = ('xpath', '//*[@id="confirmation-message"]//button[text()="Cancel"]')
confirm_delete_btn     = ('xpath', '//*[@id="confirmation-message"]//button[text()="Remove"]')
done_button            = ('id', 'save-button')

add_photo              = ("id", "thumbnail-photo")
photo_from_gallery     = ("xpath", "/html/body/div/form[9]/menu/button")
cancel_photo_source    = ("xpath", '//button[@data-action="cancel"]')
picture_thumbnails     = ("xpath", "//*[@id='thumbnails']/li")
picture_crop_done_btn  = ("id", "crop-done-button")
given_name_field       = ('id', 'givenName')
given_name_reset_icon  = ("xpath", ".//*[@id='contact-form']//p[input[@id='givenName']]//button")
family_name_field      = ('id', 'familyName')
family_name_reset_icon = ("xpath", ".//*[@id='contact-form']//p[input[@id='familyName']]//button")
email_address_list     = ("xpath", "//ul[@id='details-list']/li")
email_field            = ('id', "email_0")
add_email_button       = ("id","add-new-email")
email_fields           = ("xpath", "//input[@type='email']")
phone_field            = ('id', "number_0")
phone_field_xpath      = "//*[contains(@id, 'number_') and contains(@value, '%s')]"
street_field           = ('id', "streetAddress_0")
zip_code_field         = ('id', "postalCode_0")
city_field             = ('id', 'locality_0')
country_field          = ('id', 'countryName_0')
comment_field          = ('id', 'note_0')
sms_button             = ('id', 'send-sms-button-0')
sms_button_specific_id = 'send-sms-button-%s'
email_button_spec_id   = 'email-or-pick-%s'
link_button            = ('id', "link_button") # WARNING: >1 element has this id!


#
# Importing from gmail / hotmail etc...
#
import_all_imported_msg = ("xpath", "//*[@id='friends-msg' and contains(text(), 'your friends are imported')]")
import_cancel_login = ("id", "popup-close")
import_close_icon   = ("id", "import-close")
import_throbber     = ("id", "popup-throbber")
import_num_of_conts = ("id", "friends-msg")
import_select_all   = ("id", "select-all")
import_desel_all    = ("id", "deselect-all")
import_import_btn   = ("id", "import-action")
import_conts_list   = ("xpath", "//*[@id='groups-list']//li[@class='block-item']")
import_search_list  = ("xpath", "//*[@id='search-list']//li[@class='block-item']")
import_conts_xp     = "//span[@id='groups-list']//li[@class='block-item' and contains(@data-search, '%s')]"

import_contacts      = ("id", "importContacts")

gmail_button            = ("xpath", "//button[text()='Gmail']")
gmail_frame             = ("data-url", "google")
gmail_username          = ("id", "Email")
gmail_password          = ("id", "Passwd")
gmail_signIn_button     = ("id", "signIn")
gmail_permission_accept = ("id", "submit_approve_access")
gmail_login_error_msg   = ("id", "errormsg_0_Passwd")
gmail_import_frame      = ("src", "gmail")  # It's in the contacts iframe.

hotmail_button            = ("xpath", "//button[text()='Outlook']")
hotmail_frame             = ("data-url", ".live.com")
hotmail_username          = ("id", "i0116")
hotmail_password          = ("id", "i0118")
hotmail_signIn_button     = ("id", "idSIButton9")
hotmail_permission_accept = ("id", "idBtn_Accept")
hotmail_login_extra_msg   = ("id", "idDiv_FSI_HeaderInfo")
hotmail_login_error_msg   = ("id", "idTd_PWD_Error")
hotmail_import_frame      = ("src", "live")  # It's in the contacts iframe.

memorycard_button = ("xpath", "/html/body/article/section[2]/article/section/ul/li[2]/button")

sim_button =("xpath", "/html/body/article/section[2]/article/section/ul/li/button")

#
#Export
#
export_export_btn = ("id", "export-action")
export_contacts =("id" , "exportContacts")
export_sd_card = ("id" , "export-sd-option")
export_select_all = ("id", "select-all")
export = ("xpath" , "//*[@id='select-action']")
export_import_banner = ("id" , "statusMsg")

export_sim_card = ("id" , "export-sim-option-8934071100275319352")
export_bluetooth = ("id" , "export-bluetooth-option")


