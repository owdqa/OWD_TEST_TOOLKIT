from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def tap_alt(self):
        self._switch_to_keyboard()
        if self.is_element_present(*self._key_locator(self._numeric_sign_key)):
            self._tap(self._numeric_sign_key)
        self._tap(self._alt_key)
        self.marionette.switch_to_frame()
