from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def waitForDeviceTimeToBe(self, 
                                  p_year=False,
                                  p_month=False,
                                  p_day=False,
                                  p_hour=False, 
                                  p_minute=False):
        #
        # Waits until the clock in the homescreen shows the date and time
        # represented by the parameters.<br>
        # All parameters are numeric, 24-hour and default to 'now'.
        #
        _now_epoch_secs=time.time()
        _now = self.getDateTimeFromEpochSecs(_now_epoch_secs)

        if not p_year   : p_year    = _now.tm_year
        if not p_month  : p_month   = _now.tm_mon
        if not p_day    : p_day     = _now.tm_mday
        if not p_hour   : p_hour    = _now.tm_hour
        if not p_minute : p_minute  = _now.tm_min

        myFrame = self.currentIframe()
        
        p_minute = p_minute + 1 #(It can take > 1 min before the device shows the new time!)
        
        x    = self.switch_24_12(p_hour)
        hh   = x[0]
        ampm = x[1]
        
        Day   = self.convertDay_NumToStr(p_day)
        Month = self.convertMonth_NumToStr(p_month)
        
        #
        # Switch to homescreen frame.
        #
        self.switchToFrame(*DOM.Home.frame_locator)
        
        #
        # Wait for time to match.
        #
        self.waitForElements( ("xpath", 
                               "//*[@id='landing-clock']/span[@class='numbers' and text()='%s:%s']" % (hh, mm) ), 
                                    "Device showing current time is now '%s:%s'" % (hh, mm), False, 60, False)

        self.waitForElements( ("xpath", 
                               "//*[@id='landing-clock']/span[@class='meridiem' and text()='%s']" % ampm ), 
                                    "Device showing current AM / PM is now '%s'" % ampm, False, 60, False)

        #
        # Wait for date to match.
        #
        self.waitForElements( ("xpath", 
                               "//*[@id='landing-date' and text()='%s, %s %s']" % (Day, Month, DayNum) ), 
                                    "Device showing current date is now '%s, %s %s'" % (Day, Month, p_day), False, 60, False)

        if myFrame != "":
            self.switchToFrame("src", myFrame)



