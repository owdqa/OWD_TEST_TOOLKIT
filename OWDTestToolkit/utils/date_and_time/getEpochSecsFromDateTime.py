from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def getEpochSecsFromDateTime(self, p_dateTime):
        #
        # Converts a date-time struct into epoch seconds.
        #
        x = p_dateTime
        return float(datetime.datetime(x.tm_year,x.tm_mon,x.tm_mday,x.tm_hour,x.tm_min).strftime('%s'))