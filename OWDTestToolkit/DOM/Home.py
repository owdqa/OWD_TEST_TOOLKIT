frame_locator = ("src", "verticalhome")
cards_view = ('id', 'cards-view')
lockscreen_frame = ('id', 'lockscreen')

apps = ("css selector", "div.icon")
app_icon_xpath = "//gaia-grid[@id='icons']/div[contains(@data-identifier, '{}')]"
# The /../.. at the end is necessary so that we can long_press on the element
app_name_xpath = "//gaia-grid[@id='icons']//span[@class='title' and text()='{}']/../.."

app_icon_pages = ("xpath", "//div[@id='icongrid']/div[@class='page']")
app_delete_icon_xpath = "//div[contains(@class, 'icon')]//span[text()='{}']/../..//span[@class='remove']"
app_confirm_delete = ('css selector', 'gaia-confirm[data-type=remove] button.confirm')

app_card = ('xpath', '//div[@id="cards-view"]//li[@class="card" and @data-origin="app://{}.gaiamobile.org"]')
app_close = ('css selector', '#cards-view li.card[data-origin*="{}"] .close-card')

datetime_time_xpath = "//p[@id='landing-clock']//span[@class='numbers' and text()='{}']"
datetime_ampm_xpath = "//p[@id='landing-clock']//span[@class='meridiem' and text()='{}']"
datetime_date_xpath = "//div[@id='landing-time']//p[@id='landing-date' and text()='{}']"
dock = ("xpath", "//*[contains(@class,'dockWrapper')]")
docked_apps = ("xpath", "//div[contains(@class,'dockWrapper')]//li[@class='icon']")
