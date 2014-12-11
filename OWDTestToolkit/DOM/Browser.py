from OWDTestToolkit.utils.i18nsetup import I18nSetup
_ = I18nSetup(I18nSetup).setup()


frame_locator = ('src', 'browser')
browser_page_frame = ('mozbrowser', "")
url_input = ('id', 'url-input')
url_go_button = ('id', 'url-button')
throbber = ("id", "throbber")
secure_icon = ("id", "ssl-indicator")

awesome_cancel_btn = ("id", "awesomescreen-cancel-button")
awesome_top_sites_tab = ("id", "top-sites-tab")
awesome_bookmarks_tab = ("id", "bookmarks-tab")
awesome_history_tab = ("id", "history-tab")
awesome_top_sites_links = ("xpath", "//*[@id='top-sites']//li/a")
awesome_bookmarks_links = ("xpath", "//*[@id='bookmarks']//li/a")
awesome_history_links = ("xpath", "//*[@id='history']//li/a")

search_result_links = ("xpath", "//div[@id='search']//a")

open_in_new_tab_button = ("xpath", "//button[contains(text(), 'Open link in new tab')]")
new_tab_screen = ("id", "startscreen")

tab_screen = ("id", "main-screen")

tab_tray_counter = ("id", "tabs-badge")
tab_tray_open = ("id", "more-tabs")
tab_tray_new_tab_btn = ("id", "new-tab-button")
tab_tray_settings_btn = ("id", "settings-button")
tab_tray_screen = ("class name", "tabs-screen")
tab_tray_new_tab_btn = ("id", "new-tab-button")
tab_tray_tab_panels = ("xpath", "//div[@id='tab-panels']//li/a")
tab_tray_tab_list = ("xpath", "//div[@id='tabs-list']//li/a")
tab_tray_tab_list_curr = ("xpath", "//div[@id='tabs-list']//li[@class='current']/a")

tab_tray_tab_item_close = ("xpath", "//button[@class='close']")
tab_tray_tab_item_image = ("tag name", "div")
tab_tray_tab_item_title = ("tag name", "span")

settings_button = ("id", "settings-button")
settings_header = ("xpath", "//header[@id='settings-header']")

website_frame = ("css selector", "iframe.browser-tab")
page_title = ('xpath', ".//*[@id='results']/ul//h5[text()='{}']".format(_("Problemloadingpage")))
page_problem = ("xpath", "//*[text()='{}']".format(_("Problemloadingpage")))

bookmarkmenu_button = ("id", "bookmark-button")
bookmark_button = ('id', 'bookmark-menu-add')
bookmark_remove_btn = ('id', 'bookmark-menu-remove')
bookmarks_tab = ('id', 'bookmarks-tab')
bookmark_by_title = ('xpath', '//section[@id="bookmarks"]//li//h5[contains(text(), "{}")]')
bookmark_item = ("xpath", '//section[@id="bookmarks"]//a[@href="{}"]')

embarrasing_tag = ('xpath', '//h3[@data-l10n-id="this-is-embarrassing"]')
embarrasing_reload = ('id', 'try-reloading')
no_network_error = ('css selector', '#error-title[data-l10n-id=noNetwork]')

understand_risks = ('id', 'expertContentHeading')
add_permanent_exception = ('id', 'permanentExceptionButton')
