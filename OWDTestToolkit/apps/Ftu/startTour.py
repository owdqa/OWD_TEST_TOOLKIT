from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def startTour(self):
        #
        # Click to start the Tour.
        #
        x = self.UTILS.getElement(DOM.FTU.tour_start_btn, "Start tour button")
        x.tap()
        time.sleep(0.5)

