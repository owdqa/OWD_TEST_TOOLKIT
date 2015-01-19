from OWDTestToolkit.utils.i18nsetup import I18nSetup
_ = I18nSetup(I18nSetup).setup()

frame_locator = ("css selector", "iframe.browser:not(.hidden)")
current_browser_window = ('css selector', 'div#windows div[data-manifest-name=Browser][aria-hidden=false]')
browser_app = ('css selector', 'div.browser.active')
current_browser_menu = ('css selector', 'div.browser.active div.controls button.menu-button')
browser_page_frame = ('mozbrowser', "")
url_input = ('css selector', 'div.appWindow.active[data-manifest-name=Browser] .urlbar .title')
url_go_button = ('id', 'url-button')
throbber = ("id", "throbber")
secure_icon = ("css selector", ".title[data-ssl=secure]")
rocket_bar_input = ('id', 'rocketbar-input')

bookmark_frame_locator = ('src', 'bookmark')
bookmark_done_button = ('id', 'done-button')
awesome_cancel_btn = ("id", "awesomescreen-cancel-button")
awesome_top_sites_tab = ("id", "top-sites-tab")
awesome_bookmarks_tab = ("id", "bookmarks-tab")
awesome_history_tab = ("id", "history-tab")
awesome_top_sites_links = ("xpath", "//*[@id='top-sites']//li/a")
awesome_bookmarks_links = ("xpath", "//*[@id='bookmarks']//li/a")
awesome_history_links = ("xpath", "//*[@id='history']//li/a")

search_result_links = ("css selector", "div#search-results .apps")

search_new_window = ('css selector', 'button[data-id=new-window]')
search_show_windows = ('css selector', 'button[data-id=show-windows]')
search_add_to_homescreen = ('css selector', 'button[data-id=add-to-homescreen]')
search_share = ('css selector', 'button[data-id=share]')
search_cancel = ('id', 'ctx-cancel-button')

settings_button = ("id", "settings-button")
settings_header = ("xpath", "//header[@id='settings-header']")

page_title = ('xpath', ".//*[@id='results']/ul//h5[text()='{}']".format(_("Problemloadingpage")))
page_problem = ("xpath", "//*[text()='{}']".format(_("Problemloadingpage")))

# Menu
menu_button = ('css selector', '.menu-button')
add_to_home_button = ('css selector', 'button[data-id="add-to-homescreen"]')
share_button = ('css selector', 'button[data-id="share"]')
share_to_messages_email = ('css selector', 'button[data-value="0"]')
share_to_messages_button = ('css selector', 'button[data-value="1"]')
browser_menu = ('css selector', '.contextmenu-list')

# Navigation
back_button = ('css selector', '.back-button')
forward_button = ('css selector', '.forward-button')

embarrasing_tag = ('xpath', '//h3[@data-l10n-id="this-is-embarrassing"]')
embarrasing_reload = ('id', 'try-reloading')
no_network_error = ('css selector', '#error-title[data-l10n-id=noNetwork]')

understand_risks = ('id', 'expertContentHeading')
add_permanent_exception = ('id', 'permanentExceptionButton')
