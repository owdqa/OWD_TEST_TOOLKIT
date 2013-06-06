from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def enable_caps_lock(self):
        self._switch_to_keyboard()
        if self.is_element_present(*self._key_locator(self._alpha_key)):
            self._tap(self._alpha_key)
        key_obj = self.marionette.find_element(*self._key_locator(self._upper_case_key))
        self.marionette.double_tap(key_obj)
        self.marionette.switch_to_frame()

    # this is to detect if the element is present in a shorter time
    # default timeout to 600 and allow people to set a higher timeout
