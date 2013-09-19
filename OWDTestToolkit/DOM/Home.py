frame_locator        = ("src", "homescreen")
cards_view           = ('id', 'cards-view')
lockscreen_frame     = ('id', 'lockscreen')

apps                 = ("xpath", "//li[@class='icon']")
app_icon_css         = 'li.icon[aria-label="%s"]'
app_icon_pages       = ("xpath", "//div[@id='icongrid']/div[@class='page']")
app_delete_icon_xpath= "//li[@class='icon'][.//span[text()='%s']]//span[@class='options']"
app_confirm_delete   = ('id', 'confirm-dialog-confirm-button')

app_card             = ('xpath', '//div[@id="cards-view"]//li[@class="card" and @data-origin="app://%s.gaiamobile.org"]')
app_close            = ('css selector', '#cards-view li.card[data-origin*="%s"] .close-card')

datetime_time_xpath  = "//p[@id='landing-clock']//span[@class='numbers' and text()='%s']"
datetime_ampm_xpath  = "//p[@id='landing-clock']//span[@class='meridiem' and text()='%s']"
datetime_date_xpath  = "//div[@id='landing-time']//p[@id='landing-date' and text()='%s']"

dock                 = ("xpath", "//*[conatins(@class,'dockWrapper')]")
docked_apps          = ("xpath", "//div[contains(@class,'dockWrapper')]//li[@class='icon']")