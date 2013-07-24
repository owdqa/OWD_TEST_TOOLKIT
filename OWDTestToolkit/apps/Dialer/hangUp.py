from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def hangUp(self):
        #
        # Hangs up (assuming we're in the 'calling' frame).
        #
        
        # The call may already be terminated, s odon't throw an error if
        # the hangup bar isn't there.
        try:
        	self.maroinette.switch_to_frame()
        	x = self.marionette.find_element("xpath", "//iframe[contains(@%s, '%s')]" % \
													DOM.Dialer.frame_locator_calling[0],
													DOM.Dialer.frame_locator_calling[1])
        	if x:
				self.marionette.switch_to_frame(x)
				x = self.marionette.find_element(*DOM.Dialer.hangup_bar_locator)
				if x: x.tap()
        except:
        	pass

	 	#
	 	# Just to be sure!
	 	#    
     	self.data_layer.kill_active_call()
     	
     	self.UTILS.switchToFrame(*DOM.Dialer.frame_locator)
