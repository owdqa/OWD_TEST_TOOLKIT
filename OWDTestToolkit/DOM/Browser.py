frame_locator           = ('src', 'browser')
browser_page_frame      = ('mozbrowser', "")
url_input               = ('id', 'url-input')
url_go_button           = ('id', 'url-button')
throbber                = ("xpath", "//*[@id='throbber' and @class='loading']")

browser_iframe_xpath    = ("xpath", "//iframe[@class='browser-tab']")

awesome_cancel_btn      = ("id", "awesomescreen-cancel-button")
awesome_top_sites_tab   = ("id", "top-sites-tab")
awesome_bookmarks_tab   = ("id", "bookmarks-tab")
awesome_history_tab     = ("id", "history-tab")
awesome_top_sites_links = ("xpath", "//*[@id='top-sites']//li/a")
awesome_bookmarks_links = ("xpath", "//*[@id='bookmarks']//li/a")
awesome_history_links   = ("xpath", "//*[@id='history']//li/a")

search_result_links     = ("xpath", "//div[@id='search']//a")

open_in_new_tab_button  = ("xpath", "//button[contains(text(), 'Open link in new tab')]")
new_tab_screen          = ("id", "startscreen")

tab_screen              = ("id", "main-screen")

tab_tray_counter        = ("id", "tabs-badge")
tab_tray_open           = ("id", "more-tabs")
tab_tray_new_tab_btn    = ("id", "new-tab-button")
tab_tray_settings_btn   = ("id", "settings-button")
tab_tray_screen         = ("class name", "tabs-screen")
tab_tray_new_tab_btn    = ("id", "new-tab-button")
tab_tray_tab_panels     = ("xpath", "//div[@id='tab-panels']//li/a")
tab_tray_tab_list       = ("xpath", "//div[@id='tabs-list']//li/a")
tab_tray_tab_list_curr  = ("xpath", "//div[@id='tabs-list']//li[@class='current']/a")

tab_tray_tab_item_close = ("xpath", "//button[@class='close']") # Use these with :
tab_tray_tab_item_image = ("tag name", "div")                   #   x = getElement(...tab_tray_tab_list)[0]
tab_tray_tab_item_title = ("tag name", "span")                  #   y = x.find_element(<these>)


settings_button         = ("id", "settings-button")
settings_header         = ("xpath", "//header[@id='settings-header']")

website_frame           = ("class", "browser-tab")
page_title              = ('xpath', ".//*[@id='results']/ul//h5[text()='Problemloadingpage']")
page_problem            = ("xpath", "//*[text()='Problem loading page']")
