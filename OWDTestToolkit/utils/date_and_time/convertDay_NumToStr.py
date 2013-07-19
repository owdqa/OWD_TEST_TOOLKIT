from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def convertDay_NumToStr(self, p_wday_num):
        #
        # Converts a 'day of week' number to a day string.
        #
        days_of_the_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        return days_of_the_week[p_wday_num]