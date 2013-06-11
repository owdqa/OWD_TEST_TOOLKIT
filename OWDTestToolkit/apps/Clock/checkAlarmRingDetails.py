from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def checkAlarmRingDetails(self, p_hour, p_min, p_label):
        #
        # Check details of alarm when it rings.
        #
        # NOTE: the status bar alarm is always 'visible', so you have to manually
        #       wait until the alarm is expected to have started before calling this!
        #

        #
        # The alarm screen appears in a different frame to the clock.
        # Try to access this frame a few times to give the alarm time to appear.
        #
        self.marionette.switch_to_frame()
        
        retries = 40
        while retries >= 0:            
            if self.UTILS.switchToFrame(*DOM.Clock.alarm_alert_iframe, p_quitOnError=False):
                break
            
            time.sleep(2)
            retries = retries - 1
                
                
        if retries <= 0:
            msg =   "Cannot find the iframe containing the clock! ('" + \
                    DOM.Clock.alarm_alert_iframe[0] + "', '" + \
                    DOM.Clock.alarm_alert_iframe[1] + "')."
            self.UTILS.quitTest(msg)
            
            
        #
        # Sort the time out into 12 hour format.
        #
        x = self.UTILS.switch_24_12(p_hour)
        t_hour = x[0]
        t_ampm = x[1]

        # Put the time in a format we can compare easily with.
        p_time = str(t_hour) + ":" + str(p_min).zfill(2)
        
        x = self.UTILS.getElement(DOM.Clock.alarm_alert_time, "Alarm alert time").text
        self.UTILS.TEST(x == p_time, "Correct alarm time is shown when alarm is ringing (expected '" + p_time + "', it was '" + x + "').")
        
        x = self.UTILS.getElement(DOM.Clock.alarm_alert_ampm, "Alarm alert AM/PM").text
        self.UTILS.TEST(x == t_ampm, "Correct AM / PM shown when alarm is ringing (expected '" + t_ampm + "', it was '" + x + "').")
        
        x = self.UTILS.getElement(DOM.Clock.alarm_alert_label, "Alarm alert label").text
        self.UTILS.TEST(x == p_label, "Correct label shown when alarm is ringing (expected '" + p_label + "', it was '" + x + "').")
        
        #
        # Stop the alarm.
        #
        x = self.UTILS.getElement(DOM.Clock.alarm_alert_close, "Close alert button")
        x.tap()

