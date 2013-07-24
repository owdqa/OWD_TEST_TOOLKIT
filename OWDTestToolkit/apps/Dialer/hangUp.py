from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def hangUp(self):
        #
        # Hangs up (assuming we're in the 'calling' frame).
        #
        try:
	        x = self.UTILS.getElement(DOM.Dialer.hangup_bar_locator, "Hangup bar", True, 5, False)
	        x.tap()
        except:
        	self.UTILS.logResult("info", "<b>NOTE:</b> Could not hangup using the hangup bar!")
        	pass

	 	#
	 	# Just to be sure!
	 	#    
     	self.data_layer.kill_active_call()
