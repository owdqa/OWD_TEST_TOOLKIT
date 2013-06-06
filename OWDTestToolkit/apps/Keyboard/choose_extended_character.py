from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def choose_extended_character(self, long_press_key, selection, movement=True):
        self._switch_to_keyboard()
        action = Actions(self.marionette)

        # after switching to correct keyboard, set long press if the key is there
        self._switch_to_correct_layout(long_press_key)
        key = self._key_locator(long_press_key)
        if self.is_element_present(*key):
            keyobj = self.marionette.find_element(*key)
            action.press(keyobj).wait(2).perform()
        else:
            assert False, 'Key %s not found on the keyboard' % long_press_key

        # find the extended key and perform the action chain
        extend_keys = self.marionette.find_elements(*self._highlight_key_locator)
        if movement == True:
            action.move(extend_keys[selection - 1]).perform()
        action.release().perform()
        time.sleep(0.8)

        self.marionette.switch_to_frame()

