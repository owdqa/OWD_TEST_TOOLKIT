from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def addEvent(self):
        #
        # Press the 'add event' button.
        #
        x = self.UTILS.getElement(DOM.Calendar.add_event_btn, "Add event button")
        x.tap()
        
