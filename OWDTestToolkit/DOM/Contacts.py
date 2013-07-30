import GLOBAL
frame_locator          = ("src","contacts")
view_all_header        = ('xpath', GLOBAL.app_head_specific % 'Contacts')
view_all_contact_xpath = '//*[@data-order="%s"]'
view_all_contact_list  = ("xpath", "//li[@class='contact-item']")
view_all_contact_name_xpath  = "//li[@class='contact-item']//p[@data-order='%s']"

view_contact_tel_field = ("id", "call-or-pick-0")
view_contact_tels_xpath= "//*[contains(@id, 'call-or-pick-') and contains(@data-tel, '%s')]"
dialer_frame           = ("data-url", "oncall")

search_field           = ("xpath", ".//*[@id='search-start']/input")
search_contact_input   = ("id", "search-contact")
search_results_list    = ("xpath",".//*[@id='search-list']/li")
search_cancel_btn      = ('id', 'cancel-search')
favourites_list_xpath  = "//ol[@id='contacts-list-favorites']//p[@data-order='%s']"

social_network_contacts= ('class name', "icon-social icon-fb notorg")
settings_button        = ('id', 'settings-button')
settings_header        = ('xpath', GLOBAL.app_head_specific % 'Settings')
settings_fb_enable     = ('xpath', '//li[@class="fb-item"]')
settings_import_fb     = ('id', 'import-fb') 
settings_fb_frame      = ("id", 'fb-extensions')
settings_fb_logout_wait= ('id', 'progress-title')
settings_done_button   = ('id', 'settings-done')
add_contact_button     = ('id', 'add-contact-button')
add_contact_header     = ('xpath', GLOBAL.app_head_specific % 'Add contact')
view_details_title     = ('id', 'contact-form-title')
favourite_button       = ('id','toggle-favorite')
favourite_marker       = ('id', 'favorite-star')
details_back_button    = ('id', 'details-back')

reset_field_xpath      = ".//*[@id='%s']//button[@id='img-delete-button']"
edit_contact_header    = ('xpath', GLOBAL.app_head_specific % 'Edit contact')
edit_update_button     = ('id', 'save-button')
edit_details_button    = ('id', 'edit-contact-button')
edit_cancel_button     = ('id', 'cancel-edit')
delete_contact_btn     = ('id', 'delete-contact')
cancel_delete_btn      = ('xpath', '//*[@id="confirmation-message"]//button[text()="Cancel"]')
confirm_delete_btn     = ('xpath', '//*[@id="confirmation-message"]//button[text()="Remove"]')
done_button            = ('id', 'save-button')

add_photo              = ("id", "thumbnail-photo")
photo_from_gallery     = ("link text", "Gallery")
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

gmail_button            = ("xpath", "//button[text()='Gmail']")
gmail_frame             = ("data-url", "google")
gmail_throbber          = ("id", "popup-throbber")
gmail_username          = ("id", "Email")
gmail_password          = ("id", "Passwd")
gmail_signIn_button     = ("id", "signIn")
gmail_login_error_msg   = ("id", "errormsg_0_Passwd")