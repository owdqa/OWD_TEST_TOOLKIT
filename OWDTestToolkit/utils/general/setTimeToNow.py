from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def setTimeToNow(self, p_continent=False, p_city=False):
        #
        # Set the phone's time (using gaia data_layer instead of the UI).
        #
        _continent = p_continent if p_continent else self.get_os_variable("GLOBAL_YOUR_CONTINENT")
        _city      = p_city      if p_city      else self.get_os_variable("GLOBAL_YOUR_CITY")
        
        self.logResult("info", "(Setting timezone and time based on " + _continent + " / " + _city + ".)")
        
        self.parent.data_layer.set_setting('time.timezone', _continent + "/" + _city)
        self.parent.data_layer.set_time(time.time() * 1000)
        
