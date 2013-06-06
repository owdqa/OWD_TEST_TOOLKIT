from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def setView(self, p_type):
        #
        # Set to view type (day / week / month).
        #
        x = self.UTILS.getElement((DOM.Calendar.view_type[0], DOM.Calendar.view_type[1] % p_type),
                                  "'" + p_type + "' view type selector")
        x.tap()
        
