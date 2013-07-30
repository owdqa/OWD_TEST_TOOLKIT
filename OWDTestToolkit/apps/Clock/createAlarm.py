from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def createAlarm(self, p_hour, p_min, p_label, p_repeat="Never", p_sound="Classic Buzz", p_snooze="5 minutes"):
        #
        # Create a new alarm.
        #

        #
        # Click the new alarm button.
        #
        x = self.UTILS.getElement(DOM.Clock.new_alarm_btn, "New alarm button")
        x.tap()
        
        #
        # Just set the time in the element for now (the UI isn't working for Marionette atm).
        #
        x = self.UTILS.getElement( ("xpath", "//button[@id='time-menu']"), "Time button")
        
        x = self.UTILS.getElement(DOM.Clock.time_button, "Time button")
        x.tap()
        
        myIframe = self.UTILS.currentIframe()
        self.marionette.switch_to_frame()
		
        #
        # Sort the time out into 12 hour format.
        #
        x = self.UTILS.switch_24_12(p_hour)
        t_hour = x[0]
        t_ampm = x[1]

        self.UTILS.logComment("Creating new alarm for " + str(t_hour) + ":" + str(p_min).zfill(2) + " " + t_ampm)
    
        scroller_hours = self.UTILS.getElement(
            (DOM.Clock.time_scroller[0],DOM.Clock.time_scroller[1] % "hours"),
            "Scroller for 'hours'")
        
        scroller_minutes = self.UTILS.getElement(
            (DOM.Clock.time_scroller[0],DOM.Clock.time_scroller[1] % "minutes"),
            "Scroller for 'minutes'")
        
        self.UTILS.logResult("info", "H: %s, M: %s" % (scroller_hours.text, scroller_minutes.text))
        return

        #
        # Set the hour.
        #
        self.UTILS.setScrollerVal(scroller_hours, t_hour)
        
        #
        # Set the minutes.
        #
        self.UTILS.setScrollerVal(scroller_minutes, p_min)
        
        #
        # Set the AM / PM.
        #
        scroller = self.UTILS.getElement(DOM.Clock.time_scroller_ampm, "AM/PM picker")
        currVal  = scroller.find_element(*DOM.GLOBAL.scroller_curr_val).text
        
        if t_ampm != currVal:
            if currVal == "AM":
                self.UTILS.moveScroller(scroller)
            else:
                self.UTILS.moveScroller(scroller)

        #
        # Click the OK button and return to the calling frame.
        #
        x = self.UTILS.getElement(DOM.Clock.time_picker_ok, "OK button")
        x.tap()
        self.UTILS.switch_to_frame("src", myIframe)
                
        #
        # Set the label.
        #
        x = self.UTILS.getElement(DOM.Clock.alarm_label, "Alarm label field")
        x.clear()
        x.send_keys(p_label)
        
        #
        # TODO: Set the repeat, sound and snooze.
        #
        
        #
        # Save the alarm.
        #
        x = self.UTILS.getElement(DOM.Clock.alarm_done, "Done button")
        x.tap()
        
        #
        # Check the alarm details are displayed in the clock screen.
        #
        self.checkAlarmPreview(t_hour, p_min, t_ampm, p_label, p_repeat)
        
