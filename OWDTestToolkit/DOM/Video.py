frame_locator           = ('src', 'video')

thumbnails              = ("xpath", "//li[@class='thumbnail']//div[@class='details']")
thumb_durations         = ("xpath", "//li[@class='thumbnail']//span[@class='after']")
video_frame             = ('id', 'player')
video_loaded            = ('css selector', 'video[style]')
current_video_duration  = ("xpath", "//*[@id='duration-text']")

done_button             = ("xpath", "//*[@id='picker-done']")
