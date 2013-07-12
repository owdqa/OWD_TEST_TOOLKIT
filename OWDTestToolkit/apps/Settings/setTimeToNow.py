from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def setTimeToNow(self):
        #
        # Set date and time to 'now'.<br>
        # WARNING: DOES NOT WORK YET!!! ...<br>
        #   1. Marionette.flick() not working here.<br>
        #   2. Cannot figure out how to tell what the current value is (no 'active' setting here),
        #
        return
        self.launch()
         
        x = ("id", "menuItem-dateAndTime")
        el = self.UTILS.getElement(x, "Date & Time setting")
        el.tap()
         
        x = ("id", "clock-date")
        el = self.UTILS.getElement(x, "Date setting")
        el.tap()
         
        time.sleep(2)        
        self.marionette.switch_to_frame()
