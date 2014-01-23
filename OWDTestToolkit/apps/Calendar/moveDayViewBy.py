from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):

    def moveDayViewBy(self, p_num):
        #
        # Switches to week view, then moves 'p_num' weeks in the future or past (if the p_num is
        # positive or negative) relative to today.
        #
        self.UTILS.logResult("info","<b>Adjusting day view by %s screens ...</b>" % p_num)
        self.setView("day")
        self.setView("today")

        if p_num == 0:
            return

        #
        # Set the y-coordinate offset, depending on which
        # direction we need to flick the display.
        #
        numMoves = p_num
        if numMoves > 0:
            _moveEl = 1
        else:
            _moveEl = 2
            numMoves = numMoves * -1

        #
        # Now move to the desired screen.
        #
        for i in range (0,numMoves):
            #
            # Flick the screen to move it (tricky to find the element we can flick!).
            #
            _el = self.marionette.find_elements(*DOM.Calendar.dview_events)

            _num = 0
            for i in range(0,len(_el)):
                if _el[i].is_displayed():
                    _num = i
                    break

            x_pos1 = 0
            x_pos2 = 0
            if _moveEl == 1: x_pos1 = _el[_num].size["width"]
            if _moveEl == 2: x_pos2 = _el[_num].size["width"]
            self.actions.flick(_el[_num],x_pos1,0,x_pos2,0).perform()

        time.sleep(0.3)

        #
        # Check this is the expected day.
        #
        _new_epoch = int(time.time()) + (p_num * 24 * 60 * 60)
        _new_now   = self.UTILS.getDateTimeFromEpochSecs(_new_epoch)
        _expected_str = "%s %s, %s" % (_new_now.month_name[:3], _new_now.mday, _new_now.day_name)

        x = self.UTILS.getElement(DOM.Calendar.current_view_header, "Current view header")
        self.UTILS.TEST(x.text == _expected_str, "Header is '<b>%s</b>' (it was '%s')." % (_expected_str, x.text))


        x = self.UTILS.screenShotOnErr()
        self.UTILS.logResult("info", "Day view screen after moving %s pages: " % p_num, x)
