from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def endTour(self):
        #
        # Click to end the Tour.
        #
        x = self.UTILS.getElement(DOM.FTU.tour_finished_btn, "Finish tour button")
        x.tap()
        time.sleep(1)

