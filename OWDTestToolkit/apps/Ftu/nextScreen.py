from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def nextScreen(self):
        #
        # Click to the next screen (works until you get to the tour).
        #
        x = self.UTILS.getElement(DOM.FTU.next_button, "Next button")
        x.tap()
        time.sleep(0.5)
        
