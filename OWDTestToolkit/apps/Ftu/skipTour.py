from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def skipTour(self):
        #
        # Click to skip the Tour.
        #
        x = self.UTILS.getElement(DOM.FTU.tour_skip_btn, "Skipt tour button")
        x.tap()
        time.sleep(1)

