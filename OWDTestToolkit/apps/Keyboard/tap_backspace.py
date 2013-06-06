from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def tap_backspace(self):
        self._switch_to_keyboard()
        bs = self.marionette.find_element(self._button_locator[0], self._button_locator[1] % self._backspace_key)
        bs.tap()
        self.marionette.switch_to_frame()

