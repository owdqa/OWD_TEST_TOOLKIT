from OWDTestToolkit.global_imports import *

class main(GaiaTestCase):
    
    _TIMEOUT = 5
        
    def waitForNotElements(self, p_element, p_msg, p_displayed=True, p_timeout=_TIMEOUT, p_stop=True):
        #
        # Waits for an element to be displayed and captures the error if not.
        #
        boolOK = True
        try:
            if p_displayed:
                p_msg = p_msg + " no longer displayed within " + str(p_timeout) + " seconds.|" + str(p_element)
                self.wait_for_element_not_displayed(*p_element, timeout=p_timeout)
            else:
                p_msg = p_msg + " no longer present within " + str(p_timeout) + " seconds.|" + str(p_element)
                self.wait_for_element_not_present(*p_element, timeout=p_timeout)
        except:
            boolOK = False
            
        self.TEST(boolOK, p_msg, p_stop)
        
        return boolOK
    
    def waitForElements(self, p_element, p_msg, p_displayed=True, p_timeout=_TIMEOUT, p_stop=True):
        #
        # Waits for an element to be displayed and captures the error if not.
        #
        boolOK = True
        try:
            if p_displayed:
                p_msg = p_msg + " displayed within " + str(p_timeout) + " seconds.|" + str(p_element)
                self.wait_for_element_displayed(*p_element, timeout=p_timeout)
            else:
                p_msg = p_msg + " present within " + str(p_timeout) + " seconds.|" + str(p_element)
                self.wait_for_element_present(*p_element, timeout=p_timeout)
        except:
            boolOK = False
            
        self.TEST(boolOK, p_msg, p_stop)
        
        return boolOK
        
    def getElements(self, p_element, p_msg, p_displayed=True, p_timeout=_TIMEOUT, p_stop=True):
        #
        # Returns a list of matching elements, or False if none are found.
        #
        boolEl = self.waitForElements(p_element, p_msg, p_displayed, p_timeout, p_stop)
        
        if boolEl:
            el = self.marionette.find_elements(*p_element)
            
            return el
        else:
            return False

    def getElement(self, p_element, p_msg, p_displayed=True, p_timeout=_TIMEOUT, p_stop=True):
        #
        # Returns an element, or False it it's not found.
        #
        x = self.getElements(p_element, p_msg, p_displayed, p_timeout, p_stop)
        
        if x:
            # We're expecting ONE element back (it has different methods if it's one).
            return x[0]
        else:
            return False
    
    def headerCheck(self, p_str):
        #
        # Returns the header that matches a string.
        # NOTE: ALL headers in this iframe return true for ".is_displayed()"!
        #
        boolOK = False
        try:
            self.wait_for_element_present(*DOM.GLOBAL.app_head)
            headerNames = self.marionette.find_elements(*DOM.GLOBAL.app_head)
            for i in headerNames:
                if i.text == p_str:
                    if i.is_displayed():
                        boolOK = True
                        break
        except:
            boolOK = False
                
        self.TEST(boolOK, "Header is \"" + p_str + "\".")
        return boolOK
        
    def _calcScrollerStep(self, p_scroller):
        #
        # Calculates how big the step should be when 'flick'ing a scroller (based on the
        # number of elements in the scroller).
        # The idea is to make each step increment the scroller by 1 element.
        #
        x = float(len(p_scroller.find_elements("class name", "picker-unit")))
        
        #
        # This is a little formula I worked out - seems to work, but I've only 
        # tested it on the scrollers on my Ungai.
        #
        x = 1 - ((1/((x/100)*0.8))/100)
        
        return x
        
        
    def moveScroller(self, p_scroller, p_forward=True):
        #
        # Move the scroller back one item.
        #        
        x = self._calcScrollerStep(p_scroller)
        
        x_pos   = p_scroller.size['width']  / 2
        y_start = p_scroller.size['height'] / 2
        
        if p_forward:
            y_end   = y_start * x
        else:
            y_end   = y_start / x            
        
        self.actions.flick(p_scroller, x_pos, y_start, x_pos, y_end, 270)
        self.actions.perform()

        time.sleep(0.5)
        
    def setScrollerVal(self, p_component, p_number):
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
                self.moveScroller(scroller, True)
            if p_number < int(currVal):
                self.moveScroller(scroller, False)
                
            # Get the new 'currVal'.
            currVal = scroller.find_element(*DOM.Clock.time_picker_curr_val).text
                





