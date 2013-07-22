from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def waitForDisplayedTimeToBe(self, p_dateTime):
        #
        # Waits for the homescreen todisplay the desired
        # date and time (takes a 'datetime' object).
        #
        
        # Get day name and month name.
        days = [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday",
                ]
        
        months = [
                  "January",
                  "February",
                  "March",
                  "April",
                  "May",
                  "June",
                  "July",
                  "August",
                  "September",
                  "October",
                  "November",
                  "December",
                  ]
        
        _day_name   = days[p_dateTime.tm_wday]
        _month_name = months[p_dateTime.tm_mon - 1]
        
        # Convert hours to 12 hour and get minutes.
        x       = self.switch_24_12(p_dateTime.tm_hour)
        _hh     = x[0]
        _ampm   = x[1]
        
        # Build the strings we're expecting to see.
        _time_str   = "%s:%s" % (_hh, str(p_dateTime.tm_min).zfill(2))
        _ampm_str   = _ampm
        _date_str   = "%s, %s %s" % (_day_name, _month_name, p_dateTime.tm_mday)
        
        #
        # Now switch to the homescreen and wait for the elements to match the
        # desired date and time.
        #
        myFrame = self.currentIframe()
        self.switchToFrame(*DOM.Home.frame_locator)
        
        # Time.
        self.waitForElements( ("xpath", DOM.Home.datetime_time_xpath % _time_str),
                                    "Time matching '%s'" % _time_str, True, 60, False)
        
        self.waitForElements( ("xpath", DOM.Home.datetime_ampm_xpath % _ampm_str),
                                    "AM / PM matching '%s'" % _ampm_str, True, 60, False)
        
        
        self.waitForElements( ("xpath", DOM.Home.datetime_date_xpath % _date_str),
                                    "Day name is '%s'" % _date_str, True, 60, False)
        
        if myFrame != '':
            self.UTILS.switchToFrame("src", myFrame)
        
        
        
        
        
        
        
        