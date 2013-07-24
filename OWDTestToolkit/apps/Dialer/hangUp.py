from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def hangUp(self):
        #
        # Hangs up (assuming we're in the 'calling' frame).
        #
        x = self.UTILS.getElement(DOM.Dialer.hangup_bar_locator, "Hangup bar")
        x.tap()
