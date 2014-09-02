from OWDTestToolkit.utils.i18nsetup import I18nSetup
_ = I18nSetup(I18nSetup).setup()

statusbar_new_notif = ('xpath', ".//*[@id='desktop-notifications-container']/div[@class='notification']/div[contains(text(),'{}')]")
new_download_popup_detail = ("xpath", "//div[@id='toaster-detail' and contains(text(),'{}')]")
new_download_popup_title = ("xpath", "//div[@id='toaster-title' and contains(text(),'{}')]")

download_list = ("id", "downloadList")
download_list_elems = ('xpath', "//section[@id='downloadList']/ul/li")

download_element = ("xpath", '//li[contains(@data-url, "{}")]')
download_element_progress = ("xpath", ".//li[@data-url='{}']/progress")
download_element_info = ("xpath", "//li[contains(@data-url, {})]//p[@class='info']")
#to check
download_element_button = ("xpath", "//*[@id='{}']/aside[2]")
download_element_button_position = ("xpath", "//section[@id='downloadList']/ul/li[{}]/aside[@class='pack-end']")
download_element_checkbox = ("xpath", ".//li[@data-url='{}']/label/input")
download_element_checkbox_position = ("xpath", "//section[@id='downloadList']/ul/li[{}]")

#to check
download_status_text =  ("xpath", "//section[@id='downloadList']/ul/li[contains(@data-url, '{}')]/p[@class='info']")

#
download_confirm = ("xpath", "//*[@id='downloadConfirmUI']")
download_confirm_h1 = ("xpath", "//*[@id='downloadConfirmUI']//h1")
download_confirm_p = ("xpath", "//*[@id='downloadConfirmUI']//p")
download_confirm_yes = ("xpath", "//*[@id='downloadConfirmUI']//menu/button[@class='danger']")
download_confirm_no = ("xpath", "//*[@id='downloadConfirmUI']//menu/button[not(@class='danger')]")

download_edit_button = ("id", "downloads-edit-button")
downloads_edit_header_title = ("id", "downloads-title-edit")
download_delete_button = ("id", "downloads-delete-button")

download_select_all = ("id", "downloads-edit-select-all")
download_deselect_all = ("id", "downloads-edit-deselect-all")


download_empty_list = ("id", "download-list-empty")
download_empty_list_content = ("id", "dle-text")

download_file_option_open = ("id", "OPEN")
download_file_option_share = ("id", "SHARE")
download_file_option_ringtone = ("id", "RINGTONE")
download_file_option_wallpaper = ("id", "WALLPAPER")
download_file_option_cancel = ("id", "CANCEL")
