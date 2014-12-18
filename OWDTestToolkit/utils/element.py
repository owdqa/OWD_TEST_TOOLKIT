import time
from marionette import Actions
from OWDTestToolkit import DOM


class element(object):

    def __init__(self, parent):
        self.parent = parent
        self.marionette = parent.marionette
        self.actions = Actions(self.marionette)

    def getElement(self, elem, msg, is_displayed=True, timeout=5, stop_on_error=True):
        """
        Returns an element, or False it it's not found
        """
        x = self.getElements(elem, msg, is_displayed, timeout, stop_on_error)
        if x:
            # We're expecting ONE element back (it has different methods if it's one).
            return x[0]
        else:
            return False

    def getElements(self, elem, msg, is_displayed=True, timeout=5, stop_on_error=True):
        """
        Returns a list of matching elements, or False if none are found
        """
        boolEl = self.waitForElements(elem, msg, is_displayed, timeout, stop_on_error)

        if boolEl:
            el = self.marionette.find_elements(*elem)
            return el
        else:
            return False

    def headerCheck(self, value):
        """
        Returns the header that matches a string.
        NOTE: ALL headers in this iframe return true for ".is_displayed()"!
        """
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

        self.parent.test.test(is_ok, "Header is \"" + value + "\".")
        return is_ok

    def move_scroller(self, scroller, forward=True):
        """Move the scroller one item forward or backwards.
        """
        x_pos = scroller.size['width'] / 2
        y_start = scroller.size['height'] / 2

        y_end = -scroller.size['height'] if forward else scroller.size['height']
        self.actions.flick(scroller, x_pos, y_start, x_pos, y_end, 100)
        self.actions.perform()

    def set_scroller_val(self, scroller_elem, number):
        """
        Set the numeric value of a scroller (only works with numbers right now).
        """
        current_value = int(scroller_elem.find_element(*DOM.GLOBAL.scroller_curr_val).text)

        # Now flick the scroller as many times as required
        n = int(number)
        while n != current_value:
            # Do we need to go forwards or backwards?
            if n > int(current_value):
                self.move_scroller(scroller_elem, True)
            if n < int(current_value):
                self.move_scroller(scroller_elem, False)

            # Get the new 'current_value'.
            current_value = int(scroller_elem.find_element(*DOM.GLOBAL.scroller_curr_val).text)

    # From gaiatest Clock -> regions -> alarm.py
    def _flick_menu_up(self, locator):
        self.parent.parent.wait_for_element_displayed(*self._current_element(*locator), timeout=2)
        current_element = self.marionette.find_element(*self._current_element(*locator))
        next_element = self.marionette.find_element(*self._next_element(*locator))

        # TODO: update this with more accurate Actions
        action = Actions(self.marionette)
        action.press(next_element)
        action.move(current_element)
        action.release()
        action.perform()

    def _flick_menu_down(self, locator):
        self.parent.parent.wait_for_element_displayed(*self._current_element(*locator), timeout=2)
        current_element = self.marionette.find_element(*self._current_element(*locator))
        next_element = self.marionette.find_element(*self._next_element(*locator))

        # TODO: update this with more accurate Actions
        action = Actions(self.marionette)
        action.press(current_element)
        action.move(next_element)
        action.release()
        action.perform()

    def _current_element(self, method, target):
        self.parent.reporting.debug("*** Finding current element for target {}".format(target))
        return (method, '{}.picker-unit.selected'.format(target))

    def _next_element(self, method, target):
        self.parent.reporting.debug("*** Finding next element for target {}".format(target))
        return (method, '{}.picker-unit.selected + div'.format(target))

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

    def waitForElements(self, elem, msg, is_displayed=True, timeout=5, stop_on_error=True):
        """
        Waits for an element to be displayed and captures the error if not
        """
        is_ok = True
        msg = u"" + msg
        try:
            if is_displayed:
                msg = u"{} displayed within {} seconds.|{}".format(msg, timeout, elem)
                self.parent.parent.wait_for_element_displayed(*elem, timeout=timeout)
            else:
                msg = u"{} present within {} seconds.|{}".format(msg, timeout, elem)
                self.parent.parent.wait_for_element_present(*elem, timeout=timeout)
        except Exception:
            is_ok = False

        self.parent.test.test(is_ok, msg, stop_on_error)

        return is_ok

    def waitForNotElements(self, elem, msg, is_displayed=True, timeout=5, stop_on_error=True):
        """
        Waits for an element to be displayed and captures the error if not
        """
        is_ok = True
        try:
            if is_displayed:
                msg = "{} no longer displayed within {} seconds.|{}".format(msg, timeout, elem)
                self.parent.parent.wait_for_element_not_displayed(*elem, timeout=timeout)
            else:
                msg = "{} no longer present within {} seconds.|{}".format(msg, timeout, elem)
                self.parent.parent.wait_for_element_not_present(*elem, timeout=timeout)
        except:
            is_ok = False

        self.parent.test.test(is_ok, msg, stop_on_error)
        return is_ok

    def getElementByXpath(self, path):
        """
        Use this function when normal getElement did not work
        """
        return self.marionette.execute_script("""
            return document.evaluate(arguments[0], document, null, 9, null).singleNodeValue;
        """, script_args=[path])

    def getParent(self, element):
        """
        Gets the element's parent. Can be called recursively
        """
        return self.marionette.execute_script("""
            return arguments[0].parentNode;
        """, script_args=[element])

    def getChildren(self, element):
        """
        Gets the element's children
        """
        return self.marionette.execute_script("""
            return arguments[0].children;
        """, script_args=[element])

    def find_nested(self, context, css_selector):
        return self.marionette.execute_script("""
            return arguments[0].querySelector(arguments[1])
        """, script_args=[context, css_selector])

    def get_css_value(self, element, css_property):
        """
        Gets the value of a certain css property.
        """
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

    def is_ellipsis_active(self, element):
        """
        Checks whether a certain element is really ellipsed when its content
        overflows its width
        """
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

    def perform_action_over_element(self, locator, action, position=None):
        script = """
            var _locatorMap = {
                "id": document.getElementById,
                "class name": document.getElementsByClassName,
                "css selector": document.querySelector,
                "xpath": function () {
                            return document.evaluate(arguments[0], document, null, 9, null).singleNodeValue
                        },
                "tag name": document.getElementsByTagName
            };

            // TODO - Add more events here
            var _actionMap = {
                "click":    new MouseEvent('click', {
                                'view': window,
                                'bubbles': true,
                                'cancelable': true
                            }), //HTMLElement.prototype.click
            }

            var location_method = arguments[0][0];
            var locator         = arguments[0][1];
            var action          = arguments[1];
            var position        = arguments[2];

            if (position) {
                var element = _locatorMap[location_method].call(document, locator)[position];
            } else {
                if ((locator === "class name") || (locator === "tag name")) {
                    var e = 'JavaScriptException: InvalidParametersException: '
                    var msg = 'If using "class name" or "tag name", it is mandatory to specify a position'
                    throw  e + msg
                }
                var element = _locatorMap[location_method].call(document, locator);
            }

            if (element) {
                if (_actionMap.hasOwnProperty(action)) {
                    element.dispatchEvent(_actionMap[action])
                } else {
                    var e = 'JavaScriptException: InvalidParametersException: '
                    var msg = 'Specified action <' + action + '> not supported';
                    throw  e + msg
                }
            }
        """
        self.marionette.execute_script(script, script_args=[list(locator), action, position])
