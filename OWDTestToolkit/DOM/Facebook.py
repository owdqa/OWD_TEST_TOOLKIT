import GLOBAL
friends_header       = ('xpath', GLOBAL.app_head_specific % 'Facebook Friends')
friends_list         = ('xpath', "//li[@class='block-item']")
link_friends_list    = ('xpath', "//ol[@id='friends-list']//li[@data-visited='true']/a")
# link_friends_list    = ('xpath', "//ol[@id='contacts-list-R']//li")
totals               = ('id', 'fb-totals')

email                = ("xpath", "//input[@name='email']")
password             = ("xpath", "//input[@name='pass']")

login_button         = ("name", "login")
install_fbowd_button = ("id", "grant_clicked")

import_frame         = ("mozbrowser", "")

friends_select_all   = ('id', 'select-all')
friends_deselect_all = ('id', 'deselect-all')
friends_import       = ('id', 'import-action')
friends_update       = ('id', 'update-action')
