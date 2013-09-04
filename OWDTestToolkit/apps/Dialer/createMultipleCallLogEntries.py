from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def createMultipleCallLogEntries(self, p_num, p_amount):
        #
        # Put a number in the call log multiple times 
        # (done by manipulating the device time).
        # Leaves you in the call log.
        #
        x = self.UTILS.getDateTimeFromEpochSecs(time.time())
        
        for i in range(0, p_amount):
            _day = x.mday-i
            _mon = x.mon
            
            if _day < 1:
                #
                # Jump back a month as well.
                #
                _day = 28 #(just to be sure!)
                _mon = x.mon -1
                
            self.UTILS.setTimeToSpecific(p_day=_day, p_month=_mon)
            
            self.enterNumber(p_num)
            self.callThisNumber()
            time.sleep(2)
            self.hangUp()
            
        #
        # Open the call log to finish.
        #
        self.UTILS.checkMarionetteOK()
        self.launch()
        self.openCallLog()


        
