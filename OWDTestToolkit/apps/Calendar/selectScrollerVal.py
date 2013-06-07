from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def selectScrollerVal(self, p_component, p_number):
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
                self._moveScroller(scroller, True)
            if p_number < int(currVal):
                self._moveScroller(scroller, False)
                
            # Get the new 'currVal'.
            currVal = scroller.find_element(*DOM.Clock.time_picker_curr_val).text
                

