import time
from gaiatest   import GaiaTestCase
from marionette import Marionette
from marionette import Actions
from OWDTestToolkit import *

class AppClock(GaiaTestCase):
    
    #
    # When you create your instance of this class, include the
    # "self" object so we can access the calling class' objects.
    #
    def __init__(self, p_parent):
        self.apps       = p_parent.apps
        self.data_layer = p_parent.data_layer
        self.marionette = p_parent.marionette
        self.UTILS      = p_parent.UTILS



    def launch(self):
        #
        # Launch the app.
        #
        self.apps.kill_all()
        self.app = self.apps.launch('Clock')
        self.UTILS.waitForNotElements(DOM.GLOBAL.loading_overlay, "Clock app - loading overlay");

    def deleteAllAlarms(self):
        #
        # Deletes all current alarms.
        #
        
        #
        # "self.data_layer.delete_all_alarms()" isn't workng at the moment, so...
        #
        while True:
            try:
                x = self.marionette.find_elements(*DOM.Clock.alarm_preview_alarms)
            except:
                #
                # No alarms returned, so just move on...
                #
                break
            else:
                if len(x) <= 0: break
                
                #
                # Some alarms - delete the first one (we need to reload the
                # list each time because it changes everytime we delete
                # an alarm).
                #
                x[0].tap()
                x = self.UTILS.getElement(DOM.Clock.alarm_delete_button, "Alarm delete button")
                x.tap()
                time.sleep(1)
        
    def switch_24_12(self, p_hour):
        #
        # Returns array "hour" (12 hour format) and "ampm" based on a 24hour "p_hour".
        #
        if p_hour >= 12:
            t_ampm = "PM"
            if p_hour > 12:
                t_hour = p_hour - 12
            else:
                t_hour = p_hour
        else:
            t_hour = p_hour
            t_ampm = "AM"
        
        return (t_hour, t_ampm)
        
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
        
    def checkAlarmPreview(self, p_hour, p_min, p_ampm, p_label, p_repeat):
        #
        # Verify the alarm details in the clock screen.
        #

        #
        # Put the time in a format we can compare easily with.
        #
        p_time = str(p_hour) + ":" + str(p_min).zfill(2)
        
        alarms = self.UTILS.getElements(DOM.Clock.alarm_preview_alarms, "Alarm preview list")
        
        foundBool = False
        for alarm in alarms:
            alarm_time   = alarm.find_element(*DOM.Clock.alarm_preview_time).text
            alarm_ampm   = alarm.find_element(*DOM.Clock.alarm_preview_ampm).text
            alarm_label  = alarm.find_element(*DOM.Clock.alarm_preview_label).text
            alarm_repeat = alarm.find_element(*DOM.Clock.alarm_preview_repeat).text
            
            if  p_time      == alarm_time   and \
                p_ampm      == alarm_ampm:
                    foundBool = True
                    self.UTILS.TEST(p_label == alarm_label, 
                                    "Alarm description is correct in Clock screen preview.")
                    break
                
        self.UTILS.TEST(foundBool, 
                        "Alarm preview is found in Clock screen for " + p_time + p_ampm + ".")
             
             
    def checkStatusbarIcon(self):
        #
        # Check for the little alarm bell icon in the statusbar of the
        # homescreen.
        #
        self.marionette.switch_to_frame()
        boolOK = True
        try:
            self.UTILS.waitForElements(DOM.Clock.alarm_notifier, "Alarm notification", True, 20, False)
        except:
            boolOK = False
        
        return boolOK
                
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
        x = self.switch_24_12(p_hour)
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

    def _calcStep(self, p_scroller):
        #
        # Calculates how big the step should be
        # when 'flick'ing a scroller (based on the
        # number of elements in the scroller).
        # The idea is to make each step increment
        # the scroller by 1 element.
        #
        x = float(len(p_scroller.find_elements("class name", "picker-unit")))
        
        #
        # This is a little formula I worked out - seems to work, but I've only 
        # tested it on the scrollers on my Ungai.
        #
        x = 1 - ((1/((x/100)*0.8))/100)
        
        return x
        
        
    def _scrollForward(self, p_scroller):
        #
        # Move the scroller forward one item.
        #        
        x = self._calcStep(p_scroller)
        
        x_pos   = p_scroller.size['width']  / 2
        y_start = p_scroller.size['height'] / 2
        y_end   = y_start * x

        self.marionette.flick(p_scroller, x_pos, y_start, x_pos, y_end, 270)
#         actions = Actions(self.marionette)
#         actions.press(p_scroller, x_pos, y_start).move_by_offset(x_pos, y_end).release()
#         actions.perform()


        time.sleep(0.5)
        
    def _scrollBackward(self, p_scroller):
        #
        # Move the scroller back one item.
        #        
        x = self._calcStep(p_scroller)
        
        x_pos   = p_scroller.size['width']  / 2
        y_start = p_scroller.size['height'] / 2
        y_end   = y_start / x
        
        self.marionette.flick(p_scroller, x_pos, y_start, x_pos, y_end, 270)

        time.sleep(0.5)
        
    def _select(self, p_component, p_number):
        #
        # Set the time using the scroller.
        #        
        scroller = self.UTILS.getElement(
            (DOM.Clock.time_picker_column[0],DOM.Clock.time_picker_column[1] % p_component),
            "Scroller '" + p_component + "'")
        
        #
        # Get the current setting for this scroller.
        #
        currVal = scroller.find_element(*DOM.Clock.time_picker_curr_val).text
        
        #
        # Now flick the scroller as many times as required 
        # (the current value might be padded with 0's so check for that match too).
        #
        while str(p_number) != currVal and str(p_number).zfill(2) != currVal:
            # Do we need to go forwards or backwards?
            if p_number > int(currVal):
                self._scrollForward(scroller)
            if p_number < int(currVal):
                self._scrollBackward(scroller)
                
            # Get the new 'currVal'.
            currVal = scroller.find_element(*DOM.Clock.time_picker_curr_val).text
                

