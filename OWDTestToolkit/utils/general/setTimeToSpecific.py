from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def setTimeToSpecific(self, p_hour, p_minute, p_seconds):
        #
        # Sets the device time to a specific time based on the parameters
        # (hour is in 24 hour format).
        #
        h = str(p_hour)
        m = str(p_minute)
        s = str(p_seconds)
        
        _seconds_since_epoch = self.marionette.execute_script("""
                var today = new Date();
                var yr = today.getFullYear();
                var mth = today.getMonth();
                var day = today.getDate();
                return new Date(yr, mth, day, %s, %s, %s).getTime();""" % (h, m, s) )

        self.today = datetime.datetime.fromtimestamp(_seconds_since_epoch / 1000)

        # set the system date to the time
        self.data_layer.set_time(_seconds_since_epoch)

    
