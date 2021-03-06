import GLOBAL

from OWDTestToolkit.utils.i18nsetup import I18nSetup
_ = I18nSetup(I18nSetup).setup()


frame_locator = ("src", "contacts")
action_select_all = ("id", "select-all")
view_all_header = ('xpath', GLOBAL.app_head_specific.format(_('Contacts')))
view_all_contact_xpath = '//*[@data-order="{}"]'
# Sometimes there's a hidden data-group called 'ice', we must skip it
view_all_contact_list = ('css selector', 'li.contact-item:not([data-group=ice])')
view_all_contact_name_xpath = "//li[@class='contact-item']//p[contains(@data-search,'{}')]"
contact_names = ('css selector', '.contact-item .contact-text')
view_all_contact_specific_contact = ('xpath', '//section[@class="group-section"]//li/p[@class="contact-text"]/strong[contains(text(), "{}")]')

view_details_title = ('id', 'contact-name-title')
view_contact_image = ("id", "cover-img")
view_contact_tel_field = ("id", "call-or-pick-0")
view_contact_email_field = ("id", "email-or-pick-0")
view_contact_address = ("xpath", "//li[@id='address-details-template-0']//a[@class='action action-block']/b")
view_contact_comments = ("id", "note-details-template-0")
view_contact_tels_xpath = "//*[contains(@id, 'call-or-pick-') and contains(@data-tel, '{}')]"
view_contact_hello_option = ('css selector', '#webrtc-client-actions button[data-l10n-id={}]')
dialer_frame = ("data-url", "oncall")

search_field = ("css selector", "#search-start input")
search_contact_input = ("id", "search-contact")
search_contact_result_input = ('id', 'search-contact')
search_results_list = ("css selector", "#search-list li")
search_cancel_btn = ('id', 'cancel-search')
search_no_contacts_found = ("id", "no-result")
search_contact_header = ('id', 'contacts-list-header')
select_recipient_btn = ('xpath', '//header[@data-l10n-id="select_recipient"]/..//button[text()="{}"]')

favourites_section = ("id", "contacts-list-favorites")
favourites_list_xpath = "//ol[@id='contacts-list-favorites']//li[@data-order='{}']"
favourites_search_section = ('id', 'section-group-favorites')
favourite_by_name = ("xpath", "//section[@id='section-group-favorites']//strong[text()='{}']")

social_network_contacts = ('class name', "icon-social icon-fb")
settings_button = ('id', 'settings-button')
settings_header = ('xpath', GLOBAL.app_head_specific.format(_('Settings').encode("utf8")))
settings_done_button = ('id', 'settings-close')
settings_fb_enable = ('xpath', '//li[@class="fb-item"]')
settings_import_fb = ('id', 'import-fb')
settings_fb_frame = ("id", 'fb-extensions')
settings_fb_logout_wait = ('id', 'progress-title')
settings_delete_all_contacts = ('id', 'bulkDelete')
select_action = ("id", "select-action")
add_contact_button = ('id', 'add-contact-button')
add_contact_header = ('xpath', GLOBAL.app_head_specific.format(_('Add contact')))
contact_form_header = ('id', 'contact-form-header')
details_view_header = ('id', 'details-view-header')
favourite_button = ('id', 'toggle-favorite')
favourite_marker = ('id', 'favorite-star')
details_back_button = ('id', 'details-back')

reset_field_css = "#id='{}' button.img-delete-button"
edit_image = ("id", "thumbnail-action")
edit_contact_header = ('xpath', GLOBAL.app_head_specific.format(_('Edit contact')))
edit_update_button = ('id', 'save-button')
edit_details_button = ('id', 'edit-contact-button')
edit_cancel_button = ('id', 'cancel-edit')
delete_contact_btn = ('id', 'delete-contact')
cancel_delete_btn = ('xpath', '//*[@id="confirmation-message"]//button[text()="{}"]'.format(_("Cancel")))
confirm_delete_btn = ('xpath', '//*[@id="confirmation-message"]//button[text()="{}"]'.format(_("Delete")))
done_button = ('id', 'save-button')

add_photo = ("id", "thumbnail-photo")
cancel_photo_source = ("xpath", '//button[@data-action="cancel"]')
picture_thumbnails = ("xpath", "//*[@id='thumbnails']//div[@class='thumbnail-group-container']//img")
picture_crop_done_btn = ("id", "crop-done-button")
given_name_field = ('id', 'givenName')
given_name_reset_icon = ("xpath", ".//*[@id='contact-form']//p[input[@id='givenName']]//button")
family_name_field = ('id', 'familyName')
family_name_reset_icon = ("xpath", ".//*[@id='contact-form']//p[input[@id='familyName']]//button")
email_address_list = ('css selector', 'ul#details-list li[data-l10n-id="emailDetail"]')
email_field = ('id', "email_0")
add_phone_button = ('id', 'add-new-phone')
add_email_button = ("id", "add-new-email")
add_address_button = ('id', 'add-new-address')
email_fields = ("xpath", "//input[@type='email']")
phone_field = ('id', "number_0")
phone_field_xpath = "//*[contains(@id, 'number_') and contains(@value, '{}')]"
street_field = ('id', "streetAddress_0")
zip_code_field = ('id', "postalCode_0")
city_field = ('id', 'locality_0')
country_field = ('id', 'countryName_0')
comment_field = ('id', 'note_0')
sms_button = ('id', 'send-sms-button-0')
sms_button_specific_id = 'send-sms-button-{}'
email_button_spec_id = 'email-or-pick-{}'
link_button = ('css selector', "#contact-detail-inner #link_button")

# Importing from gmail / hotmail etc...
import_all_imported_msg = ("xpath", "//*[@id='friends-msg' and contains(text(), 'your friends are imported')]")
import_close_icon = ("id", "import-close")
import_throbber = ("id", "popup-throbber")
import_num_of_conts = ("id", "friends-msg")
import_select_all = ("id", "select-all")
import_desel_all = ("id", "deselect-all")
import_import_btn = ("id", "import-action")
import_conts_list = ("xpath", "//*[@id='groups-list']//li[@class='block-item']")
import_search_list = ("xpath", "//*[@id='search-list']//li[@class='block-item']")
import_conts_xp = "//span[@id='groups-list']//li[@class='block-item' and contains(@data-search, '{}')]"

import_contacts = ('xpath', '//button[@data-l10n-id="importContactsButton"]')
# import_contacts = ("id", "importContacts")
import_contacts_header = ("id", 'import-settings-header')
import_contacts_back = ("id", "import-settings-back")

gmail_button = ("css selector", "button.icon-gmail[data-l10n-id=importGmail]")
gmail_frame = ("css selector", ".popupWindow.active iframe[data-url*=google]")
gmail_username = ("id", "Email")
gmail_password = ("id", "Passwd")
gmail_signIn_button = ("id", "signIn")
gmail_permission_accept = ("id", "submit_approve_access")
gmail_login_error_msg = ("id", "errormsg_0_Passwd")
gmail_import_frame = ("src", "gmail")  # It's in the contacts iframe.

hotmail_button = ("xpath", "//button[text()='Outlook']")
hotmail_signin_frame = ('css selector', '.popupWindow.active iframe[data-url*=live]')
hotmail_username = ("id", "i0116")
hotmail_password = ("id", "i0118")
hotmail_signIn_button = ("id", "idSIButton9")
hotmail_permission_accept = ("id", "idBtn_Accept")
hotmail_login_extra_msg = ("id", "idDiv_FSI_HeaderInfo")
hotmail_login_error_msg = ("id", "idTd_Tile_ErrorMsg_Login")
hotmail_import_frame = ("src", "live")  # It's in the contacts iframe.
hotmail_import_frame2 = ("data-url", "live")  # It's in the contacts iframe.
hotmail_header = ("css selector", '#header')

# Import
import_contacts = ('id', 'importContacts')
import_contact_header = ('id', 'import-settings-header')
import_sim_btn = ('css selector', '#import-options button.icon-sim')
reading_sim_card = ('xpath', '//h1[@id="progress-title" and contains(text(), "{}")]'.\
                    format(_("Reading from SIM card")))
importing_sim_contacts = ('xpath', '//h1[@id="progress-title" and contains(text(), "{}")]'.\
                          format(_("Importing SIM contacts")))
importing_progress = ('css selector', '#progress-activity #progress-msg')
imported_contacts_path = "//section[@id='statusMsg']/p[contains(text(), '{}')]"

import_sd_btn = ('id', 'import-sd-option')

# Export
export_export_btn = ("id", "export-action")
export_contacts = ("id", "exportContacts")
export_sd_card = ("id", "export-sd-option")
export_import_banner = ("id", "statusMsg")

export_sim_card = ("id", "export-sim-option-8934071100275319352")
export_bluetooth = ("id", "export-bluetooth-option")
