from OWDTestToolkit.global_imports import *
	
class main(GaiaTestCase):

    def _switch_to_keyboard(self):
        self.marionette.switch_to_frame()
        keybframe = self.marionette.find_element(*self._keyboard_frame_locator)
        self.marionette.switch_to_frame(keybframe, focus=False)

    # this is to get the locator of desired key on keyboard
