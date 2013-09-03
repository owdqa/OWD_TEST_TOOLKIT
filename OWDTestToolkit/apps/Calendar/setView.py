from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def setView(self, p_type):
        #
        # Set to view type (today / day / week / month).
        #
        x = self.UTILS.getElement((DOM.Calendar.view_type[0], DOM.Calendar.view_type[1] % p_type.lower()),
                                  "'" + p_type + "' view type selector")
        x.tap()
        
        if p_type.lower() != 'today':
	        _viewTypes = { "month": DOM.Calendar.mview_container, 
						   "week" : DOM.Calendar.wview_container,
						   "day"  : DOM.Calendar.dview_container}
	        
	        self.UTILS.waitForElements(_viewTypes[p_type], "Container for '%s' view" % p_type)
        else:
        	time.sleep(0.5)
