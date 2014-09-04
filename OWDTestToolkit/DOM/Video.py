frame_locator = ('src', 'video')

thumbnails = ("xpath", "//li[@class='thumbnail']//div[@class='details']")
thumb_durations = ("xpath", "/html/body/ul/li/ul/li/div/div[3]/span[2]")
video_player = ('id', 'player')
video_loaded = ('css selector', 'video[style]')
current_video_duration = ("xpath", "//*[@id='duration-text']")
video_controls = ('id', 'videoControls')

done_button = ("xpath", "//*[@id='picker-done']")
video_title = ("xpath", "//*[@id='video-title']")
