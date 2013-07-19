from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def getDateTimeFromEpochSecs(self, p_seconds_since_epoch):
        #
        # Returns struct containing date and time strings
        # converted from 'seconds since epoch' (now = "time.time()").<br>
        # The result array elements are as follows:<br>
        # <pre>
        # Attribute   Field               Values<br>
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
        return time.localtime(p_seconds_since_epoch)
        