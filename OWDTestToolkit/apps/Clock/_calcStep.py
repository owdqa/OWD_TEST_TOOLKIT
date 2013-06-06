from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def _calcStep(self, p_scroller):
        #
        # Calculates how big the step should be
        # when 'flick'ing a scroller (based on the
        # number of elements in the scroller).
        # The idea is to make each step increment
        # the scroller by 1 element.
        #
        x = float(len(p_scroller.find_elements("class name", "picker-unit")))
        
        #
        # This is a little formula I worked out - seems to work, but I've only 
        # tested it on the scrollers on my Ungai.
        #
        x = 1 - ((1/((x/100)*0.8))/100)
        
        return x
        
        
