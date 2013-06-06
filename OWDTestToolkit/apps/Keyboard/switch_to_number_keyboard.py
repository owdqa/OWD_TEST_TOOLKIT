from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def switch_to_number_keyboard(self):
        self._switch_to_keyboard()
        self._tap(self._numeric_sign_key)
        self.marionette.switch_to_frame()

    # switch to keyboard with alphabetic keys
