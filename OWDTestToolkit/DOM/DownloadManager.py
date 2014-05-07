statusbar_new_notif      = ('xpath', ".//*[@id='desktop-notifications-container']/div[@class='notification']/div[contains(text(),'%s')]")
new_download_popup_detail     = ("xpath", "//div[@id='toaster-detail' and contains(text(),'%s')]")
new_download_popup_title      = ("xpath", "//div[@id='toaster-title' and contains(text(),'%s')]")

download_list = ("id", "downloadList")

download_element = ("xpath", ".//li[@data-url='%s']")
download_element_progress = ("xpath", ".//li[@data-url='%s']/progress")
download_element_button = ("xpath", "//*[@id='%s']/aside[2]")
download_element_button_position = ("xpath", "//section[@id='downloadList']/ul/li[{}]/aside[@class='pack-end']")
download_element_checkbox = ("xpath",".//li[@data-url='%s']/label/input")
download_status_text = ("xpath", "//*[@id='%s']/p[2]")
download_status_text_position= ("xpath", "//section[@id='downloadList']/ul/li[{}]/p[@class='info']")
download_status = ("xpath", "//*[@id='%s']")
download_status_position = ("xpath", "//section[@id='downloadList']/ul/li[{}]")

download_confirm = ("xpath", "//*[@id='downloadConfirmUI']")
download_confirm_no = ("xpath", "//*[@id='downloadConfirmUI']/section/menu/button[1]")
download_confirm_yes = ("xpath", "//*[@id='downloadConfirmUI']/section/menu/button[2]")
download__yes = ("xpath", "//*[@id='downloadConfirmUI']/section/menu/button[2]")

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
ownload_file_option_wallpaper = ("id", "WALLPAPER")
download_file_option_cancel = ("id", "CANCEL")


