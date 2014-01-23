frame_locator           = ('src', 'video')

thumbnails              = ("xpath", "//li[@class='thumbnail']//div[@class='details']")
thumb_durations         = ("xpath", "/html/body/ul/li/ul/li/div/div[3]/span[2]")
video_frame             = ('id', 'player')
video_loaded            = ('css selector', 'video[style]')
current_video_duration  = ("xpath", "//*[@id='duration-text']")

done_button             = ("xpath", "//*[@id='picker-done']")
