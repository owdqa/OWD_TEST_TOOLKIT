from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def getDateTimeAdjusted(self, p_months=0):
        #
        # Returns struct containing date and time strings for today adjusted
        # by the parameters passed in (only months so far but I'll add more as I need to).<br>
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
        # Examples:<br>
        # <pre>
        # _today = self.UTILS.getDateTimeAdjusted(p_months=24)<br>
        # _today = self.UTILS.getDateTimeAdjusted(p_months=2)<br>
        # _today = self.UTILS.getDateTimeAdjusted(p_months=-8)<br>
        # self.UTILS.logResult("info", "New month is: %s." % _today.mon)
        # <pre>
        #
        _now = time.localtime(int(time.time()))
        
        
        #
        # Adjust MONTHS.
        #
        _mon  = _now.tm_mon
        _year = _now.tm_year
        
        _num  = p_months
        _step = 1
        if _num < 0:
            _num  = _num * -1
            _step = -1

        for i in range(0,_num):
            _mon = _mon + _step
            if _mon < 1:
                _mon  = len(_months)
                _year = _year -1
            elif _mon > 12:
                _mon  = 1
                _year = _year + 1

        
        #
        # Buld the return object.
        #
        _month_end  = [31,28,31,30,31,30,31,31,30,31,30,31]
        
        # Don't let the day / month be impossible.
        _mday = _now.tm_mday
        if _mday > _month_end[_mon]:
            _mday = _month_end[_mon]
            
        x           = datetime.date(_year,_mon,_mday)
        _day_name   = x.strftime("%A")
        _month_name = x.strftime("%B")
        
#         _day_name   = _days[_now.tm_wday]
#         _month_name = _months[_mon-1]
        
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

        return x(_year,
                 _mon,
                 _mday,
                 _now.tm_hour,
                 _now.tm_min,
                 _now.tm_sec,
                 _now.tm_wday,
                 _now.tm_yday,
                 _now.tm_isdst,
                 _day_name,
                 _month_name)
    
    
