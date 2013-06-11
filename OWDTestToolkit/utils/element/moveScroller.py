from OWDTestToolkit.global_imports import *
    
class main(GaiaTestCase):

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