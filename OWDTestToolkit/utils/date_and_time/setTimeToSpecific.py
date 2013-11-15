from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def setTimeToSpecific(self, 
                          p_year="NOW",
                          p_month="NOW",
                          p_day="NOW",
                          p_hour="NOW", 
                          p_minute="NOW"):
        #
        # Sets the device time to a specific time (always today) based on the parameters:<br>
        # <pre>
        # <b>p_year   :</b> <i>YYYY</i>, i.e. "2013"<br>
        # <b>p_month  :</b> <i>mm</i>, i.e. "1" -> "12"<br>
        # <b>p_day    :</b> <i>dd</i>, i.e. "1" -> "31"<br>
        # <b>p_hour   :</b> <i>HH</i>, i.e. "0" -> "23"<br>
        # <b>p_minute :</b> <i>MM</i>, i.e. "0" -> "59"<br>
        # </pre><br>
        # All parameters will default to 'now'.<br>
        # Returns a 'dateTime' object for the new date and time:
        # <pre>
        # Attribute   Field            Values<br>
        # tm_mday     Day                 1 to 31<br>
        # tm_year     4-digit year        2008 etc...<br>
        # tm_mon      Month               1 to 12<br>
        # tm_mday     Day                 1 to 31<br>
        # tm_hour     Hour                0 to 23<br>
        # tm_min      Minute              0 to 59<br>
        # tm_sec      Second              0 to 61 (60 or 61 are leap-seconds)<br>
        # tm_wday     Day of Week         0 to 6 (0 is Monday)<br>
        # tm_yday     Day of year         1 to 366 (Julian day)<br>
        # tm_isdst    Daylight savings    -1, 0, 1, -1 means library determines DST<br>
        # </pre>
        #
        _now_epoch_secs=time.time()
        _now = self.getDateTimeFromEpochSecs(_now_epoch_secs)

        if p_year   == "NOW": p_year    = _now.year
        if p_month  == "NOW": p_month   = _now.mon
        if p_day    == "NOW": p_day     = _now.mday
        if p_hour   == "NOW": p_hour    = _now.hour
        if p_minute == "NOW": p_minute  = _now.min
        
        _dateTime = time.strptime("%s/%s/%s %s:%s" % \
                          (p_year,
                           p_month,
                           p_day,
                           p_hour,
                           p_minute), 
                          "%Y/%m/%d %H:%M")

        _seconds_since_epoch = self.getEpochSecsFromDateTime(_dateTime)
                
        self.data_layer.set_time(_seconds_since_epoch * 1000)

        self.waitForDeviceTimeToBe(p_year,
                                       p_month,
                                       p_day,
                                       p_hour,
                                       p_minute)

        #self.waitForDisplayedTimeToBe(_dateTime)

        return _dateTime