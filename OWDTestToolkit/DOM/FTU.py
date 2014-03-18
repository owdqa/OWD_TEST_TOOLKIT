# TODO: Check this identifier
frame_locator = ('src', 'ftu')

language_list       = ('xpath', ".//*[@id='languages']/article/ul/li/label/p")
language_Sel_xpath  = '//li[ starts-with( descendant-or-self::*/text(),"%s" ) ]'
next_button         = ('id', 'forward')

section_cell_data   = ('id', 'data_3g')
dataconn_switch     = ('xpath', '//li/aside[ starts-with( descendant-or-self::*/@id,"data-connection-switch" ) ]')

wifi_networks_list  = ('css selector', 'ul#networks-list li')
wifi_login_user     = ('id', 'wifi_user')
wifi_login_pass     = ('id', 'wifi_password')
wifi_login_join     = ('id', 'wifi-join-button')

timezone            = ('id', 'date_and_time')
timezone_continent  = ('id', 'tz-region')
timezone_city       = ('id', 'tz-city')
timezone_title      = ('id', 'time-zone-title')
timezone_buttons    = ('xpath', '//button[text()="Change"]')

privacy_email       = ('id', 'newsletter-input')

tour_start_btn      = ('id', 'lets-go-button')
tour_skip_btn       = ('id', 'skip-tutorial-button')
tour_next_btn       = ('id', 'forwardTutorial')
tour_finished_btn   = ('id', 'tutorialFinished')
