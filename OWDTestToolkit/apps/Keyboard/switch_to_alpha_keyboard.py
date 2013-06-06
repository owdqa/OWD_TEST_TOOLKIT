from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def switch_to_alpha_keyboard(self):
        self._switch_to_keyboard()
        self._tap(self._alpha_key)
        self.marionette.switch_to_frame()

    # following are "5 functions" to substitute finish switch_to_frame()s and tap() for you
