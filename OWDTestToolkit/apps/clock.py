from OWDTestToolkit import DOM
from marionette import Actions
import time


class Clock(object):

    def __init__(self, parent):
        self.apps = parent.apps
        self.data_layer = parent.data_layer
        self.parent = parent
        self.marionette = parent.marionette
        self.UTILS = parent.UTILS
        self.actions = Actions(self.marionette)

    def launch(self):
        #
        # Launch the app.
        #
        self.app = self.apps.launch(self.__class__.__name__)
        self.UTILS.waitForNotElements(DOM.GLOBAL.loading_overlay, self.__class__.__name__ + " app - loading overlay")
        return self.app

    def checkAlarmPreview(self, hour, minute, ampm, label, repeat):
        #
        # Verify the alarm details in the clock screen.
        #

        #
        # Put the time in a format we can compare easily with.
        #
        stime = str(hour) + ":" + str(minute).zfill(2)

        alarms = self.UTILS.getElements(DOM.Clock.alarm_preview_alarms, "Alarm preview list")

        foundBool = False
        for alarm in alarms:
            alarm_time = alarm.find_element(*DOM.Clock.alarm_preview_time).text
            alarm_ampm = alarm.find_element(*DOM.Clock.alarm_preview_ampm).text
            alarm_label = alarm.find_element(*DOM.Clock.alarm_preview_label).text

            if stime == alarm_time and ampm == alarm_ampm:
                foundBool = True
                self.UTILS.TEST(label == alarm_label, "Alarm description is correct in Clock screen preview.")
                break

        self.UTILS.TEST(foundBool, "Alarm preview is found in Clock screen for " + stime + ampm + ".")

    def checkAlarmRingDetails(self, hour, minute, label):
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
            msg = "Cannot find the iframe containing the clock! ('" + \
                  DOM.Clock.alarm_alert_iframe[0] + "' contains '" + \
                  DOM.Clock.alarm_alert_iframe[1] + "')."
            self.UTILS.quitTest(msg)

        #
        # Sort the time out into 12 hour format.
        #
        x = self.UTILS.switch_24_12(hour)
        t_hour = x[0]
        ampm = x[1]

        # Put the time in a format we can compare easily with.
        stime = str(t_hour) + ":" + str(minute).zfill(2)

        x = self.UTILS.getElement(DOM.Clock.alarm_alert_time, "Alarm alert time").text
        self.UTILS.TEST(x == stime, "Correct alarm time is shown when alarm is ringing (expected '" +
                        stime + "', it was '" + x + "').")

        x = self.UTILS.getElement(DOM.Clock.alarm_alert_ampm, "Alarm alert AM/PM").text
        self.UTILS.TEST(x == ampm, "Correct AM / PM shown when alarm is ringing (expected '" +
                        ampm + "', it was '" + x + "').")

        x = self.UTILS.getElement(DOM.Clock.alarm_alert_label, "Alarm alert label").text
        self.UTILS.TEST(x == label, "Correct label shown when alarm is ringing (expected '" +
                        label + "', it was '" + x + "').")

        #
        # Stop the alarm.
        #
        x = self.UTILS.getElement(DOM.Clock.alarm_alert_close, "Close alert button")
        x.tap()

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

    def createAlarm(self, hour, minute, label, repeat="Never", sound="Classic Buzz", snooze="5 minutes"):
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
        x = self.UTILS.getElement(("xpath", "//button[@id='time-menu']"), "Time button")

        x = self.UTILS.getElement(DOM.Clock.time_button, "Time button")
        x.tap()

        myIframe = self.UTILS.currentIframe()
        self.marionette.switch_to_frame()

        #
        # Sort the time out into 12 hour format.
        #
        x = self.UTILS.switch_24_12(hour)
        t_hour = x[0]
        ampm = x[1]

        self.UTILS.logComment("Creating new alarm for " + str(t_hour) + ":" + str(minute).zfill(2) + " " + ampm)

        scroller_hours = self.UTILS.getElement(
            (DOM.Clock.time_scroller[0], DOM.Clock.time_scroller[1].format("hours")), "Scroller for 'hours'")

        scroller_minutes = self.UTILS.getElement(
            (DOM.Clock.time_scroller[0], DOM.Clock.time_scroller[1].format("minutes")), "Scroller for 'minutes'")

        self.UTILS.logResult("info", "H: %s, M: %s" % (scroller_hours.text, scroller_minutes.text))
        return

        #
        # Set the hour.
        #
        self.UTILS.setScrollerVal(scroller_hours, t_hour)

        #
        # Set the minutes.
        #
        self.UTILS.setScrollerVal(scroller_minutes, minute)

        #
        # Set the AM / PM.
        #
        scroller = self.UTILS.getElement(DOM.Clock.time_scroller_ampm, "AM/PM picker")
        currVal = scroller.find_element(*DOM.GLOBAL.scroller_curr_val).text

        if ampm != currVal:
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
        x.send_keys(label)

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
        self.checkAlarmPreview(t_hour, minute, ampm, label, repeat)

    def deleteAllAlarms(self):
        #
        # Deletes all current alarms.
        #

        #
        # "self.data_layer.delete_all_alarms()" isn't workng at the moment, so...
        #
        while True:
            try:
                self.wait_for_element_present(*DOM.Clock.alarm_preview_alarms, timeout=3)
                x = self.marionette.find_elements(*DOM.Clock.alarm_preview_alarms)
            except:
                #
                # No alarms returned, so just move on...
                #
                break
            if len(x) <= 0:
                break

            #
            # Some alarms - delete the first one (we need to reload the
            # list each time because it changes everytime we delete
            # an alarm).
            #
            x[0].tap()
            x = self.UTILS.getElement(DOM.Clock.alarm_delete_button, "Alarm delete button")
            x.tap()
            time.sleep(1)
