from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def _switch_to_correct_layout(self, val):
        # alpha is in on keyboard
        if val.isalpha():
            if self.is_element_present(*self._key_locator(self._alpha_key)):
                self._tap(self._alpha_key)
            if not self.is_element_present(*self._key_locator(val)):
                self._tap(self._upper_case_key)
        # numbers and symbols are in another keyboard
        else:
            if self.is_element_present(*self._key_locator(self._numeric_sign_key)):
                self._tap(self._numeric_sign_key)
            if not self.is_element_present(*self._key_locator(val)):
                self._tap(self._alt_key)

    # this is to switch to the frame of keyboard
