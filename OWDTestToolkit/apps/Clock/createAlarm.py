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
        # Sort the time out into 12 hour format.
        #
        x = self.switch_24_12(p_hour)
        t_hour = x[0]
        t_ampm = x[1]

        self.UTILS.logComment("Creating new alarm for " + str(t_hour) + ":" + str(p_min).zfill(2) + " " + t_ampm)
        
        #
        # Set the hour.
        #
        self._select("hours", t_hour)
        
        #
        # Set the minutes.
        #
        self._select("minutes", p_min)
        
        #
        # Set the AM / PM.
        #
        scroller = self.UTILS.getElement(DOM.Clock.time_picker_ampm, "AM/PM picker")
        currVal  = scroller.find_element(*DOM.Clock.time_picker_curr_val).text
        
        if t_ampm != currVal:
            if currVal == "AM":
                self._scrollForward(scroller)
            else:
                self._scrollBackward(scroller)
                
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
        
