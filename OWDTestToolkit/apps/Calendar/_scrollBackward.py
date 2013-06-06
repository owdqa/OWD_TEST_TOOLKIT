from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def _scrollBackward(self, p_scroller):
        #
        # Move the scroller back one item.
        #        
        x = self._calcStep(p_scroller)
        
        x_pos   = p_scroller.size['width']  / 2
        y_start = p_scroller.size['height'] / 2
        y_end   = y_start / x
        
        self.marionette.flick(p_scroller, x_pos, y_start, x_pos, y_end, 270)

        time.sleep(0.5)
        
