from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def setTimeToSpecific(self, 
                          p_year=False,
                          p_month=False,
                          p_day=False,
                          p_hour=False, 
                          p_minute=False):
        #
        # Sets the device time to a specific time (always today) based on the parameters:<br>
        # <pre>
        # <b>p_year   :</b> <i>YYYY</i>, i.e. "2013"
        # <b>p_month  :</b> <i>mm</i>, i.e. "1" -> "12"
        # <b>p_day    :</b> <i>dd</i>, i.e. "1" -> "31"
        # <b>p_hour   :</b> <i>HH</i>, i.e. "0" -> "23"
        # <b>p_minute :</b> <i>MM</i>, i.e. "0" -> "59"
        # </pre><br>
        # All parameters will default to 'now'.
        #
        _now_epoch_secs=time.time()
        _now = self.getDateTimeFromEpochSecs(_now_epoch_secs)

        if not p_year   : p_year    = _now.tm_year
        if not p_month  : p_month   = _now.tm_mon
        if not p_day    : p_day     = _now.tm_mday
        if not p_hour   : p_hour    = _now.tm_hour
        if not p_minute : p_minute  = _now.tm_min
        
        self.logResult("info", "p_day : %s" % p_day)
        self.logResult("info", "nowday: %s" % _now.tm_mday)
        
        y = time.strptime("%s/%s/%s %s:%s" % \
                          (p_year,
                           p_month,
                           p_day,
                           p_hour,
                           p_minute), 
                          "%Y/%m/%d %H:%M")
        self.logResult("info", "y: %s" % y)
        _seconds_since_epoch = self.getEpochSecsFromDateTime(y)
        
        self.logResult("info", "_now                : %s" % _now_epoch_secs)
        self.logResult("info", "_seconds_since_epoch: %s" % _seconds_since_epoch)
        
        self.data_layer.set_time(_seconds_since_epoch * 1000)
        
        self.waitForDeviceTimeToBe(p_year,
                                   p_month,
                                   p_day,
                                   p_hour,
                                   p_minute)



    
    
    