from collections import namedtuple
import time
import datetime
from OWDTestToolkit import DOM


class date_and_time(object):

    def __init__(self, parent):
        self.parent = parent
        self.marionette = parent.marionette

    def getDateTimeFromEpochSecs(self, seconds_since_epoch):
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
        # _today = self.UTILS.date_and_time.getDateTimeFromEpochSecs( int(time.time()) )<br>
        # self.UTILS.reporting.logResults("info", "Day: %s" % _today.day_name)<br>
        # <pre>
        #
        value = time.localtime(seconds_since_epoch)

        x = datetime.date(value.tm_year, value.tm_mon, value.tm_mday)
        day_name = x.strftime("%A")
        month_name = x.strftime("%b")

        x = namedtuple("x", "year    " "mon     " "mday    " "hour    " "min     " "sec     " "wday    " \
                       "yday    " "isdst   " "day_name   " "month_name ")

        return x(value.tm_year, value.tm_mon, value.tm_mday, value.tm_hour, value.tm_min, value.tm_sec,
                 value.tm_wday, value.tm_yday, value.tm_isdst, day_name, month_name)

    def getEpochSecsFromDateTime(self, date_time):
        """
        Converts a date-time struct into epoch seconds. If date_time is the object returned
        from getDateTimeFromEpochSecs() then it will handle that too.
        """
        x = date_time

        result = False
        try:
            # This is a standard date-time struct.
            result = float(datetime.datetime(x.tm_year, x.tm_mon, x.tm_mday, x.tm_hour, x.tm_min).strftime('%s'))
        except:
            # This is the return object from getDateTimeFromEpochSecs().
            result = float(datetime.datetime(x.year, x.mon, x.mday, x.hour, x.min).strftime('%s'))

        return result

    def setTimeToNow(self, continent=False, city=False):
        """
        Set the phone's time (using gaia data_layer instead of the UI).
        <b>NOTE:</b> Also sets the timezone (continent and city).
        """
        _continent = continent if continent else self.parent.general.get_config_variable("region", "common")
        _city = city if city else self.parent.general.get_config_variable("city", "common")

        self.parent.reporting.logResult("info", "(Setting timezone and time based on {} / {}.)".format(_continent, _city))

        self.parent.data_layer.set_setting('time.timezone', _continent + "/" + _city)
        self.parent.data_layer.set_time(time.time() * 1000)

    def setTimeToSpecific(self, p_year="NOW", p_month="NOW", p_day="NOW", p_hour="NOW", p_minute="NOW"):
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
        _now_epoch_secs = time.time()
        _now = self.getDateTimeFromEpochSecs(_now_epoch_secs)

        if p_year == "NOW":
            p_year = _now.year
        if p_month == "NOW":
            p_month = _now.mon
        if p_day == "NOW":
            p_day = _now.mday
        if p_hour == "NOW":
            p_hour = _now.hour
        if p_minute == "NOW":
            p_minute = _now.min

        _dateTime = time.strptime("{}/{}/{} {}:{}".format(p_year, p_month, p_day, p_hour, p_minute), "%Y/%m/%d %H:%M")

        _seconds_since_epoch = self.getEpochSecsFromDateTime(_dateTime)

        self.parent.data_layer.set_time(_seconds_since_epoch * 1000)

        self.waitForDeviceTimeToBe(p_year, p_month, p_day, p_hour, p_minute)

        return _dateTime

    def switch_24_12(self, hour):
        """
        Switches a 24-hour number to 12-hour format.
        Returns array: ["hour" (12 hour format), "ampm"] based on a 24hour "hour".
        """
        if hour >= 12:
            t_ampm = "PM"
            t_hour = hour - 12 if hour > 12 else hour
        else:
            t_hour = hour
            t_ampm = "AM"

        return (t_hour, t_ampm)

    def waitForDeviceTimeToBe(self, p_year="NOW", p_month="NOW", p_day="NOW", p_hour="NOW", p_minute="NOW"):
        """
        Waits until the clock in the homescreen shows the date and time
        represented by the parameters.<br>
        All parameters are numeric, 24-hour and default to 'now'.
        """
        _now_epoch_secs = time.time()
        _now = self.getDateTimeFromEpochSecs(_now_epoch_secs)

        if p_year == "NOW":
            p_year = _now.year
        if p_month == "NOW":
            p_month = _now.mon
        if p_day == "NOW":
            p_day = _now.mday
        if p_hour == "NOW":
            p_hour = _now.hour
        if p_minute == "NOW":
            p_minute = _now.min

        # Wait for device date and time to match (1 minute timeout).
        time_match = False
        for i in range(30):
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

            t_expected = "{}/{}/{} {}:{}".format(p_year, p_month, p_day, p_hour, p_minute)
            t_actual = "{}/{}/{} {}:{}".format(_devtime[0], _devtime[1], _devtime[2],
                                                       int(_devtime[3]), int(_devtime[4]))

            if t_expected == t_actual:
                time_match = True
                break

            time.sleep(2)

        self.parent.test.test(time_match, "Device time matched \"{}/{}/{} {:02d}:{:02d}\" within 60s "\
                              "(It was \"{}/{}/{} {:02d}:{:02d}\")".format(p_year, p_month, p_day, p_hour, p_minute,
                               _devtime[0], _devtime[1], _devtime[2], int(_devtime[3]), int(_devtime[4])))

    def waitForDisplayedTimeToBe(self, date_time):
        """
        Waits for the homescreen to display the desired
        date and time (takes a 'datetime' object).
        """

        # Get day name and month name.
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        months = ["January", "February", "March", "April", "May", "June", "July", "August",
                  "September", "October", "November", "December"]

        _day_name = days[date_time.tm_wday]
        _month_name = months[date_time.tm_mon - 1]

        # Convert hours to 12 hour and get minutes.
        x = self.switch_24_12(date_time.tm_hour)
        _hh = x[0]
        _ampm = x[1]

        # Build the strings we're expecting to see.
        _time_str = "{}:{:02d}".format(_hh, date_time.tm_min)
        _ampm_str = _ampm
        _date_str = "{}, {} {}".format(_day_name, _month_name, date_time.tm_mday)
        """
        Now switch to the homescreen and wait for the elements to match the
        desired date and time.
        """
        myFrame = self.currentIframe()
        self.parent.iframe.switchToFrame(*DOM.Home.frame_locator)

        # Time.
        self.parent.element.waitForElements(("xpath", DOM.Home.datetime_time_xpath.format(_time_str)),
                                    "Time matching '{}'".format(_time_str), True, 60, False)
        self.parent.element.waitForElements(("xpath", DOM.Home.datetime_ampm_xpath.format(_ampm_str)),
                                    "AM / PM matching '{}'".format(_ampm_str), True, 60, False)
        self.parent.element.waitForElements(("xpath", DOM.Home.datetime_date_xpath.format(_date_str)),
                                    "Day name is '{}'".format(_date_str), True, 60, False)

        if myFrame != '':

            # Switch back to the frame we started in.
            self.parent.iframe.switchToFrame("src", myFrame)
