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
                





