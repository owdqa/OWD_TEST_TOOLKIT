from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def getEpochSecsFromDateTime(self, p_dateTime):
        #
        # Converts a date-time struct into epoch seconds. If p_dateTime is teh object returned
        # from getDateTimeFromEpochSecs() then it will handle that too.
        #
        x = p_dateTime
        
        result = False
        try:
            # This is a standard date-time struct.
            result = float(datetime.datetime(x.tm_year,x.tm_mon,x.tm_mday,x.tm_hour,x.tm_min).strftime('%s'))
        except:
            # This is the return object from getDateTimeFromEpochSecs().
            result = float(datetime.datetime(x.year,x.mon,x.mday,x.hour,x.min).strftime('%s'))
            
        return result