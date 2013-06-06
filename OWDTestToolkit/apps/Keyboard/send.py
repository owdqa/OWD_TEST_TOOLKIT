from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def send(self, string):
        self._switch_to_keyboard()
        for val in string:
            if ord(val) > 127:
                # this would get the right key to long press and switch to the right keyboard
                middle_key_val = self._find_key_for_longpress(val.encode('UTF-8'))
                self._switch_to_correct_layout(middle_key_val)
  
                # find the key to long press and press it to get the extended characters list
                middle_key = self.marionette.find_element(*self._key_locator(middle_key_val))
                action = Actions(self.marionette)
                action.press(middle_key).wait(2).perform()
  
                # find the targeted extended key to send
                target_key = self.marionette.find_element(*self._key_locator(val))
                action.move(target_key).release().perform()
            else:
                # after switching to correct keyboard, tap/click if the key is there
                self._switch_to_correct_layout(val)
                if self.is_element_present(*self._key_locator(val)):
                    self._tap(val)
                else:
                    assert False, 'Key %s not found on the keyboard' % val
 
            # after tap/click space key, it might get screwed up due to timing issue. adding 0.8sec for it.
            if ord(val) == int(self._space_key):
                time.sleep(0.8)
        self.marionette.switch_to_frame()

    # switch to keyboard with numbers and special characters
