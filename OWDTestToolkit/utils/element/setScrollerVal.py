from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

    def setScrollerVal(self, p_scrollerElement, p_number):
        #
        # Set the numeric value of a scroller (only works with numbers just now).
        #        

        #
        # Get the current setting for this scroller.
        #
        currVal = p_scrollerElement.find_element(*DOM.GLOBAL.scroller_curr_val).text
        
        #
        # Now flick the scroller as many times as required 
        # (the current value might be padded with 0's so check for that match too).
        #
        while str(p_number) != currVal and str(p_number).zfill(2) != currVal:
            # Do we need to go forwards or backwards?
            if p_number > int(currVal):
                self.moveScroller(p_scrollerElement, True)
            if p_number < int(currVal):
                self.moveScroller(p_scrollerElement, False)
                
            # Get the new 'currVal'.
            currVal = p_scrollerElement.find_element(*DOM.GLOBAL.scroller_curr_val).text
                

    #
    # From gaiatest Clock -> regions -> alarm.py
    #
    def _flick_menu_up(self, locator):
        self.wait_for_element_displayed(*self._current_element(*locator), timeout=2)
        current_element = self.marionette.find_element(*self._current_element(*locator))
        next_element = self.marionette.find_element(*self._next_element(*locator))

        #TODO: update this with more accurate Actions
        action = Actions(self.marionette)
        action.press(next_element)
        action.move(current_element)
        action.release()
        action.perform()

    def _flick_menu_down(self, locator):
        self.wait_for_element_displayed(*self._current_element(*locator), timeout=2)
        current_element = self.marionette.find_element(*self._current_element(*locator))
        next_element = self.marionette.find_element(*self._next_element(*locator))

        #TODO: update this with more accurate Actions
        action = Actions(self.marionette)
        action.press(current_element)
        action.move(next_element)
        action.release()
        action.perform()

    def _current_element(self, method, target):
        return (method, '%s.picker-unit.active' % target)

    def _next_element(self, method, target):
        return (method, '%s.picker-unit.active + div' % target)



