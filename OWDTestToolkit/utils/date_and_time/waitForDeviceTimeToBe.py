from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def waitForDeviceTimeToBe(self, 
                                  p_year="NOW",
                                  p_month="NOW",
                                  p_day="NOW",
                                  p_hour="NOW", 
                                  p_minute="NOW"):
        #
        # Waits until the clock in the homescreen shows the date and time
        # represented by the parameters.<br>
        # All parameters are numeric, 24-hour and default to 'now'.
        #
        _now_epoch_secs=time.time()
        _now = self.getDateTimeFromEpochSecs(_now_epoch_secs)

        if p_year   == "NOW": p_year    = _now.tm_year
        if p_month  == "NOW": p_month   = _now.tm_mon
        if p_day    == "NOW": p_day     = _now.tm_mday
        if p_hour   == "NOW": p_hour    = _now.tm_hour
        if p_minute == "NOW": p_minute  = _now.tm_min

        #
        # Wait for device date and time to match (1 minite timeout).
        #
        time_match = False
        for i in range(1,30):
            x = self.marionette.execute_script("""
                    var today = new Date();
                    var yr = today.getFullYear();
                    var mth = today.getMonth() + 1;
                    var day = today.getDate();
                    var hours = today.getHours();
                    var mins = today.getMinutes();
                    var x = yr + "," + mth + "," + day + "," + hours + "," + mins;
                    return x;""")
        
            _devtime = x.split(",")
            
            t_expected = "%s/%s/%s %s:%s" % (p_year, p_month, p_day, p_hour, p_minute)
            t_actual   = "%s/%s/%s %s:%s" % (_devtime[0], _devtime[1], _devtime[2], _devtime[3], _devtime[4])
            
            if  t_expected == t_actual:
                time_match = True
                break
            
            time.sleep(2)
                
        self.TEST(time_match, "Device time matched \"%s/%s/%s %s:%s\" within 60s (It was \"%s/%s/%s %s:%s\")" % \
                              (p_year, p_month, p_day, str(p_hour).zfill(2), str(p_minute).zfill(2),
                               _devtime[0], _devtime[1], _devtime[2], str(_devtime[3]).zfill(2), str(_devtime[4]).zfill(2)))

