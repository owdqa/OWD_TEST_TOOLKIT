from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def convertMonth_NumToStr(self, p_month_num):
        #
        # Converts a 'month of year' number to a day string.
        #
        months = ["January", 
                  "February", 
                  "March", 
                  "April", 
                  "May", 
                  "June", 
                  "July", 
                  "August", 
                  "September", 
                  "October", 
                  "November",
                  "December"]
        
        return months[p_month_num - 1]