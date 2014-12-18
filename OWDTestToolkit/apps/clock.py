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

        # Launch the app.
        self.app = self.apps.launch(self.__class__.__name__)
        self.UTILS.element.waitForNotElements(DOM.GLOBAL.loading_overlay,
                                              self.__class__.__name__ + " app - loading overlay")
        return self.app

    def check_alarm_preview(self, hour, minute, ampm, label, repeat):
        """Verify the alarm is set in the clock screen.
        """
        time_str = "{}:{:02d} {}".format(hour, int(minute), ampm)

        alarms = self.UTILS.element.getElements(DOM.Clock.alarm_preview_alarms, "Alarm preview list")

        found = False
        for alarm in alarms:
            alarm_time = alarm.find_element(*DOM.Clock.alarm_preview_time).text
            alarm_ampm = alarm.find_element(*DOM.Clock.alarm_preview_ampm).text
            alarm_label = alarm.find_element(*DOM.Clock.alarm_preview_label).text

            if time_str == alarm_time and ampm == alarm_ampm:
                found = True
                self.UTILS.test.test(label == alarm_label, "Alarm description is correct in Clock screen preview.")
                break

        self.UTILS.test.test(found, "Alarm preview is found in Clock screen for " + time_str + ".")

    def checkAlarmRingDetails(self, hour, minute, label):
        """
        Check details of alarm when it rings.
        NOTE: the status bar alarm is always 'visible', so you have to manually
        wait until the alarm is expected to have started before calling this!

        The alarm screen appears in a different frame to the clock.
        Try to access this frame a few times to give the alarm time to appear.
        """
        self.marionette.switch_to_frame()

        retries = 40
        while retries >= 0:
            if self.UTILS.iframe.switchToFrame(*DOM.Clock.alarm_alert_iframe, quit_on_error=False):
                break

            time.sleep(2)
            retries = retries - 1

        if retries <= 0:
            msg = "Cannot find the iframe containing the clock! ('" + \
                  DOM.Clock.alarm_alert_iframe[0] + "' contains '" + \
                  DOM.Clock.alarm_alert_iframe[1] + "')."

        # Sort the time out into 12 hour format.
        x = self.UTILS.date_and_time.switch_24_12(hour)
        t_hour = x[0]
        ampm = x[1]

        # Put the time in a format we can compare easily with.
        stime = str(t_hour) + ":" + str(minute).zfill(2)

        x = self.UTILS.element.getElement(DOM.Clock.alarm_alert_time, "Alarm alert time").text
        self.UTILS.test.test(x == stime, "Correct alarm time is shown when alarm is ringing (expected '" +
                        stime + "', it was '" + x + "').")

        x = self.UTILS.element.getElement(DOM.Clock.alarm_alert_ampm, "Alarm alert AM/PM").text
        self.UTILS.test.test(x == ampm, "Correct AM / PM shown when alarm is ringing (expected '" +
                        ampm + "', it was '" + x + "').")

        x = self.UTILS.element.getElement(DOM.Clock.alarm_alert_label, "Alarm alert label").text
        self.UTILS.test.test(x == label, "Correct label shown when alarm is ringing (expected '" +
                        label + "', it was '" + x + "').")

        # Stop the alarm.
        x = self.UTILS.element.getElement(DOM.Clock.alarm_alert_close, "Close alert button")
        x.tap()

    def checkStatusbarIcon(self):
        """
        Check for the little alarm bell icon in the statusbar of the
        homescreen.
        """
        self.marionette.switch_to_frame()
        boolOK = True
        try:
            self.UTILS.element.waitForElements(DOM.Clock.alarm_notifier, "Alarm notification", True, 20, False)
        except:
            boolOK = False
        return boolOK

    def create_alarm(self, hour, minute, label, repeat="Never", sound="Classic Buzz", snooze="5 minutes"):
        """Create a new alarm to the given time, with the given parameters.
        """
        new_alarm_btn = self.UTILS.element.getElement(DOM.Clock.new_alarm_btn, "New alarm button")
        new_alarm_btn.tap()

        time_button = self.marionette.find_element(*DOM.Clock.time_button)
        time_button.tap()

        # Sort the time out into 12 hour format.
        time_12h = self.UTILS.date_and_time.switch_24_12(int(hour))
        t_hour = time_12h[0]
        ampm = time_12h[1]

        self.UTILS.reporting.logComment("Creating new alarm for {:02}:{:02} {}".format(t_hour, int(minute), ampm))

        self.marionette.switch_to_frame()
        time.sleep(3)
        scroller_hours = self.UTILS.element.getElement(
            (DOM.Clock.time_scroller[0], DOM.Clock.time_scroller[1].format("hours")), "Scroller for 'hours'")

        scroller_minutes = self.UTILS.element.getElement(
            (DOM.Clock.time_scroller[0], DOM.Clock.time_scroller[1].format("minutes")), "Scroller for 'minutes'")

        # Set the hour.
        self.UTILS.element.set_scroller_val(scroller_hours, t_hour)

        # Set the minutes.
        self.UTILS.element.set_scroller_val(scroller_minutes, minute)

        # Set the AM / PM.
        scroller = self.UTILS.element.getElement(DOM.Clock.time_scroller_ampm, "AM/PM picker")
        curr_val = scroller.find_element(*DOM.GLOBAL.scroller_curr_val).text

        if ampm != curr_val:
            if curr_val == "AM":
                self.UTILS.element.move_scroller(scroller)
            else:
                self.UTILS.element.move_scroller(scroller)

        # Click the OK button and return to the calling frame.
        ok_btn = self.UTILS.element.getElement(DOM.Clock.time_picker_ok, "OK button")
        ok_btn.tap()
        self.UTILS.iframe.switch_to_frame(*DOM.Clock.frame_locator)

        # Set the label.
        alarm_label = self.UTILS.element.getElement(DOM.Clock.alarm_label, "Alarm label field")
        alarm_label.clear()
        alarm_label.send_keys(label)
        from marionette.keys import Keys
        alarm_label.send_keys(Keys.ENTER)

        # Set the repeat, sound and snooze values
        if isinstance(repeat, list):
            repeat_sel = self.UTILS.element.getElement(DOM.Clock.edit_alarm_repeat_menu, "Repeat menu")
            repeat_sel.tap()
            self.marionette.switch_to_frame()
            for day in repeat:
                day_elem = self.UTILS.element.getElementByXpath(DOM.Clock.edit_alarm_selector_xpath.format(day))
                day_elem.tap()
            ok_btn = self.UTILS.element.getElement(DOM.Clock.edit_alarm_repeat_ok, "OK Button")
            ok_btn.tap()

        self.UTILS.iframe.switch_to_frame(*DOM.Clock.frame_locator)
        sound_sel = self.UTILS.element.getElement(DOM.Clock.edit_alarm_sound_menu, "Sound menu")
        sound_sel.tap()
        self.marionette.switch_to_frame()
        sound_elem = self.UTILS.element.getElementByXpath(DOM.Clock.edit_alarm_selector_xpath.format(sound))
        sound_elem.tap()
        ok_btn = self.UTILS.element.getElement(DOM.Clock.edit_alarm_repeat_ok, "OK Button")
        ok_btn.tap()

        self.UTILS.iframe.switch_to_frame(*DOM.Clock.frame_locator)
        snooze_sel = self.UTILS.element.getElement(DOM.Clock.edit_alarm_snooze_menu, "Snooze selector")
        snooze_sel.tap()
        self.marionette.switch_to_frame()
        snooze_elem = self.UTILS.element.getElementByXpath(DOM.Clock.edit_alarm_selector_xpath.format(snooze))
        snooze_elem.tap()
        ok_btn = self.UTILS.element.getElement(DOM.Clock.edit_alarm_repeat_ok, "OK Button")
        ok_btn.tap()

        # Save the alarm.
        self.UTILS.iframe.switch_to_frame(*DOM.Clock.frame_locator)
        done_btn = self.UTILS.element.getElement(DOM.Clock.alarm_done, "Done button")
        done_btn.tap()

        # Check the alarm details are displayed in the clock screen.
        self.check_alarm_preview(t_hour, minute, ampm, label, repeat)

    def delete_all_alarms(self):
        """Delete all current alarms.
        """
        alarms = self.marionette.find_elements(*DOM.Clock.alarm_preview_alarms)
        while alarms and len(alarms) > 0:
            alarm = alarms[0]
            self.UTILS.element.simulateClick(alarm)
            delete_btn = self.UTILS.element.getElement(DOM.Clock.alarm_delete_button, "Alarm delete button")
            delete_btn.tap()
            time.sleep(1)
            alarms = self.marionette.find_elements(*DOM.Clock.alarm_preview_alarms)
