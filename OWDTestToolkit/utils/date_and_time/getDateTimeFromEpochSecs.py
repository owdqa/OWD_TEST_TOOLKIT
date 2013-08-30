from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def getDateTimeFromEpochSecs(self, p_seconds_since_epoch):
        #
        # Returns struct containing date and time strings
        # converted from 'seconds since epoch' 
        # (for 'today' you would use: "getDateTimeFromEpochSecs(int(time.time()))").<br>
        # The result array elements are as follows:<br>
        # <pre>
        # Attribute   Field               Values<br>
        # day_name    Day                 "Monday" to "Friday"<br>
        # month_name  Day                 "january" to "December"<br>
        # tm_mday     Day                 1 to 31<br>
        # tm_year     4-digit year        2008<br>
        # tm_mon      Month               1 to 12<br>
        # tm_mday     Day                 1 to 31<br>
        # tm_hour     Hour                0 to 23<br>
        # tm_min      Minute              0 to 59<br>
        # tm_sec      Second              0 to 61 (60 or 61 are leap-seconds)<br>
        # tm_wday     Day of Week         0 to 6 (0 is Monday)<br>
        # tm_yday     Day of year         1 to 366 (Julian day)<br>
        # tm_isdst    Daylight savings    -1, 0, 1, -1 means library determines DST<br>
        # </pre>
        # <br>
        # Example:<br>
        # <pre>
        # x = self.UTILS.getDateTimeFromEpochSecs(_myTime)<br>
        # self.UTILS.logResults(x.tm_wday)<br>
        # <pre>
        #
        _val = time.localtime(p_seconds_since_epoch)
        
        _days   = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        _months = ["January"    , "February"    , "March"   , "April", 
                   "May"        , "June"        , "July"    , "August", 
                   "September"  , "October"     , "November", "December"]
        
        _day_name   = _days[_val.tm_wday]
        _month_name = _months[_val.tm_mon-1]

        from collections import namedtuple        
        x = namedtuple("x", 
                       "tm_year    " \
                       "tm_mon     " \
                       "tm_mday    " \
                       "tm_hour    " \
                       "tm_min     " \
                       "tm_sec     " \
                       "tm_wday    " \
                       "tm_yday    " \
                       "tm_isdst   " \
                       "day_name   " \
                       "month_name "
                       ) 

        return x(_val.tm_year,
                 _val.tm_mon,
                 _val.tm_mday,
                 _val.tm_hour,
                 _val.tm_min,
                 _val.tm_sec,
                 _val.tm_wday,
                 _val.tm_yday,
                 _val.tm_isdst,
                 _day_name,
                 _month_name)
    
    