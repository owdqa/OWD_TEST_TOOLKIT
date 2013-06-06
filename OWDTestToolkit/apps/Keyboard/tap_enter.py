from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def tap_enter(self):
        self._switch_to_keyboard()
        self._tap(self._enter_key)
        self.marionette.switch_to_frame()

