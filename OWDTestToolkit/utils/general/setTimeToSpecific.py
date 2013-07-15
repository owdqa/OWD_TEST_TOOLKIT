from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def setTimeToSpecific(self, p_hour, p_minute):
        #
        # Sets the device time to a specific time based on the parameters
        # (hour is in 24 hour format).
        #
        if p_hour == 0:
            p_hour = 0;
        if p_minute == 0:
            p_minute = 0;
            
        h = str(p_hour)
        m = str(p_minute)
        
        self.logResult("info", "h: " + h + ", m: " + m)
        
        _seconds_since_epoch = self.marionette.execute_script("""
                var today = new Date();
                var yr = today.getFullYear();
                var mth = today.getMonth();
                var day = today.getDate();
                return new Date(yr, mth, day, %s, %s, 1).getTime();""" % (h, m) )

        self.today = datetime.datetime.fromtimestamp(_seconds_since_epoch / 1000)

        # set the system date to the time
        self.data_layer.set_time(_seconds_since_epoch)
        
        #
        # I can't find a setting to just get the device time, so I wait for the clock
        # in the homescreen to update.
        #
        myFrame = self.currentIframe()
        self.switchToFrame(*DOM.Home.frame_locator)
        
        if p_minute < 10:
            m = m.zfill(2)
            
        x = self.switch_24_12(p_hour)
        h = str(x[0])
        ampm = x[1]
            
        self.waitForElements( ("xpath", "//*[@id='landing-clock']/span[@class='numbers' and text()='" + h + ":" + m + "']"), 
                                    "Device showing current time is now " + h + ":" + m, False, 150)

        self.waitForElements( ("xpath", "//*[@id='landing-clock']/span[@class='meridiem' and text()='" + ampm + "']"), 
                              "AM/PM setting is correct", False, 5)

        if myFrame != "":
            self.switchToFrame("src", myFrame)
