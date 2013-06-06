from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def long_press(self, key, timeout=2000):
        if len(key) == 1:
            self._switch_to_keyboard()
            key_obj = self.marionette.find_element(*self._key_locator(key))
            action = Actions(self.marionette)
            action.press(key_obj).wait(timeout/1000).release().perform()
            self.marionette.switch_to_frame()

    # this would go through fastest way to tap/click through a string
