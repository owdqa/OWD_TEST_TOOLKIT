import time
from marionette import Actions
from OWDTestToolkit import DOM


class element(object):

    def __init__(self, parent, timeout=5):
        self.parent = parent
        self._DEFAULT_ELEMENT_TIMEOUT = timeout
        self.marionette = parent.marionette

    def getElement(self, elem, msg, is_displayed=True, timeout=False, stop_on_error=True):
        #
        # Returns an element, or False it it's not found.<br>
        # timeout defaults to _DEFAULT_ELEMENT_TIMEOUT (set in the utils.py file).
        #
        timeout = self._DEFAULT_ELEMENT_TIMEOUT if not timeout else timeout

        x = self.getElements(elem, msg, is_displayed, timeout, stop_on_error)

        if x:
            # We're expecting ONE element back (it has different methods if it's one).
            return x[0]
        else:
            return False

    def getElements(self, elem, msg, is_displayed=True, timeout=False, stop_on_error=True):
        #
        # Returns a list of matching elements, or False if none are found.<br>
        # timeout defaults to _DEFAULT_ELEMENT_TIMEOUT (set in the utils.py file).
        #
        timeout = self._DEFAULT_ELEMENT_TIMEOUT if not timeout else timeout

        boolEl = self.waitForElements(elem, msg, is_displayed, timeout, stop_on_error)

        if boolEl:
            el = self.marionette.find_elements(*elem)
            return el
        else:
            return False

    def headerCheck(self, value):
        #
        # Returns the header that matches a string.
        # NOTE: ALL headers in this iframe return true for ".is_displayed()"!
        #
        is_ok = False
        try:
            self.parent.parent.wait_for_element_present(*DOM.GLOBAL.app_head, timeout=1)
            headerNames = self.marionette.find_elements(*DOM.GLOBAL.app_head)
            for i in headerNames:
                if i.text == value:
                    if i.is_displayed():
                        is_ok = True
                        break
        except:
            is_ok = False

        self.parent.test.TEST(is_ok, "Header is \"" + value + "\".")
        return is_ok

    def moveScroller(self, scroller, forward=True):
        #
        # Move the scroller back one item.
        #
        x = self._calcScrollerStep(scroller)

        x_pos = scroller.size['width'] / 2
        y_start = scroller.size['height'] / 2

        if forward:
            y_end = y_start * x
        else:
            y_end = y_start / x

        self.actions.flick(scroller, x_pos, y_start, x_pos, y_end, 270)
        self.actions.perform()

        time.sleep(0.5)

    def _calcScrollerStep(self, scroller):
        #
        # Calculates how big the step should be when 'flick'ing a scroller (based on the
        # number of elements in the scroller).
        # The idea is to make each step increment the scroller by 1 element.
        #
        x = float(len(scroller.find_elements("class name", "picker-unit")))

        #
        # This is a little formula I worked out - seems to work, but I've only
        # tested it on the scrollers on my Ungai.
        #
        x = 1 - ((1 / ((x / 100) * 0.8)) / 100)

        return x

    def setScrollerVal(self, scroller_elem, number):
        #
        # Set the numeric value of a scroller (only works with numbers right now).
        #

        #
        # Get the current setting for this scroller.
        #
        currVal = scroller_elem.find_element(*DOM.GLOBAL.scroller_curr_val).text

        #
        # Now flick the scroller as many times as required
        # (the current value might be padded with 0's so check for that match too).
        #
        while str(number) != currVal and str(number).zfill(2) != currVal:
            # Do we need to go forwards or backwards?
            if number > int(currVal):
                self.moveScroller(scroller_elem, True)
            if number < int(currVal):
                self.moveScroller(scroller_elem, False)

            # Get the new 'currVal'.
            currVal = scroller_elem.find_element(*DOM.GLOBAL.scroller_curr_val).text

    #
    # From gaiatest Clock -> regions -> alarm.py
    #
    def _flick_menu_up(self, locator):
        self.parent.parent.wait_for_element_displayed(*self._current_element(*locator), timeout=2)
        current_element = self.marionette.find_element(*self._current_element(*locator))
        next_element = self.marionette.find_element(*self._next_element(*locator))

        #TODO: update this with more accurate Actions
        action = Actions(self.marionette)
        action.press(next_element)
        action.move(current_element)
        action.release()
        action.perform()

    def _flick_menu_down(self, locator):
        self.parent.parent.wait_for_element_displayed(*self._current_element(*locator), timeout=2)
        current_element = self.marionette.find_element(*self._current_element(*locator))
        next_element = self.marionette.find_element(*self._next_element(*locator))

        #TODO: update this with more accurate Actions
        action = Actions(self.marionette)
        action.press(current_element)
        action.move(next_element)
        action.release()
        action.perform()

    def _current_element(self, method, target):
        return (method, '{}.picker-unit.active'.format(target))

    def _next_element(self, method, target):
        return (method, '{}.picker-unit.active + div'.format(target))

    def simulateClick(self, element):
        self.marionette.execute_script("""
            /**
            * Helper method to simulate clicks on iFrames which is not currently
            *  working in the Marionette JS Runner.
            * @param {Marionette.Element} element The element to simulate the click on.
            **/

            var event = new MouseEvent('click', {
             'view': window,
             'bubbles': true,
             'cancelable': true
             });
            arguments[0].dispatchEvent(event);
        """, script_args=[element])

    def waitForElements(self, elem, msg, is_displayed=True, timeout=False, stop_on_error=True):
        #
        # Waits for an element to be displayed and captures the error if not.<br>
        # timeout defaults to _DEFAULT_ELEMENT_TIMEOUT (set in the utils.py file).
        #
        timeout = self._DEFAULT_ELEMENT_TIMEOUT if not timeout else timeout

        is_ok = True
        try:
            if is_displayed:
                msg = "<b>{}</b> displayed within {} seconds.|{}".format(msg, timeout, elem)
                self.parent.parent.wait_for_element_displayed(*elem, timeout=timeout)
            else:
                msg = "<b>{}</b> present within {} seconds.|{}".format(msg, timeout, elem)
                self.parent.parent.wait_for_element_present(*elem, timeout=timeout)
        except:
            is_ok = False

        self.parent.test.TEST(is_ok, msg, stop_on_error)

        return is_ok

    def waitForNotElements(self, elem, msg, is_displayed=True, timeout=False, stop_on_error=True):
        #
        # Waits for an element to be displayed and captures the error if not.<br>
        # timeout defaults to _DEFAULT_ELEMENT_TIMEOUT (set in the utils.py file).
        #
        timeout = self._DEFAULT_ELEMENT_TIMEOUT if not timeout else timeout

        is_ok = True
        try:
            if is_displayed:
                msg = "<b>{}</b> no longer displayed within {} seconds.|{}".format(msg, timeout, elem)
                self.parent.parent.wait_for_element_not_displayed(*elem, timeout=timeout)
            else:
                msg = "<b>{}</b> no longer present within {} seconds.|{}".format(msg, timeout, elem)
                self.parent.parent.wait_for_element_not_present(*elem, timeout=timeout)
        except:
            is_ok = False

        self.parent.test.TEST(is_ok, msg, stop_on_error)
        return is_ok

    def getElementByXpath(path):
        #
        # Use this function when normal getElement did not work
        #
        return self.marionette.execute_script("""
            return document.evaluate(arguments[0], document, null, 9, null).singleNodeValue;
        """, script_args=[path])

    def getParent(element):
        #
        # Gets the element's parent. Can be called recursively
        #
        return self.marionette.execute_script("""
            return arguments[0].parentNode;
        """, script_args=[element])

    def getChildren(element):
        #
        # Gets the element's children
        #
        return self.marionette.execute_script("""
            return arguments[0].children;
        """, script_args=[element])

    def get_css_value(element, css_property):
        #
        # Gets the value of a certain css property.
        #
        return self.marionette.execute_script(""" 
            function getStyle (el, styleProp) {
                if (el.currentStyle)
                    var y = x.currentStyle[styleProp];
                else if (window.getComputedStyle)
                    var y = document.defaultView.getComputedStyle(el,null)
                                                .getPropertyValue(styleProp);
                return y;
            }
            return getStyle(arguments[0], arguments[1])
        """, script_args=[element, css_property])

    def is_ellipsis_active(element):
        #
        # Checks whether a certain element is really ellipsed when its content
        # overflows its width
        #
        return self.marionette.execute_script("""
            function isEllipsisActive(element) {
                return (element.offsetWidth < element.scrollWidth);
            }
            return isEllipsisActive(arguments[0])
        """, script_args=[element])

    def scroll_into_view(self, element):
        self.marionette.execute_script("""
            arguments[0].scrollIntoView();
        """, script_args=[element])

    def perform_action_over_element(locator, action):
        self.marionette.execute_script("""
            var _locatorMap = {
                "id": getElementById,
                "class name": document.getElementsByClassName,
                "css selector": document.querySelector,
                "xpath": function () { 
                            return document.evaluate(arguments[0], document, null, 9, null).singleNodeValue 
                        },
                "tag name": document.getElementsByTagName
            };

            var _actionMap = {

            }

            var location_method = arguments[0][0];
            var locator = arguments[0][1];

            var element = _locatorMap(location_method)(locator);

            return element;
        """, script_args=[locator, action])    
