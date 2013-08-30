from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def getDateTimeFromEpochSecs(self, p_seconds_since_epoch):
        #
        # Returns struct containing date and time strings
        # converted from 'seconds since epoch' 
        # (for 'today' you would use: "getDateTimeFromEpochSecs(int(time.time()))").<br>
        # The result array elements are as follows:<br>
        # <pre>
        # Attribute   Field            Values<br>
        # day_name    Day              "Monday" to "Friday"<br>
        # month_name  Day              "january" to "December"<br>
        # mday     Day                 1 to 31<br>
        # year     4-digit year        2008 etc...<br>
        # mon      Month               1 to 12<br>
        # mday     Day                 1 to 31<br>
        # hour     Hour                0 to 23<br>
        # min      Minute              0 to 59<br>
        # sec      Second              0 to 61 (60 or 61 are leap-seconds)<br>
        # wday     Day of Week         0 to 6 (0 is Monday)<br>
        # yday     Day of year         1 to 366 (Julian day)<br>
        # isdst    Daylight savings    -1, 0, 1, -1 means library determines DST<br>
        # </pre>
        # <br>
        # Example:<br>
        # <pre>
        # _today = self.UTILS.getDateTimeFromEpochSecs( int(time.time()) )<br>
        # self.UTILS.logResults("info", "Day: %s" % _today.day_name)<br>
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
                       "year    " \
                       "mon     " \
                       "mday    " \
                       "hour    " \
                       "min     " \
                       "sec     " \
                       "wday    " \
                       "yday    " \
                       "isdst   " \
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
    
    
