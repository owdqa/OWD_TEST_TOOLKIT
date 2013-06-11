from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def nextTourScreen(self):
        #
        # Click to next page of the Tour.
        #
        x = self.UTILS.getElement(DOM.FTU.tour_next_btn, "Tour 'next' button")
        x.tap()
        time.sleep(1)

