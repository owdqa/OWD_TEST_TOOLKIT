import time
from marionette import Actions
from OWDTestToolkit import DOM


class Calendar(object):

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
        self.UTILS.element.waitForNotElements(DOM.GLOBAL.loading_overlay, self.__class__.__name__ + " app - loading overlay")
        return self.app

    def moveDayViewBy(self, num):
        #
        # Switches to week view, then moves 'p_num' weeks in the future or past (if the p_num is
        # positive or negative) relative to today.
        #
        self.UTILS.reporting.logResult("info", "<b>Adjusting day view by {} screens ...</b>".format(num))
        self.setView("day")
        self.setView("today")

        if num == 0:
            return

        #
        # Set the y-coordinate offset, depending on which
        # direction we need to flick the display.
        #
        numMoves = num
        if numMoves > 0:
            _moveEl = 1
        else:
            _moveEl = 2
            numMoves = numMoves * -1

        #
        # Now move to the desired screen.
        #
        for i in range(numMoves):
            #
            # Flick the screen to move it (tricky to find the element we can flick!).
            #
            _el = self.marionette.find_elements(*DOM.Calendar.dview_events)

            _num = 0
            for i in range(len(_el)):
                if _el[i].is_displayed():
                    _num = i
                    break

            x_pos1 = 0
            x_pos2 = 0
            if _moveEl == 1:
                x_pos1 = _el[_num].size["width"]
            if _moveEl == 2:
                x_pos2 = _el[_num].size["width"]
            self.actions.flick(_el[_num], x_pos1, 0, x_pos2, 0).perform()

        time.sleep(0.3)

        #
        # Check this is the expected day.
        #
        _new_epoch = int(time.time()) + (num * 24 * 60 * 60)
        _new_now = self.UTILS.date_and_time.getDateTimeFromEpochSecs(_new_epoch)
        _expected_str = "{} {}, {}".format(_new_now.month_name[:3], _new_now.mday, _new_now.day_name)

        x = self.UTILS.element.getElement(DOM.Calendar.current_view_header, "Current view header")
        self.UTILS.test.test(x.text == _expected_str, "Header is '<b>%s</b>' (it was '%s')." % (_expected_str, x.text))

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Day view screen after moving {} pages: ".format(num), x)

    def getEventPreview(self, p_view, p_hour24, p_title, p_location=False):
        #
        # Return object for an event in month / week or day view.
        #

        #
        # The tag identifiers aren't consistent, so set them here.
        #
        # <type>: (<event preview identifier>, <event title identifier>)
        #
        event_view = {
            "month": (DOM.Calendar.view_events_block_m % p_hour24, DOM.Calendar.view_events_title_month),
            "week": (DOM.Calendar.view_events_block_w % p_hour24, DOM.Calendar.view_events_title_week),
            "day": (DOM.Calendar.view_events_block_d % p_hour24, DOM.Calendar.view_events_title_day)
        }

        viewStr = event_view[p_view]

        #
        # Switch to the desired view.
        #
        # For the life of me I can't get 'wait_for_element' ... to work in day view, so I'm
        # just waiting a few seconds then checking with .is_displayed() instead.
        #
        self.setView(p_view)
        time.sleep(2)

        #
        # Start by getting the parent element objects, which could contain event details.
        #
        event_objects = self.UTILS.element.getElements(('xpath', viewStr[0]), "'" + p_view + "' event details list",
                                               False, 20, False)
        if not event_objects:
            return False

        if len(event_objects) <= 0:
            return False

        for event_object in event_objects:
            if p_title in event_object.text:
                return event_object

        #
        # If we get to here we failed to return the element we're after.
        #
        return False

    def createEvent(self):
        #
        # Create a new event - use 'False' in the following fields if you want to leave them at default:
        #
        #   start date,
        #   end date,
        #   location,
        #   notes
        #
        x = self.UTILS.element.getElement(DOM.Calendar.add_event_btn, "Add event button")
        x.tap()

        title = ("xpath", "//input[@name='title']")
        where = ("xpath", "//input[@name='location']")
        # allday checkbox, True False (use tap())
        allday = ("xpath", "//li[@class='allday']")

        x = self.UTILS.element.getElement(title, "Title", True, 10)
        x.send_keys("hello title")

        x = self.UTILS.element.getElement(where, "Where")
        x.send_keys("hello where")

        x = self.UTILS.element.getElement(allday, "All day")
        x.tap()

        self.marionette.execute_script("document.getElementById('start-date-locale').click()")

    def changeDay(self, numDays, viewType):
        #
        # Changes the calendar day to a different day relative to 'today' - <b>uses the
        # month view to do this, then switches back to whichever
        # view you want (month, week, day)</b>.<br>
        # <b>numDays</b> is a number (can be negative to go back, i.e. -5,-2,1,3,5 etc...).<br>
        # <b>viewType</b> is the calendar view to return to (today / day / week / month)<br>
        # Returns a modified DateTime object from <i>UTILS.getDateTimeFromEpochSecs()</i>.
        #
        self.setView("month")
        self.setView("today")

        now_secs = time.time()
        now_diff = int(now_secs) + (86400 * numDays)
        now_today = self.UTILS.date_and_time.getDateTimeFromEpochSecs(now_secs)
        new_today = self.UTILS.date_and_time.getDateTimeFromEpochSecs(now_diff)

        #
        # Switch to month view and tap this day, then switch back to our view.
        #
        if now_today.mon != new_today.mon:
            x = new_today.mon - now_today.mon
            self.moveMonthViewBy(x)

        el_id_str = "d-%s-%s-%s" % (new_today.year, new_today.mon - 1, new_today.mday)
        x = self.UTILS.element.getElement(("xpath", "//li[@data-date='{}']".format(el_id_str)),
                                  "Cell for day {}/{}/{}".format(new_today.mday, new_today.mon, new_today.year))
        x.tap()
        self.setView(viewType.lower())
        return new_today

    def moveMonthViewBy(self, num):
        #
        # Switches to month view, then moves 'num' months in the future or past (if the num is
        # positive or negative) relative to today.
        #
        self.UTILS.reporting.logResult("info", "<b>Adjusting month view by {} months ...</b>".format(num))
        self.setView("month")
        self.setView("today")

        if num == 0:
            return

        #
        # Set the y-coordinate offset, depending on which
        # direction we need to flick the display.
        #
        numMoves = num
        x2 = 0
        if numMoves > 0:
            el_num = -1
            x2 = -500
        if numMoves < 0:
            el_num = 0
            x2 = 500
            numMoves = numMoves * -1

        now = time.localtime(int(time.time()))
        month = now.tm_mon
        year = now.tm_year

        for i in range(numMoves):
            #
            # Flick the display to show the date we're aiming for.
            #
            el = self.marionette.find_elements(*DOM.Calendar.mview_first_row_for_flick)[el_num]
            self.actions.flick(el, 0, 0, x2, 0).perform()

            #
            # Increment the month and year so we keep track of what's expected.
            #
            if num < 0:
                month = month - 1
            else:
                month = month + 1

            if month <= 0:
                month = 12
                year = year - 1
            elif month >= 13:
                month = 1
                year = year + 1

        time.sleep(0.3)

        #
        # Work out what the header should now be.
        #
        month_names = ["January", "February", "March", "April", "May", "June",
                        "July", "August", "September", "October", "November", "December"]

        expect = "{} {}".format(month_names[month - 1], year)
        actual = self.UTILS.element.getElement(DOM.Calendar.current_view_header, "Header").text

        self.UTILS.test.test(expect.lower() in actual.lower(), "Expecting header to contain '{}' (received '{}')"
                        .format(expect, actual))

    def moveWeekViewBy(self, num):
        #
        # Switches to week view, then moves 'num' weeks in the future or past (if the num is
        # positive or negative) relative to today.
        #
        self.UTILS.reporting.logResult("info", "<b>Adjusting week view by {} screens ...</b>".format(num))
        self.setView("week")
        self.setView("today")

        if num == 0:
            return

        #
        # Set the y-coordinate offset, depending on which
        # direction we need to flick the display.
        #
        numMoves = num
        x2 = 0
        if numMoves > 0:
            el = -1
            x2 = -500
        if numMoves < 0:
            el = 0
            x2 = 500
            numMoves = numMoves * -1

        #
        # Keep track of how many days we're adjusting the display by (so we can check
        # we're looking at the correct display at the end).
        #
        days_offset = 0
        now_epoch = int(time.time())
        now = self.UTILS.date_and_time.getDateTimeFromEpochSecs(now_epoch)
        now_str = "{} {}".format(now.day_name[:3].upper(), now.mday)

        displayed_days = self.UTILS.element.getElements(DOM.Calendar.wview_active_days, "Active days")
        startpos = 0
        for i in range(len(displayed_days)):
            x = displayed_days[i].text
            if x:
                if now_str in x:
                    startpos = i - 1
                    break

        if num < 0:
            days_offset = startpos
        else:
            days_offset = len(displayed_days) - startpos - 2

        #
        # Now move to the desired screen.
        #
        for i in range(numMoves):
            #
            # Flick the screen to move it.
            #
            self.actions.flick(displayed_days[el], 0, 0, x2, 0).perform()

            #
            # Get the count of days we're adjusting (so we can check later).
            #
            displayed_days = self.UTILS.element.getElements(DOM.Calendar.wview_active_days, "Active days")
            days_offset = days_offset + len(displayed_days)

        time.sleep(0.3)

        #
        # Work out what the display should now be:
        #
        # 1. Today + days_offset should be displayed.
        # 2. Header should be month + year, now + days_offset should be in active days.
        #
        if num < 0:
            new_epoch = now_epoch - (days_offset * 24 * 60 * 60)
        else:
            new_epoch = now_epoch + (days_offset * 24 * 60 * 60)

        new_now = self.UTILS.date_and_time.getDateTimeFromEpochSecs(new_epoch)

        new_now_str = "{} {}".format(new_now.day_name[:3].upper(), new_now.mday)

        x = self.UTILS.element.getElements(DOM.Calendar.wview_active_days, "Active days")
        boolOK = False
        for i in range(len(x)):
            x = displayed_days[i].text
            if x:
                if new_now_str in x:
                    boolOK = True
                    break

        self.UTILS.test.test(boolOK, "The column for date '<b>{}</b>' displayed.".format(new_now_str))

        x = self.UTILS.element.getElement(DOM.Calendar.current_view_header, "Current view header")
        self.UTILS.test.test(new_now.month_name in x.text, "'<b>{}</b>' is in header ('{}')."
                        .format(new_now.month_name, x.text))
        self.UTILS.test.test(str(new_now.year) in x.text, "'<b>{}</b>' is in header ('{}').".format(new_now.year, x.text))

        x = self.UTILS.debug.screenShotOnErr()
        self.UTILS.reporting.logResult("info", "Week view screen after moving {} pages: ".format(num), x)

    def setView(self, typ):
        #
        # Set to view typ (today / day / week / month).
        #
        x = self.UTILS.element.getElement((DOM.Calendar.view_type[0], DOM.Calendar.view_type[1] % typ.lower()),
                                  "'" + typ + "' view type selector")
        x.tap()

        if typ.lower() != 'today':
            viewTypes = {"month": DOM.Calendar.mview_container,
                         "week": DOM.Calendar.wview_container,
                         "day": DOM.Calendar.dview_container}

            self.UTILS.element.waitForElements(viewTypes[typ], "Container for '{}' view".format(typ))
        else:
            time.sleep(0.5)
