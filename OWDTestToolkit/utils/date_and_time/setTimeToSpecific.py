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
        # All parameters will default to 'now'.
        #
        _now_epoch_secs=time.time()
        _now = self.getDateTimeFromEpochSecs(_now_epoch_secs)

        if p_year   == "NOW": p_year    = _now.tm_year
        if p_month  == "NOW": p_month   = _now.tm_mon
        if p_day    == "NOW": p_day     = _now.tm_mday
        if p_hour   == "NOW": p_hour    = _now.tm_hour
        if p_minute == "NOW": p_minute  = _now.tm_min
        
        y = time.strptime("%s/%s/%s %s:%s" % \
                          (p_year,
                           p_month,
                           p_day,
                           p_hour,
                           p_minute), 
                          "%Y/%m/%d %H:%M")

        _seconds_since_epoch = self.getEpochSecsFromDateTime(y)
                
        self.data_layer.set_time(_seconds_since_epoch * 1000)
        
        self.waitForDeviceTimeToBe(p_year,
                                   p_month,
                                   p_day,
                                   p_hour,
                                   p_minute)



    
    
    