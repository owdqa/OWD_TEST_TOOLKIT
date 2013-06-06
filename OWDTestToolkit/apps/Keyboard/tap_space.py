from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def tap_space(self):
        self._switch_to_keyboard()
        self._tap(self._space_key)
        self.marionette.switch_to_frame()

