from OWDTestToolkit.utils.i18nsetup import I18nSetup
_ = I18nSetup(I18nSetup).setup()


# TODO: Check this identifier
frame_locator = ('src', 'facebook')

import GLOBAL
friends_header = ('xpath', GLOBAL.app_head_specific.format(_('Facebook Friends')))
friends_list = ('css selector', "li.block-item")
link_friends_list = ('css selector', "#friends-list li[data-visited=true] a")
friend_link_path = '//ol[@id="friends-list"]//li//p[contains(text(),"{}")]/..'
# link_friends_list    = ('xpath', "//ol[@id='contacts-list-R']//li")
totals = ('id', 'fb-totals')

email = ("css selector", "input[name=email]")
password = ("css selector", "input[name=pass]")

login_button = ("name", "login")
install_fbowd_button = ("id", "grant_clicked")

import_frame = ("mozbrowser", "")

friends_select_all = ('id', 'select-all')
friends_deselect_all = ('id', 'deselect-all')
friends_import = ('id', 'import-action')
friends_update = ('id', 'update-action')
